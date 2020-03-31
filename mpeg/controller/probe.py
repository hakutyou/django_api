import ffmpeg

from api.exception import ClientError
from api.shortcuts import Response, request_check


@request_check(
    url=(str, True),
)
def show_format(request):
    """
    查看多媒体的封装格式
    nb_stream       包含的流的个数 (show_streams)
    nb_programs     节目数
    format_name     使用的封装模块的名称
    format_long_name
    start_time      媒体文件的起始时间
    duration        媒体文件的总时间长度
    size            媒体文件的大小
    bit_rate        媒体文件的码率
    """
    try:
        data = ffmpeg.probe(request.post.get('url'), show_format=None).get('format')
    except ffmpeg.Error:
        raise ClientError('多媒体文件错误')
    return Response(request, 0, data=data)


@request_check(
    url=(str, True),
)
def show_streams(request):
    """
    查看多媒体文件的流信息（list）
    index           序号
    codec_name      编码名
    codec_long_name
    profile
    level
    width           视频画面大小
    height          视频画面大小
    has_b_frame
    r_frame_rate    能够准确表示所有时间戳的最低帧速率, 整个视频帧率的最小公倍数
    例如 第一秒为 2帧/秒 第三秒为 3帧/秒, 该值为 6（6帧/秒 才可以表示所有帧的时间戳）
    avg_frame_rate  平均帧率(帧/s)
    bit_rate        码率(bps)
    codec_type      video/audio/subtitle
    time_base       时间戳计算基础单位
    duration_ts     duration_ts * time_base = duration  视频时间长度
    codec_time_base 编码的时间戳计算基础单位
    """
    try:
        data = ffmpeg.probe(request.post.get('url'), show_streams=None).get('streams')
    except ffmpeg.Error:
        raise ClientError('多媒体文件错误')
    return Response(request, 0, data=data)


if __name__ == '__main__':
    # data = ffmpeg.probe('/mnt/c/Users/hakutyou/Videos/output.mp4', show_format=None).get('format')
    # http://ting6.yymp3.net:86/new27/zhuangxinyan16/1.mp3
    dd = ffmpeg.probe('/mnt/c/Users/hakutyou/Videos/output.mp4', show_streams=None).get('streams')
    print(dd)
    # a = ffmpeg.probe('/mnt/c/Users/hakutyou/Videos/output.mp4', show_packets=None).get('packets')
    # # packets = 17362
    b = ffmpeg.probe('/mnt/c/Users/hakutyou/Videos/output.mp4', show_frames=None, select_streams='v').get('frames')
    # print(len(a))
    c = 0
    for item in b:
        print(item['pict_type'], end='')
        c += 1
        if c % 100 == 0:
            print('')
