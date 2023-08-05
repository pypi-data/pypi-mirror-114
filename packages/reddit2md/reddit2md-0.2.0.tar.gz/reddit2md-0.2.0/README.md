# reddit2md

Turn your favorite reddit post to .md file... That's it.

## Description

Put in praw.Submission object and get Markdown file of that post for printing/archiving stuff.

## Getting Started

### Dependencies

* Praw
* pytz (for Posted date timezone stuff)

### Installing

* `pip install reddit2md`

### Quickstart

```
import praw, reddit2md, settings

reddit = praw.Reddit(
                client_id = settings.credentials['client_id'],
                client_secret = settings.credentials['client_secret'],
                user_agent = settings.credentials['user_agent'],
            )

# reddit.config.decode_html_entities = True # Consider decoding HTML as some of the HTML entities might show up undecoded.

posts = reddit.subreddit('learnpython').hot(limit=5)

for post in posts:
    reddit2md.r2md(post, file_name=post.title ,timezone='Asia/Seoul') # file_name and timezone are both optional.
```

## Before you use

*reddit2md does not do any file management.* It will actually raise an Exception when the file already exists. It simply writes new file.

## Author

Lewis Lee
[@lewisleedev](https://github.com/lewisleedev)

## Version History

* 0.1.0
    * Initial Release

## License

This project is licensed under the MIT License - see the LICENSE file for details