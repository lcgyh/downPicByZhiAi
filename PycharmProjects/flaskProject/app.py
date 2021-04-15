from flask import Flask,request
import urllib.parse
import urllib.request
import ssl
from bs4 import BeautifulSoup


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'hello_world'

def urllib_download(inx,IMAGE_URL):
    print(IMAGE_URL)
    if IMAGE_URL.find('CategoryIMG') >= 0:
        urllib.request.urlretrieve(IMAGE_URL, 'E:\\myProject\\zhiaiDown\\image\\CategoryIMG\\' + str(inx) + '.jpg')
    elif IMAGE_URL.find('product') >= 0:
        urllib.request.urlretrieve(IMAGE_URL, 'E:\\myProject\\zhiaiDown\\image\\product\\' + str(inx) + '.jpg')
    elif IMAGE_URL.find('EditorFile') >= 0:
        urllib.request.urlretrieve(IMAGE_URL, 'E:\\myProject\\zhiaiDown\\image\\EditorFile\\' + str(inx) + '.jpg')
    else:
        urllib.request.urlretrieve(IMAGE_URL, 'E:\\myProject\\zhiaiDown\\image\\other\\' + str(inx) + '.jpg')





@app.route('/getPic', methods=['POST'])
def getPic():
    ssl._create_default_https_context = ssl._create_unverified_context
    url = request.json.get('url')
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
            "Cookie": "ASP.NET_SessionId=sklcfihk2azmgeiye3zkktjf; cookieId=A5D1D097BE;",
            "authority": 'www.babyzhiai.net'
        }
        newUrl = urllib.request.Request(url, headers=headers)
        html = urllib.request.urlopen(newUrl)
        html = html.read()
        soup = BeautifulSoup(html, "html.parser")
        images = soup.findAll('img')
        srcs = []
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
        for index, item in enumerate(list(set(srcs))):
            urllib_download(index, item)
    except Exception as err:
        print(err)

    return "success"


if __name__ == '__main__':
    app.run(debug=True)


