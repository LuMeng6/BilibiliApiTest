import requests

def get_video_list(page_number=None):
    url = "http://api.bilibili.com/x/web-interface/newlist?rid=25" # 25 is MMD/3D
    if page_number:
        url += "&pn=%d" % page_number
    response = requests.get(url)
    return response.json()

def record_video_info(videos, filename=None):
    global end, stop, video_list
    for video in videos:
        if video["copyright"] == 1: # 1 is original
            if start <= video["pubdate"] <= end:
                video_list.append(video["aid"])
                end = video["pubdate"]
            elif video["pubdate"] < start:
                stop = True

# January
start = 1577808000
end = 1580486399

page_num = 1
stop = False

video_list = []

f = open("video_list_Jan.txt", "w+")

# won't stop until hitting the start datetime
while not stop:
    response_json = get_video_list(page_num)
    record_video_info(response_json["data"]["archives"])
    page_num += 1

f.writelines("%d\n" % video for video in video_list)
f.writelines("counts: %d\n" % len(video_list))
f.writelines("end time: %d\n" % end)

f.close()