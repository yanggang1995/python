# -*- coding: UTF-8 -*-
import pymysql
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

# ------ Email Config ------
EMAIL_SERVER = "smtp.exmail.qq.com"
EMAIL_SENDER = "1036556426@qq.com"
EMAIL_PASS = ""
EMAIL_RECEIVER = ["651464160@qq.com"]

# ------ Mysql Config ------
MYSQL_HOST = ""
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


if __name__ == '__main__':
    # 计算农历日期
    print("")
    # 查询数据
    b_sql = "select "
    b_data = m_load_data(b_sql)
    # 生成邮件
    msg_root = MIMEMultipart('related')
    msg_root['From'] = Header("Remind", 'utf-8')
    msg_root['To'] = "Y.G"
    subject = f'生日提醒-记得关注'
    msg_root['Subject'] = Header(subject, 'utf-8')
    msg_alternative = MIMEMultipart('alternative')
    b_info = ""
    for item in b_data:
        b_info += "<tr>"
        for var2 in range(0, 3):
            b_info += f"<td>{item[var2]}</td>"
        b_info += "</tr>"
    mail_msg = f"""
    {CSS_INFO}
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
