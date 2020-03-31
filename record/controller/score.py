import datetime

from rest_framework.decorators import permission_classes, api_view

from api.exception import ClientError
from api.shortcuts import Response, request_check
from permission import permission
from record.controller.supermemo import supermemo_2
from record.models import DictKanjiItem, DictScore
from utils.xtime import to_date, now


@api_view(['POST'])
@permission_classes((permission.LoginPermission,))
def score_get(request):
    dict_kanji = DictKanjiItem.objects.exclude(score__account=request.user).select_related('kana').first()
    if not dict_kanji:
        raise ClientError('没有新的项目', code=100)
    data = {
        'kanji_id': dict_kanji.id,
        'kana': dict_kanji.kana.kana,
        'kanji': dict_kanji.kanji,
        'imi': dict_kanji.imi,
        'hinnsi': dict_kanji.hinnsi,
        'rei': dict_kanji.rei,
    }
    return Response(request, 0, data=data)


@api_view(['POST'])
@permission_classes((permission.LoginPermission,))
@request_check(
    kanji_id=(int, True),
    score=(int, True),  # 0-5
)
def score_set(request):
    dict_kanji = DictKanjiItem.objects.get(id=request.post.get('kanji_id'))
    try:
        dict_score = dict_kanji.score.get(account=request.user)
    except DictScore.DoesNotExist:
        dict_score = DictScore.objects.create(
            next_date=to_date(now()),
            score=0,
            account=request.user,
            kanji=dict_kanji,
        )
    # 更新分数
    score = str(int(dict_score.score) * 6 + int(request.post.get('score')))
    dict_score.score = score
    dict_score.next_date = to_date(now() + datetime.timedelta(days=supermemo_2(score)))
    dict_score.save(update_fields=('score', 'next_date'))
    data = {
        'id': dict_score.id,
        'score': dict_score.score,
        'next_date': str(dict_score.next_date),
    }
    return Response(request, 0, data=data)


@api_view(['POST'])
@permission_classes((permission.LoginPermission,))
def score_review(request):
    today = to_date(now())
    dict_score = DictScore.objects.filter(account=request.user, next_date=today).select_related('kanji',
                                                                                                'kanji__kana').first()
    if not dict_score:
        raise ClientError('没有新的项目', code=100)
    data = {
        'id': dict_score.id,
        'kanji_id': dict_score.kanji.id,
        'kana': dict_score.kanji.kana.kana,
        'kanji': dict_score.kanji.kanji,
        'imi': dict_score.kanji.imi,
        'hinnsi': dict_score.kanji.hinnsi,
        'rei': dict_score.kanji.rei,
    }
    return Response(request, 0, data=data)
