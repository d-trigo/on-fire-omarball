library(hoopR)
library(tidyverse)

#scrape players
nba24players <- nba_leaguedashplayerstats(league_id = '00', season = year_to_season(most_recent_nba_season() - 1)) 
#you can replicate everything after for past seasons by changing the season arg and GP cut-off if desired
#try to calculate the avg values for those seasons though before making z scores

nba24playertbl <- nba24players[["LeagueDashPlayerStats"]]

#convert to numeric columns

nba24playertbl <- nba24playertbl%>%
  mutate(across(AGE:FT_PCT_RANK, as.numeric))

#only have players with 33 or more games played (about half of the season played)
players24ormore <- nba24playertbl%>%
  filter(GP>=33)

#only have players with 24 or more min. played
players24ormore <- players24ormore%>%
  mutate(MPG=MIN/GP)

players24ormore <- players24ormore%>%
  filter(MPG>=24)

#collapse dataset to relevant columns 
players24ormore <- players24ormore%>%
  select(PLAYER_ID:TEAM_ABBREVIATION, GP, FGM:BLK, MPG, PTS)


#construct formula for percentage cats which consider volume (source: https://www.reddit.com/r/fantasybball/comments/z40qvk/noob_question_on_percentages_for_cat_leagues/ixqfbyx/)
mean(players24ormore$FT_PCT, na.rm=TRUE) # = 0.7940223
mean(players24ormore$FG_PCT, na.rm=TRUE) # = 0.4834302

players24ormore <- players24ormore%>%
  mutate(FTAR=(FTM-(0.7940223*FTA)))%>%
  mutate(FGAR=(FGM-(0.4834302*FGA)))

#create per game values
players24ormore <- players24ormore%>%
  mutate(across(FGM:FGA, ~ .x/GP))%>%
  mutate(across(FG3M:FG3A, ~ .x/GP))%>%
  mutate(across(FTA:FTM, ~ .x/GP))%>%
  mutate(across(OREB:BLK, ~ .x/GP))%>%
  mutate(across(PTS:FGAR, ~ .x/GP))


#see fg and ft impact
playerspct <- players24ormore%>%
  select(PLAYER_NAME, FGAR, FTAR)

#plot distributions

statslong <- players24ormore%>%
  pivot_longer(FGA:FGAR, names_to='category', values_to ='stats')

ggplot(data=subset(statslong, !is.na(stats)), aes(stats)) +
  geom_histogram(bins = 10) + 
  facet_wrap(~category, scales = 'free_x')

#this will mean that with the z scores we calc, we *cannot* estimate quartile or percentage of dist above/below mean. see how cats like BLKs are skewed


#get means and sds for overall CATs
means <- players24ormore%>%
  summarise_if(is.numeric, mean, na.rm=TRUE)

sds <- players24ormore%>%
  summarise_if(is.numeric, sd, na.rm=TRUE)

averages <- rbind(means, sds)


#create z values for each player; compare to Hashtag if desired
players24ormore <- players24ormore%>%
  mutate(FG3Z=((FG3M-1.7496388)/0.9290426))%>%
  mutate(REBZ=((REB-5.451973)/2.525530))%>%
  mutate(ASTZ=((AST-3.700322)/2.067065))%>%
  mutate(TOVZ=(((TOV-1.758401)/0.749323)*-0.25))%>%
  mutate(STLZ=((STL-0.9037216)/0.2925993))%>%
  mutate(BLKZ=((BLK-0.6413044)/0.5216844))%>%
  mutate(PTSZ=((PTS-16.192476)/5.956778))%>%
  mutate(FGARZ=((FGAR--0.03505124)/0.65614770))%>%
  mutate(FTARZ=((FTAR-0.02214733)/0.28761030))%>%
  mutate(ZSUM=rowSums(across(FG3Z:FTARZ)))

#see just the z values
playerz <- players24ormore%>%
  select(PLAYER_NAME, FG3Z:ZSUM)%>%
  mutate_if(is.numeric, \(x) round(x, digits = 3))


players24ormorenegcheck <- players24ormore%>%
  mutate(FG3Z=((FG3M-1.7496388)/0.9290426))%>%
  mutate(REBZ=((REB-5.451973)/2.525530))%>%
  mutate(ASTZ=((AST-3.700322)/2.067065))%>%
  mutate(TOVZ=(((TOV-1.758401)/0.749323)*(-0.25)))%>%
  mutate(STLZ=((STL-0.9037216)/0.2925993))%>%
  mutate(BLKZ=((BLK-0.6413044)/0.5216844))%>%
  mutate(PTSZ=((PTS-16.192476)/5.956778))%>%
  mutate(FGARZ=((FGAR--0.03505124)/0.65614770))%>%
  mutate(FTARZ=((FTAR-0.02214733)/0.28761030))%>%
  mutate(ZSUM=rowSums(across(FG3Z:FTARZ)))
  