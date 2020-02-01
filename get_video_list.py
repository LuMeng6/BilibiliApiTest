import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

import video_info as vi

page_num = 1
stop = False
top_list = [{"view": 0, "aids": []},
            {"like": 0, "aids": []},
            {"coin": 0, "aids": []},
            {"favorite": 0, "aids": []}]


def get_video_list_response(page_number=None):
    url = "http://api.bilibili.com/x/web-interface/newlist?rid=25" # 25 is MMD/3D

    retries = 3
    backoff_factor = 0.3,
    status_forcelist = (500, 502, 504)
    retry = Retry(total=retries,
                  read=retries,
                  connect=retries,
                  backoff_factor=backoff_factor,
                  status_forcelist=status_forcelist,)
    bili_adapter = HTTPAdapter(max_retries=retry)
    session = requests.session()
    session.mount(url, bili_adapter)

    if page_number:
        url += "&pn=%d" % page_number

    print("11111111111")
    response = session.get(url)
    print("22222222222")
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
                break


def get_video_info(video_aid, video_stat):
    global top_list
    video_info = vi.VideoInfo(video_aid,
                              video_stat["view"],
                              video_stat["like"],
                              video_stat["coin"],
                              video_stat["favorite"])
    top_list = video_info.compare(top_list)
    return video_info.to_dic()


def get_video_list():
    global page_num, stop
    f = open("video_list_Jan.txt", "w+")

    # January
    for day in range(31):
        print("day: " + str(31 - day))
        stop = False
        video_list = []
        day_sec = 86400

        end = 1580486400 - (day_sec * day)
        start = end - day_sec # 2020.01.01 00:00:00 => 1577808000

        # won't stop until hitting the start datetime
        while not stop:
            print("page: " + str(page_num))
            response_json = get_video_list_response(page_num)

            if response_json is None:
                raise ValueError("response is null")

            record_video_info(response_json["data"]["archives"], start, end, video_list)
            if not stop:
                page_num += 1

        f.writelines("%s\n" % video for video in video_list)

    f.close()
