from django.db import models


# Create your models here.
class p_message(models.Model):
    username = models.CharField(max_length=30, help_text="关联用户")
    type = models.CharField(max_length=30, help_text="1：供应 2：需求", default=1)
    m_title = models.CharField(max_length=50, help_text="信息标题", default="")
    m_pz = models.CharField(max_length=30, help_text="产品品种", default="")
    m_begin = models.CharField(max_length=30, help_text="上市开始日期时间", default="")
    m_end = models.CharField(max_length=30, help_text="上市结束日期时间", default="")
    m_size = models.CharField(max_length=30, help_text="报价规格", default="")
    m_today_price = models.CharField(max_length=30, help_text="今日价格", default="")
    m_today_size = models.CharField(max_length=30, help_text="今日价格的单位", default="")
    m_today_date = models.CharField(max_length=30, help_text="上架日期", default="")
    m_photo = models.CharField(max_length=200, help_text="实拍图片，展示图片", default="")
    m_address_province = models.IntegerField(help_text="所属地区代码(省级)", default=0)
    m_address_city = models.IntegerField(help_text="所属地区代码(市级)", default=0)
    m_address_belong = models.IntegerField(help_text="所属地区代码（地区）", default=0)
    m_address_detail = models.CharField(max_length=200, help_text="详细地址", default="")
    m_f_id = models.CharField(max_length=200, help_text="关联的大类别", default="")
    m_c_id = models.CharField(max_length=200, help_text="关联的子类别", default="")
    m_content = models.TextField(help_text="信息内容正文")
    create_time = models.CharField(max_length=30, help_text="创建时间", default="0")
    update_time = models.CharField(max_length=30, help_text="修改时间", default="0")
    auth = models.IntegerField(help_text="封禁 1：正常 2：封禁", default=1)
    num = models.IntegerField(help_text="浏览人数", default=1)
    m_ip = models.TextField(help_text="ip记录", default='0')


class p_message_contact(models.Model):
    p_id = models.CharField(max_length=30, help_text="关联信息ID")
    username = models.CharField(max_length=30, help_text="关联用户")
    company_name = models.CharField(max_length=80, help_text="公司名称", default="")
    address_province = models.IntegerField(help_text="所属地区代码(省级)", default=0)
    address_city = models.IntegerField(help_text="所属地区代码(市级)", default=0)
    address_belong = models.IntegerField(help_text="所属地区代码（地区）", default=0)
    address_detail = models.CharField(max_length=200, help_text="详细地址", default="")
    contact_person = models.CharField(max_length=200, help_text="联系人", default="")
    contact_phone = models.CharField(max_length=200, help_text="联系人手机号码", default="")
    contact_tel = models.CharField(max_length=200, help_text="联系人固定号码", default="")
    contact_email = models.CharField(max_length=200, help_text="联系人邮箱", default="")
    contact_qq = models.CharField(max_length=200, help_text="联系人QQ", default="")


class p_menber(models.Model):
    username = models.CharField(max_length=30, help_text="关联用户")
    nickname = models.CharField(max_length=30, help_text="昵称", default="")
    type = models.CharField(max_length=10, help_text="1:代办（农产品经纪人）2：经销商 3：种养殖户 4：涉农企业 5：农业合作社", default="")
    company_name = models.CharField(max_length=80, help_text="公司名称", default="")
    password = models.CharField(max_length=90, help_text="密码")
    address_province = models.IntegerField(help_text="所属地区代码(省级)", default=0)
    address_city = models.IntegerField(help_text="所属地区代码(市级)", default=0)
    address_belong = models.IntegerField(help_text="所属地区代码（地区）", default=0)
    address_detail = models.CharField(max_length=200, help_text="详细地址", default="")
    contact_person = models.CharField(max_length=200, help_text="联系人", default="")
    contact_phone = models.CharField(max_length=200, help_text="联系人手机号码", default="")
    contact_tel = models.CharField(max_length=200, help_text="联系人固定号码", default="")
    contact_email = models.CharField(max_length=200, help_text="联系人邮箱", default="")
    contact_qq = models.CharField(max_length=200, help_text="联系人QQ", default="")
    company_des = models.CharField(max_length=600, help_text="公司介绍,不超过300字", default="")
    auth = models.IntegerField(help_text="封禁 1：正常 2：封禁", default=1)

class p_menber_auth(models.Model):
    username = models.CharField(max_length=30, help_text="关联用户")
    photo = models.CharField(max_length=800, help_text="营业许可证或者组织证明材料")
    person = models.CharField(max_length=20, help_text="法人")
    person_card = models.CharField(max_length=30, help_text="法人身份证号码")
    person_phone = models.CharField(max_length=20, help_text="法人手机")
    person_compony = models.CharField(max_length=20, help_text="公司/组织名称")
    address_province = models.IntegerField(help_text="所属地区代码(省级)", default=0)
    address_city = models.IntegerField(help_text="所属地区代码(市级)", default=0)
    address_belong = models.IntegerField(help_text="所属地区代码（地区）", default=0)
    address_detail = models.CharField(max_length=200, help_text="详细地址", default="")
    contact_person = models.CharField(max_length=200, help_text="联系人", default="")
    contact_phone = models.CharField(max_length=200, help_text="联系人手机号码", default="")
    contact_tel = models.CharField(max_length=200, help_text="联系人固定号码", default="")
    contact_email = models.CharField(max_length=200, help_text="联系人邮箱", default="")
    contact_qq = models.CharField(max_length=200, help_text="联系人QQ", default="")
    company_des = models.CharField(max_length=600, help_text="公司简介", default="")
    auth = models.IntegerField(help_text="认证情况 1：通过 2：不通过 0：待审核", default=0)

class p_menber_email(models.Model):
    username = models.CharField(max_length=30, help_text="关联用户")
    type = models.IntegerField(help_text="作用：1：注册 2：找回密码 3：修改密码", default=0)
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


class p_file(models.Model):
    name = models.CharField(max_length=30, help_text="文件名称", default="")
    username = models.CharField(max_length=30, help_text="关联用户")
    path = models.CharField(max_length=200, help_text="文件路径")
    create_time = models.CharField(max_length=30, help_text="创建时间", default="0")
    update_time = models.CharField(max_length=30, help_text="修改时间", default="0")

class p_report(models.Model):
    username = models.CharField(max_length=30, help_text="关联用户")
    content = models.CharField(max_length=500, help_text="举报描述", default="")
    contact = models.CharField(max_length=500, help_text="联系方式", default="")
