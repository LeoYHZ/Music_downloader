import requests
import json

class QQ_Music:
    def __init__(self, music_name):
        self.url = "https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1&remoteplace=txt.yqq.top&searchid=20195022171686391&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n=10&w=" + music_name + "&g_tk_new_20200303=1805662696&g_tk=1805662696&loginUin=1543660640&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8%C2%ACice=0&platform=yqq.json&needNewCode=0"
        self.header = {
            # 'Cookie': 'ptui_loginuin=2298825248@qq.com; RK=u2CRJqAuNj; ptcz=52e2a0fa95edcdf93d9e51ae656e26256d6c3ee4c5bf66f6dc4ef5b892dad205; pgv_pvid=1542401804; fqm_pvqid=66ec091a-4ee5-4132-bafa-06f4cea81297; ts_refer=music.qq.com/; ts_uid=2785669816; fqm_sessionid=9a45ac5f-5c2f-461e-9d47-bd25a1d32e06; pgv_info=ssid=s2649892967; ts_last=y.qq.com/n/ryqq/player',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36 Edg/96.0.1054.53'
        }
        self.datas = list()

    def get_request(self):
        response = requests.get(url=self.url, headers=self.header)
        # with open('./QQ.txt', 'a', encoding='utf-8') as file:
        #     file.write(str(response.content.decode()))
        return response.content.decode()

    def parse_data(self, index, saver):
        next(saver)
        index_dict = json.loads(index)
        for index_obj in index_dict["data"]["song"]["list"]:
            result_dict = dict()
            result_dict["music_name"] = index_obj["title"]
            result_dict["singer_name"] = index_obj["singer"][0]["name"]
            result_dict["music_url"] = "https://y.qq.com/n/ryqq/songDetail/" + index_obj["mid"]
            self.datas.append(result_dict)
        saver.send(self.datas)

    def save_data(self):
        while True:
            n = yield
            if not n:
                return
            with open('./QQ.txt', 'a', encoding='utf-8') as file:
                file.write(json.dumps(n, ensure_ascii=False, indent=4))

        # "https://dl.stream.qqmusic.qq.com/C400003ae8GI3mQimV.m4a?guid=272199759&vkey=A393CE2CCA1414184E5E1CC09ACB266606EBA0C4A22075E20D30745B85F08FF6F15D873C6845699EB44D474F702DC6E88B863B797F231D90"
        # "https://dl.stream.qqmusic.qq.com/C400003ae8GI3mQimV.m4a?guid=5815593000&vkey=7F8C972AC126953EE00CAC285AA5CE81DB5DC7BDEFB51D5DD699F6DE0B30BD00ED4F2B56CEFC56062CD6137F159BE5BDABDC538A72B537CF&uin=&fromtag=66"
        # "https://dl.stream.qqmusic.qq.com/C400004OQ5Mt0EmEzv.m4a?guid=5815593000&vkey=7F8C972AC126953EE00CAC285AA5CE81DB5DC7BDEFB51D5DD699F6DE0B30BD00ED4F2B56CEFC56062CD6137F159BE5BDABDC538A72B537CF&uin=&fromtag=66"
        # "https://u.y.qq.com/cgi-bin/musics.fcg?_=1639618889082&sign=zzbdc3b3b85rdkyyqbb4qoj4um1dvcxg38ff1d8a"

    def music_down(self, song_url):
        return "QQ音乐暂时无法下载Wrong"
        # self.url = "http://www.kuwo.cn/api/v1/www/music/playUrl?mid=" + song_url[31:] + "&type=music&httpsStatus=1&reqId=896d8591-5db6-11ec-bb2a-a98ceb9a3731"
        song_url = "https://u.y.qq.com/cgi-bin/musics.fcg?_=1639625387166&sign=zzb43ffddc6dlftulyv2ezpbyrh7bn3zgb6c98611"
        # song_url = '''https://u.y.qq.com/cgi-bin/musicu.fcg?-=getplaysongvkey5559460738919986&g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0&data={'req":{"module":"CDN.SrfCdnDispatchServer","method":"GetCdnDispatch","param":{"guid":"1825194589","calltype":0,"userip":""}},"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"1825194589","songmid":["''' + song_url[35:] + '''"],"songtype":[0],"uin":"0","loginflag":1,"platform":"20"}},"comm":{"uin":0,"format":"json","ct":24,"cv":0}}'''
        # print(song_url)
        # form_data = {
        #     ":authority": "u.y.qq.com",
        #     "accept": "application/json",
        #     "accept-encoding": "gzip, deflate, br",
        #     "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        #     "content-length": "939",
        #     "content-type": "application/x-www-form-urlencoded",
        #     "cookie": "ptui_loginuin=1872056877@qq.com; RK=u2CRJqAuNj; ptcz=52e2a0fa95edcdf93d9e51ae656e26256d6c3ee4c5bf66f6dc4ef5b892dad205; pgv_pvid=1542401804; fqm_pvqid=66ec091a-4ee5-4132-bafa-06f4cea81297; ts_refer=music.qq.com/; ts_uid=2785669816; fqm_sessionid=9a45ac5f-5c2f-461e-9d47-bd25a1d32e06; pgv_info=ssid=s2649892967",
        #     "origin": "https://y.qq.com",
        #     "referer": "https://y.qq.com/",
        #     "sec-ch-ua": '''" Not A;Brand";v="99", "Chromium";v="96", "Microsoft Edge";v="96"''',
        #     "sec-ch-ua-mobile": "?0",
        #     "sec-ch-ua-platform": "Windows",
        #     "sec-fetch-dest": "empty",
        #     "sec-fetch-mode": "cors",
        #     "sec-fetch-site": "same-site"
        # }
        form_data = {
            "access-control-allow-credentials": "true",
            "access-control-allow-origin": "https://y.qq.com",
            "access-control-expose-headers": "Area",
            "area": "sh",
            "content-encoding": "gzip",
            "content-length": "2029",
            "u-location": "195021664_195161822_160691142_195021369_195161753"
        }
        response = requests.post(url=song_url, data=form_data,headers=self.header)
        # response = self.get_request()
        # response = json.loads(response)
        # return response["data"]["url"]
        print(response.content.decode())

    def run(self):
        response = self.get_request()
        c = self.save_data()
        self.parse_data(response,c)
        return self.datas

if __name__ == "__main__":
    music_name = input()
    QQ_Music(music_name).run()
    # QQ_Music("大鱼").run()
