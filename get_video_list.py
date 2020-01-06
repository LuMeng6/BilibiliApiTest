import requests
import video_info as vi

page_num = 1
stop = False

def get_video_list_response(page_number=None):
    url = "http://api.bilibili.com/x/web-interface/newlist?rid=25" # 25 is MMD/3D
    if page_number:
        url += "&pn=%d" % page_number
    response = requests.get(url)
    return response.json()

def record_video_info(videos, start, end, video_list):
    global stop
    for video in videos:
        if video["copyright"] == 1: # 1 is original
            if start < video["pubdate"] < end:
                video_info = get_video_info(video["aid"], video["stat"])
                video_list.append(video_info)
                end = video["pubdate"]
            elif video["pubdate"] <= start:
                stop = True

def get_video_info(video_aid, video_stat):
    video_info = vi.VideoInfo(video_aid,
                           video_stat["view"],
                           video_stat["like"],
                           video_stat["coin"],
                           video_stat["favorite"])
    return video_info.to_dic()

def get_video_list():
    global page_num, stop

    f = open("video_list_Jan.txt", "w+")

    # January
    for day in range(31):
        stop = False
        video_list = []
        day_sec = 86400

        # start = 1577808000
        end = 1580486400 - (day_sec * day)
        start = end - day_sec

        # won't stop until hitting the start datetime
        while not stop:
            response_json = get_video_list_response(page_num)
            record_video_info(response_json["data"]["archives"], start, end, video_list)
            if not stop:
                page_num += 1

        f.writelines("%s\n" % video for video in video_list)

    f.close()