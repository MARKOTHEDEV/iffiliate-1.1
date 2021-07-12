# this module create news and delete it 

from bs4 import BeautifulSoup
from urllib.request import urlopen,Request
from urllib.error import HTTPError,URLError
from users import models

# vanguard and daily times




class Website:
    'this models the website what we wanna scrape'

    # when we say class we mean css class
    def __init__(self,websitelink,cssTogetPostLinks,TitleClass,ContentClass):
        self.websitelink = websitelink
        self.cssTogetPostLinks = cssTogetPostLinks
        self.TitleClass = TitleClass
        self.ContentClass = ContentClass


class Content:
    'this class stores all the data we scrape from the news website'
    def __init__(self,postTitle,postContent):
        self.postTitle =postTitle
        self.postContent =postContent

    def upload_to_db(self):
        'as the name suggest it upload to '
        moneypost,created =models.MoneyPost.objects.get_or_create(title=self.postTitle,content=self.postContent)
        moneypost.save()



    def __str__(self):
        return self.postTitle



class Scrapper:
    'this takes care of all the scrapping jargons'
    
    def __init__(self,website):
        self.website =website

    def get_page_obj(self,url):
        try:
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            html = urlopen(req)
            bs = BeautifulSoup(html,'html.parser')
            # if it worked return a beatiful soup cobject
            return bs
        except HTTPError:
            return False

        except URLError:
            return False



    def get_title(self,pageObj):
        'gets the title of the post'

        return pageObj.select_one(self.website.TitleClass).text

    def get_content(self,pageObj):
        'gets the post content'

        # print(self.website.ContentClass)
        listOfPtag = pageObj.select(self.website.ContentClass)
        # listOfPtag.pop(0)
        content = ''
        for pTag in listOfPtag:
            content = content + '\n'+pTag.text

        
        return content



    def get_data(self):
        'this function runs the show of the class it like the play button'
        bs = self.get_page_obj(self.website.websitelink)
        if bs != False:
            ListOfPostLinks = bs.select(self.website.cssTogetPostLinks)
            print(len(ListOfPostLinks))
            for link in ListOfPostLinks:
                # for each link we open the page obj and ge the title and post
                newPage = self.get_page_obj('https://en.wikinews.org/'+link['href'])
                if newPage != False:
                    # after we have collected th title and content it time to save to db

                    title = self.get_title(newPage)
                    postcontent = self.get_content(newPage)
                    content = Content(title,postcontent)
                    # this upload what we scraped to the db
                    content.upload_to_db()

                    # print(title)


def clear_db():
    'delete all data before we add new one'
    for data in models.MoneyPost.objects.all():
        data.delete()


def runScraper():

    clear_db()
    websites = [
#     ['https://www.vanguardngr.com/category/national-news/','span.rtp-latest-news-title a','.entry-header .entry-title','.entry-content p'],
     ['https://en.wikinews.org/wiki/Main_Page/','div.latest_news_text li a','h1.firstHeading','div.mw-parser-output p']
    ]


    for website in websites:
        scrapper = Scrapper(Website(website[0],website[1],website[2],website[3],))
        scrapper.get_data()



