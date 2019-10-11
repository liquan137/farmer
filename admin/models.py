from django.db import models


# Create your models here.
class p_admin(models.Model):
    username = models.CharField(max_length=30, help_text="关联的普通用户")
    user = models.CharField(max_length=30, help_text="管理员账号", default='')
    password = models.CharField(max_length=30, help_text="管理员密码")
    auth = models.IntegerField(help_text="管理员权限 1：超级管理员 2：子管理员", default=2)


class p_sys(models.Model):
    title = models.CharField(max_length=30, help_text="网站名称", default='农业信息网')
    dec = models.CharField(max_length=500, help_text="网站描述", default='网站的描述')
    keyword = models.CharField(max_length=30, help_text="网站关键词", default='农产品交易,农业信息,供应信息,求购信息')
    url = models.CharField(max_length=30, help_text="网站域名", default="")
    img_limit = models.IntegerField(help_text="用户上传总图片限制/每天", default=100)
    article_limit = models.IntegerField(help_text="用户发表文章限制/每天", default=10)
