# Reddit Bot 🤖
Bot crawls a subreddit to serve requested data to users by parsing comments for keywords.

## Technology 👨‍💻

* Python for general scripting
* SQLite3 database stores comments that have been replied to, preventing duplicates
* Python Reddit API Wrapper(PRAW) streamlines interacting with Reddit API

## Config 🛠
Reddit login credentials are stored in a seperate file, and pulled in like the example below. See [PRAW](https://praw.readthedocs.io/en/stable/) documentation for setting your credentials.
```
import praw
import config

r = praw.Reddit(
    client_id= config.diablo_client_id,
    client_secret= config.diablo_client_secret,
    user_agent= config.diablo_user_agent,
    username= config.diablo_username,
    password= config.diablo_password,
    check_for_async=False,
)
```

Set the subreddit you wish to use the bot with.
```
sub = r.subreddit('projectdiablo2')
```

The variable **reply** holds key:value pairs that the bot will scan comments for the key, and reply with the value. 
```
 reply = {...}
```

A database is needed to ensure posts that have been seen and resolved are marked as such. Database can be configured here
```
conn = sqlite3.connect('diablo.db') #input your database in place of diablo.db
```

Kind of posts(new, hot, etc) and number of posts on a subreddit can both be changed. Refer to [PRAW](https://praw.readthedocs.io/en/stable/).
```
for post in sub.hot(limit=50):
```

Posts are handled first with `handle_post_body` followed by iterating over all the comments on each post with `handle_comment`
```
def run_search(): #performs the search of posts and comments
        db_data = parse_data(db_fetch())
        for post in sub.hot(limit=50):
            handle_post_body(post, db_data) # parse and reply to post
            submission = r.submission(id=post.id)
            submission.comments.replace_more(limit=0)
            for comment in submission.comments.list():
                handle_comment(comment, db_data) # parse and reply to comments
```

## Handling Complex Requests 💡
Most of the requests in my current implementation are static. A key generates a response of a single string(question asked, and answered type of uses). If a request needs a more complex answer, it will be handled in a custom if/else statement.
```
if k == 'complexKey':
  complex_response = --prepare complex response--
  newMessage += complex_response
```

## Error Handling 🚨
When being rate limited, the error message is parsed for the timeout amount, and sleeps for that amount of time until executing next query.

If an error besides rate limit is returned, it is stored in a counter. Reddit bot will idle for one minute before restarting.

Hard exit after 15 non-rate-limit errors.
