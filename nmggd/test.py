import hashlib
import json
import os
import time

# key1 = time.mktime(time.strptime('2019-03-12 08:22:00', '%Y-%m-%d %H:%M:%S'))
# key2 = time.mktime(time.strptime('2019-03-12 09:22:00', '%Y-%m-%d %H:%M:%S'))
# print(int(key2) - int(key1))

# print(hashlib.md5("123".encode("utf-8")).hexdigest())

# client = redis.Redis(host='192.168.90.77', port=16379, password='ideal')
# print(client.hgetall("live_playbill_info_by_video_id"))
# jsonArray = []
# jsonObject = {}
# jsonObject["video_name"] = "CCTV-4"
# jsonObject["video_id"] = "0ad5b86534e39cb9a77b00a76ac9fe12"
# jsonArray.append(jsonObject)
#
# print(json.dumps(jsonArray, ensure_ascii=False))
#
# # client.hset("live_playbill_info_by_video_id", "0ad5b86534e39cb9a77b00a76ac9fe12",json.dumps(jsonArray, ensure_ascii=False))
# key = [""]*2
# key[0] = 1
# key[1] = 1
# print(key)
# def radix16To2(param):
#     list_num = []
#     for i in range(0, int(len(param) / 2)):
#         list_num.append(int(param[2 * i:2 * i + 2], 16))
#     return bytes(list_num)
#
#
# print(radix16To2("03fe0d0a"))

# # ftp ip地址
# FTP_HOST = "192.168.90.77"
# # 用户名
# FTP_USER = "sdk"
# # 密码
# FTP_PWD = "sdk"
# # ftp 地址
# FTP_DIR = "/nmggd/20181030"
#
# os.system("ftp -v -n " + FTP_HOST + "<<EOF \n" +
#           "user  " + FTP_USER + " " + FTP_PWD + "\n" +
#           "binary \n"
#           "lcd /tmp" + "\n" +
#           "cd " + FTP_DIR + "\n"
#           "prompt \n" +
#           "mget  nns_assists_item.20181031100401.1.csv nns_vod_index.20181031100411.1.csv\n" +
#           "bye \n" +
#           "EOF"
#           )

# FTP_LIVE_LIST = " 阿拉善新闻综合.txt 巴彦淖尔新闻综合.txt 包头新闻综合.txt 赤峰新闻综合.txt 鄂尔多斯新闻综合.txt " \
#                 "呼和浩特-1.txt 呼和浩特-2.txt 呼和浩特-3.txt 呼和浩特新闻综合.txt 呼伦贝尔新闻综合.txt 满洲里新闻综合.txt " \
#                 "通辽新闻综合.txt 乌海新闻综合.txt 乌兰察布新闻综合.txt 锡林郭勒新闻综合.txt 兴安新闻综合.txt 都市生活318-324.txt " \
#                 "新闻综合318-324.txt 影视娱乐318-324.txt"
#
# print(FTP_LIVE_LIST)

# print(time.strftime("%Y-%m-%d %H:%M:%S",
#                     time.localtime(int(time.mktime(time.strptime("2019-03-13", "%Y-%m-%d"))) + 86400)).split(" ")[0])

test_s = "\xe9\x9d\x92\xe5\x9f\x8e\xe7\x9c\xbc"
key = test_s.encode("raw_unicode_escape")
print(test_s)
print(key.decode("utf-8"))


decode_test = "青城警务"
print(decode_test.encode("utf-8"))
print("不存在。")
