import base64
import json
import re

import requests

from .controller import command
from .models import CoolqReply

admin_qq = [
    2295122015,
]

blacklist_qq = [
]

whitelist_group = [
    737855501,  # 百香果双响炮
    164730098,  # 测试
    798333509,  # 朝花夕拾
]

receive_group = [
    205375321,  # 天刀体服航海玩家群
]

title_group = {
}
default_title = 'Main'  # 默认的主模式

headers = {'Authorization': 'Bearer Lihu4hA49kUtYou'}


def Response(reply=None, auto_escape=False, at_sender=False):
    response = {"block": True}
    if reply:
        response['reply'] = reply
        response['auto_escape'] = auto_escape
        response['at_sender'] = at_sender
    return response


# 总入口
def qchat(request):
    post_type_map = {
        'message': qchat_message,
        'notice': qchat_notice,
        'request': qchat_request,
    }
    # self_id = request.META.get('X-SELF-ID')
    post = json.loads(request.body)
    self_id = post.get('self_id')
    post_type = post.get('post_type')
    return post_type_map[post_type](post, self_id)


# 0 消息
def qchat_message(post, self_id):
    message_type_map = {
        'group': qchat_group,  # 群消息
        'private': qchat_private,  # 私聊消息
        'discuss': qchat_discuss,  # 讨论组消息
    }
    message_type = post.get('message_type')
    return message_type_map[message_type](post, self_id)


# 0.0 群消息
def qchat_group(post, self_id):
    sub_type_map = {
        'normal': qchat_gnormal,  # 正常群消息
        'anonymous': qchat_ganonymous,
        'notice': qchat_gnotice,
    }
    sub_type = post.get('sub_type')

    message = post.get('message')  # 消息内容
    group_id = post.get('group_id')  # 群号

    if self_id == 3468460294:  # sirat
        if group_id == 792626419:  # Secret base
            # 万里弦歌
            requests.get(f'https://sirat.emilia.fun/send_group_msg?group_id=188283809&message={message}',
                         headers=headers)
            # 朝花夕拾
            requests.get(f'https://sirat.emilia.fun/send_group_msg?group_id=798333509&message={message}',
                         headers=headers)
        return Response()

    if (sub_type == 'normal') and (group_id in receive_group):
        notice_checkout = re.match(r'^\[CQ:rich.*$', message)
        if notice_checkout:
            notice = re.match(r'^.*title":"(?P<title>.+?)".*text":"(?P<text>.+?)".*$', message)  # 群公告
            title = base64.b64decode(notice.group('title')).decode('utf-8')
            text = base64.b64decode(notice.group('text')).decode('utf-8')
            if title != '群公告':
                text = title + '\n' + text
            # 测试
            requests.get(f'https://coolq.emilia.fun/send_group_msg?group_id=164730098&message={text}', headers=headers)
            # Secret base
            requests.get(f'https://coolq.emilia.fun/send_group_msg?group_id=792626419&message={text}', headers=headers)
            # 百香果双响炮
            requests.get(f'https://coolq.emilia.fun/send_group_msg?group_id=737855501&message={text}', headers=headers)
        return Response()

    # 无视的群
    if group_id not in whitelist_group:
        return Response()

    # 正常发言的群
    return sub_type_map[sub_type](post, self_id)


# 0.1 私聊消息
def qchat_private(post, self_id):
    sub_type = post.get('sub_type')  # 消息子类型 (friend, group, discuss)
    user_id = post.get('user_id')  # 发送者 QQ 号
    message = post.get('message')  # 消息内容
    _sender = post.get('sender')  # 发送人信息
    nickname = _sender.get('nickname')
    sex = _sender.get('sex')
    age = _sender.get('age')

    if message == '/userinfo':
        reply = '----用户信息----\n'
        for i in ['user_id', 'nickname', 'sex', 'age']:
            reply += f'{i}: {locals()[i]}\n'
        return Response(reply=reply)

    if user_id in admin_qq:  # 管理员功能
        return Response(reply=message)
    return Response()


# 0.0.0 普通群消息
def qchat_gnormal(post, self_id):  # 群消息
    user_id = post.get('user_id')  # QQ 号
    message = post.get('message')  # 消息内容
    group_id = post.get('group_id')  # 群号

    if user_id in admin_qq:
        pass

    if message[0] == '/':
        m = re.match('^/(?P<command>[a-z]+?)(?:(?P<flag>[^a-z])(?P<args>.+?))?$', message)
        if m:
            _command = m.group('command')
            _flag = m.group('flag')
            if m.group('args'):
                _args = [i for i in m.group('args').split(_flag) if i != '']
            else:
                _args = []
            argc = len(_args)
            if _command in command.COMMAND_LIST[str(argc)]:
                return Response(command.COMMAND_LIST[str(argc)][_command](post, self_id, _args))
        return Response()

    title = title_group.get(str(group_id), default_title)
    try_no_regex = CoolqReply.objects.filter(
        pattern=message, group_id=group_id,
        regex=False, status=True, from_title=title).first()
    if try_no_regex:
        title_group[str(group_id)] = try_no_regex.to_title
        return Response(reply=try_no_regex.reply)
    if message[0] == '#':
        title_group[str(group_id)] = 'Main'
        return Response(reply=message[1:])
    return Response()


# 0.0.1 群匿名消息
def qchat_ganonymous(post, self_id):
    # _anonymous = post.get('anonymous')  # id, name, flag
    return Response()


# 0.0.2 群系统消息
def qchat_gnotice(post, self_id):
    return Response()


# 0.2 讨论组消息
def qchat_discuss(post, self_id):
    return Response()


# 0.1.1 群、讨论组变动等通知类事件
def qchat_notice(post, self_id):
    return Response()


# 0.1.2 加好友请求、加群请求／邀请
def qchat_request(post, self_id):
    return Response()
