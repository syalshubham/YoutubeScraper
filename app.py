from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin
import requests
import logging
import csv
logging.basicConfig(filename="scraper.log", level = logging.INFO)
from selenium import webdriver

driver = webdriver.Chrome()
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen

app = Flask(__name__)
@app.route("/", methods=['GET'])
def homepage():
    return render_template("index.html")

@app.route("/channel", methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        try:
            searchstring = request.form['content']
            youtube_url = "https://www.youtube.com/@" + searchstring + "/videos"
            print(youtube_url)
            driver.get(youtube_url)
            content = driver.page_source.encode('utf-8').strip()
            soup = bs(content, 'html.parser')
            titles = soup.find_all('a', id='video-title-link')
            views = soup.find_all('span', class_ = 'inline-metadata-item style-scope ytd-video-meta-block')
            video_urls = soup.find_all('a', id = 'video-title-link')
            i = 0 
            j = 0
            li = []
            for title in titles[:5]:
                raw_dic = {}
                raw_dic['Title']= (title.text)
                raw_dic['Views'] = (views[i].text)
                raw_dic['Time of Posting'] = (views[i+1].text)
                raw_dic['Youtube URL'] = "https://www.youtube.com{}".format(video_urls[j].get('href'))
                print('\n{}\n{}\n{}\nhttps://www.youtube.com{}'.format(title.text, views[i].text, views[i+1].text, video_urls[j].get('href')))
                i+=2
                j+=1
                li.append(raw_dic)
            fields = ['Title', 'Views', 'Time of Posting', 'Youtube URL']
            print(li)
            filename = searchstring + "_scraped.csv"
            with open(filename,'w', encoding="utf-8") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fields)
                writer.writeheader()
                searchstring = request.form['content']
                youtube_url = "https://www.youtube.com/@" + searchstring + "/videos"
                print(youtube_url)
                driver.get(youtube_url)
                content = driver.page_source.encode('utf-8').strip()
                soup = bs(content, 'html.parser')
                titles = soup.find_all('a', id='video-title-link')
                views = soup.find_all('span', class_ = 'inline-metadata-item style-scope ytd-video-meta-block')
                video_urls = soup.find_all('a', id = 'video-title-link')
                i = 0 
                j = 0
                li = []
                for title in titles[:5]:
                    raw_dic = {}
                    raw_dic['Title']= (title.text)
                    raw_dic['Views'] = (views[i].text)
                    raw_dic['Time of Posting'] = (views[i+1].text)
                    raw_dic['Youtube URL'] = "https://www.youtube.com{}".format(video_urls[j].get('href'))
                    print('\n{}\n{}\n{}\nhttps://www.youtube.com{}'.format(title.text, views[i].text, views[i+1].text, video_urls[j].get('href')))
                    i+=2
                    j+=1
                    li.append(raw_dic)
                fields = ['Title', 'Views', 'Time of Posting', 'Youtube URL']
                print(li)
                filename = searchstring + "_scraped.csv"
                with open(filename,'w', encoding="utf-8") as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=fields)
                    writer.writeheader()
                    writer.writerows(li)
                    
                return render_template('result.html', list_scrape = li[0:(len(li))])
        except Exception as e:
            logging.info(e)
            return "Something Wrong"
    else:
        return render_template("index.html")
        
        
if __name__ == "__main__":
    app.run(host = "0.0.0.0")
    