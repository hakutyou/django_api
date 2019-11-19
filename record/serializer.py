from rest_framework import serializers

from .models import DictKanaItem, DictKanjiItem


class DictKanjiItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = DictKanjiItem
        fields = ('id', 'kanji', 'score', 'hinnsi', 'rei',)


class DictKanaItemSerializer(serializers.ModelSerializer):
    kanji = DictKanjiItemSerializer(many=True)

    class Meta:
        model = DictKanaItem
        fields = ('id', 'kana', 'kanji',)
