import requests

# January
start = 1577808000
end = 1580486399

page_num = 1
stop = False

video_list = []

def get_video_list_response(page_number=None):
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
                video_info = {video["aid"]: get_video_info(video["stat"])}
                video_list.append(video_info)
                end = video["pubdate"]
            elif video["pubdate"] < start:
                stop = True

def get_video_info(video_stat):
    video_info = {
        "view": video_stat["view"],
        "like": video_stat["like"],
        "coin": video_stat["coin"],
        "favorite": video_stat["favorite"]
    }
    return video_info

def get_video_list():
    global page_num, stop

    f = open("video_list_Jan.txt", "w+")

    # won't stop until hitting the start datetime
    while not stop:
        response_json = get_video_list_response(page_num)
        record_video_info(response_json["data"]["archives"])
        page_num += 1

    f.writelines("%s\n" % video for video in video_list)
    f.writelines("counts: %d" % len(video_list))
    # f.writelines("end time: %d" % end)

    f.close()

    return video_list