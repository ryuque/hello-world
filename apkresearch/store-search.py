# -*- coding: utf-8 -*-
from email.encoders import encode_7or8bit
import sys
import csv
import time
from google_play_scraper import Sort, reviews_all, app, search
from operator import itemgetter

def search_apps(keyword):
    result = search(
        keyword,
        lang='ja', # 日本語を指定
        country='jp', # 日本を指定
    )
    
    return [{'App Name': app['title'], 'App ID': app['appId'], 'Genre': app['genre'], 'Installs': app['installs']} for app in result]

def write_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8_sig') as f:
        writer = csv.DictWriter(f, fieldnames=['App Name', 'App ID', 'Genre', 'Installs'])
        writer.writeheader()
        for row in data:
            writer.writerow(row)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8_sig') as f:
            reader = csv.reader(f)
            keywords = [row[0] for row in reader]
        
        all_results = []
        for keyword in keywords:
            print(f"Searching for keyword: {keyword}")
            results = search_apps(keyword)
            all_results.extend(results)
            time.sleep(2)  # add delay to avoid being blocked
        
        # all_resultsを'App Name'でソート
        all_results.sort(key=itemgetter('App Name'))

        # 'App Name'で重複を削除
        all_results = list(dict((i['App Name'], i) for i in all_results).values())

        write_to_csv(all_results, 'output.csv')
    else:
        print("Please provide a keyword CSV file as an argument.")