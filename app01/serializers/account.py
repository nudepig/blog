from app01 import models

from rest_framework import serializers

class CourseSerializer(serializers.ModelSerializer):
    """
    课程序列化
    """
    level = serializers.CharField(source='get_level_display')
    class Meta:
        model = models.UserInfo
        fields = ['id','username','phone','avatar','anhao']


