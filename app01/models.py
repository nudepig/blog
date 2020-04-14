from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

class UserInfo(AbstractUser):
    """
    用户信息表
    """
    #nid = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=11, null=True, unique=True)
    avatar = models.FileField(upload_to="media/avatars/", default="media/avatars/default.png", verbose_name="头像")
    #create_time = models.DateTimeField()
    anhao = models.CharField(max_length=60, null=True, unique=False)
    #blog = models.OneToOneField(to="Blog", to_field="nid", null=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

class UserToken(models.Model):
    user = models.OneToOneField(to="UserInfo", on_delete=models.CASCADE)
    token = models.CharField(max_length=64, null=True)

class Room(models.Model):
    """
    会议室表
    """
    caption = models.CharField(max_length=32)
    num = models.IntegerField()  # 容纳人数
    def __str__(self):
        return self.caption


class Book(models.Model):
    """
    会议室预定信息

    """
    user = models.ForeignKey('UserInfo', on_delete=models.CASCADE)
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    date = models.DateField()
    time_choices = (
        (1, '8:00'),
        (2, '9:00'),
        (3, '10:00'),
        (4, '11:00'),
        (5, '12:00'),
        (6, '13:00'),
        (7, '14:00'),
        (8, '15:00'),
        (9, '16:00'),
        (10, '17:00'),
        (11, '18:00'),
        (12, '19:00'),
        (13, '20:00'),
    )


    time_id = models.IntegerField(choices=time_choices)

    class Meta:
        unique_together = (
            ('room','date','time_id'),
        )


    def __str__(self):
        return str(self.user)+"预定了"+str(self.room)
