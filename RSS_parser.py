import re
import pandas as pd
import feedparser

rss_url = 'http://www.pressherald.com/category/news/feed/'


results = feedparser.parse(rss_url)

len(results.entries[0][0])