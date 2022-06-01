import feedparser
from datetime import datetime
import pytz
from dateutil import parser
import dateutil.tz as tz
from dateutil.tz import UTC

NewsFeed = feedparser.parse("http://feeds.bbci.co.uk/news/world/rss.xml")

entry = NewsFeed.entries[1]


if __name__ == "__main__":
    date_string = 'Jun 1 2005  1:33PM'
    datetime_object = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
    # datetime_article = datetime.strptime(entry.published, "%a, %b %d %Y %H:%M:%S %Z")
    # datetime_str = datetime.strptime('Wed, 03 Oct 2018 23:47:32 EDT', "%a, %d %b %Y %H:%M:%S %Z")
    # datetime_str = datetime.strptime('Wed, 03 Oct 2018 23:47:32 EDT', "%a, %d %b %Y %H:%M:%S %Z")
    tzinfos = {"CST": tz.gettz("America/Chicago"),
           "CDT": tz.gettz("America/Chicago"),                
           "EST": tz.gettz("America/Eastern"),
           "EDT": tz.gettz("America/Eastern")                 
           }
    parsed_date = parser.parse('Wed, 03 Oct 2018 23:47:32 PDT', tzinfos=tzinfos)
    to_utc = parsed_date.astimezone(UTC).replace(tzinfo=None)
    now_time = datetime.utcnow()
    print(now_time)
    print(to_utc)
    diff = now_time - to_utc 
    print(diff.days)

    