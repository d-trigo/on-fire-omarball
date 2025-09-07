from discord.ext import commands
import discord

import requests

import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

import io 

from datetime import date 

#importing line module for custom intros and outros
import lines

#importing keys, create a config file with your relevant keys or in a VENV file and do NOT share them!!!!!!!
import config

#importing league
from espn_api.basketball import League
league = League(league_id=config.leagueid, year=2025, espn_s2=config.espn_s2config, swid=config.swid)
#note that you WILL need to reload the league if you want to refresh data; i.e. if you use an older instance, it won't understand if a player was added to someone's team afterwards





#grabbing Ball Don't Lie info 
#get date
today = date.today()
yeardate = today.strftime("%Y-%m-%d") #for BDL request and graph
monthdate = today.strftime("%m-%d") #for the lines module

#create list for all ball don't lie (BDL) json scrape lists to go into
jsonlist = []
next_cursor_page = None

#create scraping loop
while True:
    params = {'start_date':yeardate, 'end_date':yeardate, 'per_page':'100'}
    if next_cursor_page:
        params['cursor'] = next_cursor_page #we get the first page by default, so this won't be added on the first run. later runs get the cursor when applicable

    try:
        r = requests.get('https://api.balldontlie.io/v1/stats', headers=config.bdltoken, params=params)
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(f'Error: {err}')
        break

    rjson = r.json()
    jsonlist.append(rjson)

    next_cursor_page = rjson['meta'].get('next_cursor', None) #if next cursor number exists, get next cursor
    if not next_cursor_page:
        print('There are no more pages available. All games for specified day logged. Check the "bdlmerged" dataframe for all lines.')
        break

bdldfs = [] 
for jsons in jsonlist:
    bdldf = pd.json_normalize(jsons, record_path='data') #normalize all jsons into dfs
    bdldfs.append(bdldf)

bdlmerged = pd.concat(bdldfs, ignore_index=True) #this will also work on days where there is only one dataframe to take in; best to use this instead of "bdlmerged = dfs[0]" given that we want to modify a "full" dataframe rather than a copy of it 

#grabbing ESPN league info 
gms = league.teams #fetch all team names

abbrevs = [] #for graph 
for i in range(len(gms)):
    abbrev = league.teams[i].team_abbrev
    abbrevs.append(abbrev)

playerslist = [] #fetch all rostered players 
for i in range(len(gms)):
    players = league.teams[i].roster #get roster via index obtained with len(); each gm number corresponds to their respective roster 
    playerslist.append(players) #each entry is a list of rosters; this will be separated when we use explode() with Pandas  

def getstatus(playerlist): #see if player is benched, in IR, etc. 
    for i, lists in enumerate(playerlist):
        for z, players in enumerate(lists):
            status = league.teams[i].roster[z].lineupSlot
            players = str(players)
            players = players + ', ' + status
            lists[z] = players

getstatus(playerslist)

    
espndf = pd.DataFrame((zip(gms, playerslist, abbrevs)), 
    columns = ['GM', 'Player', 'Abbrev'])

espndf = espndf.explode('Player')
espndf = espndf.astype(str)

espndf[['Player', 'Status']] = espndf['Player'].str.split(', ', n=1, expand=True)
espndf['GM'] = espndf['GM'].str.replace('Team(', '')
espndf['GM'] = espndf['GM'].str.replace(')', '')

espndf['Player'] = espndf['Player'].str.replace('Player(', '')
espndf['Player'] = espndf['Player'].str.replace(')', '')

playerdict = espndf.set_index('Player')['GM'].to_dict()
statusdict = espndf.set_index('Player')['Status'].to_dict()
abbrevdict = espndf.set_index('GM')['Abbrev'].to_dict()

#create emoji criteria for "mindblowing stats"
def zcheck(bdldf, zcolumn, x) -> str: 
    """Checks if the counting Z-score is equal to or above 3.50. If it is, it returns the mindblown emoji."""
    if bdldf[zcolumn].iloc[x] >= 3.50:
        return ' 🤯'
    else:
        return ''

def stlcheck(bdldf, stlcol, x) -> str:
    """Checks if the steal z-score is equal to or above 8.46557978778486 (or, four steals). If it is, it returns the mindblown emoji."""
    if bdldf[stlcol].iloc[x] >= 8.46557978778486:
        return ' 🤯'
    else:
        return ''
    
def volcheck(bdldf, zcolumn, x) -> str:
    """Checks if the player's efficiency (FGARZ or FTARZ) was at or above/below 3.25/-3.25. Will either return target emoji (great accuracy) or brick emoji (awful accuracy). """
    if bdldf[zcolumn].iloc[x] >= 3.25:
        return ' 🎯'
    elif bdldf[zcolumn].iloc[x] <= -3.25:
        return ' 🧱'
    else:
        return ''
    
def tocheck(bdldf, tozcolumn, x) -> str:
    """Checks if the player's TOZ was at -1.08150924234275 or below (or, five turnovers or more). If so, return the vomit emoji. """
    if bdldf[tozcolumn].iloc[x] <= -1.08150924234275: 
        return ' 🤮 '
    else:
        return ' '
    

def printout(bdldf, maxlines) -> str:
    """Forms the printout of the selected range of lines from the Ball Don't Lie dataframe. Also checks if a player's line included a triple double. 
    Note: 'maxlines' will determine how many lines from the dataframe to print out. This can be modified depending on how many lines you want to print depending on any conditions (i.e. game volume, etc.)"""
    alllines = []
    for i in range (0, maxlines):
        if sum([(bdldf['pts'].iloc[i]>=10), (bdldf['reb'].iloc[i]>=10), (bdldf['ast'].iloc[i]>=10), (bdldf['stl'].iloc[i]>=10), (bdldf['blk'].iloc[i]>=10)]) == 3: #make sure to add paranthesis to each Pandas index or else Python will incorrectly assume you're closing off the command
            statdubline = str(' 3️⃣🚀')
        elif sum([(bdldf['pts'].iloc[i]>=10), (bdldf['reb'].iloc[i]>=10), (bdldf['ast'].iloc[i]>=10), (bdldf['stl'].iloc[i]>=10), (bdldf['blk'].iloc[i]>=10)]) == 4:
            statdubline = str(' 4️⃣🎆') #make sure to add paranthesis to each Pandas index or else Python will incorrectly assume you're closing off the command
        else:
            statdubline = None 
        line = str(f"{i+1}. **{bdldf['PlayerName'].iloc[i]}**{statdubline if statdubline is not None else ''} (*{bdldf['GM'].iloc[i]}*) with {bdldf['pts_s'].iloc[i]}{zcheck(bdldf, 'PTSZ', i)}, {bdldf['reb_s'].iloc[i]}{zcheck(bdldf, 'REBZ', i)}, {bdldf['ast_s'].iloc[i]}{zcheck(bdldf, 'ASTZ', i)}, {bdldf['fg3m_s'].iloc[i]}{zcheck(bdldf, 'FG3Z', i)}, {bdldf['stl_s'].iloc[i]}{stlcheck(bdldf, 'STLZ', i)}, {bdldf['blk_s'].iloc[i]}{zcheck(bdldf, 'blk', i)}, and {bdldf['tov_s'].iloc[i]}{(tocheck(bdldf, 'TOVZ', i))}on {bdldf['fgm'].iloc[i]}/{bdldf['fga'].iloc[i]} FG{volcheck(bdldf, 'FGARZ', i)} and {bdldf['ftm'].iloc[i]}/{bdldf['fta'].iloc[i]} FT{volcheck(bdldf, 'FTARZ', i)} splits in {bdldf['min'].iloc[i]} min.")
        alllines.append(line)
    printed = "\n".join([str(playerline) for playerline in alllines])
    print(printed) 
    return printed
        
if bdlmerged.empty is True:
    print('No games found.')
else:
    bdlmerged['PlayerName'] = bdlmerged['player.first_name'] + " " + bdlmerged['player.last_name']
    #mapping espn info
    bdlmerged['GM'] = bdlmerged['PlayerName'].map(playerdict)
    bdlmerged['Status'] = bdlmerged['PlayerName'].map(statusdict)
    bdlmerged['Abbrev'] = bdlmerged['GM'].map(abbrevdict)
    #queries
    bdlmerged = bdlmerged.dropna(subset=["GM"])
    bdlmerged['min'] = bdlmerged['min'].astype('int64')
    bdlmerged = bdlmerged.query('min > 0')
    bdlmerged = bdlmerged.query("Status != 'BE'")  
    bdlmerged = bdlmerged.query("Status != 'IR'")


    #volume calcs
    bdlmerged['FGAR'] = (bdlmerged['fgm']-(0.4834302*bdlmerged['fga'])) 
    bdlmerged['FTAR'] = (bdlmerged['ftm']-(0.7940223*bdlmerged['fta']))

    #z calcs
    bdlmerged['REBZ'] = ((bdlmerged['reb']-5.451973)/2.525530)
    bdlmerged['FG3Z'] = (((bdlmerged['fg3m']-1.7496388)/0.9290426)*0.80)
    bdlmerged['ASTZ'] = ((bdlmerged['ast']-3.700322)/2.067065)
    bdlmerged['TOVZ'] = (((bdlmerged['turnover']-1.758401)/0.749323)*-0.25)
    bdlmerged['STLZ'] = (((bdlmerged['stl']-0.9037216)/0.2925993)*0.80)
    bdlmerged['BLKZ'] = (((bdlmerged['blk']-0.6413044)/0.5216844)*0.80)
    bdlmerged['PTSZ'] = ((bdlmerged['pts']-16.192476)/5.956778)
    bdlmerged['FGARZ'] = (((bdlmerged['FGAR']-(-0.03505124))/0.65614770)*0.90)
    bdlmerged['FTARZ'] = (((bdlmerged['FTAR']-0.02214733)/0.28761030)*0.80)

    #sum across all z columns to get final z sum for player 
    col_list = list(bdlmerged)
    zcols = col_list[55:64] #rebz through ftarz
    bdlmerged['ZSUM'] = bdlmerged[zcols].sum(axis=1)

    #convert score cols to strings; this will be passed into the string while allowing us to keep int versions for checking for a triple dub 
    #manly needed so we can use bolded text (via **) for good stats
    bdlmerged['pts_s'] = bdlmerged['pts'].astype(str) + ' PTS'
    bdlmerged['blk_s'] = bdlmerged['blk'].astype(str) + ' BLK'
    bdlmerged['reb_s'] = bdlmerged['reb'].astype(str) + ' REB'
    bdlmerged['ast_s'] = bdlmerged['ast'].astype(str) + ' AST'
    bdlmerged['stl_s'] = bdlmerged['stl'].astype(str) + ' STL'
    bdlmerged['pts_s'] = bdlmerged['pts'].astype(str) + ' PTS'
    bdlmerged['fg3m_s'] = bdlmerged['fg3m'].astype(str) + ' 3PM'
    bdlmerged['tov_s'] = bdlmerged['turnover'].astype(str) + ' TO'

    bdlmerged.loc[bdlmerged['REBZ'] > 2.5, 'reb_s'] = '**' + bdlmerged['reb_s'] + '**'
    bdlmerged.loc[bdlmerged['FG3Z'] > 2.5, 'fg3m_s'] = '**' + bdlmerged['fg3m_s'] + '**'
    bdlmerged.loc[bdlmerged['ASTZ'] > 2.5, 'ast_s'] = '**' + bdlmerged['ast_s'] + '**'
    bdlmerged.loc[bdlmerged['BLKZ'] > 2.5, 'blk_s'] = '**' + bdlmerged['blk_s'] + '**'
    bdlmerged.loc[bdlmerged['PTSZ'] > 2.5, 'pts_s'] = '**' + bdlmerged['pts_s'] + '**'
    bdlmerged.loc[bdlmerged['STLZ'] > 2.5, 'stl_s'] = '**' + bdlmerged['stl_s'] + '**'

    #finding best lines 
    top = bdlmerged.sort_values(by='ZSUM', ascending=False)
    if len(top.index) < 30:
        topprintout = printout(top, 5)
    else:
        topprintout = printout(top, 10)

    #finding worst lines 
    bottom = bdlmerged.sort_values(by='ZSUM', ascending=True)
    bottom = bottom.query('min >= 14') #players must play 14 min to make it into the worst list (excluding injured players)
    bottomprintout = printout(bottom, 5)
    #debug note: when you're running this query set to 14 or more minutes, it won't work well if it's the beginning of the game. 


    #create daily zsum graph

    bdlmerged = bdlmerged.rename(columns={
    'min':'MIN'
    })

    gmsums = bdlmerged.groupby('Abbrev').agg({
    'MIN':'sum',
    'ZSUM':'sum'
    }).round(decimals=2
    ).reset_index()


    #graph setup with seaborn and mpl 

    data_stream = io.BytesIO()

    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=(12,9))

    ax.set(ylim=(-30, 30))
    ax.set_title(str(f"Daily Z-Sum for {yeardate}"), fontsize=25)

    barplot = sns.barplot(
    gmsums,
    x='Abbrev',
    y='ZSUM',
    hue='Abbrev',
    order=gmsums.sort_values(by='ZSUM', ascending=False).Abbrev
    )

    for i, (containers, values) in enumerate(zip(ax.containers, gmsums['ZSUM'])):
        if 2.5 >= values >= -2.5: #if value is below 2.5 and above -2.5...
            ax.bar_label(ax.containers[i], fontsize=11.5, padding=1.5) #values go outside bar due to narrow length in this case
        else:
            ax.bar_label(ax.containers[i], fontsize=11.5, padding=1.5, label_type='center', color='k')
        

    plt.xlabel('Team', labelpad=13, fontsize=20)
    plt.ylabel('Z-Sum', fontsize=20)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)

    #if you need to debug the image with the actual width/height before it gets sent out, download the simply-view-image-for-python-debugging extension and input "fig" to use it once the plot is done: https://marketplace.visualstudio.com/items?itemName=elazarcoh.simply-view-image-for-python-debugging
    fig
    plt.savefig(data_stream, format='png', bbox_inches="tight", dpi = 80) #bbox inches insures that our graph margins aren't too big
    plt.close()

    data_stream.seek(0)
    chart=discord.File(data_stream, filename='dailyzsum.png')
        
#running bot
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    channel = bot.get_channel(config.channel_id)
    if bdlmerged.empty is True:
        await channel.send("If you're seeing this message, On Fire did not retrieve any lines for today. This could be because there were no games or something wrong happened while scraping. If it's the latter, please contact On Fire's owner!")
    else:
        await channel.send(f"{lines.intro(monthdate)}\n{topprintout}")
        await channel.send(f"{lines.worstintro(monthdate)}\n{bottomprintout}")
        await channel.send("Let\'s end today\'s episode of On Fire with a visualization of how each team did as a whole relative to their active player\'s Z-scores:", file=chart)

bot.run(config.discord_token)
