URL_String=input("Please enter your Instagram url {https://www.instagram.com/username/}: ")

from tkinter import filedialog
Folder_saved=filedialog.askdirectory(title="Select the folder where you want to save the images: ")
if Folder_saved == '':
    print('Folder not selected')
    exit(0)

from lxml import html
import requests
page=requests.get(URL_String)
print(page.status_code)
if page.status_code != 200:
    print('Check your Url')
    exit(0)

tree=html.fromstring(page.content)

import requests, bs4
import urllib
from bs4 import BeautifulSoup
import re
import json
soup = BeautifulSoup(page.content, "lxml")
script_tag = soup.find('script', text=re.compile('window\._sharedData'))
#print(script_tag)
json_data = script_tag.string.partition('=')[-1].strip(' ;')
print("Output start")
json_string = json.loads(json_data)
print(json_string["country_code"])
n = 0
print("Full Name: " + json_string["entry_data"]["ProfilePage"][0]["graphql"]["user"]["full_name"])
print("Username: " + json_string["entry_data"]["ProfilePage"][0]["graphql"]["user"]["username"])
print("Followers: " + str(json_string["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_followed_by"]["count"]))
print("Follows: " + str(json_string["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_follow"]["count"]))
print("Profile Pic: " + json_string["entry_data"]["ProfilePage"][0]["graphql"]["user"]["profile_pic_url_hd"])
max = len(json_string["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"])
while n < max:
    thumbnail = json_string["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][n]["node"]
    if thumbnail["is_video"]:
        print("Saving Video")
        Video_URL = "https://www.instagram.com/p/" + thumbnail["shortcode"]
        video_page = requests.get(Video_URL)
        tree = html.fromstring(video_page.content)
        video_soup = BeautifulSoup(video_page.content, "lxml")
        video_script_tag = video_soup.find('script', text=re.compile('window\._sharedData'))
        video_json_data = video_script_tag.string.partition('=')[-1].strip(' ;')
        video_link = json.loads(video_json_data)
        print(video_link["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["video_url"])
        resource = urllib.request.urlopen(video_link["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["video_url"])
        output = open(Folder_saved + "/" + thumbnail["shortcode"] + ".mp4", "wb")
        output.write(resource.read())
        output.close()
    if thumbnail["__typename"] == "GraphSidecar":
        print("Saving Carousel")
        Car_URL = "https://www.instagram.com/p/" + thumbnail["shortcode"]
        car_page = requests.get(Car_URL)
        tree = html.fromstring(car_page.content)
        car_soup = BeautifulSoup(car_page.content, "lxml")
        car_script_tag = car_soup.find('script', text=re.compile('window\._sharedData'))
        car_json_data = car_script_tag.string.partition('=')[-1].strip(' ;')
        car_link = json.loads(car_json_data)
        car_count = len(car_link["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["edge_sidecar_to_children"]["edges"])
        j = 0
        while(j < car_count):
            print(car_link["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["edge_sidecar_to_children"]["edges"][j]["node"]["display_url"])
            resource = urllib.request.urlopen(car_link["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["edge_sidecar_to_children"]["edges"][j]["node"]["display_url"])
            output = open(Folder_saved + "/" + thumbnail["shortcode"] + ".jpg", "wb")
            output.write(resource.read())
            output.close()
            j=j+1
        print("Carousel Saved")
    print(thumbnail['display_url'])
    print("Saving Image")
    resource = urllib.request.urlopen(thumbnail['display_url'])
    output = open(Folder_saved + "/" + thumbnail["shortcode"] + ".jpg", "wb")
    output.write(resource.read())
    output.close()
    n=n+1
print("Output end")
