import requests
import json


class UserProfile:
    USER_API_URL = None
    USER_DATA = None

    def __init__(self, username):
        try:
            self.USER_API_URL = "https://www.instagram.com/{}/?__a=1".format(
                username)
            self.USER_DATA = requests.get(self.USER_API_URL,headers = {'User-agent': 'browser'}).json()
        except:
            return None

    def GetProfilePicURL(self):
        try:
            return(self.USER_DATA['graphql']['user']['profile_pic_url_hd'])
        except:
            return "Cannot Get Data . Please Check if the username is valid"

    def IsPrivate(self):
        try:
            return(bool(self.USER_DATA['graphql']['user']['is_private']))
        except:
            return "Cannot Get Data . Please Check if the username is valid"

    def IsBusinessAccount(self):
        try:
            return(bool(self.USER_DATA['graphql']['user']['is_business_account']))
        except:
            return "Cannot Get Data . Please Check if the username is valid"

    def IsJoinedRecently(self):
        try:
            return(bool(self.USER_DATA['graphql']['user']['is_joined_recently']))
        except:
            return "Cannot Get Data . Please Check if the username is valid"

    def FollowersCount(self):
        try:
            return(self.USER_DATA['graphql']['user']['edge_follow']['count'])
        except:
            return "Cannot Get Data . Please Check if the username is valid"

    def FollowedByCount(self):
        try:
            return(self.USER_DATA['graphql']['user']['edge_followed_by']['count'])
        except:
            return "Cannot Get Data . Please Check if the username is valid"
