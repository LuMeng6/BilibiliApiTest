class VideoInfo:
    def __init__(self, aid, view, like, coin, favorite):
        self.aid = aid
        self.view = view
        self.like = like
        self.coin = coin
        self.favorite = favorite

    def to_dic(self):
        return {
            self.aid: {
                "view": self.view,
                "like": self.like,
                "coin": self.coin,
                "favorite": self.favorite
            }
        }

    '''
    top_list = [{"view":0, "aid":[]},
                {"like":0, "aid":[]},
                {"coin":0, "aid":[]},
                {"favorite":0, "aid":[]}]
    '''
    def compare(self, top_list):
        top_view = _compare_helper(self.aid, self.view, top_list[0], "view")
        top_like = _compare_helper(self.aid, self.like, top_list[1], "like")
        top_coin = _compare_helper(self.aid, self.coin, top_list[2], "coin")
        top_favorite = _compare_helper(self.aid, self.favorite, top_list[3], "favorite")
        return [top_view, top_like, top_coin, top_favorite]

def _compare_helper(aid, value, top_record, name):
    if value == top_record[name]:
        return {name:value, "aid":top_record["aid"].append(aid)}
    elif value > top_record[name]:
        return {name:value, "aid":aid}
    else:
        return top_record