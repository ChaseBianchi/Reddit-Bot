import praw

r = praw.Reddit(
    client_id="ASvc8XWI0XipBHmwnpBayQ",
    client_secret="Ol0C-2a85_OGOPPoAdBlVIp1D7h5rQ",
    user_agent="<console:DIABLOBOT:1.0>",
    username='Diablo-Bot',
    password='~E3Qzc-=8RH+Ws.',
)

sub = r.subreddit('projectdiablo2')

for post in sub.new(limit=50):
    title = post.title.lower()
    if 'pc' in title:
        print(title)
    