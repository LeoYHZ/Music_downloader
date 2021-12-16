import requests
import random
import json

class Music163:
    def __init__(self, music_name):
        # self.url = "https://music.163.com/#/search/m/?s=" + music_name +"&type=1"
        self.url = "https://music.163.com/weapi/cloudsearch/get/web?csrf_token="
        self.headers = [
            {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
            },
            {
                "User-Agent": "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11"
            }
        ]
        # self.urls = [self.url.format(i) for i in range(1, 2, 1)]
        self.urls = [self.url]
        # print(self.urls)
        self.datas = list()

    def get_request(self, url):
        form_data = {
            "params": "bArQX7jHwTYo+q9PWB25dfDYeqD0sywm/ez6t+8WQ3V9wyP9MdniNKe8OdcWwk+oG4mJh9UwD4ou/9h01Av8b9ZcO+Yp32hB6M70Kmi5PPlkAMwhxz9RmKFKgdgFU59ZggebI2DQHzYYaUhCxaP/iExZM3CbjKUeBrdYqIuiSuXthd75f/45qpR4IvziNVT7aaiqYHS8mbVkNN8piXKH6AAJjnj9UxeYl+rnrfgJMHjtVbC95TcR028pvnJe0dJrRXdufIiKczC+MJPpIjPdOw==",
            "encSecKey": "741a1bf30f8a3e86100abbe4ec1a847bef51f2f87221b8e27215e2ab4d510fb40344208ac72bb167d6d422da10c3f075c6656b40a5713427679b8e85d8b0b0077da82147ca8196445a59f4ccdd26525a4e3a049355a895b7cbef44cd3376d3967228005a5b7ad9617eafbce49cf2dc37a81115ca272b17f9b9a37e948409c783"
        }
        # form_data = {
        #     "params": "IYxhXRNqFTH2qsAIj0ymJcvrQ58D5F1zMTL5PiJqGV61XvWWs7SoMZjYHozXR4TfHF13cvXu5gY469r32HyTu8NEFygmPbUebXrec019mDV+EnMTZJyc/bkkPUsy6R+VvK1QEYIPu2aaup7meXQ7DGeF1/hh/79nSOvj7jG/5sXy4NtASRkPN+l+S0DWDRzXdVYNl1dwS6ET0RIP7Qz20TCN+ULrwX9D5xesD3/2mnp28piYkrjK87Gz+wCgl4fC8IMZN4MsgirSQMXzjyBYjlJBkv5pIxFmFdWF+vtExYWQRLBMqOSgCl6rydvjwRNk"
        #     "encSecKey": "a410fcb9aed07f04540e6d95fb4000f83b4164fe476d2e46b07dc6dbdf1475347735ae62cb2a3fc763acdfea92e59546980209fc4663b4572a9f2969c805c3c67cfc4adea5fdfab73e8983d323833a31979330bdf11681e53c9057f3af57cf01a71c6850ca80935938b9b3d353bcdcab6b15b9f59c16c1976ca3bb2b83bc2f4f"
        # }
        response = requests.post(url=self.url, data=form_data,
                                 headers=self.headers[random.randint(0, len(self.headers) - 1)])

        # with open('./home.txt', 'a', encoding='utf-8') as file:
        #     file.write(str(response.content, 'utf-8'))
        # return response.content
        return response.content.decode()


    def parse_data(self, content, saver):
        next(saver)
        content_json = json.loads(content)
        result_list = []
        for content_detial in content_json["result"]["songs"]:
            # result_dict = {'music_name': '', 'music_id': '', 'album_id': '', 'singer_name': ''}
            result_dict = dict()
            result_dict["music_name"] = content_detial["name"]
            result_dict["music_id"] = content_detial["id"]
            result_dict["album_id"] = content_detial["ar"][0]["id"]
            result_dict["singer_name"] = content_detial["ar"][0]["name"]
            result_list.append(result_dict)
        saver.send(result_list)


    def save_data(self):
        while True:
            n = yield
            if not n:
                return
            with open('./music163.txt', 'a', encoding='utf-8') as file:
                file.write(json.dumps(n, ensure_ascii=False, indent=4))


    def run(self):
        for url in self.urls:
            response = self.get_request(url)
            c = self.save_data()
            self.parse_data(response,c)

if __name__ == "__main__":
    # music_name = input()
    # Music163(music_name).run()
    Music163("大鱼").run()