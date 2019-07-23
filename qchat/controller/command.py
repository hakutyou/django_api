from qchat.models import CoolqReply
from . import wuxia


def userinfo(post, self_id):
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
    cr = CoolqReply.objects.filter(pattern=pattern, group_id=group_id, status=True).first()
    if cr:
        if (int(cr.create_qq) != int(user_id)) and (role == 'member'):
            return f'只能由创建者[CQ:at,qq={cr.create_qq}]或者管理员删除'
        cr.status = False
        cr.save()
        return f'成功: {pattern}'
    return None


def learn(post, _, args):
    user_id = post.get('user_id')
    group_id = post.get('group_id')
    pattern = args[0]
    reply = args[1]
    if CoolqReply.objects.filter(pattern=pattern, group_id=group_id, status=True):
        return f'失败 {pattern} 已使用'
    CoolqReply.objects.create(pattern=pattern, reply=reply, create_qq=user_id, group_id=group_id)
    return f'成功: {pattern}, {reply}'


COMMAND_LIST = {
    '0': {
        'userinfo': userinfo,
    },
    '1': {
        'forget': forget,
    },
    '2': {
        'role': role,
        'learn': learn,
    }
}
