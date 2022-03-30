import praw
#from praw.models import InlineGif, InlineImage, InlineVideo
import config
import time
import re
import sqlite3
import random


reply = {
    'pd2': 'Project Diablo 2 - A mod for and by passionate Diablo 2 fans. \n\n PD2 aims to maintain the Lord of Destruction experience and provide consistent ladder resets while improving on the game as if development never ceased. !reset for dates',
    'pc': 'Price check items by navigating to https://www.projectdiablo2.com/ and looking up your item on the trade tab. Find the lowest commonly listed price. Many even undercut the lowest listed prices to make a quick trade. Remember, mules dont kill monsters!',
    'fhr': '**Faster Hit Recovery Frames**\n\n&#x200B;\n\n|Character|Weapon|17|16|15|14|13|12|11|10|9|8|7|6|5|4|3|2|\n|:-|:-|-:|-:|-:|-:|-:|-:|-:|-:|-:|-:|-:|-:|-:|-:|-:|-:|\n|Amazon|all| | | | | | |0|6|13|20|32|52|86|174|600| |\n|Assassin|all| | | | | | | | |0|7|15|27|48|86|200| |\n|Barbarian|all| | | | | | | | |0|7|15|27|48|86|200| |\n|Druid Human|1H swinging| | | |0|3|7|13|19|29|42|63|99|174|456| | |\n|Druid human|other weapons| | | | |0|5|10|16|26|39|56|86|152|377| | |\n|Druid bear|all| | | | |0|5|10|16|24|37|54|86|152|360| | |\n|Druid wolf|all| | | | | | | | | | |0|9|20|42|86|280|\n|Necro human|all| | | | |0|5|10|16|26|39|56|86|152|377| | |\n|Necro vampire|all| | |0|2|6|10|16|24|34|48|72|117|?|?|?|?|\n|Paladin|spears / staves| | | | |0|3|7|13|20|32|48|75|129|280| | | |\n|Paladin|other| | | | | | | | |0|7|15|27|48|86|200| |\n|Sorceress|all| | |0|5|9|14|20|30|42|60|86|142|280| | | |\n|Merc Act 1|all| | | | | | |0|6|13|20|32|52|86|174|600| |\n|Merc Act 2|all| | |0|5|9|14|20|30|42|60|86|142|280| | |\n|Merc Act 3|all|0|5|8|13|18|24|32|46|63|86|133|232|600| | | |\n|Merc Act 5| | | | | | | | | |0|7|15|27|48|86|200| |\n\n&#x200B;',
    'fbr': '**Faster Block Rate Frames**\n\n&#x200B;\n\n|Character|Weapon / Skill / Form|17|16|15|14|13|12|11|10|9|8|7|6|5|4|3|2|1|\n|:-|:-|-:|-:|-:|-:|-:|-:|-:|-:|-:|-:|-:|-:|-:|-:|-:|-:|-:|\n|Amazon|1H Swinging|0|4|6|11|15|23|29|40|56|80|120|200|480| | | | |\n|Amazon|other weapons| | | | | | | | | | | | |0|13|32|86|600|\n|Assassin|all| | | | | | | | | | | | |0|13|32|86|600|\n|Barbarian|all| | | | | | | | | | |0|9|20|42|86|280| |\n|Druid|Human form| | | | | | |0|6|13|20|32|52|86|174|600| | |\n|Druid|Bear form| | | | | |0|5|10|16|27|40|65|109|223| | | |\n|Druid|Wolf form| | | | | | | | |0|7|15|27|48|86|200| | |\n|Necromancer|all| | | | | | |0|6|13|20|32|52|86|174|600| | |\n|Paladin|normal| | | | | | | | | | | | |0|13|32|86|600|\n|Paladin|w Holy Shield| | | | | | | | | | | | | | | |0|86|\n|Sorceress|all| | | | | | | | |0|7|15|27|48|86|200| | |\n\n&#x200B;',
    'fcr': '**Faster Cast Rate Frames**\n\n&#x200B;\n\n|Character|Skill / Form|23|22|21|20|19|18|17|16|15|14|13|12|11|10|9|8|7|\n|:-|:-|-:|-:|-:|-:|-:|-:|-:|-:|-:|-:|-:|-:|-:|-:|-:|-:|-:|\n|Amazon|all| | | | |0|7|14|22|32|48|68|99|152| | | | |\n|Assassin|all| | | | | | | |0|8|16|27|42|65|102|174| | |\n|Barbarian|all| | | | | | | | | | |0|9|20|37|63|105|200|\n|Druid|Human| | | | | |0|4|10|19|30|46|68|99|163| | | |\n|Druid|Bear form| | | | | | | |0|7|15|26|40|63|99|163| | |\n|Druid|Wolf form| | | | | | | |0|6|14|26|40|60|95|157| | |\n|Necromancer|Human| | | | | | | | |0|9|18|30|48|75|125| | |\n|Necromancer|Vampire|0|6|11|18|24|35|48|65|86|120|180| | | | | | |\n|Paladin|all| | | | | | | | |0|9|18|30|48|75|125| | |\n|Sorceress|Teleport / Chain Lightning| | | | |0|7|15|23|35|52|78|117|194| | | | |\n|Sorceress|other spells| | | | | | | | | | |0|9|20|37|63|105|200|\n|Merc Act 3|all| | | | | | |0|8|15|26|39|58|86|138| | | |\n\n&#x200B;',
    'reset': 'Reset dates: \n\n D2R - April 28, 2022 | PD2 - 6-8 weeks after D2R reset | POD - who knows _(o.O)/ \n\n updated 2/2/2022',
    'quote': '',
    'charsi': '',
    'roll': '',
    'lvl17druid': "hey guys, i play a level 17 druid, new to pod. I was just in a act 2 game where my group was killing the tombs over and over again, i think the game name was tombs-03 or something like that. well I am disconnected right now and can't log in. How do i make sure I get in the next game? I think think the exp was good",
    'craftleague': ' Crafters Race League 10AM PST April 1 - April 22. \n\n * Magic, rare, crafted items only. \n * 200% experience in hell mode \n * Dclone and Rathma materials sold by vendors \n * No full rejuvs(smalls still drop) \n * Player 5 map drops \n\n https://www.reddit.com/r/ProjectDiablo2/comments/tp6mx8/crafted_rare_only_league_announced_for_april_1st/',
    'help': 'Stay awhile and listen... \n\n Available commands: !',
    }
# build help command reply
commands = []
listCommands = list(reply.keys())
for i in range(len(listCommands)):
    commands.append(listCommands[i])
reply['help'] = reply['help'] + ' !'.join(commands)

quotes = ["Caravans take people where they want to go - until they get there. \n\n -Warriv", "I've met Meshif many times in my travels here. I've always enjoy trading stories with him about the exotic lands of the east. I'd wager he's sailed to many strange lands. \n\n -Warriv","Warriv may not remember me, but I helped him out when I was a young Paladin. There's no need for me to remind him. The rewards for honor will not come in this life. \n\n -Fara","Fate is like a caged gorilla. It will pelt you with dung if you mock it. \n\n -Warriv","The hero seemed more tormented every passing day. I remember he awoke many times -- screaming in the night -- always something about 'the East'. \n\n -Deckard Cain","I believe now that Tristram's hero was that Dark Wanderer who passed this way before the Monastery fell. \n\n -Deckard Cain","Long ago, Diablo and his brothers were cast out of Hell by the Lesser Evils. It seems that Hell's balance has shifted, as Andariel is now aligned with the Lord of Terror. Her presence here in the mortal realm does not bode well for us. \n\n -Deckard Cain","The story of Wirt is a frightening and tragic one. He was taken from the arms of his mother and dragged into the labyrinth by the small, foul demons that wield wicked spears. There were many other children taken that day, including the son of King Leoric. The Knights of the palace went below, but never returned. The Blacksmith found the boy, but only after the foul beasts had begun to torture him for their sadistic pleasures. \n\n -Deckard Cain","Griswold - a man of great action and great courage. I bet he never told you about the time he went into the Labyrinth to save Wirt, did he?  \n\n -Deckard Cain","This, Cain, whom you brought with you. He has the bearing of great power, yet I sense no magic about him. He is an enigma to me. \n\n -Hratli","Alkor is a potion dealer given over to a life steeped in ceaseless study and dissipation. \n\n -Hratli","My Order has been keeping watch over Ormus for many years, now. He seems to champion the cause of good, but who knows what shadow lurks within his soul? \n\n -Natalya","The Travincal can be breached by the loss of one's wits, not by the use of them. \n\n -Ormus", "Deckard Cain... Ormus has no time for the last son of the Horadrim. Pride led that holy Order to failure. \n\n -Ormus", "Asheara...? Oh, she's a tough-talking mage, but I'd wager she's never faced true Evil. Pampering drunken mercenaries is one thing, but standing face to face with a Hell-spawned Demon is another. \n\n -Natalya","Some find my prices unreasonable. That is because I am unreasonable. \n\n Hratli","You have questions for Ormus and doubt in yourself. Ormus sees a strange dichotomy in you... as he does in all would-be heroes. \n\n -Ormus","Back so soon? Don't be ashamed. Even Ormus knows that the fires of hell would wilt any man's resolve. \n\n - Ormus", "can you imagine having to wake up every night just to piss for the next thousand years? \n\n -Meshif", "Good luck! Though this be our darkest hour, it may yet be your greatest moment. \n\n -Tyrael", "This act will change your world forever -- with consequences even I cannot foresee. However, it is the only way to ensure mankind's survival. \n\n -Tyrael", "May I remind you that my caravan can only go east if the Monastery is cleansed? \n\n -Warriv"]

conn = sqlite3.connect('diablo.db')
c = conn.cursor()

def db_write(postid, author, keywords):
    c.execute(f"INSERT INTO post VALUES ('{postid}', '{author}', '{keywords}')")
        
def db_fetch(): # returns list of tuples
    c.execute("SELECT * FROM post")
    return c.fetchall()

def db_update_keywords(keywords, commentid):
    c.execute(f"UPDATE post SET keywords = '{keywords}' WHERE id = '{commentid}'")


def parse_data(data): # returns dict with postid as keys
    parsed = {}
    for item in data:
        if len(item) == 3:
            parsed[item[0]] = {'author': item[1], 'keywords': item[2]}
        else:
            print(f'error, db entry length item {item}')
    return parsed

def handle_post_body(post, db_data): # parsing post body and generating replies
    if post.author != 'Diablo-Bot' and post.selftext:
        body = post.selftext.lower()
        foundKeys = []
        for i in range(len(reply)):
            replyKey = list(reply.keys())[i]
            if f'!{replyKey}' in body:
                foundKeys.append(replyKey)
        if len(foundKeys) > 0:
            if post.id in db_data.keys():
                newMessage = ''
                for k in foundKeys:
                    if k not in db_data[post.id]['keywords']:
                        if k == 'charsi':
                            # post.reply(praw.models.InlineGif('https://static.wikia.nocookie.net/diablo/images/8/8b/Charsi.gif/revision/latest/zoom-crop/width/360/height/360?cb=20080817212751', f"Best I can do is {random.randrange(1, 35001)} gold."))
                            # newkeywords = db_data[post.id]['keywords'] + ' charsi'
                            # db_update_keywords(newkeywords, post.id)
                            newMessage += f'Charsi: "Best I can do is {str(random.randrange(1, 35001))} gold." \n\n '
                            if len(foundKeys)>1:
                                newMessage += ' ********** \n\n '
                        elif k == 'quote':
                            randomQuote = quotes[random.randrange(0, len(quotes))]
                            newMessage = newMessage + randomQuote + ' \n\n '
                            if len(foundKeys)>1:
                                newMessage += ' ********** \n\n '
                        elif k == 'roll':
                            newMessage += f'{post.author} rolled {str(random.randrange(1, 101))}. \n\n '
                            if len(foundKeys)>1:
                                newMessage += ' ********** \n\n '
                        else:
                            newMessage += reply[k] + ' \n\n '
                            if len(foundKeys)>1:
                                newMessage += ' ********** \n\n '
                if len(newMessage) > 0:
                    newMessage += '`Reply !help to see all commands. Make this bot better by sending suggestions and bugs to` /u/ChaseBianchi'
                    post.reply(newMessage)
                    c.execute(f"UPDATE post SET keywords = '{' '.join(foundKeys)}' WHERE id = '{post.id}'")
                    print('***REPLY OLD POST***')
                    time.sleep(10)

            else:
                newMessage = ''
                for k in foundKeys:
                    if k == 'charsi':
                        # post.reply(praw.models.InlineGif('https://static.wikia.nocookie.net/diablo/images/8/8b/Charsi.gif/revision/latest/zoom-crop/width/360/height/360?cb=20080817212751', f"Best I can do is {random.randrange(1, 35001)} gold."))
                        # if len(foundKeys) == 1: 
                        #     db_write(post.id, post.author, 'charsi')
                        newMessage += f'Charsi: "Best I can do is {str(random.randrange(1, 35001))} gold." \n\n '
                        if len(foundKeys)>1:
                            newMessage += ' ********** \n\n '
                    elif k == 'quote':
                        randomQuote = quotes[random.randrange(0, len(quotes))]
                        newMessage = newMessage + randomQuote + ' \n\n '
                        if len(foundKeys)>1:
                            newMessage += ' ********** \n\n '
                    elif k == 'roll':
                        newMessage += f'{post.author} rolled {str(random.randrange(1, 101))}. \n\n '
                        if len(foundKeys)>1:
                            newMessage += ' ********** \n\n '
                    else:
                        newMessage += reply[k] + ' \n\n '
                        if len(foundKeys)>1:
                            newMessage += ' ********** \n\n '
                    
                if len(newMessage) > 0:   
                    newMessage += '`Reply !help to see all commands. Make this bot better by sending suggestions and bugs to` /u/ChaseBianchi'
                    post.reply(newMessage)
                    db_write(post.id, post.author, ' '.join(foundKeys))
                    print('***REPLY NEW POST SLEEP 10***')
                    time.sleep(10)


def handle_comment(comment, db_data): # parsing comments and generating replies
    if hasattr(comment, 'body') and comment.author != 'Diablo-Bot':
        body = comment.body.lower()
        foundKeys = []
        for i in range(len(reply)):
            replyKey = list(reply.keys())[i]
            if f'!{replyKey}' in body:
                foundKeys.append(replyKey)
        if len(foundKeys) > 0:
            if comment.id in db_data.keys():
                newMessage = ''
                for k in foundKeys:
                    if k not in db_data[comment.id]['keywords']:
                        if k == 'charsi':
                            # comment.reply(praw.models.InlineGif('https://static.wikia.nocookie.net/diablo/images/8/8b/Charsi.gif/revision/latest/zoom-crop/width/360/height/360?cb=20080817212751', f"Best I can do is {random.randrange(1, 35001)} gold."))
                            # newkeywords = db_data[comment.id]['keywords'] + ' charsi'
                            # db_update_keywords(newkeywords, comment.id)
                            newMessage += f'Charsi: "Best I can do is {str(random.randrange(1, 35001))} gold." \n\n '
                            if len(foundKeys)>1:
                                newMessage += ' ********** \n\n '
                        elif k == 'quote':
                            randomQuote = quotes[random.randrange(0, len(quotes))]
                            newMessage = newMessage + randomQuote + ' \n\n '
                            if len(foundKeys)>1:
                                newMessage += ' ********** \n\n '
                        elif k == 'roll':
                            newMessage += f'{comment.author} rolled {str(random.randrange(1, 101))}. \n\n '
                            if len(foundKeys)>1:
                                newMessage += ' ********** \n\n '
                        else:
                            newMessage += reply[k] + ' \n\n '
                            if len(foundKeys)>1:
                                newMessage += ' ********** \n\n '
                if len(newMessage) > 0:
                    newMessage += '`Reply !help to see all commands. Make this bot better by sending suggestions and bugs to` /u/ChaseBianchi'
                    comment.reply(newMessage)
                    c.execute(f"UPDATE post SET keywords = '{' '.join(foundKeys)}' WHERE id = '{comment.id}'")
                    print('*** REPLY OLD COMMENT ***')
                    time.sleep(10)

            else:
                newMessage = ''
                for k in foundKeys:
                    if k == 'charsi':
                        # comment.reply(praw.models.InlineGif('https://static.wikia.nocookie.net/diablo/images/8/8b/Charsi.gif/revision/latest/zoom-crop/width/360/height/360?cb=20080817212751', f"Best I can do is {random.randrange(1, 35001)} gold."))
                        # if len(foundKeys) == 1: 
                        #     db_write(comment.id, comment.author, 'charsi')
                        newMessage += f'Charsi: "Best I can do is {str(random.randrange(1, 35001))} gold." \n\n '
                        if len(foundKeys)>1:
                            newMessage += ' ********** \n\n '
                    elif k == 'quote':
                        randomQuote = quotes[random.randrange(0, len(quotes))]
                        newMessage = newMessage + randomQuote + ' \n\n '
                        if len(foundKeys)>1:
                            newMessage += ' ********** \n\n '
                    elif k == 'roll':
                        newMessage += f'{comment.author} rolled {str(random.randrange(1, 101))}. \n\n '
                        if len(foundKeys)>1:
                            newMessage += ' ********** \n\n '
                    else:
                        newMessage += reply[k] + ' \n\n '
                        if len(foundKeys)>1:
                            newMessage += ' ********** \n\n '
                    
                if len(newMessage) > 0:   
                    newMessage += '`Reply !help to see all commands. Make this bot better by sending suggestions and bugs to` /u/ChaseBianchi'
                    comment.reply(newMessage)
                    db_write(comment.id, comment.author, ' '.join(foundKeys))
                    print('*** REPLY NEW COMMENT ***')
                    time.sleep(10)
    

def run_bot():
    fails = 0
    
    r = praw.Reddit(
        client_id= config.diablo_client_id,
        client_secret= config.diablo_client_secret,
        user_agent= config.diablo_user_agent,
        username= config.diablo_username,
        password= config.diablo_password,
        check_for_async=False,
    )
   
    sub = r.subreddit('projectdiablo2')

    def run_search(): #performs the search of posts and comments
        db_data = parse_data(db_fetch())
        for post in sub.hot(limit=50):
            handle_post_body(post, db_data) # parse and reply to post
            submission = r.submission(id=post.id)
            submission.comments.replace_more(limit=0)
            for comment in submission.comments.list():
                handle_comment(comment, db_data) # parse and reply to comments

        conn.commit()
        #print('sleeping for 60 seconds')
        #print('******')
        time.sleep(60)
        run_search()
        
    try:
        run_search()
        
    # ERROR HANDLING
    except praw.exceptions.RedditAPIException as e:
        print(e)
        if fails>15:
            print('15 fails, EXIT')
            conn.close()
            exit()
        for error in e.items:
            if error.error_type == 'RATELIMIT':
                delay = re.search('(\d+) minute', error.error_message)
                if delay:
                    seconds = float(int(delay.group(1))*60 + 61)
                    print('***RATE LIMIT*** sleeping for ' + str(seconds) + ' seconds')
                    time.sleep(seconds)
                    run_search()
                else:
                    delay = re.search('(\d+) second', error.error_message)
                    seconds = float(delay.group(1))
                    print('***RATE LIMIT*** sleeping for ' + str(seconds) + ' seconds')
                    time.sleep(seconds + 2)
                    run_search()
            else:
                fails += 1
                print(error)
                print('***ERROR*** Sleeping for 300 seconds')
                time.sleep(300)
                run_search()
                
run_bot()
                
                
   