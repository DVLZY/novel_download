# http://www.itangyuan.com/index.html
print()
print('------汤圆小说下载器 0.1------')
print('------   By lin  --------')
print()

import re
import requests
from urllib import parse
import html


searchkey = input('请输入书名或者作者名：')
print()
search = requests.get('http://www.itangyuan.com/search/book/'+searchkey+'.html').text #获取搜索页内容
search = parse.unquote_plus(search)     # url转码
tempN = re.compile('<p class="bname"><a href="/book/.*?html">  (.*?)</a>',re.S).findall(search) #提取书名
tempN = html.unescape(tempN)    #处理HTML转义字符
tempW = re.compile('<p class="author"><a href="/author/.*?html">(.*?)</a>',re.S).findall(search)      #提取作者
tempW = html.unescape(tempW)    #处理HTML转义字符
tempU = re.compile('<p class="bname"><a href="/book/(.*?)\.html">',re.S).findall(search)     #提取URL
for i in range(len(tempN)):
    try:
        print('【'+str(i+1)+'】《'+tempN[i]+'》'+tempW[i])
    except Exception as err:
        pass
    #输出作品对应作者的列表
print()
book_id = int(input('请输入要下载书籍的编号:'))
url0 = 'http://www.itangyuan.com/book/catalogue/'+ tempU[book_id-1] + '.html'
ua = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'}
rst0 = requests.get(url0,headers=ua).text                                       # 抓取目录页内容
book_name = str('《'+tempN[book_id-1]+'》'+tempW[book_id-1])                    # 拼接小说名称和作者名
unit_url = re.compile('<a href="/book/chapter/.*?/(\d{4,9}).html"',re.S).findall(rst0)  # 获取章节页面编号
file_down = open(book_name + '.txt', 'a+', encoding='utf-8')                    # 创建和标题同名的文件
file_down.write(book_name)
# 写入书名


print('开始下载：' + book_name+' 一共有 '+ str(len(unit_url)) +' 章')
for i in unit_url:
    book_unit_url = 'http://www.itangyuan.com/book/chapter/' + tempU[book_id-1] + '/' + i + '.html'  #完成章节网址拼接
    rst1 = requests.get(book_unit_url, headers=ua)               #抓取章节页内容
    rst1 = bytes(rst1.text,rst1.encoding).decode('utf-8','ignore') #重编码，去除乱码
    title = re.compile('<h1>(.*?)</h1>',re.S).findall(rst1)[0]          #获取文章标题
    title = html.unescape(title)    #处理HTML转义字符
    time =  re.compile('<span class="section-info">发布于(\d\d\d\d-\d\d-\d\d)',re.S).findall(rst1)[0] #获取发布时间
    file_down.write('\r\n-----' + title + '  发布于 ' + time +'-----\r\n')      # 写入标题和发布时间

    content = re.compile('<div class="section-main-con" data-name="section-con">(.*?)</div>',re.S).findall(rst1)        # 获取文章内容

    for sentence in content:
        sentence1 = (re.compile('<p>　　(.*?)</p>',re.S).findall(sentence))
        for sentence2 in sentence1:
            file_down.write(sentence2 + '\n\n')  # 写入正文
    print('正在下载：' + title)
print(book_name +'下载完成,一共有 '+ str(len(unit_url)) +' 章')

