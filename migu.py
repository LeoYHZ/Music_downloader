import requests
import json

from lxml import etree


class migu_Music:
    def __init__(self, music_name):
        self.url = "https://music.migu.cn/v3/search?page=1&type=song&i=266469c20087ab7c55226ea4d16f58500beb6ce4&f=html&s=1639566203&c=001002A&keyword=" + music_name + "&v=3.21.8"
        # "https://music.migu.cn/v3/search?page=1&type=song&i=6b5798785368001a981a9e17193ef27455acd27f&f=html&s=1639562449&c=001002A&keyword=%E5%A4%A7%E9%B1%BC&v=3.21.8"
        # "https://music.migu.cn/v3/search?page=1&type=song&i=ab3475396855c65c8f6712740b1383c8cdf474b7&f=html&s=1639562490&c=001002A&keyword=ayasa&v=3.21.8"
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36 Edg/96.0.1054.53'
        }
        self.datas = list()

    def get_request(self):
        response = requests.get(url=self.url, headers=self.header)
        # with open('./migu.txt', 'a', encoding='utf-8') as file:
        #     file.write(str(response.content.decode()))
        return response.content

    def parse_data(self, index, saver):
        next(saver)
        index_obj = etree.HTML(index)
        results = index_obj.xpath('//a[@class="J-btn-share"]/@data-share')
        for result in results:
            result = json.loads(result)
            result_dict = dict()
            result_dict["singer_name"] = result["singer"]
            result_dict["music_name"] = result["title"]
            result_dict["music_url"] = "https://music.migu.cn" + result["linkUrl"]
            self.datas.append(result_dict)
        saver.send(self.datas)

    def save_data(self):
        while True:
            n = yield
            if not n:
                return
            with open('./migu.txt', 'a', encoding='utf-8') as file:
                file.write(json.dumps(n, ensure_ascii=False, indent=4))

    def run(self):
        response = self.get_request()
        c = self.save_data()
        self.parse_data(response,c)

if __name__ == "__main__":
    # music_name = input()
    # migu_Music(music_name).run()
    migu_Music("大鱼").run()
