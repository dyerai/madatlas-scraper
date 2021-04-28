from bs4 import BeautifulSoup as Soup, Tag
import requests


response = requests.get("https://guide.wisc.edu/courses/#text")
soup = Soup(response.content, "html.parser")

index = soup.find("div", {"id": "atozindex"})
f = open("../data/subjectpaths.csv", "w")

for item in index.find_all('li'):
    if isinstance(item, Tag):
        link = item.find('a')
        f.write(link['href'] + ",")

f.close()
