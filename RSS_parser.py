import re
import pandas as pd
import feedparser
import datetime
import psycopg2
from placeFilter import *


conn_info = {'dbname':'rss_feeds','username':'postgres','password':'redalert'}


def get_rss_info(conn_info):
    conn = connectToDatabase(conn_info)
    
    with conn:
        with conn.cursor() as curs:
            curs.execute("SELECT * FROM feeds;")
            results = curs.fetchall()

    return results


def updateDB(results, conn_info, place_filter):
    
    conn = connectToDatabase(conn_info)
    for r in results:
        updateRSS(r[3], r[0], conn, place_filter)
    

def updateRSS(url, feed_id, conn_obj, place_filter):
    
    parsed_results = parse_feed(url, place_filter)
    for results in parsed_results:
        writeToDatabase(results, feed_id, conn_obj)


         
############ RSS feed parsing functions ###############


def entry_parser(rss_entry):
    
    # need to add error handling
    parsed_results = dict()
    parsed_results['id'] = rss_entry.id
    parsed_results['title'] = rss_entry.title
    parsed_results['url'] = rss_entry.link
    parsed_results['summary'] = re.sub('<.*?>', '', rss_entry.summary)  # filter out HTML tags
    parsed_results['content'] = re.sub('<.*?>', '', rss_entry.content[0]['value'])
    date_temp = rss_entry.published_parsed[:3]
    parsed_results['date'] = datetime.date(year = date_temp[0], month = date_temp[1], day = date_temp[2])

    return parsed_results



def filter_entry(rss_entry, place_filter):
    
    parsed_entry = entry_parser(rss_entry)
    textblob = " ".join([parsed_entry['title'], parsed_entry['content'], parsed_entry['summary']])
    place_list = place_filter.checkFilters(textblob)
    
    if len(place_list) > 0:
        return {'entry':parsed_entry, 'places':place_list}
    else:
        return None




def parse_feed(rss_url, place_filter):
    
    assert isinstance(place_filter, placeFilter) == True
    
    results = feedparser.parse(rss_url)
    
    parsed_entries = []
    for entry in results.entries:
        parsed = filter_entry(entry, place_filter)
        if parsed != None:
            parsed_entries.append(parsed)
    
    return parsed_entries




######### write to database ###########

def writeArticle(data, feed_id, conn_object):
    
    data.update({'feed_id':feed_id})
    
    with conn_object:
        with conn_object.cursor() as curs:
            
            q = "INSERT INTO article (feed_id, content_id, title, date, summary, url) VALUES (%(feed_id)s, %(id)s, %(title)s, %(date)s, %(summary)s, %(url)s) RETURNING id;"
            curs.execute(q, data)
            return  curs.fetchone()
            


def writePlace(data, article_id, conn_object):
    
    q = "INSERT INTO place (article_id, place) VALUES (%s,%s);"
    with conn_object:
        with conn_object.cursor() as curs:
            for d in data:
                curs.execute(q, (article_id, d))
                
    
    
    
def writeToDatabase(data, feed_id, conn_obj):
    
    try:
        article_id = writeArticle(data['entry'], feed_id, conn_obj)
        writePlace(data['places'], article_id, conn_obj)
    except psycopg2.IntegrityError:
        pass
    


        




