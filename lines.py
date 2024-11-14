from datetime import date
import random 

#get date in month-date format
day = date.today()
monthdate = day.strftime("%m-%d")

lines = [ #corny intros to start up each On Fire message; message is selected at random 
    'On Fire is on the wire!',
    'If you touch these lines you\'ll get burned!',
    'There\'s a heatwave in the league!',
    'A water hose can\'t put out this level of heat!',
    'Another day of Omarball, another set of All-Star lines!',
    'These lines will make you shout \'Boomshakalaka!\''
]

elseline = random.choice(lines) #choose a random non-holiday intro line 

leadinline = f'Let\'s see who was on 🔥 for {day}' #line created for non-holiday intro 

leadoutline = 'Of course, not everyone can be a winner...here\'s who was on 🥶 tonight' #line created for non-holiday bad line section 



def intro(todaysdate) -> str:
    """Creates the beginning to the printout. On the defined holidays, On Fire will post a special holiday intro. Otherwise, it will fallback to a regular intro."""
    if todaysdate == '10-22':
        return 'It\'s what you\'ve all been waiting for...**Omarball \'25 has begun!** Let\'s kick things off with the return of On Fire! Who made a strong first impression on opening night?'
    elif todaysdate == '10-31':
        return 'Happy Halloween! What\'s scarier: ghosts, mummies, or 🔥 lines from your opponent? Let\'s answer this by taking a look at who was on 🔥 today.'
    elif todaysdate == '12-25':
        return 'Merry Christmas! Tis the season to not only be jolly but to also receive the great gift of 🔥 lines from your team! Let\'s see who got the best gifts in Omarball today:'
    elif todaysdate == '1-01':
        return 'Happy New Year! A new year for Omarball not only means a new you but also a new set of 🔥 lines for the day! Let\'s see who kicking off the new year the right way:'
    elif todaysdate == '11-27':
        return 'Happy day before Thanksgiving! What are you grateful for most: friends and family or 🔥 lines that come in clutch for your team? Let\'s answer that right now by taking a look which players cooked an entree line to feast on:'
    elif todaysdate == '02-13': #meant for last games before all star break, will change date when i found out correct day before break
        return 'Happy All Star Weekend! On Fire will be on break this weekend along with the NBA regular season, but before we go let\'s take a look at what your All-Stars are up to:'
    elif todaysdate == '11-14':
            return 'Hi all, today is an odd day since we only had one game between Mavericks-Jazz. On Fire\'s recap is ready, but there will be missing teams here along with limited stats to draw from, so "worst" stats today might not be all that bad! With that said, time for the 🔥 lines of the night:'
    elif todaysdate == '12-17':
            return 'Hope you all enjoyed NBA Cup championship day! Today\'s stats will *not* count for fantasy this week, but for fun On Fire will go ahead and post anyways to see which of your guys balled out the most. Here\'s who was on 🔥 during championship day:'
    else:
        return f'{elseline} {leadinline}:' #the default non-holiday line 
    


def worstintro(todaysdate) -> str: #more to be added here
    """Creates the first line of the worst line printout. Like 'intro(todaysdate)', this will post a special Holiday intro or otherwise fallback to a regular intro."""
    if todaysdate == '10-22':
        return 'Unfortunately, some players had the opening night jitters...here\'s who froze up on stage 🥶:'
    elif todaysdate == '10-31':
        return 'Even more frightening? Seeing bad lines from your roster...here\'s the ones who acted like 🧟‍♂️s on the court:'
    elif todaysdate == '12-25':
        return 'Unfortunately, some have been on the naughty list and are getting coal in their team\'s stocking...let\'s see who was on ❄ today:'
    elif todaysdate == '1-01':
        return 'Unfortunately, some are still feeling the effects of all that champagne...here\'s the ones who are still in 2024:'
    elif todaysdate == '11-27':
        return 'Unfortunately, some players couldn\'t cook even a side dish on the court...here\'s who looked like a headless 🦃:'
    elif todaysdate == '02-13': #meant for last games before all star break, will change date when i found out correct day before break
        return 'Unfortunately, some seem to already be playing like it\'s the All-Star Game...here\'s the ones who were on 🥶 tonight:'
    elif todaysdate == '11-14':
        return 'Here are the "worst" lines, but again remember there weren\'t many lines today overall!'
    elif todaysdate == '12-17':
        return 'Here are the "worst" lines, but similar to a couple weeks ago remember that sample size was limited!:'
    else:
        return f'{leadoutline}:' 
    


#use tests to validate holiday posts:

if __name__=="__main__":    
    christmasdaytest = date.fromisoformat('2024-12-25')
    christmasdaytest = christmasdaytest.strftime("%m-%d")
    
    halloweentest = date.fromisoformat('2024-10-31')
    halloweentest = halloweentest.strftime("%m-%d")
    
    thanksgivingtest = date.fromisoformat('2024-11-27')
    thanksgivingtest = thanksgivingtest.strftime("%m-%d")

    kickoff =  date.today()
    kickoff = kickoff.strftime("%m-%d")
    
    print(f"{intro(kickoff)}\ninsert printout here\n{worstintro(kickoff)}\ninsert bottom printout here")