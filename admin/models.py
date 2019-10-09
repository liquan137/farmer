from django.db import models


# Create your models here.
class p_admin(models.Model):
    username = models.CharField(max_length=30, help_text="关联的普通用户")
    user = models.CharField(max_length=30, help_text="管理员账号", default='')
    password = models.CharField(max_length=30, help_text="管理员密码")
    auth = models.IntegerField(help_text="管理员权限 1：超级管理员 2：子管理员", default=2)
