import requests,json

from requests.api import delete, post
from users import models
import http.client, urllib.parse
from django.conf import settings
import time


class NewsApi:

    def __init__(self,url,url2,number_of_post):
        self.url = url
        self.url2 = url2#this is just a back up url
        self.number_of_post = number_of_post

    def convert_from_json(self,str_data):
        "this convert json to python data type"
        return json.loads(str_data)

    def get_api_data(self):
        'this get all the data or response from the internet'
        posts = []
        try:

            conn = http.client.HTTPConnection('api.mediastack.com')

            params = urllib.parse.urlencode({
                'access_key': api_key,
                'categories': '-general,-sports',
                'sort': 'published_desc',
                'limit': self.number_of_post,
                })
            conn.request('GET', '/v1/news?{}'.format(params))
            res = conn.getresponse()
            data = res.read()
            respData = self.convert_from_json(data.decode('utf-8'))
            posts.append(respData)
            totalPostNum = respData.get('pagination').get('count')
            print(totalPostNum,'Post Number')
            if totalPostNum >= self.number_of_post:
                "so we saying if the total number is not up to the number of post just request again"
                print(len(posts),'len of posts')
                return posts
            else:
                # this means we did not get enough post the we have to re fecth
                self.url = self.url2
                time.sleep(30)
                self.get_api_data()
        except :
            "We wait for 30s Before We start Try again"
            time.sleep(30)
            print("trying again Because of Network Error")
            self.get_api_data()
            
    def format_api_data(self,raw_data):
        '''
            this format the data for inserting to db also
            reduce how may post we gonna see using the "self.number_of_post"
        '''
        main_post = []
        """
          the if below checks if we have two different resouce that means we used to diffrent urls which is
          url and url2
        """
        

        if len(raw_data) == 2:
            main_post.extend(raw_data[0]['data'])
            main_post.extend(raw_data[1]['data'])
        else:
            # print(raw_data)
            main_post.extend(raw_data[0]['data'])

        # just return the amount of post specified
        return main_post[0:self.number_of_post]

    def save_to_db(self,clean_data):
        'save arranged data to db'
        print(len(clean_data),"Going into database")
        print(clean_data,"Going into database")
        count = 0
        for news in clean_data:
           print(news)
           print('-----')
           print('-----')
           
           moneypost = models.MoneyPost.objects.create(title=f"{news.get('title','title could not load')}",
           content=f"{news.get('description','Failed To Load Content')}"+str(count),
           image_link=news.get('image',"none"))
           moneypost.save() 
           count+=1
    
    def run(self):
        """ 
            Steps
            get the data from the internet - using  self.get_api_data()
            arrange  the data for the database -- using self.format_api_data()
            then we save that data = using self.save_to_db()
        """
        self.delete_previous_posts()
        # we store what we get form th api in the unFormated_data variable
        unFormated_data =  self.get_api_data()
        if unFormated_data is None:
            "if it none wait for 30 seconds and try again"
            time.sleep(30)
            unFormated_data =  self.get_api_data()
        # format_api_data will clean the data for us
        cleaned_data = self.format_api_data(unFormated_data)
        print('leght finall data',len(cleaned_data))
        print(cleaned_data)
        self.save_to_db(cleaned_data)

    def delete_previous_posts(self):
        for formal_post in models.MoneyPost.objects.all():
            formal_post.delete()

api_key =settings.MEDIASTACK_APIKEY
url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}'
url2 = f'https://newsapi.org/v2/top-headlines?country=br&apiKey={api_key}'


NEWS = NewsApi(url,url,10)
# NEWS.run()


