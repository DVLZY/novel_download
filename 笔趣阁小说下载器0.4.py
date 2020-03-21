'''
小说下载器0.4
说明：
1、调用的笔趣阁小说网址接口
更新日志：
1、增加了书名，作者名搜索功能
2、移除了书籍ID下载功能
待优化内容：
1、容错和异常处理（无搜索结果、唯一搜索结果）
2、优化写入文章正则
'''
print()
print('------小说下载器 0.4------')
print('------   By lin  --------')
print()

import re
import requests

searchkey = input('请输入书名或者作者名，请您少字也别输错字：')
search = requests.get('http://www.paoshu8.com/modules/article/search.php',params={'searchkey':searchkey}).text.encode('ISO-8859-1').decode('utf8') #获取搜索页内容
tempN = re.compile('<td class="odd">.*?/">(.*?)</a></td>',re.S).findall(search) #提取书名
tempW = re.compile('<td class="odd">[^<](.*?)</td>',re.S).findall(search)       #提取作者
tempU = re.compile('<td class="odd"><a href="(.*?)">',re.S).findall(search)     #提取URL
for i in range(len(tempN)):
    try:
        print('【'+str(i+1)+'】《'+tempN[i]+'》'+tempW[i])
    except Exception as err:
        pass

    #输出作品对应作者的列表

book_id = int(input('请输入要下载书籍的编号:'))
url0 = tempU[book_id-1]
ua = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'}
rst0 = requests.get(url0,headers=ua).text                                       # 抓取目录页内容
book_name = str('《'+tempN[book_id-1]+'》'+tempW[book_id-1])                    # 拼接小说名称和作者名
unit_url = re.compile('<dd><a href="/.*?/(\d{4,9}).html">',re.S).findall(rst0)  # 获取章节页面编号
file_down = open(book_name + '.txt', 'a+', encoding='utf-8')                    # 创建和标题同名的文件
file_down.write(book_name)
# 写入书名
print('开始下载：' + book_name+'一共有'+ str(len(unit_url)) +'章')
for i in unit_url:
    book_unit_url = url0 + i + '.html'                                  #完成章节网址拼接
    rst1 = requests.get(book_unit_url, headers=ua).text                 #抓取章节页内容
    title = re.compile('<h1>(.*?)</h1>',re.S).findall(rst1)[0]          #获取文章标题
    file_down.write('\r\n-----' + title + '-----\r\n')                  # 写入标题
    content = re.compile('<div id="content">(.*?)</div>',re.S).findall(rst1)        # 获取文章内容
    for sentence in content:
        sentence1 = (re.compile('<p>\u3000\u3000(.*?)</p>').findall(sentence))
        for sentence2 in sentence1:
            file_down.write(sentence2 + '\r\n')                         # 写入正文
    print('正在下载：' + title)
print(book_name +'下载完成,一共有'+ str(len(unit_url)) +'章')

