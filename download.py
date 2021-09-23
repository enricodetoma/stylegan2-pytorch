import urllib
import urllib.request
import re
from bs4 import BeautifulSoup
import time
import os

file_path = "modern_paintings"
os.makedirs(file_path, exist_ok=True)

def url_open(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    retrycount = 0
    s = None
    while s is None:
        try:
            s = urllib.request.urlopen(req,timeout=50).read()
        except Exception as e:
            print(str(e))
            retrycount+=1
            if retrycount > 10:
                raise
            time.sleep(10)

    return BeautifulSoup(s, "lxml")

def urlretrieve(image_url, save_path):
    retrycount = 0
    s = None
    while s is None:
        try:
            s = urllib.request.urlretrieve(image_url, save_path)
        except Exception as e:
            print(str(e))
            retrycount+=1
            if retrycount > 10:
                raise
            time.sleep(10)

def get_images(url):
  print(url)
  genre_soup = url_open(url)
  artist_list_main = genre_soup.find("main")
  lis = artist_list_main.find_all("li")

  # for each list element
  for li in lis: 
    born = 0
    died = 0

    # get the date range
    for line in li.text.splitlines():
      if line.startswith(",") and "-" in line:
        parts = line.split('-')
        if len(parts) == 2:
          born = int(re.sub("[^0-9]", "",parts[0]))
          died = int(re.sub("[^0-9]", "",parts[1]))

    # look for artists who may have created work that could in public domain
    if born>1800 and died>0 and died<1978:
      link = li.find("a")
      artist = link.attrs["href"]

      # get the artist's main page
      artist_url = base_url + artist
      artist_soup = url_open(artist_url)

      # only look for artists with the word modern on their main page
      if "modern" in artist_soup.text.lower():
        print(artist + " " + str(born) + " - " + str(died))

        # get the artist's web page for the artwork
        url = base_url + artist + '/all-works/text-list'
        artist_work_soup = url_open(url)

        # get the main section
        artist_main = artist_work_soup.find("main")
        image_count = 0
        artist_name = artist.split("/")[2]
        os.makedirs(file_path + "/" + artist_name, exist_ok=True)

        # get the list of artwork
        lis = artist_main.find_all("li")

        # for each list element
        for li in lis:
          link = li.find("a")

          if link != None:
            painting = link.attrs["href"]

            # get the painting
            url = base_url + painting
            print(url)

            try:
              painting_soup = url_open(url)

            except:
              print("error retreiving page")
              continue

            # check the copyright
            if "Public domain" in painting_soup.text:

              # get the url
              og_image = painting_soup.find("meta", {"property":"og:image"})
              image_url = og_image["content"].split("!")[0] # ignore the !Large.jpg at the end
              print(image_url)

              parts = url.split("/")
              painting_name = parts[-1]
              save_path = file_path + "/" + artist_name + "/" + painting_name + ".jpg"

              #download the file
              try:
                print("downloading to " + save_path)
                time.sleep(0.2)  # try not to get a 403                    
                urlretrieve(image_url, save_path)
                image_count = image_count + 1
              except Exception as e:
                print("failed downloading " + image_url, e)

base_url = "https://www.wikiart.org"
urls = []
for c in range(ord('a'), ord('z') + 1):
  char = chr(c)
  artist_list_url = base_url + "/en/Alphabet/" + char + "/text-list"
  urls.append(artist_list_url)

print(urls)

from concurrent.futures import ThreadPoolExecutor
executor = None
with ThreadPoolExecutor(max_workers = 16) as executor:
  ex = executor
  executor.map(get_images, urls)
 