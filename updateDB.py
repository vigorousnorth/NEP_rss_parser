
import psycopg2
from placeFilter import placeFilter
from rss_config import CONN_INFO, connectToDatabase
from RSS_parser import processRSS, writeToArticleDB


def updateSource(r):
    
    _source = r[0]
    _filters = r[1]
        
    with conn:
        with conn.cursor() as curs:
            curs.execute("SELECT * FROM feeds WHERE source = %s;", (_source,))
            the_feeds = curs.fetchall()
        
    print("Source: %s" % _source)
    filter_obj = placeFilter(_filters)
    processor = processRSS(filter_obj)
    
    for feed in the_feeds:
        url = feed[3]
        feed_id = feed[0]
        query_results = processor.parse_feed(url)
        writer = writeToArticleDB(CONN_INFO, feed_id)
        for r in query_results:
            writer.writeToDatabase(r)
        
        print("Feed: %s" % feed_id)
        

#### update database ####

conn = connectToDatabase(CONN_INFO, False)
with conn:
    with conn.cursor() as curs:
        curs.execute("SELECT * FROM filters;")
        filter_info = curs.fetchall()
        
        
for f in filter_info:
    updateSource(f)