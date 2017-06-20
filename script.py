import csv
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

def getCompanyURL(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        return None
    bsObj = BeautifulSoup(html.read())

    try:
        for am in bsObj.findAll("span",{"class":"url"}):
            continue
        for m in am.findAll("a"):
            if 'href' in m.attrs:
                companyURL = m.attrs['href']
    except NameError as e:

        try:
            for link in bsObj.findAll("td",{"class":"url"}):
                continue
            for m in link.findAll("a"):
                if 'href' in m.attrs:
                    companyURL = m.attrs['href']
        except NameError as e:
            return None

    return companyURL

input_file = open("wikipedia_links.csv", "r")
rdr = csv.reader(input_file)

wiki_link = []
for link in rdr:
    wiki_link +=link

company_link = {}
for link in wiki_link:
    company_link[link] = getCompanyURL(link)

input_file.close()
keys = company_link.keys()

with open('answer.csv', 'w') as f:
    wr = csv.writer(f)
    wr.writerows([("wikipedia_page","website")])
    wr.writerows([(i,company_link[i]) for i in keys])
