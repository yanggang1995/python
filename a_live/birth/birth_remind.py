# -*- coding: UTF-8 -*-
import pymysql
import smtplib
import time
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from borax.calendars.lunardate import LunarDate

# ------ Email Config ------
EMAIL_SERVER = "smtp.qq.com"
EMAIL_SENDER = "1036556426@qq.com"
EMAIL_PASS = "154_226_221_202_227_156_169_172_152_225_208_220_212_202_215_212_"
EMAIL_RECEIVER = ["651464160@qq.com"]

# ------ Mysql Config ------
MYSQL_HOST = "mysql_cnt"
MYSQL_USER = "root"
MYSQL_PWD = "yg"
MYSQL_DB = "yg_live"

# ------    随机因子   ------
CSS_INFO = """
<style type="text/css">
    html {
        font-family: sans-serif;
        -ms-text-size-adjust: 100%;
        -webkit-text-size-adjust: 100%;
    }

    body {
        margin: 10px;
    }
    table {
        border-collapse: collapse;
        border-spacing: 0;
    }

    td,th {
        padding: 0;
    }

    .pure-table {
        border-collapse: collapse;
        border-spacing: 0;
        empty-cells: show;
        border: 1px solid #cbcbcb;
    }

    .pure-table caption {
        color: #000;
        font: italic 85%/1 arial,sans-serif;
        padding: 1em 0;
        text-align: center;
    }

    .pure-table td,.pure-table th {
        border-left: 1px solid #cbcbcb;
        border-width: 0 0 0 1px;
        font-size: inherit;
        margin: 0;
        overflow: visible;
        padding: .5em 1em;
    }

    .pure-table thead {
        background-color: #e0e0e0;
        color: #000;
        text-align: left;
        vertical-align: bottom;
    }

    .pure-table td {
        background-color: transparent;
    }
    .pure-table-horizontal td,.pure-table-horizontal th {
        border-width: 0 0 1px 0;
        border-bottom: 1px solid #cbcbcb;
    }

    .pure-table-horizontal tbody>tr:last-child>td {
        border-bottom-width: 0;
    }
</style>
"""
FACTOR = "3rner034&ioereor4^jknaer2%dfwpier_ipfepfn6723_irfwrp"


def m_load_data(sql):
    conn = pymysql.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PWD, MYSQL_DB, charset='utf8')
    cursor = conn.cursor()
    cursor.execute(sql)
    rs = cursor.fetchall()
    conn.close()
    return rs


def send_email(msg):
    try:
        s_obj = smtplib.SMTP_SSL(EMAIL_SERVER)
        s_obj.connect(EMAIL_SERVER, 465)
        s_obj.login(EMAIL_SENDER, decrypt(EMAIL_PASS))
        s_obj.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        print("邮件发送成功")
        return 0
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")
        return 1


def decrypt(p):
    dec_str = ""
    for i, j in zip(p.split("_")[:-1], FACTOR):
        temp = chr(int(i) - ord(j))
        dec_str = dec_str + temp
    return dec_str


def fix_zero(num):
    if num < 10:
        return f"0{num}"
    else:
        return f"{num}"


def main():
    # 获取明天的农历日期（农历2018年七月初一）
    lu_date = LunarDate.tomorrow()
    tom_day = f"{fix_zero(lu_date.month)}{fix_zero(lu_date.day)}"
    # 查询数据
    b_sql = f"select modify_time,name,relation,lunar_birth from birth where lunar_birth='{tom_day}'"
    b_data = m_load_data(b_sql)
    if len(b_data) > 0:
        # 生成邮件
        msg_root = MIMEMultipart('related')
        msg_root['From'] = Header("Remind", 'utf-8')
        msg_root['To'] = "Y.G"
        subject = f'明日生日提醒-记得关注'
        msg_root['Subject'] = Header(subject, 'utf-8')
        msg_alternative = MIMEMultipart('alternative')
        b_info = ""
        for item in b_data:
            b_info += "<tr>"
            for var2 in range(0, 4):
                b_info += f"<td>{item[var2]}</td>"
            b_info += "</tr>"
        mail_msg = f"""
        {CSS_INFO}
        <h2>这些小可爱明天要过生日了，记得送祝福哦！！！</h2>
        <table class="pure-table pure-table-horizontal">
            <thead>
            <tr>
                <th>-_-</th>
                <th>Name</th>
                <th>relation</th>
                <th>birth</th>
            </tr>
            </thead>
            <tbody>
                {b_info}
            </tbody>
        </table>
        <br/>
        <hr size=1 color='gray' width='600' align='left'/>
        """
        msg_alternative.attach(MIMEText(mail_msg, 'html', 'utf-8'))
        msg_root.attach(msg_alternative)
        # 发送邮件
        send_email(msg_root)
    else:
        print("明天没有过生日的人")


if __name__ == '__main__':
    while True:
        main()
        time.sleep(43200)
