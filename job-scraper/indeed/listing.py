import hashlib

class Listing:

    def __init__(self,url,company,title,salary):#,description):
        self.url = url
        self.company = company
        self.title = title
        self.salary = salary
        self.id = hashlib.md5(url.encode()).hexdigest()
        #self.description = description

    def to_string(self):
        return '{id},{title},{company},{url},{salary}'.format(id=self.id,
                                       title=self.title,
                                       company=self.company,
                                       url=self.url,
                                       salary=self.salary)