import webbrowser
import kugou
import QQ
import kuwo

if __name__ == "__main__":
    # music_name = "大鱼"
    # music_data = QQ.QQ_Music(music_name).run()
    # for num in range(min(len(music_data), 10)):
    #     music_detial = music_data[num]
    #     print(str(num + 1) + " - " + music_detial["music_name"] + " - " + music_detial["singer_name"] + " - " + music_detial["music_url"])
    # music_detial = music_data[0]
    # music_audio_url = QQ.QQ_Music(music_name).music_down(music_detial["music_url"])
    # print(music_detial["music_name"] + " - " + music_detial["singer_name"] + " - 下载链接：" + music_audio_url)



    music_name = input("输入歌曲名称：")
    print("请选择下载来源")
    data_source = input("[1]:QQ音乐  [2]:酷我音乐  [3]:酷狗音乐\n")
    flag_all = True
    if (data_source == "1"):
        class_music = QQ.QQ_Music(music_name)
    elif(data_source == "2"):
        class_music = kuwo.kuwo(music_name)
    elif(data_source == "3"):
        class_music = kugou.kugou(music_name)
    else:
        flag_all = False
    if (flag_all):
        music_data = class_music.run()
        for num in range(min(len(music_data), 10)):
            music_detial = music_data[num]
            print(str(num + 1) + " - " + music_detial["music_name"] + " - " + music_detial["singer_name"] + " - " +
                  music_detial["music_url"])
        try:
            music_num = int(input("输出下载序号（歌名前方数字）可以下载歌曲，直接回车退出程序："))
            if (music_num < 1):
                music_num = int(input("输入下载序号过小，请重新输入："))
            elif (music_num > 10):
                music_num = int(input("输入下载序号过大，请重新输入："))
            if (music_num >= 1) and (music_num <= 10):
                music_detial = music_data[music_num - 1]
                music_audio_url = class_music.music_down(music_detial["music_url"])
                if (music_audio_url[-5:] == "Wrong"):
                    print(music_audio_url[:-5])
                else:
                    print(music_detial["music_name"] + " - " + music_detial["singer_name"] + " - 下载链接：" + music_audio_url)
                    webbrowser.open(music_audio_url)


            else:
                print("输入下载序号出错，程序停止！")
        except:
            print("输入下载序号出错！")
    else:
        print("输入数据源出错！")
