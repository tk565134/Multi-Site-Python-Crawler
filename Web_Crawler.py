from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re
import os,json
import logging
# function to write data to the output json file
def writeToJSONFile(entry):
    with open('output.json', 'a',encoding='utf-8') as f:
        json.dump(entry, f)
        f.write(os.linesep)
#function to scrawl on the page to get all the needed information
def pageScrawl(url,u_lst):
    logger.info('Connecting URL {}'.format(url))
    try:
        page=urlopen(url)
        logger.info('Connection Successful {}'.format(url))
    except:
        logger.info('Connection Failed {}'.format(url))
        return
    bsObj= BeautifulSoup(page, 'html.parser')
    #collecting all the links found on the current url page
    all_links= bsObj.findAll('a', attrs={'href': re.compile("^http://")})
    #collecting all p tag values on the current url page
    pvalues=bsObj.findAll('p')
    s=""
    for values in pvalues:
        try:
            s=s+values.get_text()+" "
        except:
            print("non printable characters")
    entry={}
    entry['page']=url
    entry['content']=s
    writeToJSONFile(entry)
    for link in all_links:
        n_url=link.get('href')
        if n_url in u_lst or start_url not in n_url:
            continue
        u_lst.append(n_url)
        #recursively scrawling on the urls collected
        pageScrawl(n_url,u_lst)
    return

s_url=input("Enter the url :")
u_lst=[s_url]
logging.basicConfig(level=logging.DEBUG,filename='log.txt',format="%(asctime)s:%(levelname)s:%(message)s")
logger = logging.getLogger('scraper')
start_url=s_url
start_url=start_url.replace("www.", "")
start_url=start_url.replace("http://", "")
start_url=start_url.replace("https://", "")
start_url=start_url.replace(".com/", ".com")
pageScrawl(s_url,u_lst)
