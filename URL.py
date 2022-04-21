import validators 
from Exceptions import InvaildURL

class URL():
    def __init__(self,url):
        self.link = self.validate_url(url)
    
    def validate_url(self,url):
        valid=validators.url(url)
        if valid:
            return url
        else:
            raise InvaildURL(url)