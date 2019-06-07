# Bilibili_video_download
Bilibili_video_download-B站视频下载

## 开发环境
    Windows7 + python3 + requests

## 页面分析
    通过分析b站视频播放请求可以得到以下几个关键api：
    
    视频详情地址api https://api.bilibili.com/x/player/playurl?aid={}&cid={}&qn=0
    
    获取cid详情api  https://api.bilibili.com/x/web-interface/view?aid={}
    
    这样，思路很清晰了，首先通过av号获取到cid，再通过av号与cid来获取视频地址

## 测试
```python
python bilibli_video_download.py
```
效果如下：

![](https://github.com/gdmec07150735/Bilibili_video_download/blob/master/ret.jpg)

## 核心代码
```python
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
```

    
