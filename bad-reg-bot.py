import praw
import config

r = praw.Reddit(
    client_id= config.poker_client_id,
    client_secret= config.poker_client_secret,
    user_agent= config.poker_user_agent,
    username= config.poker_username,
    password= config.poker_password,
)

sub = r.subreddit('poker')

for post in sub.hot(limit=40):
    print('####################')
    print(post.title)
    print('####################')
    
    for comment in post.comments:
        if hasattr(comment, 'body'):
            print(comment.body)
            print('------------------')