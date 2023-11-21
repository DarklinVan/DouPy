import requests
import re,os

def get_file_extension(url):
   filename, file_extension = os.path.splitext(url)
   return file_extension.split("?")[0].split("&")[0].split("=")[0]

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

def getObjUrl(url):
    uuid = getID(openPage(url,False).text)
    item = openPage(f"https://www.douyin.com/web/api/v2/aweme/iteminfo/?reflow_source=reflow_page&item_ids={uuid}&a_bogus=666666666").json()['item_list'][0]
    groups = item["images"]
    id = []
    if len(groups)==0:
        id = item["video"]["play_addr"]["uri"]
        urls = [f"https://aweme.snssdk.com/aweme/v1/play/?video_id={id}"]
    else:
        for i in groups:
           id.append(i["url_list"][3])
        urls = id
    return urls
    
def download(urls,name):
    
    for url in urls:
        i = urls.index(url)
        response = openPage(url)
        with open(f"{name}_{i+1}{get_file_extension(response.url)}","wb") as f:
            f.write(response.content)

def getObj(url):
    download(getObjUrl(url),f"{url.rstrip('/').split('/')[-1]}")

if __name__ == "__main__":
    while True:
        Url = input("请输入抖音链接：")
        getObj(Url)    