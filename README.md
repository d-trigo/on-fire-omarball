# On Fire

# What is this?

This project was developed for my local fantasy league (Omarball) to be used in the league's Discord server. This project is inspired by r/fantasybball posts from u/fantasyog15 where each post would sum the best and worst lines of the day. 

# What packages and APIs are used in this project?

I coded this in Python using the Ball Don't Lie API and ESPN API package. There is also an R script stored that holds all the calculations for z-scores; the script fetches all cumulative stats for players per season and then calculates the average stats for players who play 24 minutes or more on average per game during the season. The mean and SD values are taken from the script into the Python script to calculate the final Z-scores. 

# How does the bot work?

This bot is given a unique channel in the Omarball server to post in. Every night at 11:30 PM PST (as generally all NBA games will be done for the day by this point), a BAT file I created is automatically run to activate the scraping and then the bot to post the list of best and worst lines.

The scraping aspect utilizes the ESPN API package to fetch rosters for each Omarball GM along with the name of the GM. Once player lines are obtained via Ball Don't Lie, the script maps GMs who own the respective players into the dataframe. After scraping is completed, z scores are calculated for each player line using mean and SD values obtained for the NBA categories on a season-wide basis. With the z-scores, two printouts are created: one is for the best lines with the BDL DF sorted by descending order in regard to the 'ZSUM' (or, sum of a player's z scores across all categories) and another is for the worst lines with the same DF sorted by ascending order. Once these printouts are created, the script moves into the Discord bot phase where it will make two separate posts, one for the best lines and another for the worst lines.

*Note: How many lines the bot will post depends on the amount of lines available and, in turn, how many games were played for the day. If there are less than 20 lines available once unrostered players are dropped (and, for the worst lines, all players who played less than 24 min. are also dropped), the script will shorten the posts to provide only the best and worst 5 five lines. Otherwise, it will post the best and worst 10 lines.*



# Why did I use ESPN API info?

There are two reasons as to why this bot does this, both ultimately in order to differentiate itself in purpose and functionality from Reddit posts with the best lines:
1) Being able to hook ESPN API info allows the bot to comprehend who exactly is reaping the best lines of the day. For example, if we didn't have this info, the bot could still understand Steph having the best line of the night with a 50-bomb, but it's not going to know what GM is reaping Steph's 50-bomb. In other words, this can showcase which teams are dominating each day in terms of getting the best lines or also show when there's competitive nights between all GMs, ultimately adding a personal element of analysis relevant to the Omarball league.
2) Part of the fun of fantasy is scouting in (relative) secrecy for FAs that are beginning to develop on the court and providing competitive lines. A functionality of this bot is being able to show only lines from those who are rostered in Omarball in order to retain a bit of this secrecy. If this bot showed all lines, we might run the risk of having all GMs in Omarball see great FA lines at the same time, which could then reduce the element of scouting into simply being the first to add a player once the nightly list post drops. The template of this function can help a bit with encouraging your GMs to conduct independent scouting and take an active role in looking for great players.

# Can I run this script for my league's server?
Sure! This bot doesn't have an OAuth invite link on hand given that it only uses API info for my league, but you can utilize the basic template, create your own Discord bot to host it and things should work the same. Things you would need to specifically do outside of using the basic script would mainly be in setting up a 'config.py' file which includes:
- Your own Ball Don't Lie API key on the BDL website (*API access is free for scraping data for the current season!*)
- Your ESPN league ID + your cookie and SWID if in a private league (*find them through here: https://chromewebstore.google.com/detail/espn-cookie-finder/oapfffhnckhffnpiophbcmjnpomjkfcj*)
- Your own Discord bot token (*check out the Discord.py quickstart if you want to get an idea of how to start up and host a bot https://discordpy.readthedocs.io/en/stable/*)

**WARNING: IF you fork and/or host a version of this script on GitHub, DO __NOT__ PLACE YOUR API KEYS AND TOKENS IN THE MAIN SCRIPT! Create a separate config file with the defined API keys included or a VENV file, mark the file to be ignored on commits with .gitignore (along with all PYC files), and DO NOT give out any of these keys.**

In terms of the automation for posting it every night at 11:30 PM PST (or whichever time you prefer), if you just want to host it locally, you can utilize Windows task scheduler to do so. If you're specifically using an Anaconda environment to and host the actual On Fire script, you would create a BAT file with this template after cloning the repo and doing the work in setting up the config:
```
call C:\Users\InsertUserNameHere\anaconda3\Scripts\activate.bat
call conda activate discord_fantasy_bot
call python C:\Users\InsertUserNameHere\InsertRepoParentFolderName\omarball-onfire-bot\on_fire.py
call conda deactivate
pause
```

This will run the script and keep the terminal open to assist in debugging when needed. 

# Will you automate set-up for all leagues and create a invite link for the bot in the future?
It's a possibility, but more details and personal time are needed here before I can proceed. I would need to specifically consider if there are any potential security concerns with obtaining ESPN cookie and SWID info through user input (this would be through DM if I were to do so). For now, you are free to use the basic template of the script to host it on whichever server you desire.

# Who do you want to thank?

- API for pulling scores provided by [Ball Don't Lie](https://new.balldontlie.io/)
- API for pulling ESPN fantasy league info provided by [cwendt94](https://github.com/cwendt94/espn-api)
- API for pulling season-wide NBA stats provided through [*hoopR* by Saiem Gilani et al.](https://hoopr.sportsdataverse.org/)
- Discord bot wrapper for Python provided by [Rapptz et al.](https://github.com/Rapptz/discord.py)
- FTAR and FGAR concept and formulas provided by [u/DancingWithTheCars](https://www.reddit.com/r/fantasybball/comments/z40qvk/noob_question_on_percentages_for_cat_leagues/ixqfbyx/?context=3&share_id=zgGIC5jyaZA2LIfqls7UV)
- [Omar Uraimov](https://github.com/ouraimov) for his help and creating Omarball!
