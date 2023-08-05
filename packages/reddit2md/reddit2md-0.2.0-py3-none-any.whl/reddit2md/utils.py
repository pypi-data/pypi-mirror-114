from urllib.parse import urlparse
import datetime

def is_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def is_url_image(url):
    if is_url(url):
        image_formats = ("image/png", "image/jpeg", "image/jpg")
        r = requests.head(image_url)
        try:
            if r.headers["content-type"] in image_formats:
                return True
        except:
            return False
    else:
        return False

def get_posted_date(submission, timezone=None):
    date_plain = submission.created_utc
    posted_date = datetime.datetime.fromtimestamp(date_plain)
    return posted_date

def make_reddit_url(str):
    url = "https://reddit.com"
    url = '{}/{}'.format(url, str)
    return url