import os
import argparse
from time import sleep
from string import ascii_letters

import requests
from bs4 import BeautifulSoup



DATA_DIR = "data/"
URL = "https://www.lyrics.com/random.php"


parser = argparse.ArgumentParser()
parser.add_argument('-n', type=int, default=100)
args = parser.parse_args()


def clean_word(word):
    return ''.join(l for l in word if l in ascii_letters + "'-")


def main(url):
    title_out = None
    artist_out = None
    r = requests.get(url)
    html = BeautifulSoup(r.text, 'lxml')
    try:
        title = html.find('h2', attrs={'id': 'lyric-title-text'}).text
        artist = html.find('h3', attrs={'class': 'lyric-artist'}).find('a').text
        lyrics = html.find('pre', attrs={'id': 'lyric-body-text'}).text.split("\n")

        title_out = '_'.join(clean_word(word) for word in title.lower().split())
        artist_out = '_'.join(clean_word(word) for word in artist.lower().split())
        # lyrics_out = [clean_word(word) for word in lyrics]

        if not os.path.exists(os.path.join(DATA_DIR, artist_out)):
            os.mkdir(os.path.join(DATA_DIR, artist_out))

        with open(os.path.join(DATA_DIR, artist_out, title_out), 'w') as f:
            for word in lyrics:
                f.write(word + "\n")

    except:
        pass

    sleep(0.5)

    return title_out, artist_out


if __name__ == "__main__":
    for i in range(args.n):
        artist, title = main(URL)
        print(f"{i+1}.", artist, title)
