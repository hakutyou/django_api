import re

from external.package import baidu
from qchat import qchat
from qchat.models import CoolqReply, CoolqSubject
from utils.utils import list_get
from . import wuxia


def userinfo(post, self_id, _):
    user_id = post.get('user_id')  # QQ 号
    message = post.get('message')  # 消息内容
    group_id = post.get('group_id')  # 群号
    _sender = post.get('sender')  # 发送人信息
    nickname = _sender.get('nickname')
    card = _sender.get('card')
    sex = _sender.get('sex')
    age = _sender.get('age')
    area = _sender.get('area')
    level = _sender.get('level')
    role = _sender.get('role')
    title = _sender.get('title')
    reply = ''
    for i in ['user_id', 'nickname', 'card', 'sex', 'age', 'area', 'level', 'role', 'title']:
        reply += f'{i}: {locals()[i]}\n'
    return reply


def state(post, _, _1):
    group_id = post.get('group_id')
    from_title = qchat.title_group.get(str(group_id), qchat.default_title)
    if from_title:
        return f'当前状态: {from_title}'
    return None


def role(_, self_id, args):
    # m = re.match('^/role(?P<flag>.)(?P<qq_number>[0-9]+)(?P=flag)(?P<zone>.+)', message)
    try:
        qq_number = int(args[0])
        zone = args[1]
    except ValueError:
        return None
    return wuxia.get_wuxia_role(qq_number, zone, self_id)


def forget(post, _, args):
    user_id = post.get('user_id')
    group_id = post.get('group_id')
    pattern = args[0]
    from_title = qchat.title_group.get(str(group_id), qchat.default_title)

    coolq_subject = CoolqSubject.objects.filter(subject=from_title).first()
    if not coolq_subject:
        return None

    cr = CoolqReply.objects.filter(pattern=pattern, group_id=group_id, status=True)
    cr = cr.filter(from_title=coolq_subject).first() or \
         cr.filter(from_title=None).first()

    if cr:
        if (int(cr.create_qq) != int(user_id)) and (role == 'member'):
            return f'只能由创建者[CQ:at,qq={cr.create_qq}]或者管理员删除'
        cr.delete()  # 真实删除
        ret = f'成功: {pattern}'
        if from_title is not None:
            ret += f'({from_title})'
        return ret
    return None


def learn(post, _, args):
    command = post.get('command')
    user_id = post.get('user_id')
    group_id = post.get('group_id')
    pattern = args[0]
    reply = args[1]

    if command == 'learn*':
        coolq_subject = None
    else:
        from_title = qchat.title_group.get(str(group_id), qchat.default_title)
        coolq_subject = CoolqSubject.objects.filter(subject=from_title).first() or \
                        CoolqSubject.objects.create(subject=from_title)

    to_title = list_get(args, 2, qchat.default_title)
    coolq_to_subject = CoolqSubject.objects.filter(subject=to_title).first() or \
                       CoolqSubject.objects.create(subject=to_title)

    if CoolqReply.objects.filter(pattern=pattern, group_id=group_id, status=True,
                                 from_title=coolq_subject):
        return f'失败 {pattern} 已使用'

    CoolqReply.objects.create(pattern=pattern, reply=reply, create_qq=user_id, group_id=group_id,
                              from_title=coolq_subject, to_title=coolq_to_subject)
    ret = f'成功: {pattern}, {reply}'
    if to_title is not None:
        ret += f'({to_title})'
    return ret


def image(_, _1, args):
    picture_url = args[0]
    m = re.match(r'^\[CQ:image,file=(?P<file>.+),url=(?P<url>.+)\]$', picture_url)
    if not m:
        return None
    url = m.group('url')
    result = baidu.image_detect(url)
    try:
        result = result['result']
    except KeyError:
        return '图片格式错误'
    ret = ''
    count = 0
    for i in result:
        ret += f'猜测结果: {i["keyword"]}({i["root"]}), 确信度: {i["score"]:.2f}\n'
        count += 1
        if count >= 2:
            break
    return ret


def ocr(_, _1, args):
    picture_url = args[0]
    m = re.match(r'^\[CQ:image,file=(?P<file>.+),url=(?P<url>.+)\]$', picture_url)
    url = m.group('url')
    try:
        lang = args[1]
    except KeyError:
        lang = 'CHN_ENG'
    result = baidu.ocr_basic(url, lang)
    try:
        result = result['words_result']
    except KeyError:
        return '图片格式错误'
    ret = ''
    for i in result:
        ret += f'{i["keyword"]}({i["root"]})\n'
    return ret


COMMAND_LIST = {
    '0': {
        'userinfo': userinfo,
        'state': state,
    },
    '1': {
        'forget': forget,
        'image': image,
        'ocr': ocr,
    },
    '2': {
        'role': role,
        'learn': learn,
        'learn*': learn,
        'ocr': ocr,
    },
    '3': {
        'learn': learn,
        'learn*': learn,
    },
}
