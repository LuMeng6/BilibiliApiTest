import requests

original = 1

def get_video_list(page_number=None):
    url = "http://api.bilibili.com/x/web-interface/newlist?rid=25"
    if page_number:
        url += "&pn=%d" % page_number
    response = requests.get(url)
    return response.json()

f = open("test.txt", "a+")

f.write("\n")

f.close()