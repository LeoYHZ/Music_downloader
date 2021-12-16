import requests
import json

class kugou:
    def __init__(self, music_name):
        self.url = "https://songsearch.kugou.com/song_search_v2?callback=jQuery1124042761514747027074_1580194546707&keyword=" + music_name + "&page=1&pagesize=30&userid=-1&clientver=&platform=WebFilter&tag=em&filter=2&iscorrection=1&privilege_filter=0&_=1580194546709"
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36 Edg/96.0.1054.53'
        }
        self.datas = list()

    def get_request(self):
        response = requests.get(url=self.url, headers=self.header)
        # with open('./kugou.txt', 'a', encoding='utf-8') as file:
        #     file.write(str(response.content.decode()))
        return response.content.decode()[43:-2]

    def parse_data(self, index, saver):
        next(saver)
        index_dict = json.loads(index)
        for index_obj in index_dict["data"]["lists"]:
            result_dict = dict()
            music_singer = list(index_obj["FileName"].replace("<em>","").replace("</em>","").split(" - "))
            result_dict["music_name"] = music_singer[1]
            result_dict["singer_name"] = music_singer[0]
            if(len(index_obj["AlbumID"]) == 0):
                result_dict["music_url"] = "https://www.kugou.com/song/#hash=" + index_obj["FileHash"]
            else:
                result_dict["music_url"] = "https://www.kugou.com/song/#hash=" + index_obj["FileHash"] + "&album_id=" + index_obj["AlbumID"]
            self.datas.append(result_dict)
        saver.send(self.datas)

    def save_data(self):
        while True:
            n = yield
            if not n:
                return
            with open('./kugou.txt', 'a', encoding='utf-8') as file:
                file.write(json.dumps(n, ensure_ascii=False, indent=4))

    def music_down(self, song_url):
        if (song_url.find("album_id") >= 0):
            hash_code, album_id = song_url[33:].split("&album_id=")
            song_url = "https://wwwapi.kugou.com/yy/index.php?r=play/getdata&callback=jQuery19106396361014218102_1639583596974&hash=" + hash_code + "&dfid=11TSLi27rAcU4QNnAV3lpjiS&appid=1014&mid=bb95e4b5044717d1f9ac1cd937808066&platid=4&album_id=" + album_id + "&_=1639583596976"
        else:
            hash_code = song_url[33:]
            song_url = "https://wwwapi.kugou.com/yy/index.php?r=play/getdata&callback=jQuery19106396361014218102_1639583596974&hash=" + hash_code + "&dfid=11TSLi27rAcU4QNnAV3lpjiS&appid=1014&mid=bb95e4b5044717d1f9ac1cd937808066&platid=4&_=1639583596976"
        response = requests.get(url=song_url, headers=self.header)
        response = json.loads(response.content.decode()[41:-2])
        return response["data"]["play_backup_url"]

    def run(self):
        response = self.get_request()
        c = self.save_data()
        self.parse_data(response,c)
        return self.datas

if __name__ == "__main__":
    music_name = input()
    kugou(music_name).run()
