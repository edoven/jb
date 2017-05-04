import requests
from bs4 import BeautifulSoup
import numpy as np
import time
import requests
from listing import Listing
from db_interface import Db_Interface


#BASE_URL = 'https://www.indeed.co.uk/jobs?q=Data+Scientist&l=London&fromage=last&start={}'



class IndeedScraper:


    def __init__(self,db_interface,base_url,base_link_url):
        self.db_interface = db_interface
        self.base_url = base_url
        self.base_link_url = base_link_url


    def get_salary(self,div):
        try:
            return div.find('nobr').text
        except:
            return -1

    def get_link(self,div):
        path = div.find('a',{'class':'turnstileLink'})['href']
        indeed_link = '{}{}'.format(self.base_link_url,path)
        try:
            r = requests.get(indeed_link, allow_redirects=True,timeout=3)
            return r.url
        except:
            return indeed_link

    def get_company(self,div):
        try:
            return div.find('span',{'class':'company'}).find('span').text.strip()
        except AttributeError:
            return None
        except:
            #TODO: log
            return None

    def get_title(self,div):
        section = div.find('a',{'data-tn-element':'jobTitle'} )
        return(section.text)

    def get_jobs_from_page(self,url,store=False,filename='CHANGEME.html'):
        soup = BeautifulSoup(requests.get(url).text, "lxml")
        if store:
            with open(filename, "w") as file:
                file.write(str(soup))
        i = 1
        for el in soup.findAll('div', {'class': '  row  result'}):
            l = Listing(url=self.get_link(el),
                        company=self.get_company(el),
                        title=self.get_title(el),
                        salary=self.get_salary(el))
            self.db_interface.persist_listing(l)
            print(l.to_string())
            i = i + 1
            time.sleep(max([0,np.random.poisson() + np.random.normal(loc=1,scale=0.5)]))
        #last item
        #last_listing = soup.find('div', {'class': 'lastRow  row  result"'})
        #print('{}) {} ({}) - {} - {}'.format(i,
        #                                     get_title(last_listing),
        #                                     get_company(last_listing),
        #                                     get_link(last_listing),
        #                                     get_salary(last_listing)))

    def run(self):
        page_starts = np.arange(0, 101, 10)
        for page_start in page_starts:
            url = BASE_URL.format(page_start)
            print(url)
            scraper.get_jobs_from_page(url, store=True, filename='{}.html'.format(page_start))
            waiting_time = np.random.normal(loc=3, scale=1)
            print('### WAITING {} sec'.format(waiting_time))
            time.sleep(waiting_time)

if __name__ == "__main__":
    BASE_URL = 'https://www.indeed.co.uk/jobs?q=data+engineer&l=London%2C+Greater+London&radius=100&jt=contract&fromage=last&start={}'
    BASE_LINK_URL = 'https://www.indeed.co.uk'

    db_interface = Db_Interface()
    #db_interface.init_tables()

    scraper = IndeedScraper(db_interface,BASE_URL,BASE_LINK_URL)
    scraper.run()


