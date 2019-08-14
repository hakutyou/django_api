from rest_framework import serializers

from .models import RecordItem


class RecordItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecordItem
        fields = '__all__'
