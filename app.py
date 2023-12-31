from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

base_url = "https://pagalworldi.com"
main_url = "https://pagalworldi.com/list/bollywood-movies-mp3-songs-2022s/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}


def getSongDescription(url):
    req_url = requests.get(url, headers=headers)
    soup = BeautifulSoup(req_url.content, "html.parser")
    song_download_source = soup.find("source")
    if song_download_source != None:
        song_download_url = base_url + song_download_source.get("src")
        return song_download_url
    return None

def get_songs(url):
    count = 1
    song_list = []
    req_url = requests.get(url, headers=headers)
    soup = BeautifulSoup(req_url.content, "html.parser")
    main_div = soup.find("ul", "list")
    all_songs = main_div.find_all("li")

    for song in all_songs:
        song_detail = {
            "song_title": "",
            "song_desc": "",
            "song_img_url": "",
            "song_download_url": "",
        }

        song_title_el = song.find("h3")
        if song_title_el != None:
            song_detail["song_title"] = song_title_el.get_text()

        song_desc_el = song.find("p")
        if song_desc_el != None:
            song_detail["song_desc"] = song_desc_el.get_text()

        song_img_el = song.find("img")
        if song_img_el != None:
            song_detail["song_img_url"] = song_img_el.get("src")

        song_url = song.find("a")
        if song_url != None:
            req_song_url = song_url.get("href")
            song_base_url = base_url + req_song_url
            song_download_url = getSongDescription(song_base_url)
            song_detail["song_download_url"] = song_download_url

        song_list.append(song_detail)

        count += 1

    return song_list


app = Flask(__name__)


@app.route("/")
def index():
    hit_url = main_url + "1" + ".html"
    scraped_data = get_songs(hit_url)
    if scraped_data:
        return scraped_data
    else:
        return "Failed to scrape data."


if __name__ == "__main__":
    app.run(debug=True)
