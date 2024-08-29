from playwright.sync_api import sync_playwright
import time


# define the base url
base_url = "https://play.google.com/store/apps/details?id="

# open the file containing the list of app ids
file_name = "apk_list_full.csv"

with open(file_name, "r") as f:
    app_ids = f.read().split("\n")

final_ids = []

for app_id in app_ids:
    # remove double quotation marks and save the app id
    app_id = app_id.replace('"', "")
    final_ids.append(app_id)

# rewrite the file with the cleaned app ids
with open(file_name, "w") as f:
    for app_id in final_ids:
        f.write(app_id + "\n")