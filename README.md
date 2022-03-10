# Reddit Bot 🤖
Bot crawls a subreddit to serve requested data to users by parsing comments for keywords.

## Technology 👨‍💻

-Python for general scripting
-SQLite3 database stores comments that have been replied to, preventing duplicates
-Python Reddit API Wrapper(PRAW) streamlines interacting with Reddit API

## Config 🛠
Reddit login credentials are stored in a seperate file, and pulled in like the example below. See [PRAW](https://praw.readthedocs.io/en/stable/) documentation for setting your credentials.
```
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

Kind of posts(new, hot, etc) and number of posts on a subreddit can both be changed. Refer to [PRAW](https://praw.readthedocs.io/en/stable/).
```
for post in sub.hot(limit=50):
```

## Handling Complex Requests
Most of the requests in my current implementation are static. A key generates a response of a single string(question asked, and answered type of uses). If a request needs a more complex answer, it will be handled in a custom if/else statement.
```
if k == 'complexKey':
  complex_response = --prepare complex response--
  newMessage += complex_response
```

## Error Handling
When being rate limited, the error message is parsed for the timeout amount, and sleeps for that amount of time until executing next query.

If an error besides rate limit is returned, it is stored in a counter. Reddit bot will idle for one minute before restarting.

Hard exit after 15 non-rate-limit errors.
