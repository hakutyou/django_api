import os
from typing import Union

from external.service.base import BaseService
from utils import message_digest


class BilibiliService(BaseService):
    base_url = ''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/55.0.2883.87 Safari/537.36'
    }

    def get_video_info(self, bv: str = '', av: str = '') -> list:
        interface = 'https://api.bilibili.com/x/web-interface/view'
        if bv:
            interface += f'?bvid={bv}'
        else:
            interface += f'?aid={av}'
        return self.get(interface)

    def get_play_list(self, referer, cid, quality) -> list:
        """
        quality 可能取 80(1080P), 64(720P), 32(480P), 16(360P)
        """
        interface = 'https://interface.bilibili.com/v2/playurl'
        appkey = 'iVGUTjsxvpLeuDCf'
        sec = 'aHRmhWMLkdeMuILqORnYZocwMBpMEOdt'
        params = 'appkey=%s&cid=%s&otype=json&qn=%s&quality=%s&type=' % (appkey, cid, quality, quality)
        chksum = message_digest(params + sec, method='md5')
        return self.get(f'{interface}?{params}&sign={chksum}', headers={
            'Referer': referer
        })

    def down_video(self, referer: str, video_list: list, filename: str = 'tmp') -> list:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:56.0) Gecko/20100101 Firefox/56.0',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Range': 'bytes=0-',  # Range 的值要为 bytes=0- 才能下载完整视频
            'Referer': referer,  # 注意修改referer,必须要加的!
            'Origin': 'https://www.bilibili.com',
            'Connection': 'keep-alive',
        }
        filename_list = []
        for c, video_url in enumerate(video_list):
            filename_c = f'{filename}_{c}'
            # 已经存在就不再生成了
            if not os.path.exists(filename_c):
                with open(filename_c, 'wb') as fd:
                    self.download(video_url, fd, headers)
            filename_list.append(filename_c)
        return filename_list

    def get(self, interface: str, data: Union[dict, list] = None, headers=None) -> list:
        if headers:
            headers = dict(self.headers, **headers)
        else:
            headers = self.headers
        result = super(BilibiliService, self).get(interface, data, headers).json()
        result['Referer'] = self.base_url + interface
        return result
