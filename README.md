# On Fire

# What is this?

This project was developed for my local fantasy league (Omarball) to be used in the league's Discord server. This project is inspired by r/fantasybball posts from u/fantasyog15 where each post would sum the best and worst lines of the day. 

# What packages and APIs are used in this project?

I coded this in Python using the Ball Don't Lie API and ESPN API package. There is also an R script stored that holds all the calculations for z-scores; the script fetches all cumulative stats for players per season and then calculates the average stats for players who play 24 minutes or more on average per game during the season. The mean and SD values are taken from the script into the Python script to calculate the final Z-scores. 

*Note: The R script is not meant to be used when performing the actual On Fire script, but rather serves as a separate document that can be ran on its own to demonstrate the mathematical concepts and values utilized in the final script. Make sure to download Tidyverse and hoopR if you would like to (mostly) replicate it.* 

# How does the bot work?

This bot is given a unique channel in the Omarball server to post in. Every night at 11:30 PM PST (as generally all NBA games will be done for the day by this point), a BAT file I created is automatically run to activate the scraping and then the bot to post the list of best and worst lines.

The scraping aspect utilizes the ESPN API package to fetch rosters for each Omarball GM along with the name of the GM. Once player lines are obtained via Ball Don't Lie, the script maps GMs who own the respective players into the dataframe. After scraping is completed, z scores are calculated for each player line using mean and SD values obtained for the NBA categories on a season-wide basis. With the z-scores, two printouts are created: one is for the best lines with the BDL DF sorted by descending order in regard to the 'ZSUM' (or, sum of a player's z scores across all categories) and another is for the worst lines with the same DF sorted by ascending order. Once these printouts are created, the script moves into the Discord bot phase where it will make two separate posts, one for the best lines and another for the worst lines.

*Note: How many lines the bot will post depends on the amount of lines available and, in turn, how many games were played for the day. If there are less than 20 lines available once unrostered players are dropped (and, for the worst lines, all players who played less than 24 min. are also dropped), the script will shorten the posts to provide only the best and worst 5 five lines. Otherwise, it will post the best and worst 10 lines.*



# Why did I use ESPN API info?

There are two reasons as to why this bot does this, both ultimately in order to differentiate itself in purpose and functionality from Reddit posts with the best lines:
1) Being able to hook ESPN API info allows the bot to comprehend who exactly is reaping the best lines of the day. For example, if we didn't have this info, the bot could still understand Steph having the best line of the night with a 50-bomb, but it's not going to know what GM is reaping Steph's 50-bomb. In other words, this can showcase which teams are dominating each day in terms of getting the best lines or also show when there's competitive nights between all GMs, ultimately adding a personal element of analysis relevant to the Omarball league.
2) Part of the fun of fantasy is scouting in (relative) secrecy for FAs that are beginning to develop on the court and providing competitive lines. A functionality of this bot is being able to show only lines from those who are rostered in Omarball in order to retain a bit of this secrecy. If this bot showed all lines, we might run the risk of having all GMs in Omarball see great FA lines at the same time, which could then reduce the element of scouting into simply being the first to add a player once the nightly list post drops. The template of this function can help a bit with encouraging your GMs to conduct independent scouting and take an active role in looking for great players.

# Why filter out players who played less than 24 min. for the worst lines printout?
The problematic aspect of not filtering out players with low minutes is primarily in regard to how the Z score is calculated. There are two scenarios to consider:
1) If a player is injured and did not play (or, in rarer cases for fantasy, got DNPed), the ESPN API which will fetch the roster is not able to automatically filter out players who played zero minutes for a specific game (as by and large, it does not get individual scores for a game but rather cumulative stats). This would mean that if the players who played zero minutes were included in the final printout, they're effectively considered some of the "worst" when z-values are calculated becase they have no stats in the first place. We need to filter out these players in this situation so we can understand which players truly disappointed in the spotlight.
2) Even when not considering players who DNP in a game, there's other factors which make it risky to include players who played between 1-20 minutes. For example, if a player fouls out early or picks up a decent portion of fouls, their stats will, again, be considered deflated compared to other players. Injuries also remain key to consider: a player might get injured only a couple minutes after they start playing and then be forced to miss the game. We avoid low z-score situations making the cut-off for 24 minutes too in this case.

# Why not use the same filter on the best lines section for consistency?
I find this idea more subject to change (I welcome feedback here!), but my belief is that good stats will be of immense impact for the GM no matter how many minutes they played. Take for example Malik Monk from the Sacramento Kings; he's a player who will often come off the bench and, at times, will play less than 24 minutes. Yet, he can still score with low minutes, which can be seen on Feb 9 2024 where he scored 23 against Denver on 9-13 FG splits as one example. Generally players who can generate stats like this while playing less than 24 is rare, and it's still subject to being outscored by other player lines. However, we want to consider the possibility of lines like Monk's on low minutes and give these lines a chance to shine. Of course, a concern is that players with low minutes have inflated value due to also having little to no turnovers (see the post I linked to u/DancingWithTheCars for a larger explanation of this); this should be mitigated as turnovers are effectively "punted" as they are weighed by -0.25 (see below for info on other relevant weights). 

Meanwhile, for "worst" scores with low minutes, as aforementioned it will simply weigh injured players or players who got in tough situations with fouls by too much unless they are filtered out early. In other words, if a player is on IR, they should not be expected to be defined as players to be judged based on their (non-existent) "performance." 

# I see constants added on top of most of the z-score category calculations, why is that?

I have applied weights to CATs that have high variance in order to mitigate inflated value produced by players having more blocks or steals than usual, slightly higher FG% per volume than the average, or having low turnovers when they didn't do much else in the first place due to limited minutes and/or a sidelined role. This is *not* to discount the values players can provide in these CATs: they are still considered valuable especially in situations where 1) stocks are rare to find in the first place or 2) just a tenth of an increase in FG% or one more turnover can make or break the week. However, this bot is attempting to highlight the best overall lines, and lines with even slightly higher than usual FG, stocks (blocks and steals) or zero turnovers can make it eligible for being one of the "best" lines even if the player's overall value wasn't that great for the GM (i.e. Holmes's line on March 20th 2024 would have been #10 on the list had we not weighed FG down). I consider this as another idea subject to change though; I welcome any suggestions on how to approach the weights, and of course you're also free to modify how you weigh these calculations in the actual script.

# Will the mean and SDs used for the z-score calculations change in future NBA seasons?
Probably. Gilani's hoopR package is excellent and you would only need to modify certain arguments such as the year values are obtained from in order to generate new mean and SD values for each season. Ideally I would like to update the calculation values once a year around mid-March when the majority of the regular season is done and teams are beginning to fully tank or shut down players for off-season or pre-playoff rest. 

# With the mean and SD values for each category, could I use z scores to calculate the percentile of lines for the day relative to average player lines?
In most cases, no. The reason why is in regard to the nature of the distributions that you would obtain via the hoopR package (or whichever NBA API package you prefer in Python): much of the distributions, even if you were to control for players who played less than 24 minutes on average per game, are still heavily skewed. Although Z-scores can be calculated for any type of distribution, normal or not, you cannot interpret a percentile value from a Z value calculated for a skewed distribution. 

![image](https://github.com/d-trigo/on-fire-omarball/assets/153132523/cc8ba12c-4286-4d6c-a970-23e24cf72874)

If you want to read more about what you can and can't do with Z scores, I would advise reading this comment thread from r/fantasybball that served as a counter-argument against the metric propsoed by the original poster. Of specific note is a comment here by u/zeros113 in regard to [documentation he wrote](https://github.com/zer2/Fantasy-Basketball--in-progress-/blob/main/readme.md) on the broader idea of z scores in fantasy and why, vice versa, we shouldn't try to convert the distributions (such as through log transformations) and attempt to make it standard in this case:
```
I wrote the readme, and agree fully with your explanation for why people are getting confused here.

The Z-score is only "valid" for calculating percentiles based on the standard normal table under the condition that data is normally distributed. However, that has no bearing for its use in other contexts. The argument I presented in the readme never assumes that the underlying data is normally distributed

In addition to being unnecessary, artificially transforming non-normal distributions into normal distributions can also cause problems. Scores should always be linearly additive, that is, two players who score two 3-pointers each should be exactly as valuable as one player who scores zero and one who scores four. If we warp the data to make it fit a normal distribution, that may no longer be true, which is clearly undesirable for a value-quantification system
```


# Can I run this script for my league's server?
Sure! This bot doesn't have an OAuth invite link on hand given that it only uses API info for my league, but you can utilize the basic template, create your own Discord bot to host it and things should work the same. Things you would need to specifically do outside of using the basic script would mainly be in setting up a 'config.py' file which includes:
- Your own Ball Don't Lie API key on the BDL website (*API access is free for scraping data for the current season!*)
- Your ESPN league ID + your cookie and SWID if in a private league (*find them through here: https://chromewebstore.google.com/detail/espn-cookie-finder/oapfffhnckhffnpiophbcmjnpomjkfcj*)
- Your own Discord bot token (*check out the Discord.py quickstart if you want to get an idea of how to start up and host a bot https://discordpy.readthedocs.io/en/stable/*)
- Relevant Python packages, including:
    - Pandas
    - Discord.py
    - ESPN API 

**WARNING: IF you fork and/or host a version of this script on GitHub, DO __NOT__ PLACE YOUR API KEYS AND TOKENS IN THE MAIN SCRIPT! Create a separate config file with the defined API keys included or a VENV file, mark the file to be ignored on commits with .gitignore (along with all PYC files), and DO NOT give out any of these keys.**

In terms of the automation for posting it every night at 11:30 PM PST (or whichever time you prefer), if you just want to host it locally, you can utilize Windows Task Scheduler to do so. If you're specifically using an Anaconda environment to and host the actual On Fire script, you would create a BAT file with this template after cloning the repo and doing the work in setting up the config:
```
call C:\Users\InsertUserNameHere\anaconda3\Scripts\activate.bat
call conda activate environment_name
call python C:\Users\InsertUserNameHere\InsertRepoParentFolderName\omarball-onfire-bot\on_fire.py
call conda deactivate
pause
```

This will run the script and keep the terminal open to assist in debugging when needed. When the BAT file is ready, point Task Scheduler to the BAT file and schedule it for the time you prefer.

# Will you automate set-up for all leagues and create a invite link for the bot in the future?
It's a possibility, but more details and personal time are needed here before I can proceed. I would need to specifically consider if there are any potential security concerns with obtaining ESPN cookie and SWID info through user input (this would be through DM if I were to do so). If I pursue a version that can join any server and take in user's S2 and SWID to create the league connection, it would be through a branch of the original repo. For now, you are free to use the basic template of the script to host it on whichever server you desire.

# Who do you want to thank?

- API for pulling scores provided by [Ball Don't Lie](https://new.balldontlie.io/)
- API for pulling ESPN fantasy league info provided by [cwendt94](https://github.com/cwendt94/espn-api)
- API for pulling season-wide NBA stats provided through [*hoopR* by Saiem Gilani et al.](https://hoopr.sportsdataverse.org/)
- Discord bot wrapper for Python provided by [Rapptz et al.](https://github.com/Rapptz/discord.py)
- FTAR and FGAR concept and formulas provided by [u/DancingWithTheCars](https://www.reddit.com/r/fantasybball/comments/z40qvk/noob_question_on_percentages_for_cat_leagues/ixqfbyx/?context=3)
- [Omar Uraimov](https://github.com/ouraimov) for his help and creating Omarball!
