from rest_framework.decorators import permission_classes, api_view

from api.exception import ServiceError
from api.shortcuts import request_check, Response
from external.celery.tasks import celery_download_video
from external.interface import bilibili_api
from permission import permission
from utils.celery import celery_check, append_celery


@api_view(['POST'])
@permission_classes((permission.LoginPermission,))
@request_check(
    av=(int, False),
    bv=(str, False),
)
def get_video_info(request):
    """
    获得视频信息
    """
    av = request.post.get('av')
    bv = request.post.get('bv')
    if not av and not bv:
        raise ServiceError('Argument Error', code=400)

    response = bilibili_api.get_video_info(bv, av)
    return Response(request, 0, data=response.get('data'))


@api_view(['POST'])
@permission_classes((permission.LoginPermission,))
@request_check(
    av=(int, False),
    bv=(str, False),
    quality=(int, False),
)
def get_video(request):
    """
    下载视频（异步）
    """
    av = request.post.get('av')
    bv = request.post.get('bv')
    # 视频品质, 80 表示 1080P
    quality = request.post.get('quality', 80)
    if not av and not bv:
        raise ServiceError('Argument Error', code=400)

    response = bilibili_api.get_video_info(bv, av)
    data = response.get('data')
    bvid = data.get('bvid')
    title = data.get('title').replace(' ', '-')
    desc = response.get('desc')  # 简介
    pic = response.get('pic')  # 封面
    referer = response.get('Referer')

    ic_list = []
    for item in data['pages']:
        cid = str(item['cid'])
        page = str(item['page'])
        part_title = item['part']  # 分 P 的标题
        video_list = []
        for d_url in bilibili_api.get_play_list(referer, cid, quality)['durl']:
            video_list.append(d_url['url'])
        # 加入 celery 队列
        ic = append_celery('download', celery_download_video, referer, video_list,
                           filename=f'{title}_{part_title}',
                           codename=f'{bvid}_{page}')
        ic_list.append(ic)
    # 返回 celery 队列中的 ID
    return Response(request, 0, data={
        'title': title,
        'desc': desc,
        'pic': pic,
        'ic_list': ic_list,
    })


@api_view(['POST'])
@permission_classes((permission.LoginPermission,))
@request_check(
    ic=(str, True),
)
def get_video_check(request):
    """
    获取异步下载的视频
    """
    ic = request.post.get('ic')
    state, result = celery_check(ic)
    if state < 0:
        return Response(request, 1, msg='failed')
    if state != 2:
        return Response(request, 2, msg='loading')
    return Response(request, 0, data=result)
