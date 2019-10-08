from django.db import models


# Create your models here.
class p_message(models.Model):
    username = models.CharField(max_length=30, help_text="关联用户")
    m_title = models.CharField(max_length=50, help_text="信息标题", default="")
    m_pz = models.CharField(max_length=30, help_text="产品品种", default="")
    m_begin = models.CharField(max_length=30, help_text="上市开始日期时间", default="")
    m_end = models.CharField(max_length=30, help_text="上市结束日期时间", default="")
    m_size = models.CharField(max_length=30, help_text="报价规格", default="")
    m_today_price = models.CharField(max_length=30, help_text="今日价格", default="")
    m_today_date = models.CharField(max_length=30, help_text="上架日期", default="")
    m_photo = models.CharField(max_length=200, help_text="实拍图片，展示图片", default="")
    m_address_belong = models.CharField(max_length=200, help_text="所属地区代码", default="")
    m_address_detail = models.CharField(max_length=200, help_text="详细地址", default="")
    m_content = models.TextField(help_text="信息内容正文")
    create_time = models.CharField(max_length=30, help_text="创建时间", default="0")
    update_time = models.CharField(max_length=30, help_text="修改时间", default="0")


class p_menber(models.Model):
    username = models.CharField(max_length=30, help_text="关联用户")
    nickname = models.CharField(max_length=30, help_text="昵称", default="")
    type = models.CharField(max_length=10, help_text="1:代办（农产品经纪人）2：经销商 3：种养殖户 4：涉农企业 5：农业合作社", default="")
    company_name = models.CharField(max_length=80, help_text="公司名称", default="")
    password = models.CharField(max_length=90, help_text="密码")
    address_belong = models.CharField(max_length=80, help_text="所属地区代码", default="")
    address_detail = models.CharField(max_length=200, help_text="详细地址", default="")
    contact_person = models.CharField(max_length=200, help_text="联系人", default="")
    contact_phone = models.CharField(max_length=200, help_text="联系人手机号码", default="")
    contact_tel = models.CharField(max_length=200, help_text="联系人固定号码", default="")
    contact_email = models.CharField(max_length=200, help_text="联系人邮箱", default="")
    contact_qq = models.CharField(max_length=200, help_text="联系人QQ", default="")
    company_des = models.CharField(max_length=600, help_text="公司介绍,不超过300字", default="")


class p_menber_email(models.Model):
    username = models.CharField(max_length=30, help_text="关联用户")
    type = models.CharField(max_length=30, help_text="作用：1：注册 2：找回密码 3：修改密码", default="0")
    code = models.CharField(max_length=30, help_text="验证码", default="0")
    create_time = models.CharField(max_length=30, help_text="创建时间", default="0")


class p_product(models.Model):
    p_name = models.CharField(max_length=30, help_text="类别名称")
    create_time = models.CharField(max_length=30, help_text="创建时间", default="0")
    update_time = models.CharField(max_length=30, help_text="修改时间", default="0")


class p_product_child(models.Model):
    p_name = models.CharField(max_length=30, help_text="产品名称")
    p_id = models.IntegerField(help_text="父ID")
    create_time = models.CharField(max_length=30, help_text="创建时间", default="0")
    update_time = models.CharField(max_length=30, help_text="修改时间", default="0")


class p_admin(models.Model):
    username = models.CharField(max_length=30, help_text="关联的普通用户")
    user = models.CharField(max_length=30, help_text="管理员账号")
    password = models.CharField(max_length=30, help_text="管理员密码")
    auth = models.IntegerField(help_text="管理员权限 1：超级管理员 2：子管理员", default=2)
