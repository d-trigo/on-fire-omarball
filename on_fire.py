from discord.ext import commands
import config #create a config file with your relevant keys or in a VENV file and do NOT share them!!!!!!!
import discord
import requests
import pandas as pd
from datetime import date 
#importing league
from espn_api.basketball import League
league = League(league_id=config.leagueid, year=2024, espn_s2=config.espn_s2config, swid=config.swid)
#note that you WILL need to reload the league if you want to refresh data; i.e. if you use an older instance, it won't understand if a player was added to someone's team afterwards

#get date
today = date.today()
today = today.strftime("%Y-%m-%d")


jsonlist = []
next_cursor_page = None

while True:
    params = {'start_date':today, 'end_date':today, 'per_page':'100'}
    if next_cursor_page:
        params['cursor'] = next_cursor_page

    try:
        r = requests.get('https://api.balldontlie.io/v1/stats', headers=config.bdltoken, params=params)
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(f'Error: {err}')
        break

    rjson = r.json()
    jsonlist.append(rjson)

    next_cursor_page = rjson['meta'].get('next_cursor', None)
    if not next_cursor_page:
        print('There are no more pages available. All games for specified day logged. Check the "mergedpd" dataframe for all lines.')
        break

dfs = []
for i, jsons in enumerate(jsonlist):
    df = pd.json_normalize(jsons, record_path='data')
    dfs.append(df)

if len(dfs) > 1:
    mergedpd = pd.concat(dfs, ignore_index=True)
else:
    mergedpd = dfs[0]
    

gmlist = []
for i in range(0, 12):
    gm = league.teams[i]
    gmlist.append(gm)

playerslist = []
for i, gms in enumerate(gmlist):
    players = league.teams[i].roster #get roster via index obtained with enumerate
    playerslist.append(players) 
    
df = pd.DataFrame((zip(gmlist, playerslist)), #don't think we needed list in the first place. 
    columns = ['GM', 'Player'])

df2 = df.explode('Player')
df2 = df2.astype(str)
df2['GM'] = df2['GM'].str.replace('Team(', '')
df2['GM'] = df2['GM'].str.replace(')', '')
df2['Player'] = df2['Player'].str.replace('Player(', '')
df2['Player'] = df2['Player'].str.replace(')', '')
playerdict = df2.set_index('Player')['GM'].to_dict()

def printout(bdldf, colmax):
    alllines = []
    for i in range (0, colmax):
        if sum([(bdldf['pts'].iloc[i]>=10), (bdldf['reb'].iloc[i]>=10), (bdldf['ast'].iloc[i]>=10), (bdldf['stl'].iloc[i]>=10), (bdldf['blk'].iloc[i]>=10)]) >= 3: #make sure to add paranthesis to each Pandas index or else Python will incorrectly assume you're closing off the command
            tripledubline = str('3️⃣🚀')
        else:
            tripledubline = None 
        line = str(f"{i+1}. **{bdldf['PlayerName'].iloc[i]}**{tripledubline if tripledubline is not None else ''} (*{bdldf['GM'].iloc[i]}*) with {bdldf['pts'].iloc[i]} PTS, {bdldf['reb'].iloc[i]} REB, {bdldf['ast'].iloc[i]} AST, {bdldf['fg3m'].iloc[i]} 3PM, {bdldf['stl'].iloc[i]} STL, {bdldf['blk'].iloc[i]} BLK, and {bdldf['turnover'].iloc[i]} TO on {bdldf['fgm'].iloc[i]}/{bdldf['fga'].iloc[i]} FG and {bdldf['ftm'].iloc[i]}/{bdldf['fta'].iloc[i]} FT splits")
        alllines.append(line)
    printed = "\n".join([str(playerline) for playerline in alllines])
    print(printed)
    return printed
        
if mergedpd.empty is False:
    mergedpd['PlayerName'] = mergedpd['player.first_name'] + " " + mergedpd['player.last_name']
    mergedpd['GM'] = mergedpd['PlayerName'].map(playerdict)
    mergedpd = mergedpd.dropna()


    mergedpd['FGAR'] = (mergedpd['fgm']-(0.4834302*mergedpd['fga'])) 
    mergedpd['FTAR'] = (mergedpd['ftm']-(0.7940223*mergedpd['fta']))


    mergedpd['REBZ'] = ((mergedpd['reb']-5.451973)/2.525530)
    mergedpd['FG3Z'] = (((mergedpd['fg3m']-1.7496388)/0.9290426)*0.80)
    mergedpd['ASTZ'] = ((mergedpd['ast']-3.700322)/2.067065)
    mergedpd['TOVZ'] = (((mergedpd['turnover']-1.758401)/0.749323)*-0.25)
    mergedpd['STLZ'] = (((mergedpd['stl']-0.9037216)/0.2925993)*0.80)
    mergedpd['BLKZ'] = (((mergedpd['blk']-0.6413044)/0.5216844)*0.80)
    mergedpd['PTSZ'] = ((mergedpd['pts']-16.192476)/5.956778)
    mergedpd['FGARZ'] = (((mergedpd['FGAR']-(-0.03505124))/0.65614770)*0.90) #paranthesis fixed?
    mergedpd['FTARZ'] = (((mergedpd['FTAR']-0.02214733)/0.28761030)*0.90)

    col_list = list(mergedpd)
    zcols = col_list[55:64]
    mergedpd['ZSUM'] = mergedpd[zcols].sum(axis=1)


    top = mergedpd.sort_values(by='ZSUM', ascending=False)
    if len(top.index) < 20:
        topprintout = printout(top, 5)
    else:
        topprintout = printout(top, 10)

    #finding worst lines 
    bottom = mergedpd.sort_values(by='ZSUM', ascending=True)
    bottom['min'] = bottom['min'].astype('int64')
    bottom = bottom.query('min >= 24')
    if len(bottom.index) < 20:
        bottomprintout = printout(bottom, 5)
    else:
        bottomprintout = printout(bottom, 10)
        
#debug note: when you're running this query set to 24 or more minutes, it won't work well if it's the beginning of the game. 
#running bot
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    channel = bot.get_channel(config.channel_id)
    if mergedpd.empty is True:
        await channel.send("If you're seeing this message, On Fire did not retrieve any lines for today. This could be because there were no games or something wrong happened while scraping. If it's the latter, please contact On Fire's owner!")
    else:
        await channel.send("Another day of Omarball, another set of All-Star lines! Let's see who was on 🔥 tonight for {}:\n{}".format(today, topprintout))
        await channel.send("Of course, not everyone can be a winner...here's who was on 🥶 tonight:\n{}".format(bottomprintout))

bot.run(config.discord_token)
