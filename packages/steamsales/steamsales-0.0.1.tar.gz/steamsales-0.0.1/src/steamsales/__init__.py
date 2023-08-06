# Import
import requests
import lxml

# From 
from bs4 import BeautifulSoup

# Variable
URL = "https://prepareyourwallet.com/"
Headers = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0"
	} 

r = requests.get(URL, headers=Headers)
soup = BeautifulSoup(r.content, "lxml")

sale_name = soup.find("h2", attrs={'class': 'h5 mb-3 text-white'}).text
start_date = soup.find("span", attrs={'itemprop': 'startDate'}).text
end_date = soup.find("span", attrs={'itemprop': 'endDate'}).text
countdown = soup.find('span', attrs={'id': 'countdown'}).text
status = soup.find('span', attrs={'class': "status mb-0 mt-2 float-lg-right"}).text

# Class
class Steam(object):

    """
    API Wrapper for https://prepareyourwallet.com/ 

    :param api_domain: domain for api.
    """

    def __init__(self, api_domain='https://prepareyourwallet.com/'):
        self.api_domain = api_domain

    def sale_name():
        """
        Return Steam sale name from https://prepareyourwallet.com/
        """

        sale_name = sale_name
        return sale_name
    
    def start_date():
        """
        Return Steam sale start date from https://prepareyourwallet.com/
        """

        start_date = start_date
        return start_date

    def end_date():
        """
        Return Steam sale end date from https://prepareyourwallet.com/
        """

        end_date = end_date
        return end_date 

    def countdown():
        """
        Return Steam sale countdown from https://prepareyourwallet.com/
        """

        countdown = countdown
        return countdown

    def status():
        """
        Return Steam sale status from https://prepareyourwallet.com/
        """

        status = status
        return status

