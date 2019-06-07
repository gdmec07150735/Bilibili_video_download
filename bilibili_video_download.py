'''
详情页api
https://api.bilibili.com/x/web-interface/view?aid=40629179

视频简介详情api
https://api.bilibili.com/x/web-interface/archive/stat?aid=40629179

视频地址api
https://api.bilibili.com/x/player/playurl?aid=40629179&cid=71348096&qn=0


获取av号，或者是链接提取额av号
通过下面链接获取cid
https://api.bilibili.com/x/web-interface/view?aid={}

再通过下面链接获取视频下载地址
https://api.bilibili.com/x/player/playurl?cid={}&avid={}&qn=0

'''
import requests,re

def download_html(url, header=None,num_retires=2):
    print("connect to {}".format(url))
    ret = None
    response = requests.get(url, headers=header)
    try:
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        ret = response.json()
    except requests.exceptions.HTTPError as e:
        print('error: {}'.format(e))
        if num_retires > 0 :
            if 500 <= response.status_code < 600:
                html = download(url, num_retires-1)
    except Exception as e:
        print(" unknown error : {}" . format(e))
    return ret

def get_base_info( data ):
    cid = 0
    title = ''
    if not data:
        print('download_html function failed to return data')
        exit()
    try:
        cid = data['data']['cid'] #主cid，还可以在data、pages获取多页的cid
        title = data['data']['title']
    except Exception as e:
        print('failed to get cid')
        exit()
    return cid,title

def get_video_attribute( data, attribute):
    ret = ''
    if not data:
        print('failed to return data')
        exit()
    try:
        ret = data['data']['durl'][0][attribute]
        if attribute == 'url':
            ret = ret.replace('&platform=pc', '')
        #需要将这个参数去掉才可以访问
    except Exception as e:
        print('failed to get video_path')
        exit()
    return ret

def init():
    while True:
        print("请输入av号或者是链接地址".center(50, '*'))
        try:
            s = input('请输入要下载的B站av号或者视频链接地址:')
            av_id = re.search(r'av(\d+)', s).group(0)[2:]
            return av_id
        except AttributeError as e:
            print('请输入正确的参数')

def download_video( path, file_name, file_size):
    with open('{}.flv'.format(file_name), 'wb') as f:
        try:
            r = requests.get(path, stream=True)
            r.raise_for_status()
            print('视频大小为{}个字节，开始下载'.format(file_size))
            for i, chunk in enumerate(r.iter_content(1024)):
                f.write(chunk)
                process_bar( (i+1)*1024, file_size)
        except Exception as e:
            print('error : {}'.format(e))


def process_bar(current, all):
    length = 100
    scale = all / length
    a = int(current/scale) *'*'
    b = '.' * (int(all/scale) - int(current/scale))
    c = ( (current/scale) / (all/scale) )*100
    print("\r{:<3.0f}%[{}->{}]".format(c,a,b), end="")

def main():
    av_id = init()
    header = {
        'User-Agent':'Mozilla/5.0',
        'Host':'api.bilibili.com'
    }
    av_description_json = download_html('https://api.bilibili.com/x/web-interface/view?aid={}'.format(av_id),header)
    cid, title = get_base_info(av_description_json)

    av_video_json = download_html('https://api.bilibili.com/x/player/playurl?cid={}&avid={}&qn=0'.format(cid, av_id))
    video_path = get_video_attribute( av_video_json, 'url')
    video_size = get_video_attribute( av_video_json, 'size')
    download_video( video_path, title, video_size)

if __name__ == "__main__":
    main()
