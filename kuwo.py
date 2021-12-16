import requests
import json

from lxml import etree


class kuwo:
    def __init__(self, music_name):
        self.url = "http://www.kuwo.cn/api/www/search/searchMusicBykeyWord?key=" + music_name +"&pn=1&rn=30&httpsStatus=1&reqId=" + "da11ad51-d211-11ea-b197-8bff3b9f83d2e"
        self.header = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Cookie': '_ga=GA1.2.1500987479.1595755923; _gid=GA1.2.568444838.1596065504; Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1595755923,1596065505; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1596076178; kw_token=P5XA2TZXG9',
            'csrf': 'P5XA2TZXG9',
            'Host': 'www.kuwo.cn',
            'Referer': 'http://www.kuwo.cn/search/list?key=%E5%A4%95%E9%98%B3%E7%BA%A2',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
        }
        self.datas = list()

    def get_request(self):
        response = requests.get(url=self.url, headers=self.header)
        # with open('./kuwo.txt', 'a', encoding='utf-8') as file:
        #     file.write(str(response.content.decode()))
        return response.content.decode()

    def parse_data(self, index, saver):
        next(saver)
        index_dict = json.loads(index)
        for index_obj in index_dict["data"]["list"]:
            result_dict = dict()
            result_dict["music_name"] = index_obj["name"]
            result_dict["singer_name"] = index_obj["artist"]
            result_dict["music_url"] = "http://www.kuwo.cn/play_detail/" + index_obj["musicrid"][6:]
            # try:
            #     result_dict["album_img"] = index_obj["pic"]
            # except KeyError:
            #     result_dict["album_img"] = "no_url"
            self.datas.append(result_dict)
            # saver.send(result_dict["album_img"])
        saver.send(self.datas)

    def save_data(self):
        while True:
            n = yield
            if not n:
                return
            with open('./kuwo.txt', 'a', encoding='utf-8') as file:
                file.write(json.dumps(n, ensure_ascii=False, indent=4))
            # if (isinstance(n, str)):
            #     if(n != "no_url"):
            #         with open('./kuwo/' + self.datas[-1]["music_url"][-6:] + ".jpg", 'wb') as file:
            #             file.write(requests.get(self.datas[-1]["album_img"]).content)
            # else:
            #     with open('./kuwo.txt', 'a', encoding='utf-8') as file:
            #         file.write(json.dumps(n, ensure_ascii=False, indent=4))

    def music_down(self, song_url):
        self.url = "http://www.kuwo.cn/api/v1/www/music/playUrl?mid=" + song_url[31:] + "&type=music&httpsStatus=1&reqId=896d8591-5db6-11ec-bb2a-a98ceb9a3731"
        response = self.get_request()
        response = json.loads(response)
        return response["data"]["url"]


    def run(self):
        response = self.get_request()
        c = self.save_data()
        self.parse_data(response,c)
        return self.datas

if __name__ == "__main__":
    music_name = input()
    kuwo(music_name).run()