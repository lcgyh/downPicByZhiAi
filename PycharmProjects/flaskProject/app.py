from flask import Flask,request,jsonify
import urllib.parse
import urllib.request
import ssl
from bs4 import BeautifulSoup


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'hello_world'

def urllib_download_zhiai(inx,IMAGE_URL):
    print(IMAGE_URL)
    if IMAGE_URL.find('CategoryIMG') >= 0:
        urllib.request.urlretrieve(IMAGE_URL, 'D:\\myProject\\zhiaiDown\\image\\CategoryIMG\\' + str(inx) + '.jpg')
    elif IMAGE_URL.find('product') >= 0:
        urllib.request.urlretrieve(IMAGE_URL, 'D:\\myProject\\zhiaiDown\\image\\product\\' + str(inx) + '.jpg')
    elif IMAGE_URL.find('EditorFile') >= 0:
        urllib.request.urlretrieve(IMAGE_URL, 'D:\\myProject\\zhiaiDown\\image\\EditorFile\\' + str(inx) + '.jpg')
    else:
        urllib.request.urlretrieve(IMAGE_URL, 'D:\\myProject\\zhiaiDown\\image\\other\\' + str(inx) + '.jpg')


def urllib_download_Tb(inx,IMAGE_URL,type):
    print(IMAGE_URL)
    if type == 1:
        urllib.request.urlretrieve(IMAGE_URL, 'D:\\myProject\\taobao\\spuPic\\' + str(inx) + '.jpg')
    if type == 2:
        urllib.request.urlretrieve(IMAGE_URL, 'D:\\myProject\\taobao\\info\\' + str(inx) + '.jpg')


def urllib_download_Tb_attr(inx,IMAGE_URL):
    print(IMAGE_URL)
    urllib.request.urlretrieve(IMAGE_URL, 'D:\\myProject\\taobao\\skuPic\\' + str(inx) + '.jpg')



@app.route('/tool/api/getPic', methods=['POST'])
def getPic():
    ssl._create_default_https_context = ssl._create_unverified_context
    url = request.json.get('url')
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
            "Cookie": "ASP.NET_SessionId=lsqhwuvelg5frdeaglyyytjj; cookieId=D273FACA07;",
            "authority": 'www.babyzhiai.net'
        }
        newUrl = urllib.request.Request(url, headers=headers)
        html = urllib.request.urlopen(newUrl)
        html = html.read()
        soup = BeautifulSoup(html, "html.parser")
        images = soup.findAll('img')
        srcs = []
        print('images-',images)
        for image in images:
            if 'upload' in image['src']:
                if image['src'].find('_small_') >= 0:
                    index1 = image['src'].find('_small_')
                    index2 = image['src'].rfind('.')
                    strUrl = image['src'][0:index1] + image['src'][index2:]
                    if 'https://www.babyzhiai.net' not in strUrl:
                        srcs.append('https://www.babyzhiai.net' + strUrl)
                    else:
                        srcs.append(strUrl)
                else:
                    strUrl = image['src']
                    if 'https://www.babyzhiai.net' not in strUrl:
                        srcs.append('https://www.babyzhiai.net' + strUrl)
                    else:
                        srcs.append(strUrl)

        print(srcs)
        return jsonify({"info": srcs})
        # for index, item in enumerate(list(set(srcs))):
        #     urllib_download_zhiai(index, item)
    except Exception as err:
        print(err)

    return "success"



@app.route('/tool/api/getTbPic', methods=['POST'])
def getTbPic():
    ssl._create_default_https_context = ssl._create_unverified_context
    url = request.json.get('url')
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
            "Cookie": "ASP.NET_SessionId=lsqhwuvelg5frdeaglyyytjj; cookieId=D273FACA07;",
            "authority": 'www.babyzhiai.net'
        }
        newUrl = urllib.request.Request(url, headers=headers)
        html = urllib.request.urlopen(newUrl)
        html = html.read()
        soup = BeautifulSoup(html, "html.parser")
        images = soup.findAll('img')
        srcs1 = []
        srcs2 = []
        print('images-', images)
        for image in images:
            print('image-', image)
            if 'aria-label' in str(image):
                print('images-', 66666)
                print('images-', image['aria-label'])
                if  image['aria-label']=='商品主图':
                    strUrl1 = image['data-src']
                    print('images-ZHU', 122)
                    if 'https:' in strUrl1:
                        srcs1.append(strUrl1)
                    else:
                        srcs1.append('https:' + strUrl1)

                if image['aria-label'] == '商品详情图':
                    strUrl2 = image['data-ks-lazyload']
                    if 'https:' in strUrl2:
                        print('images-ZHU', 133)
                        srcs2.append(strUrl2)
                    else:
                        srcs2.append('https:' + strUrl2)


        print(srcs1)
        print(srcs2)
        # for index, item in enumerate(list(set(srcs1))):
        #     urllib_download_Tb(index, item, 1)
        # for index, item in enumerate(list(set(srcs2))):
        #     urllib_download_Tb(index, item, 2)
        return jsonify({"spuPic":srcs1,"info":srcs2})

    except Exception as err:
        print(err)

    return "success"




@app.route('/tool/api/getTbPicAttr', methods=['POST'])
def getTbPicAttr():
    ssl._create_default_https_context = ssl._create_unverified_context
    url = request.json.get('url')
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
            "Cookie": "ASP.NET_SessionId=lsqhwuvelg5frdeaglyyytjj; cookieId=D273FACA07;",
            "authority": 'www.babyzhiai.net'
        }
        newUrl = urllib.request.Request(url, headers=headers)
        html = urllib.request.urlopen(newUrl)
        html = html.read()
        soup = BeautifulSoup(html, "html.parser")
        images = soup.findAll('a')
        srcs = []
        print('images-', images)
        for image in images:
            if 'background' in str(image):
                attrStr=str(image['style'])
                print('attrStr-', attrStr)
                ind1 = attrStr.index('(')+1
                ind2 = attrStr.index(')')
                item = attrStr[ind1:ind2]
                if 'jpg' in item:
                    num = item.find('jpg') + 3
                    item1 = item[0:num]
                if 'png' in item:
                    num = item.find('png') + 3
                    item1 = item[0:num]
                if 'jpeg' in item:
                    num = item.find('png') + 4
                    item1 = item[0:num]
                if 'https:' in item1:
                    url = item1
                    srcs.append(url)
                else:
                    url = 'https:' + item1
                    srcs.append(url)

        print('srcs-', srcs)
        return jsonify({"skuPic": srcs})
        # for index, item in enumerate(list(set(srcs))):
        #     urllib_download_Tb_attr(index, item)


    except Exception as err:
        print(err)

    return "success"






if __name__ == '__main__':
    app.run(debug=True)


