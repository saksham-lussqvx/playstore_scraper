from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup


# define the base url
base_url = "https://play.google.com/store/apps/details?id="
# define a session for the browser
page = None
# open the file containing the list of app ids
file_name = "apk_list_full.csv"

with open(file_name, "r") as f:
    app_ids = f.read().split("\n")


def fetch_app_info(app_id:str) -> dict:
    global page
    url = base_url + app_id
    page.goto(url, wait_until="domcontentloaded")
    time.sleep(2)
    app_info = {}
    #<div id="error-section" class="uaxL4e">We're sorry, the requested URL was not found on this server.</div>
    # first check if the app is available, if not then return None
    if page.query_selector("#error-section"):
        return None
    # get the html
    html = page.content()
    # parse the html
    soup = BeautifulSoup(html, "html.parser")
    # get the title
    #<h1 class="Fd93Bb F5UCq p5VxAd" itemprop="name">QuickBooks Online Accounting</h1>
    title = soup.find("h1", {"class": "Fd93Bb F5UCq p5VxAd"}).text
    app_info["title"] = title
    # get the category
    #<a class="WpHeLc VfPpkd-mRLv6 VfPpkd-RLmnJb" href="/store/apps/category/BUSINESS" aria-label="Business" jsname="hSRGPd"></a>
    category = soup.find_all("a", {"class": "WpHeLc VfPpkd-mRLv6 VfPpkd-RLmnJb"})[-1].text
    app_info["category"] = category
    # get the rating
    #<div class="wVqUob"><div class="ClM7O"><div itemprop="starRating"><div class="TT9eCd" aria-label="Rated 4.7 stars out of five stars">4.7<i class="google-material-icons ERwvGb" aria-hidden="true">star</i></div></div></div><div class="g1rdde">33K reviews</div></div>
    rating = soup.find("div", {"itemprop": "starRating"}).text
    app_info["rating"] = rating
    # get the review count
    review_count = soup.find("div", {"class": "g1rdde"}).text.split()[0]
    app_info["review_count"] = review_count
    # get the download count
    #<div class="wVqUob"><div class="ClM7O">1M+</div><div class="g1rdde">Downloads</div></div>
    download_count = soup.find("div", {"class": "ClM7O"}).text
    app_info["download_count"] = download_count
    # get the icon link
    #<div class="l8YSdd"><img src="https://play-lh.googleusercontent.com/VX1WlbpWZDSmPLhsBwJ8H6GYnBQD2MQiAr7FgC3KpLhN8NeVx7t_oD9MxSymGiryDg=s48-rw" srcset="https://play-lh.googleusercontent.com/VX1WlbpWZDSmPLhsBwJ8H6GYnBQD2MQiAr7FgC3KpLhN8NeVx7t_oD9MxSymGiryDg=s96-rw 2x" class="T75of QhHVZd" aria-hidden="true" alt="Icon image" itemprop="image" data-iml="24310473.6"><div class="w7Iutd"><div class="wVqUob"><div class="ClM7O"><div itemprop="starRating"><div class="TT9eCd" aria-label="Rated 3.3 stars out of five stars">3.3<i class="google-material-icons ERwvGb" aria-hidden="true">star</i></div></div></div><div class="g1rdde">13.8K reviews</div></div><div class="wVqUob"><div class="ClM7O">1M+</div><div class="g1rdde">Downloads</div></div><div class="wVqUob"><div class="ClM7O"><img src="https://play-lh.googleusercontent.com/EbEX3AN4FC4pu3lsElAHCiksluOVU8OgkgtWC43-wmm_aHVq2D65FmEM97bPexilUAvlAY5_4ARH8Tb3RxQ=w48-h16-rw" srcset="https://play-lh.googleusercontent.com/EbEX3AN4FC4pu3lsElAHCiksluOVU8OgkgtWC43-wmm_aHVq2D65FmEM97bPexilUAvlAY5_4ARH8Tb3RxQ=w96-h32-rw 2x" class="T75of xGa6dd" alt="Content rating" itemprop="image" data-iml="24310447.800000004"></div><div class="g1rdde"><span itemprop="contentRating"><span>Rated for 3+</span></span><div jsaction="click:CnOdef" class="MKV5ee" role="button" tabindex="0" jscontroller="kJXwXb" aria-label="More info about this content rating"><i class="google-material-icons oUaal" aria-hidden="true">info</i></div></div></div></div></div>
    icon_link = soup.find("img", {"itemprop": "image"}).get("src")
    app_info["icon_link"] = icon_link
    # get the developer email
    #<a class="Si6A0c RrSxVb" target="_blank" href="mailto:support+mobile@datacamp.com" aria-label="Support email mailto:support+mobile@datacamp.com will open in a new window or tab."><i class="google-material-icons j25Vu" aria-hidden="true">email</i><div class="pZ8Djf"><div class="xFVDSb">Support email</div><div class="pSEeg">support+mobile@datacamp.com</div></div></a>
    developer_email = soup.find("a", {"class": "Si6A0c RrSxVb"}).text
    app_info["developer_email"] = developer_email
    # get the short description
    desc_short = soup.find("meta", {"itemprop": "description"}).get("content")
    app_info["desc_short"] = desc_short
    # get the long description
    desc_long = soup.find("div", {"data-g-id": "description"}).text
    app_info["desc_long"] = desc_long
    #convert desc_long to a raw string to preserve the new lines and commas too
    desc_long = repr(desc_long)
    # do this for desc_short too
    desc_short = repr(desc_short)
    # return the app info
    return app_info



if __name__ == "__main__":
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    for app_id in app_ids:
        processed_app_ids = []
        with open("processed_app_ids.txt", "r") as f:
            processed_app_ids = f.read().split("\n")
        if app_id in processed_app_ids:
            continue
        app_info = fetch_app_info(app_id)
        if app_info:
            print(app_info)
            with open("final_data.csv", "a", encoding="utf-8") as f:
                f.write(f"{app_info['title']},{app_info['category']},{app_info['rating']},{app_info['review_count']},{app_info['download_count']},{app_info['icon_link']},{app_info['desc_short']},{app_info['desc_long']},{app_info['developer_email']}\n")
            with open("processed_app_ids.txt", "a") as f:
                f.write(f"{app_id}\n")
        # if app info is None then just add the app id to the file
        else:
            with open("final_data.csv", "a", encoding="utf-8") as f:
                f.write(f"{app_id},,,,,,,,\n")
            with open("processed_app_ids.txt", "a") as f:
                f.write(f"{app_id}\n")
    browser.close()
