#真实视频链接
#https://aweme.snssdk.com/aweme/v1/playwm/?video_id=

import requests
import re

def getID(text):
    pattern = r'/(\d+)'
    match = re.search(pattern, text)
    
    if match:
        return match.group(1)
    else:
        return ""

def openPage(url,ar=True):
    try:
        headers = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36',
        }
        response = requests.get(url,headers=headers,allow_redirects=ar)
        return response
    except requests.exceptions.RequestException as e:
        # 处理请求异常
        print(f"请求发生异常: {e}")
        return None

def getVideoUrl(url):
    id = getID(openPage(url,False).text)
    id = openPage(f"https://www.douyin.com/web/api/v2/aweme/iteminfo/?reflow_source=reflow_page&item_ids={id}&a_bogus=666666666").json()['item_list'][0]["video"]["play_addr"]["uri"]
    print(id)
    return f"https://aweme.snssdk.com/aweme/v1/play/?video_id={id}"
    
def download(url,name):
    response = openPage(url)
    with open(name,"wb") as f:
        f.write(response.content)

def getVideo(url):
    download(getVideoUrl(url),f"{url.rstrip('/').split('/')[-1]}.mp4")

if __name__ == "__main__":
    while True:
        Url = input("请输入抖音链接：")
        getVideo(Url)
    