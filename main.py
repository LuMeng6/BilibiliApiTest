import get_video_list as vl

vl.get_video_list()

with open("top_record_Feb.txt", "w+") as f:
    f.writelines("%s\n" % top for top in vl.top_list)