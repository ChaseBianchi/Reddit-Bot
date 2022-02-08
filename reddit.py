import praw

r = praw.Reddit(
    client_id="P8ulzNkYLBu6Yhgyn_Q5gQ",
    client_secret="zYcGlC7nVdJn89gLwFHs4Z3WCETBbg",
    user_agent="<console:BADREG:1.0>",
    username='Bad-Reg-Bot',
    password='j7$%wTg^4F+UBAK',
)

sub = r.subreddit('poker')

for post in sub.hot(limit=20):
    print('####################')
    print(post.title)
    print('####################')
    
    for comment in post.comments:
        if hasattr(comment, 'body'):
            print(comment.body)
            print('------------------')