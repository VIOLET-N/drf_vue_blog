from django.contrib.auth.models import User

from rest_framework import serializers


class UserDescSerializers(serializers.ModelSerializer):
    """于文章列表中引用的嵌套化序列器"""
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'last_login',
            'date_joined',
        ]
