import os

import ffmpeg
from django.conf import settings
from django.core import mail

from api.service import app
from external.service import bilibili_api
from utils.celery import celery_catch


@app.task(bind=True)
@celery_catch
def celery_send_mail(self, subject, message, receive):
    mail.send_mail(subject, message,
                   settings.EMAIL_HOST_USER, receive)


@app.task(bind=True)
@celery_catch
def celery_download_video(self, referer: str, video_list: list,
                          filename: str = 'tmp',
                          codename: str = 'tmp', overwrite=False) -> str:
    command = ''
    video_file_list = bilibili_api.down_video(referer, video_list,
                                              filename=f'tmp/{codename}')
    for video_file in video_file_list:
        command += f'{video_file}|'
    if not command:
        return ''
    # 合并文件生成 .mp4
    command = 'concat:' + command[:-1]
    output_name = f'tmp/{filename}.mp4'
    # 已经存在就不再生成了
    if not os.path.exists(output_name) or overwrite:
        ffmpeg.input(command).output(output_name).run()
    # TODO: [上传]合并后的文件
    # TODO: 删除本地所有文件
    for video_file in video_file_list:
        if os.path.exists(video_file):
            os.remove(video_file)
    # if os.path.exists(output_name):
    #     os.remove(output_name)
    # 输出文件名, TODO: 需要改成 url
    return output_name
