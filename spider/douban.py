# -*- coding = utf-8 -*-
# 豆瓣爬虫（urllib+re+bs4方式）

import time
from bs4 import BeautifulSoup
import re
import urllib.error
import urllib.request
import xlwt
import sqlite3


def main():
    base_url = "https://movie.douban.com/top250?start="
    # save_path = '豆瓣.xls'
    db_path = "movie.db"
    # 爬取网页
    data_list = get_data(base_url)
    # 保存数据
    # save_data(data_list, save_path)
    save_to_db(data_list, db_path)
    print("爬取完毕")


# 向url发送请求
def ask_url(url):
    head = {
        'User-Agent': "Mozilla / 5.0(Windows; NT; 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, like; Gecko) Chrome / "
                      "96.0; .4664; .110; Safari / 537.36"
    }
    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


# 爬取网页
def get_data(base_url):
    data_list = []
    for i in range(0, 10):
        print("正在爬取第{}页".format(i + 1))
        time.sleep(1)
        url = base_url + str(i * 25)
        html = ask_url(url)  # 保存获取到的网页源码
        # 逐一解析数据
        soup = BeautifulSoup(html, "html.parser")  # html.parser是一种页面解析器
        for item in soup.find_all('div', class_="item"):  # 查找复合要求的字符串，形成列表
            data = []
            item = str(item)
            # 创建正则表达式对象（字符串模式）re.S忽视换行符
            link = re.findall(re.compile(r'<a href="(.*?)">'), item)[0]  # 影片详情的链接
            data.append(link)
            img_src = re.findall(re.compile(r'<img.*src="(.*?)"', re.S), item)[0]  # 影片图片链接
            data.append(img_src)
            title = re.findall(re.compile(r'<span class="title">(.*)</span>'), item)  # 影片标题的链接
            # 片名可能只有一个中文
            if len(title) == 2:
                c_title = title[0]
                data.append(c_title)
                o_title = title[1].replace("/", "").replace("\xa0", "")
                data.append(o_title)
            else:
                data.append(title[0])
                data.append(" ")  # 留空
            rating = re.findall(re.compile(r'<span class="rating_num" '
                                           r'property="v:average">(.*)</span>'), item)[0]  # 影片评分
            data.append(rating)
            judge = re.findall(re.compile(r'<span>(\d*)人评价</span>'), item)[0]  # 影片评价人数
            data.append(judge)
            inq = re.findall(re.compile(r'<span class="inq">(.*)</span>'), item)  # 影片概况
            if len(inq) != 0:
                inq = inq[0].replace("。", "")
                data.append(inq)
            else:
                data.append(" ")  # 留空
            bd = re.findall(re.compile(r'<p class="">(.*?)</p>', re.S), item)[0]  # 影片相关内容
            bd = re.sub('<br(\s+)?/>(\s+)?', " ", bd).replace("/", "").replace("\xa0", "")
            data.append(bd.strip())  # 去空格
            data_list.append(data)  # 把处理好的一部电影信息放入data_list
    return data_list


# 保存数据
def save_data(data_list, save_path):
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)
    sheet = book.add_sheet("豆瓣TOP250", cell_overwrite_ok=True)
    col = ("电影详情链接", "图片链接", "影片中文名", "影片外国名", "评分", "评价数", "概况", "相关信息")
    for i in range(len(col)):
        sheet.write(0, i, col[i])  # 列名
    for i in range(250):
        print("正在保存第{}条".format(i+1))
        data = data_list[i]
        for j in range(len(col)):
            sheet.write(i+1, j, data[j])
    book.save(save_path)


# 保存数据到数据库
def save_to_db(data_list, db_path):
    init_db(db_path)
    conn = sqlite3.connect(db_path)  # 连接数据库
    cursor = conn.cursor()  # 获取游标

    for data in data_list:
        for index in range(len(data)):
            if index == 4 or index == 5:
                continue
            data[index] = '"'+data[index]+'"'
        sql = '''
            insert into movie250(
            info_link, pic_link, c_name, e_name, score, rated, introduction, info
            ) values(%s)
        '''%",".join(data)
        cursor.execute(sql)
        conn.commit()
    cursor.close()
    conn.close()


# 初始化数据库
def init_db(db_path):
    sql = '''
        create table movie250(
        id integer primary key autoincrement,
        info_link text,
        pic_link text,
        c_name varchar,
        e_name varchar,
        score numeric,
        rated numeric,
        introduction text,
        info text
        )
    '''
    conn = sqlite3.connect(db_path)  # 连接数据库
    cursor = conn.cursor()  # 获取游标
    cursor.execute(sql)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    main()
    print("over")
