import praw
from praw.models import InlineGif, InlineImage, InlineVideo
import config
import sched
import time
import re
import sqlite3
import random

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
    
    reply = {
        'pd2': 'Project Diablo 2 - A mod for and by passionate Diablo 2 fans. \n\n PD2 aims to maintain the Lord of Destruction experience and provide consistent ladder resets while improving on the game as if development never ceased. !reset for dates',
        'pc': 'Price check items by navigating to https://www.projectdiablo2.com/ and looking up your item on the trade tab. Find the lowest commonly listed price. Many even undercut the lowest listed prices to make a quick trade. Remember, mules dont kill monsters!',
        # 'fhr': 'Faster Hit Recovery frames can be found at https://diablo2.diablowiki.net/Breakpoints#Faster_Hit_Recovery \n\n To get FHR of a specific class type !fhr[class] e.g. !fhramazon',
        # 'fbr': 'Faster Block Rate frames can be found at https://diablo2.diablowiki.net/Breakpoints#Increased_Blocking_Speed \n\n Get fbr of a specific class, type !fbr[class] e.g. !fbrpaladin ',
        # 'fcr': 'Faster Cast Rate frames can be found at https://diablo2.diablowiki.net/Breakpoints#Faster_Cast_Rate \n\n Get fcr of a specific class, type !fcr[class] e.g. !fcrsorceress',
        'breakpoints': 'Breakpoints can be found at https://diablo2.diablowiki.net/Breakpoints \n\n For specific breakpoints by type and class use ![breakpoint][class] e.g. !fcrsorceress !fhrbarbarian !fbrpaladin',
        'reset': 'Reset dates: \n\n D2R - April 28, 2022 | PD2 - 6-8 weeks after D2R reset | POD - who knows _(o.O)/ \n\n updated 2/2/2022',
        'fcrsorceress': 'Sorceress FCR breakpoints, shown as fcr(frames) \n\n All other Spells - 0(13) 9(12) 20(11) 37(10) 63(9) 105(8) 200(7) \n\n Lightning/CL(teleport in PD2) - 0(19) 7(18) 15(17) 23(16) 35(15) 52(14) 78(13) 117(12) 194(11)',
        'fcramazon': 'Amazon FCR breakpoints, shown as fcr(frames) \n\n 0(19) 7(18) 14(17) 22(16) 32(15) 48(14) 68(13) 99(12) 152(11)',
        'fcrassassin': 'Assassin FCR breakpoints, shown as fcr(frames) \n\n 0(16) 8(15) 16(14) 27(13) 42(12) 65(11) 102(10) 174(9)',
        'fcrnecromancer': 'Necromancer FCR breakpoints, shown as fcr(frames) \n\n Human - 0(15) 9(14) 18(13) 30(12) 48(11) 75(10) 125(9) \n\n Vampire - 0(23) 6(22) 11(21) 18(20) 24(19) 35(18) 48(17) 65(16) 86(15) 120(14) 180(13)',
        'fcrbarbarian': 'Barbarian FCR breakpoints, shown as fcr(frames) \n\n 0(13) 9(12) 20(11) 37(10) 63(9) 105(8) 200(7)',
        'fcrdruid': 'Druid FCR breakpoints, shown as fcr(frames) \n\n  Human - 0(18) 4(17) 10(16) 19(15) 30(14) 46(13) 68(12) 99(11) 163(10) \n\n Bear - 0(16) 7(15) 15(14) 26(13) 40(12) 63(11) 99(10) 163(9) \n\n Wolf - 0(16) 6(15) 14(14) 26(13) 40(12) 60(11) 95(10) 157(9)',
        'fcrpaladin': 'Paladin FCR breakpoints, shown as fcr(frames) \n\n 0(15) 9(14) 18(13) 30(12) 48(11) 75(10) 125(9)',
        'fhrsorceress': 'Sorceress FHR breakpoints, shown as fhr(frames) \n\n 0(15) 5(14) 9(13) 14(12) 20(11) 30(10) 42(9) 60(8) 86(7) 142(6) 280(5)',
        'fhramazon': 'Amazon FHR breakpoints, shown as fhr(frames) \n\n 0(11) 6(10) 13(9) 20(8) 32(7) 52(6) 86(5) 174(4)',
        'fhrassassin': 'Assassin FHR breakpoints, shown as fhr(frames) \n\n 0(9) 7(8) 15(7) 27(6) 48(5) 86(4) 200(3)',
        'fhrnecromancer': 'Necromancer FHR breakpoints, shown as fhr(frames) \n\n Human - 0(13) 5(12) 10(11) 16(10) 26(9) 39(8) 56(7) 86(6) 152(5) \n\n Vampire - 0(15) 2(14) 6(13) 10(12) 16(11) 24(10) 34(9) 48(8) 72(7) 117(6)',
        'fhrbarbarian': 'Barbarian FHR breakpoints, shown as fhr(frames) \n\n 0(9) 7(8) 15(7) 27(6) 48(5) 86(4) 200(3)',
        'fhrdruid': 'Druid FHR breakpoints, shown as fhr(frames) \n\n Human(1h weapon) - 0(14) 3(13) 7(12) 13(11) 19(10) 29(9) 42(8) 63(7) 99(6) 174(5) \n\n Human(other weapons) - 0(13) 5(12) 10(11) 16(10) 26(9) 39(8) 56(7) 86(6) 152(5) \n\n Bear - 0(13) 5(12) 10(11) 16(10) 24(9) 37(8) 54(7) 86(6) 152(5) \n\n Wolf - 0(7) 9(6) 20(5) 42(4) 86(3) 280(2)',
        'fhrpaladin': 'Paladin FHR breakpoints, shown as fhr(frames) \n\n All other weapons - 0(9) 7(8) 15(7) 27(6) 48(5) 86(4) 200(3) \n\n Spears/Staves - 0(13) 3(12) 7(11) 13(10) 20(9) 32(8) 48(7) 75(6) 129(5)',
        'fbrsorcoress': 'Sorceress FBR breakpoints, shown as fbr(frames) \n\n 0(9) 7(8) 15(7) 27(6) 48(5) 86(4) 200(3)',
        'fbramazon': 'Amazon FBR breakpoints, shown as fbr(frames) \n\n 1h Swinging Weapon - 0(17) 4(16) 6(15) 11(14) 15(13) 23(12) 29(11) 40(10) 56(9) 80(8) 120(7) \n\n Other Weapons - 0(5) 13(4) 32(3) 86(2)',
        'fbrassassin': 'Assassin FBR breakpoints, shown as fbr(frames) \n\n 0(5) 13(4) 32(3) 86(2)',
        'fbrnecromancer': 'Necromancer FBR breakpoints, shown as fbr(frames) \n\n 0(11) 6(10) 13(9) 20(8) 32(7) 52(6) 86(5)',
        'fbrbarbarian': 'Barbarian FBR breakpoints, shown as fbr(frames) \n\n 0(7) 9(6) 20(5) 42(4) 86(3)',
        'fbrdruid': 'Druid FBR breakpoints, shown as fbr(frames) \n\n Human - 0(11) 6(10) 13(9) 20(8) 32(7) 52(6) 86(5) \n\n Bear 0(12) 5(11) 10(10) 16(9) 27(8) 40(7) 65(6) 109(5) \n\n Wolf - 0(9) 7(8) 15(7) 27(6) 48(5) 86(4)',
        'fbrpaladin': 'Paladin FBR breakpoints, shown as fbr(frames) \n\n without Holy shield - 0(5) 13(4) 32(3) 86(2) \n\n With Holy Shield - 0(2) 86(1)',
        'quote': '',
        'charsi': '',
        'roll': '',
        'lvl17druid': "hey guys, i play a level 17 druid, new to pod. I was just in a act 2 game where my group was killing the tombs over and over again, i think the game name was tombs-03 or something like that. well I am disconnected right now and can't log in. How do i make sure I get in the next game? I think think the exp was good",
        'help': 'Stay awhile and listen... \n\n Available commands: !',
        'craftleague': ' Crafters Race League 10AM PST April 1 - April 22. \n\n * Magic, rare, crafted items only. \n * 200% experience in hell mode \n * Dclone and Rathma materials sold by vendors \n * No full rejuvs(smalls still drop) \n * Player 5 map drops \n\n https://www.reddit.com/r/ProjectDiablo2/comments/tp6mx8/crafted_rare_only_league_announced_for_april_1st/'
        }
    # build help command reply
    commands = []
    listCommands = list(reply.keys())
    for i in range(len(listCommands)):
        commands.append(listCommands[i])
    reply['help'] = reply['help'] + ' !'.join(commands)
    
    quotes = ["Caravans take people where they want to go - until they get there. \n\n -Warriv", "I've met Meshif many times in my travels here. I've always enjoy trading stories with him about the exotic lands of the east. I'd wager he's sailed to many strange lands. \n\n -Warriv","Warriv may not remember me, but I helped him out when I was a young Paladin. There's no need for me to remind him. The rewards for honor will not come in this life. \n\n -Fara","Fate is like a caged gorilla. It will pelt you with dung if you mock it. \n\n -Warriv","The hero seemed more tormented every passing day. I remember he awoke many times -- screaming in the night -- always something about 'the East'. \n\n -Deckard Cain","I believe now that Tristram's hero was that Dark Wanderer who passed this way before the Monastery fell. \n\n -Deckard Cain","Long ago, Diablo and his brothers were cast out of Hell by the Lesser Evils. It seems that Hell's balance has shifted, as Andariel is now aligned with the Lord of Terror. Her presence here in the mortal realm does not bode well for us. \n\n -Deckard Cain","The story of Wirt is a frightening and tragic one. He was taken from the arms of his mother and dragged into the labyrinth by the small, foul demons that wield wicked spears. There were many other children taken that day, including the son of King Leoric. The Knights of the palace went below, but never returned. The Blacksmith found the boy, but only after the foul beasts had begun to torture him for their sadistic pleasures. \n\n -Deckard Cain","Griswold - a man of great action and great courage. I bet he never told you about the time he went into the Labyrinth to save Wirt, did he?  \n\n -Deckard Cain","This, Cain, whom you brought with you. He has the bearing of great power, yet I sense no magic about him. He is an enigma to me. \n\n -Hratli","Alkor is a potion dealer given over to a life steeped in ceaseless study and dissipation. \n\n -Hratli","My Order has been keeping watch over Ormus for many years, now. He seems to champion the cause of good, but who knows what shadow lurks within his soul? \n\n -Natalya","The Travincal can be breached by the loss of one's wits, not by the use of them. \n\n -Ormus", "Deckard Cain... Ormus has no time for the last son of the Horadrim. Pride led that holy Order to failure. \n\n -Ormus", "Asheara...? Oh, she's a tough-talking mage, but I'd wager she's never faced true Evil. Pampering drunken mercenaries is one thing, but standing face to face with a Hell-spawned Demon is another. \n\n -Natalya","Some find my prices unreasonable. That is because I am unreasonable. \n\n Hratli","You have questions for Ormus and doubt in yourself. Ormus sees a strange dichotomy in you... as he does in all would-be heroes. \n\n -Ormus","Back so soon? Don't be ashamed. Even Ormus knows that the fires of hell would wilt any man's resolve. \n\n - Ormus", "can you imagine having to wake up every night just to piss for the next thousand years? \n\n -Meshif", "Good luck! Though this be our darkest hour, it may yet be your greatest moment. \n\n -Tyrael", "This act will change your world forever -- with consequences even I cannot foresee. However, it is the only way to ensure mankind's survival. \n\n -Tyrael", "May I remind you that my caravan can only go east if the Monastery is cleansed? \n\n -Warriv"]
    

    def run_search():
        dbData = parse_data(db_fetch())
        for post in sub.hot(limit=50):
            submission = r.submission(id=post.id)
            submission.comments.replace_more(limit=0)
            for comment in submission.comments.list():
                if hasattr(comment, 'body') and comment.author != 'Diablo-Bot':
                    body = comment.body.lower()
                    foundKeys = []
                    for i in range(len(reply)):
                        replyKey = list(reply.keys())[i]
                        if f'!{replyKey}' in body:
                            foundKeys.append(replyKey)
                    if len(foundKeys) > 0:
                        if comment.id in dbData.keys():
                            newMessage = ''
                            for k in foundKeys:
                                if k not in dbData[comment.id]['keywords']:
                                    if k == 'charsi':
                                        # comment.reply(praw.models.InlineGif('https://static.wikia.nocookie.net/diablo/images/8/8b/Charsi.gif/revision/latest/zoom-crop/width/360/height/360?cb=20080817212751', f"Best I can do is {random.randrange(1, 35001)} gold."))
                                        # newkeywords = dbData[comment.id]['keywords'] + ' charsi'
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
                                newMessage += 'Comment !help to see all commands. Report bugs or send suggestions to /u/ChaseBianchi'
                                comment.reply(newMessage)
                                c.execute(f"UPDATE post SET keywords = '{' '.join(foundKeys)}' WHERE id = '{comment.id}'")
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
                                newMessage += 'Comment !help to see all commands. Report bugs or send suggestions to /u/ChaseBianchi'
                                comment.reply(newMessage)
                                db_write(comment.id, comment.author, ' '.join(foundKeys))

        conn.commit()
        print('sleeping for 60 seconds')
        print('******')
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
                    print('sleeping for ' + str(seconds) + ' seconds')
                    time.sleep(seconds)
                    run_search()
                else:
                    delay = re.search('(\d+) second', error.error_message)
                    seconds = float(delay.group(1))
                    print('sleeping for ' + str(seconds) + ' seconds')
                    time.sleep(seconds + 2)
                    run_search()
            else:
                fails += 1
                print(error)
                time.sleep(60)
                run_search()
                
run_bot()
                
                
   