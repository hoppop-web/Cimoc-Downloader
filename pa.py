import requests
import re 
from tqdm import tqdm
import topdf
import os

def download_comic(url):
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'
    }

    r = requests.get(url, headers=headers)
    html = r.text

    result = re.findall(r'<a href="https://e-hentai\.org/s/(.*?)">', html)
    url_images = []
    for page in result:
        page_url = f'https://e-hentai.org/s/{page}'
        r2 = requests.get(page_url, headers=headers)
        r2_text = r2.text

        image_url = re.findall(r'<img id="img" src="(.*?)" style=".*?" onerror=".*?">', r2_text,re.S)[0]
        if image_url:
            image_url = image_url[0]
        else:
            print('未能找到图片 URL，请检查正则表达式是否正确')
        url_images.append(image_url)

    print(f'即将下载您的漫画，一共 {len(url_images)} 张')

    if not os.path.exists('image'):
        os.makedirs('image')

    for i, image_url in tqdm(enumerate(url_images), total=len(url_images)):
        r = requests.get(image_url)
        with open(f'image/{i+1}.jpg', 'wb') as f:
            f.write(r.content)
    topdf.combine2Pdf('image/', 'comic.pdf')
    
    try:
        r = requests.get(url, headers=headers)
    except requests.exceptions.ConnectionError:
        print('无法连接到网络，请检查你的网络连接')
    return
    # 判断错误


if __name__ == '__main__':
    url = input('输入对用漫画地址：')
    download_comic(url)
