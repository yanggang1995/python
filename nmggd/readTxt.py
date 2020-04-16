# _*_ coding:UTF-8 _*_

import copy
import hashlib
import json
import os
import time
from datetime import datetime
import redis

# 节目单存放目录
CHANNEL_PATH = "D:\STARCOR\MISSION\内蒙频道id一对多\盟市"
# 列分隔符
COLUMN = "33ff"
# 行分隔符
ROW = "03fe0d0a"
# 直播节目单key
REDISKEY = "live_playbill_info_by_video_id"


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
    return hashlib.md5(param.encode("utf-8")).hexdigest()


def listToJson(live_id, live_name, category_id, line):
    jsonObject = {}
    jsonObject["video_id"] = live_id
    jsonObject["video_name"] = live_name
    jsonObject["asset_id"] = ""
    jsonObject["category_id"] = category_id
    jsonObject["playbill_name"] = line[1]
    jsonObject["playbill_start_time"] = line[2]
    jsonObject["playbill_length"] = line[3]
    jsonObject["nns_original_id"] = ""
    return jsonObject


def writeToCSV(outFile, line):
    for i in range(0, len(line)):
        outFile.write(bytes(str(line[i]).encode("utf-8")))
        if i < len(line) - 1:
            outFile.write(radix16To2("33ff"))
        else:
            outFile.write(radix16To2("03fe0d0a"))


def writeToRedis(client, live_id, array):
    client.hset(REDISKEY, live_id,
                json.dumps(array, ensure_ascii=False))


def main():
    readDir = os.listdir(CHANNEL_PATH)
    nns_live = open("nns_live." + time.strftime('%Y%m%d%H%M', time.localtime(time.time())) + ".1ton.csv",
                    mode="wb")
    nns_live_playbill_item = open(
        "nns_live_playbill_item." + time.strftime('%Y%m%d%H%M', time.localtime(time.time())) + ".1ton.csv",
        mode="wb")
    redisClient = redis.Redis(host='192.168.90.77', port=16379, password='ideal')
    for allDir in readDir:
        print(allDir)
        child = os.path.join('%s/%s' % (CHANNEL_PATH, allDir))
        begin_time = ""
        write_line = [""] * 7
        tmp_line = [""] * 7
        live_name = allDir.rstrip("\\.txt")
        # 频道id
        nns_live_id = strToMD5(live_name)
        nns_live.write(bytes(nns_live_id.encode("utf-8")))
        nns_live.write(radix16To2("33ff"))
        # 频道名称
        nns_live.write(bytes(live_name.encode("utf-8")))
        nns_live.write(radix16To2("33ff"))
        # 直播状态
        nns_live.write(bytes("1".encode("utf-8")))
        nns_live.write(radix16To2("33ff"))
        # 栏目ID
        category_id = "261"
        nns_live.write(bytes(category_id.encode("utf-8")))
        nns_live.write(radix16To2("33ff"))
        # 提供商
        nns_live.write(bytes("".encode("utf-8")))
        nns_live.write(radix16To2("33ff"))
        # 创建时间
        nns_live.write(bytes("".encode("utf-8")))
        nns_live.write(radix16To2("33ff"))
        # 栏目分类名称
        nns_live.write(bytes("本地频道".encode("utf-8")))
        nns_live.write(radix16To2("33ff"))
        # 运营商
        nns_live.write(bytes("suma".encode("utf-8")))
        array = []
        for line in open(child, "rb"):
            strLine = loadLine(line)
            if strLine.strip() == "" or not strLine.strip()[:1].isdigit():
                continue
            try:
                # "20"+
                begin_time = str(datetime.strptime(strLine, "%Y/%m/%d")).split(" ")[0]
                continue
            except Exception:
                write_line = copy.deepcopy(tmp_line)
                playbill_time = (begin_time + " " + strLine[0:5].replace("：", ":") + ":00")

                # 节目单id
                tmp_line[0] = strToMD5(live_name + playbill_time)
                # 节目单名称
                tmp_line[1] = strLine[5:].strip()
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
                else:
                    write_line[3] = time_len
                writeToCSV(nns_live_playbill_item, write_line)
                array.append(listToJson(nns_live_id, live_name, category_id, write_line))
        tmp_time_len = strToUnix(begin_time + " 00:00:00") + 86400 - strToUnix(tmp_line[2])
        if tmp_line < 0:
            tmp_line[3] = tmp_time_len + 86400
        else:
            tmp_line[3] = tmp_time_len
        writeToCSV(nns_live_playbill_item, tmp_line)
        array.append(listToJson(nns_live_id, live_name, category_id, write_line))
        nns_live.write(radix16To2("03fe0d0a"))
        writeToRedis(redisClient, nns_live_id, array)
    nns_live.close()
    nns_live_playbill_item.close()


if __name__ == '__main__':
    main()
