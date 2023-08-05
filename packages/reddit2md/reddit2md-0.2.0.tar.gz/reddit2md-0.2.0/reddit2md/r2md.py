import praw, datetime, pytz
from . import utils, exceptions

def r2md(post, **kwargs):
    '''
    Convert given post to markdown and save it as a file in current path as given file name.

            Parameters:
                    post (:obj:`praw.models.Submission`): A Praw's submission object
                    file_name (str): File name for the converted markdown file. If left empty, post id will be the file name automatically. (file format(.md) should also be specified.)
                    timezone (str): Timezone for a posted time/date. Default is UTC.
    '''

    for key in kwargs:
        if key not in ('file_name', 'timezone'):
            raise exceptions.reddit2mdValueError("Unknown parameter(s) is/are given.")

    if not post.is_self:
        raise exceptions.reddit2mdValueError("Only selftext posts are supported.")
    
    if not kwargs.get('file_name'):
        file_name = "{}.md".format(post.id)
    else:
        file_name = kwargs.get('file_name')
    
    md_splitted = post.selftext.splitlines()
    
    result_md = []

    for line in md_splitted:
        if utils.is_url_image(line):
            line = '![]({url})'.format(url = line)
        result_md.append(line)

    result = {
        "title": post.title,
        "author": post.author.name,
        "selftext": result_md,
        "url": utils.make_reddit_url(post.permalink),
        "created_date": utils.get_posted_date(post),
        "subreddit": post.subreddit.display_name
    }

    author_as_link = "[{}]({})".format(result['author'], utils.make_reddit_url("u/{}".format(result['author'])))

    if kwargs.get('timezone'):
        timezone = kwargs.get('timezone')
        if not timezone in pytz.all_timezones:
            raise reddit2mdValueError("Timezone {} is not listed in pytz.")
        tz_converted = pytz.timezone(timezone)
        result['created_date'] = tz_converted.fromutc(result['created_date'])
    else:
        timezone = 'UTC'
    
    try:
        f = open(file_name, "x")
        f.write("# {}".format(result["title"]) + '\n\n')
        for l in result["selftext"]:
            f.write(l + '\n')
        f.write('\n' + "---" + '\n')
        f.write("Author: {}".format(author_as_link) + '\n\n')
        f.write("URL: {}".format(result["url"]) + '\n\n')
        f.write("Created: {} ({})".format(result["created_date"], timezone) + '\n\n')
        f.write("Subreddit: r/{}".format(result["subreddit"]))
    except OSError as e:
        raise exceptions.reddit2mdOSError("OSError during file creation: {}".format(e))