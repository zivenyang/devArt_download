# coding:utf-8

from __future__ import absolute_import, division, print_function
import urllib.request
import re
import os


class Spider:

    def __init__(self):
        self.siteURL = 'http://disi.unitn.it/~sartori/datasets/deviantart-dataset/'
        self.save_dir = 'save/'
        self.save_error = 'save/_____error_url.txt'
        self.error_url = []

    def getPage(self, url):
        request = urllib.request.Request(url)
        try:
            response = urllib.request.urlopen(request)
            return response.read().decode('ISO-8859-1')
        except urllib.request.URLError as e:
            self.error_url.append(str(url))
            print(e, u'发现无法打开的链接：', self.error_url[-1])

    def getImgUrl(self):
        page = self.getPage(url=self.siteURL)
        pattern = re.compile('<td width="657" valign="top"><font size="2"><a href="(.*?)">.*?</a></font></td>', re.S)
        items = re.findall(pattern, page)
        contents = []
        for item in items:
            contents.append(item)
        return contents

    def getImg(self):
        img_list = self.getImgUrl()
        idx = 1
        for img_url in img_list:
            page = self.getPage(url=img_url)
            pattern = re.compile('<meta name="twitter:image" content="(.*?)">', re.S)
            try:
                items = re.findall(pattern, page)
                print(items[0])
                file_name = self.save_dir + str(items[0].split('/')[-1])
                if os.path.exists(file_name):
                    print('第%d张图片%s已存在' % (idx, file_name))
                    pass
                else:
                    self.saveImg(imageURL=items[0], fileName=file_name)
                    print(u'第%d张图片%s已保存' % (idx, file_name))
                idx += 1
            except:
                pass
        f = open(self.save_error, 'w')
        for error_url in self.error_url:
            f.write(error_url)
            f.write('\n')
        f.close()
        print(u'已将错误链接保存至 %s' % self.save_error)

    def saveImg(self, imageURL, fileName):
        u = urllib.request.urlopen(imageURL)
        data = u.read()
        f = open(fileName, 'wb')
        f.write(data)
        f.close()


if __name__ == '__main__':
    Spider().getImg()
