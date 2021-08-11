import requests,json

from requests.api import post
from users import models






class NewsApi:

    def __init__(self,url,url2,number_of_post):
        self.url = url
        self.url2 = url2#this is just a back up url
        self.number_of_post = number_of_post



    def get_api_data(self):
        'this get all the data or response from the internet'
        posts = []
        try:

            resp = requests.get(url=url)
            respData = resp.json()
            posts.append(respData)
            print(respData.get('totalResults'),'Post Number')
            if respData.get('totalResults') >= self.number_of_post:
                "so we saying if the total number is not up to the number of post just request again"
                print(len(posts),'len of posts')
                return posts
            else:
                # this means we did not get enough post the we have to re fecth
                self.url = self.url2
                self.get_api_data()
        except requests.exceptions.ConnectionError:
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
            main_post.extend(raw_data[0]['articles'])
            main_post.extend(raw_data[1]['articles'])
        else:
            # print(raw_data)
            main_post.extend(raw_data[0]['articles'])

        
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
           moneypost = models.MoneyPost.objects.create(title=news.get('title'),content=news.get('content')+str(count))
           moneypost.save() 
           count+=1
    
    def run(self):
        """ 
            Steps
            get the data from the internet - using  self.get_api_data()
            arrange  the data for the database -- using self.format_api_data()
            then we save that data = using self.save_to_db()
        """
        unFormated_data =  self.get_api_data()
        cleaned_data = self.format_api_data(unFormated_data)
        print('leght finall data',len(cleaned_data))
        self.save_to_db(cleaned_data)



api_key ='24b5744b7c444e4aabc4d26213ee15e7'
url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}'
url2 = f'https://newsapi.org/v2/top-headlines?country=br&apiKey={api_key}'


NEWS = NewsApi(url,url,10)
# NEWS.run()