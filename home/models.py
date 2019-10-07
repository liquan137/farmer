from django.db import models


# Create your models here.
class p_message(models.Model):
    username = models.CharField(max_length=30, help_text="关联用户")
    m_title = models.CharField(max_length=50, help_text="信息标题")
    m_pz = models.CharField(max_length=30, help_text="产品品种")
    m_begin = models.CharField(max_length=30, help_text="上市开始日期时间")
    m_end = models.CharField(max_length=30, help_text="上市结束日期时间")
    m_size = models.CharField(max_length=30, help_text="报价规格")
    m_today_price = models.CharField(max_length=30, help_text="今日价格")
    m_today_date = models.CharField(max_length=30, help_text="上架日期")
    m_photo = models.CharField(max_length=200, help_text="实拍图片，展示图片")
    m_address_belong = models.CharField(max_length=200, help_text="所属地区代码")
    m_address_detail = models.CharField(max_length=200, help_text="详细地址")
    m_content = models.TextField(help_text="信息内容正文")
    create_time = models.CharField(max_length=30, help_text="创建时间")
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


class p_product(models.Model):
    p_name = models.CharField(max_length=30, help_text="类别名称")
    create_time = models.CharField(max_length=30, help_text="创建时间")
    update_time = models.CharField(max_length=30, help_text="修改时间", default="0")


class p_product_child(models.Model):
    p_name = models.CharField(max_length=30, help_text="产品名称")
    p_id = models.IntegerField(help_text="父ID")
    create_time = models.CharField(max_length=30, help_text="创建时间")
    update_time = models.CharField(max_length=30, help_text="修改时间", default="0")
