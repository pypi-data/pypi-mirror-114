# Kei is an unofficial, Pure Python API for gogoanime2.org
# Uses BeautifulSoup to scrap webpages
#
# Can fetch:
# - search results(series_url, series_title, episode_count, cover_url) in JSON
# - info about newly updated series in JSON
# - info about newly added series in JSON
# - info about ongoing series in JSON
# - video file url (only if the any server has direct links to .mp4)
# - working url for gogoanime (scraps bing results because Google blocks such attempts :( )
#
# Author: onkardahale
# email: dahaleonkar@gmail.com


from bs4 import BeautifulSoup
import requests
import json

headers_list = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"}
BINGURL = "https://bing.com"
URL = "https://gogoanime2.org"

#Returns soup for a url
def req_soup(url):

    try:
        return BeautifulSoup(requests.get(url, headers=headers_list).text, "html.parser")
    except requests.exceptions.ConnectionError:
        return {"status":"404", "reason":"Connection error occurred"}
    except requests.exceptions.ConnectTimeout:
        return {"status":"408", "reason":"Connection Timeout"}
    except:
        return {"status":"418", "reason":"I'm a teapot"}


#Returns search results in JSON
def search(query):

    search_data = {}
    try:
        soup_results = req_soup(URL + "/search/" + query).find("ul", {"class" : "items"}).find_all("div", {"class" : "img"})
    except:
        return {"status":"400", "reason":"No result for given query"}

    item_count = 1
    for tag in soup_results:

        series = {}

        a_tag = tag.find("a")
        series["series_title"] = a_tag["title"]
        series["series_url"] = URL + a_tag["href"]
        series["cover_url"] = URL + tag.find("img")["src"]

        try:
            soup_episode = req_soup(URL + a_tag["href"]).find("ul", {"id" : "episode_related"}).find_all("li")
        except:
            return {"status":"400", "reason":"No result for given query"}

        series["episode_count"] = str(len(soup_episode))

        search_data["series" + str(item_count)] = series
        item_count += 1

    return json.dumps(search_data, indent=4)


#Returns info of newly updated episodes in JSON
def get_new_updated(page_number):

    new_updated ={}

    try:
        soup_new_updated = req_soup(URL + "/ajax/page-recent-release.html?page=" + str(page_number)).find("ul", {"class" : "items"}).find_all("li")

        series_count = 1
        for li in soup_new_updated:

            series = {}

            a_name_class = li.find("p", {"class" : "name"}).find("a")
            a_episode_class = li.find("p", {"class" : "episode"})

            series["series_title"] = a_name_class["title"]
            series["episode_url"] = URL + a_name_class["href"]
            series["episode_number"] = str(a_episode_class.get_text()[9:])

            new_updated["series" + str(series_count)] = series
            series_count += 1

    except:
        return {"status":"400", "reason":"Bad Request"}


    return json.dumps(new_updated, indent=4)



#Return info of ongoing series in JSON
def get_ongoing():

    ongoing = {}

    try:
        soup_ongoing = req_soup(URL).find("nav", {"class" : "menu_series cron"}).find_all("li")

        series_count = 1
        for li in soup_ongoing:

            series = {}

            a_tag = li.find("a")
            series["series_title"] = a_tag["title"]
            series["series_url"] = URL + a_tag["href"]

            ongoing["series" + str(series_count)] = series
            series_count += 1
    except:
        return {"status":"400", "reason":"Bad Request"}


    return json.dumps(ongoing, indent=4)



#Returns info of newly added series in JSON
def get_recently_added():

    recently_added = {}

    try:
        soup_recently_added = req_soup(URL).find("ul", {"class" : "listing"}).find_all("li")

        series_count = 1
        for li in soup_recently_added:

            series = {}

            a_tag = li.find("a")
            series["series_title"] = a_tag["title"]
            series["series_url"] = URL + a_tag["href"]

            recently_added["series" + str(series_count)] = series
            series_count += 1
    except:
        return {"status":"400", "reason":"Bad Request"}


    return json.dumps(recently_added, indent=4)


#Returns direct url for video file of given episode_url
def get_video(episode_url):

    soup_episode = req_soup(episode_url)
    try:
        iframe_src = soup_episode.find("iframe",{"id" : "playerframe"}).get("src")[2:]
    except:
        return {"status":"400", "reason":"Bad Request"}

    soup_player = req_soup("https://" + iframe_src)
    try:
        server_list = soup_player.find("ul", {"class" : "list-server-items"}).find_all("li", {"data-status" : "1"})

        for lnk in server_list:
            if lnk["data-video"].endswith(".mp4"):
                open_video_link = lnk["data-video"]
                break
    except:
        return {"status":"404", "reason":"Cannot find direct link to .mp4"}

    return open_video_link

#Scraps Bing results for "gogoanime" and gets link of first result
def get_valid_link():

    try:
        valid_link = req_soup(BINGURL + "/search"+ "?q=gogoanime").find("h2", {"class" : "b_topTitle"}).a["href"]
    except:
        return {"status":"400", "reason":"Bad Request"}

    return valid_link
