import json, os, bz2
import unicodecsv as csv
from IPython.display import clear_output
import multiprocessing as mp
import time
from multiprocessing import Pool, Manager,Lock
import numpy as np
keywords = ['dog']
directory = r'C:\Users\jqw18\Desktop\01'
outfile = r'C:\Users\jqw18\Desktop\out02'


def init(l):
	global lock
	lock = l


def process_json(keywords, directory, outfile,my_dict):
    cursor = '  >>  '
    pool = Pool(processes=15, initializer=init, initargs=(lock,))
    allfiles = []
    for dirs, subdirs, files in os.walk(directory):
        for file in files:
            #allfiles.append(file)
    #print(len(allfiles))
            #func(my_dict,dirs, file, keywords,outfile)
            pool.apply_async(func, args=(my_dict,dirs, file, keywords,outfile),callback=log_result)
    pool.close()
    pool.join()
    clear_output()
    print(cursor, 'mentions:', my_dict['count_mentions'])
    print(cursor, 'replies:', my_dict['count_replies'])
    print(cursor, ' tweets:', my_dict['count_tweets'])
    print(cursor, ' * total: ', my_dict['count_mentions'] + my_dict['count_replies'] + my_dict['count_tweets'])
    print('-' * 10)
    print(cursor, 'currently searching', dirs)

def log_result(result):
    tweet =result['tweet']
    poster = result['poster']
    tweet_date = result['tweet_date']
    tweet_id = result['tweet_id']
    tweet_text = result['tweet_text']
    tweet_followers = result['tweet_followers']
    hashes = result['hashes']
    retweet = result['retweet']
    recipient =result["recipient"]

    #tweet,poster,tweet_date,tweet_id,tweet_text,tweet_followers,hashes,retweet,recipient
    outfile = r'C:\Users\jqw18\Desktop\out02'
    with open(outfile, 'wb') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            ['poster', 'recipient', 'relationship', ' tweet date', ' tweet id', 'tweet', 'followers', 'hashtags',
             'retweet status'])


        reply_status = 0
        if not tweet['in_reply_to_screen_name'] is None:
            writer.writerow(
                [poster, tweet['in_reply_to_screen_name'], 'reply', tweet_date, tweet_id,
                 tweet_text, tweet_followers, hashes, retweet])
            reply_status = 1
            flag = lock.acquire(True)
            if flag:
                my_dict['count_replies'] = my_dict['count_replies'] + 1
                lock.release()

            if recipient != tweet['in_reply_to_screen_name']:
                writer.writerow([poster, recipient, 'mentions', tweet_date, tweet_id, tweet_text,
                                 tweet_followers, hashes, retweet])
                reply_status = 1
                flag = lock.acquire(True)
                if flag:
                    my_dict['count_mentions'] = my_dict['count_mentions'] + 1
                    lock.release()

            if reply_status == 0:
                writer.writerow(
                    [poster, poster, 'tweet', tweet_date, tweet_id, tweet_text, tweet_followers, hashes,
                     retweet])
                flag = lock.acquire(True)
                if flag:
                    my_dict['count_tweets'] = my_dict['count_tweets'] + 1
                    lock.release()



def func(my_dict,dirs, file, keywords,outfile):
    #for file in allfiles:
    if file.endswith('.bz2'):
        file = bz2.BZ2File(os.path.join(dirs, file), 'r')
        for line in file:
            status = 0

            for keyword in keywords:
                if keyword in line.decode().lower():
                    status = 1

            if status == 1:
                tweet = json.loads(line)
                poster = tweet['user']['screen_name']
                tweet_date = tweet['created_at']
                tweet_id = tweet['id']
                tweet_text = tweet['text']
                tweet_followers = tweet['user']['followers_count']

                if 'retweeted_status' in line.lower().decode():
                    retweet = 'True'
                else:
                    retweet = 'False'

                hashes = list()
                for hashtag in tweet['entities']['hashtags']:
                    text = hashtag['text']
                    hashes.append(text)

                mentions = list()
                for mention in tweet['entities']['user_mentions']:
                    recipient = mention['screen_name']
        result = {"tweet":tweet,"poster":poster,"tweet_date":tweet_date,"tweet_id":tweet_id,"tweet_text":tweet_text,"tweet_followers":tweet_followers,"hashes":hashes,"retweet":retweet,"recipient":recipient}
    return result


if __name__ == '__main__':
    start = time.time()
    manager = Manager()
    my_dict = manager.dict({'count_mentions': 0, 'count_replies': 0,'count_tweets':0})
    lock = manager.Lock()
    process_json(keywords, directory, outfile,my_dict)
    end = time.time()
    print(end - start)
    print('-' * 10)
    print('complete!')




