# _*_ coding:utf-8 _*_

import copy
import datetime
import hashlib
import json
import os
import time
import redis

# ----------------------------------------------------------------------------------------
# -------------------------- 以下配置需要根据线上环境修改  ---------------------------------
# -- 脚本需要部署在元数据入库程序同一台服务器、需要安装ftp、python环境2.6、python redis模块 --
# ----------------------------------------------------------------------------------------
# 节目单存放目录
CHANNEL_PATH = "/tmp/srtmp/data"
# CSV 写入目录 --> 磁盘ftp目录，日期目录上一级
CSV_PATH = "/data/nmggd"
# redis IP
REDIS_HOST = "192.168.90.77"
# redis 端口
REDIS_PORT = 16379
# redis 密码
REDIS_PWD = "ideal"
# 直播节目单key
REDISKEY = "live_playbill_info_by_video_id"
# ftp ip地址
FTP_HOST = "192.168.90.77"
# 用户名
FTP_USER = "sdk"
# 密码
FTP_PWD = "sdk"
# ftp 地址
FTP_DIR = "/nmggd/20181030"
# ftp 文件列表
FTP_LIVE_LIST = " 阿拉善新闻综合.txt 巴彦淖尔新闻综合.txt 包头新闻综合.txt 赤峰新闻综合.txt 鄂尔多斯新闻综合.txt " \
                "呼和浩特-1.txt 呼和浩特-2.txt 呼和浩特-3.txt 呼和浩特新闻综合.txt 呼伦贝尔新闻综合.txt 满洲里新闻综合.txt " \
                "通辽新闻综合.txt 乌海新闻综合.txt 乌兰察布新闻综合.txt 锡林郭勒新闻综合.txt 兴安新闻综合.txt 都市生活318-324.txt " \
                "新闻综合318-324.txt 影视娱乐318-324.txt"
# ----------------------------------------------------------------------------------------
# -----------------------------------  END  ----------------------------------------------
# ----------------------------------------------------------------------------------------

# 列分隔符
COLUMN = b'3\xff'
# 行分隔符
ROW = b'\x03\xfe\r\n'

# 初始化日期目录
for j in range(0, 7):
    outPath = CSV_PATH + "/" + (datetime.datetime.now() + datetime.timedelta(days=2 + j)).strftime('%Y%m%d')
    if not os.path.exists(outPath):
        os.mkdir(outPath)
outPath = CSV_PATH + "/" + (datetime.datetime.now() + datetime.timedelta(days=2)).strftime('%Y%m%d')

# 拉取ftp文件到存放目录CHANNEL_PATH
os.system("ftp -v -n " + FTP_HOST + "<<EOF \n" +
          "user  " + FTP_USER + " " + FTP_PWD + "\n" +
          "binary \n"
          "lcd " + CHANNEL_PATH + "\n" +
          "cd " + FTP_DIR + "\n"
          "prompt \n" +
          "mget  " + FTP_LIVE_LIST + "\n" +
          "bye \n" +
          "EOF"
          )


def loadLine(param):
    try:
        return param.decode("utf-8").rstrip("\r\n").strip()
    except Exception:
        return param.decode("gb2312").rstrip("\r\n").strip()


def radix16To2(param):
    list_num = []
    for i in range(0, int(len(param) / 2)):
        list_num.append(int(param[2 * i:2 * i + 2], 16))
    return bytes(list_num)


def strToUnix(param):
    return int(time.mktime(time.strptime(param, '%Y-%m-%d %H:%M:%S')))


def strToMD5(param):
    return hashlib.md5(param).hexdigest()


def listToJson(live_id, live_name, category_id, line):
    jsonObject = {}
    jsonObject["video_id"] = live_id
    jsonObject["video_name"] = live_name.decode("utf-8")
    jsonObject["asset_id"] = ""
    jsonObject["category_id"] = category_id
    jsonObject["playbill_name"] = line[1].decode("utf-8")
    jsonObject["playbill_start_time"] = line[2]
    jsonObject["playbill_length"] = line[3]
    jsonObject["nns_original_id"] = ""
    return jsonObject


def writeToCSV(outFile, line):
    for i in range(0, len(line)):
        outFile.write(str(line[i]))
        if i < len(line) - 1:
            outFile.write(COLUMN)
        else:
            outFile.write(ROW)


def writeToRedis(client, live_id, array):
    client.hset(REDISKEY, live_id,
                json.dumps(array, ensure_ascii=False))


def main():
    readDir = os.listdir(CHANNEL_PATH)
    nns_live = open(outPath + "/nns_live." + time.strftime('%Y%m%d%H%M', time.localtime(time.time())) + ".1ton.csv",
                    mode="wb")
    nns_live_playbill_item = open(
        outPath + "/nns_live_playbill_item." + time.strftime('%Y%m%d%H%M', time.localtime(time.time())) + ".1ton.csv",
        mode="wb")
    redisClient = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PWD)
    for allDir in readDir:
        print(allDir)
        child = os.path.join('%s/%s' % (CHANNEL_PATH, allDir))
        begin_time = ""
        flag = 0
        first_line_time = ""
        write_line = [""] * 7
        tmp_line = [""] * 7
        live_name = allDir.rstrip("\\.txt")
        # 频道id
        nns_live_id = strToMD5(live_name)
        nns_live.write(bytes(nns_live_id.encode("utf-8")))
        nns_live.write(COLUMN)
        # 频道名称
        nns_live.write(bytes(live_name))
        nns_live.write(COLUMN)
        # 直播状态
        nns_live.write(bytes("1"))
        nns_live.write(COLUMN)
        # 栏目ID
        category_id = "261"
        nns_live.write(bytes(category_id))
        nns_live.write(COLUMN)
        # 提供商
        nns_live.write(bytes(""))
        nns_live.write(COLUMN)
        # 创建时间
        nns_live.write(bytes("".encode("utf-8")))
        nns_live.write(COLUMN)
        # 栏目分类名称
        nns_live.write(bytes("本地频道"))
        nns_live.write(COLUMN)
        # 运营商
        nns_live.write(bytes("suma".encode("utf-8")))
        array = []
        for line in open(child, "rb"):
            strLine = loadLine(line)
            if strLine.strip() == "" or not strLine.strip()[:1].isdigit():
                continue
            try:
                begin_time = str(datetime.datetime.strptime("20" + strLine, "%Y/%m/%d")).split(" ")[0]
                flag = 1
                continue
            except Exception:
                if flag == 1:
                    first_line_time = " " + strLine[0:5].replace(u'：', ":") + ":00"
                    flag = 0
                write_line = copy.deepcopy(tmp_line)
                playbill_time = begin_time + " " + strLine[0:5].replace(u'：', ":") + ":00"

                # 节目单id
                tmp_line[0] = strToMD5((live_name.decode("utf-8") + playbill_time.decode("utf-8")).encode("utf-8"))
                # 节目单名称
                tmp_line[1] = strLine[5:].strip().encode("utf-8")
                # 开始时间
                tmp_line[2] = playbill_time
                # 节目单时长
                tmp_line[3] = ""
                # 频道id
                tmp_line[4] = nns_live_id
                # 创建时间
                tmp_line[5] = playbill_time
                # 运营商id
                tmp_line[6] = "suma"
                if write_line[0] == "":
                    continue
                time_len = strToUnix(tmp_line[2]) - strToUnix(write_line[2])
                if time_len < 0:
                    write_line[3] = time_len + 86400
                    begin_time = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.mktime(time.strptime(begin_time, "%Y-%m-%d"))) + 86400))).split(" ")[0]
                    tmp_line[2] = begin_time + " " + strLine[0:5].replace(u'：', ":") + ":00"
                else:
                    write_line[3] = time_len
                writeToCSV(nns_live_playbill_item, write_line)
                array.append(listToJson(nns_live_id, live_name, category_id, write_line))
        tmp_time_len = strToUnix(begin_time + first_line_time) - strToUnix(tmp_line[2])
        if tmp_time_len < 0:
            tmp_line[3] = tmp_time_len + 86400
            begin_time = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.mktime(time.strptime(begin_time, "%Y-%m-%d"))) + 86400))).split(" ")[0]
            tmp_line[2] = begin_time + " " + strLine[0:5].replace(u'：', ":") + ":00"
        else:
            tmp_line[3] = tmp_time_len
        writeToCSV(nns_live_playbill_item, tmp_line)
        array.append(listToJson(nns_live_id, live_name, category_id, write_line))
        nns_live.write(ROW)
        writeToRedis(redisClient, nns_live_id, array)
    nns_live.close()
    nns_live_playbill_item.close()
    print(" 生成csv完成  目录 - " + outPath)
    print(" 节目单写入redis完成  key - live_playbill_info_by_video_id")
    for k in range(1, 7):
        mvPath = CSV_PATH + "/" + (datetime.datetime.now() + datetime.timedelta(days=2 + k)).strftime('%Y%m%d')
        os.system(" cp " + outPath + "/*  " + mvPath + "/")


if __name__ == '__main__':
    main()
