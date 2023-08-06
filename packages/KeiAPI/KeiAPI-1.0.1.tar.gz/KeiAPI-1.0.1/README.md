# Kei

**Kei** is an unofficial, Pure Python API for [gogoanime2.org](https://gogoanime2.org).\
It uses BeautifulSoup4 for scraping data from the website.

----
### Installation
Kei is pip installable.
[PyPi](https://pypi.org/project/KeiAPI/)

```
pip install KeiAPI
```

-----
### Usage
##### 1) Simply import by
```
import Kei
```

##### 2) Get search results for given query
```
Kei.search("fumetsu")
```
will return
```
  {
    "series1": {
        "series_title": "Fumetsu no Anata e",
        "series_url": "https://gogoanime2.org/anime/fumetsu-no-anata-e",
        "cover_url": "https://gogoanime2.org/images/225_318/fumetsu-no-anata-e.jpg",
        "episode_count": "15"
    },
    "series2": {
        "series_title": "Fumetsu no Anata e (Dub)",
        "series_url": "https://gogoanime2.org/anime/fumetsu-no-anata-e-dub",
        "cover_url": "https://gogoanime2.org/images/225_318/fumetsu-no-anata-e-dub.jpg",
        "episode_count": "9"
    }
}
```

##### 3) Get newly updated episodes
```
Kei.get_new_updated(1)
```
will return the info of newly updated episode on 1st page in the format-
```
{
    "series1": {
        "series_title": "Beyblade Burst Dynamite Battle",
        "episode_url": "https://gogoanime2.org/watch/beyblade-burst-dynamite-battle/18",
        "episode_number": "18"
    },
    "series2": {
        "series_title": "Holo no Graffiti",
        "episode_url": "https://gogoanime2.org/watch/holo-no-graffiti/110",
        "episode_number": "110"
    }
}
```

##### 4) Get list of ongoing series
```
Kei.get_ongoing()
```
will return info in the format-
```
{
    "series1": {
        "series_title": "Yu\u2606Gi\u2606Oh!: Sevens",
        "series_url": "https://gogoanime2.org/anime/yugioh-sevens"
    },
    "series2": {
        "series_title": "Yuuki Yuuna wa Yuusha de Aru Churutto!",
        "series_url": "https://gogoanime2.org/anime/yuuki-yuuna-wa-yuusha-de-aru-churutto"
    }
}
```
##### 5)Get list of recently added series
```
Kei.get_recently_added()
```
will return in the format-
```
{
    "series1": {
        "series_title": "Yu\u2606Gi\u2606Oh!: Sevens",
        "series_url": "https://gogoanime2.org/anime/yugioh-sevens"
    },
    "series2": {
        "series_title": "Yuuki Yuuna wa Yuusha de Aru Churutto!",
        "series_url": "https://gogoanime2.org/anime/yuuki-yuuna-wa-yuusha-de-aru-churutto"
    }
}
```

##### 6)Get download link for given episode_url
```
Kei.get_video("https://gogoanime2.org/watch/fumetsu-no-anata-e/15")
```
will return a link to .mp4 file for downloading.

##### 7) Get working link for gogoanime
```
Kei.get_valid_link()
```
will return link of the first Bing result for the query "gogoanime"


----
### Features
- Get download link for video by passing episode_url
- Get working link for gogoanime (scraps Bing results)
- Get search results data in JSON format for:
  - Series title
  - Episode count of Series
  - Series URL
  - Cover Image URL
- Get info(series_title, episode_url) about all newly updated series(pagewise) in JSON
- Get info(series_title, series_url) about all ongoing series in JSON

----
### Contributing

- Fork it!
- Create your feature branch: `git checkout -b my-new-feature`
- Commit your changes: `git commit -m 'Add some feature'`
- Push to the branch: `git push origin my-new-feature`
- Submit a pull request

----
##### Licensed under MIT License.
