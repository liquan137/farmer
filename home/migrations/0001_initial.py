# Generated by Django 2.2.6 on 2019-10-14 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='p_file',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', help_text='文件名称', max_length=30)),
                ('username', models.CharField(help_text='关联用户', max_length=30)),
                ('path', models.CharField(help_text='文件路径', max_length=200)),
                ('create_time', models.CharField(default='0', help_text='创建时间', max_length=30)),
                ('update_time', models.CharField(default='0', help_text='修改时间', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='p_menber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(help_text='关联用户', max_length=30)),
                ('nickname', models.CharField(default='', help_text='昵称', max_length=30)),
                ('type', models.CharField(default='', help_text='1:代办（农产品经纪人）2：经销商 3：种养殖户 4：涉农企业 5：农业合作社', max_length=10)),
                ('company_name', models.CharField(default='', help_text='公司名称', max_length=80)),
                ('password', models.CharField(help_text='密码', max_length=90)),
                ('address_province', models.IntegerField(default='', help_text='所属地区代码(省级)')),
                ('address_city', models.IntegerField(default='', help_text='所属地区代码(市级)')),
                ('address_belong', models.IntegerField(default='', help_text='所属地区代码（地区）')),
                ('address_detail', models.CharField(default='', help_text='详细地址', max_length=200)),
                ('contact_person', models.CharField(default='', help_text='联系人', max_length=200)),
                ('contact_phone', models.CharField(default='', help_text='联系人手机号码', max_length=200)),
                ('contact_tel', models.CharField(default='', help_text='联系人固定号码', max_length=200)),
                ('contact_email', models.CharField(default='', help_text='联系人邮箱', max_length=200)),
                ('contact_qq', models.CharField(default='', help_text='联系人QQ', max_length=200)),
                ('company_des', models.CharField(default='', help_text='公司介绍,不超过300字', max_length=600)),
                ('auth', models.IntegerField(default=1, help_text='封禁 1：正常 2：封禁')),
            ],
        ),
        migrations.CreateModel(
            name='p_menber_email',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(help_text='关联用户', max_length=30)),
                ('type', models.CharField(default='0', help_text='作用：1：注册 2：找回密码 3：修改密码', max_length=30)),
                ('code', models.CharField(default='0', help_text='验证码', max_length=30)),
                ('create_time', models.CharField(default='0', help_text='创建时间', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='p_message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(help_text='关联用户', max_length=30)),
                ('type', models.CharField(default=1, help_text='1：供应 2：需求', max_length=30)),
                ('m_title', models.CharField(default='', help_text='信息标题', max_length=50)),
                ('m_pz', models.CharField(default='', help_text='产品品种', max_length=30)),
                ('m_begin', models.CharField(default='', help_text='上市开始日期时间', max_length=30)),
                ('m_end', models.CharField(default='', help_text='上市结束日期时间', max_length=30)),
                ('m_size', models.CharField(default='', help_text='报价规格', max_length=30)),
                ('m_today_price', models.CharField(default='', help_text='今日价格', max_length=30)),
                ('m_today_size', models.CharField(default='', help_text='今日价格的单位', max_length=30)),
                ('m_today_date', models.CharField(default='', help_text='上架日期', max_length=30)),
                ('m_photo', models.CharField(default='', help_text='实拍图片，展示图片', max_length=200)),
                ('m_address_province', models.IntegerField(default='', help_text='所属地区代码(省级)')),
                ('m_address_city', models.IntegerField(default='', help_text='所属地区代码(市级)')),
                ('m_address_belong', models.IntegerField(default='', help_text='所属地区代码（地区）')),
                ('m_address_detail', models.CharField(default='', help_text='详细地址', max_length=200)),
                ('m_f_id', models.CharField(default='', help_text='关联的大类别', max_length=200)),
                ('m_c_id', models.CharField(default='', help_text='关联的子类别', max_length=200)),
                ('m_content', models.TextField(help_text='信息内容正文')),
                ('create_time', models.CharField(default='0', help_text='创建时间', max_length=30)),
                ('update_time', models.CharField(default='0', help_text='修改时间', max_length=30)),
                ('auth', models.IntegerField(default=1, help_text='封禁 1：正常 2：封禁')),
            ],
        ),
        migrations.CreateModel(
            name='p_message_contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_id', models.CharField(help_text='关联信息ID', max_length=30)),
                ('username', models.CharField(help_text='关联用户', max_length=30)),
                ('company_name', models.CharField(default='', help_text='公司名称', max_length=80)),
                ('address_province', models.IntegerField(default='', help_text='所属地区代码(省级)')),
                ('address_city', models.IntegerField(default='', help_text='所属地区代码(市级)')),
                ('address_belong', models.IntegerField(default='', help_text='所属地区代码（地区）')),
                ('address_detail', models.CharField(default='', help_text='详细地址', max_length=200)),
                ('contact_person', models.CharField(default='', help_text='联系人', max_length=200)),
                ('contact_phone', models.CharField(default='', help_text='联系人手机号码', max_length=200)),
                ('contact_tel', models.CharField(default='', help_text='联系人固定号码', max_length=200)),
                ('contact_email', models.CharField(default='', help_text='联系人邮箱', max_length=200)),
                ('contact_qq', models.CharField(default='', help_text='联系人QQ', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='p_product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_name', models.CharField(help_text='类别名称', max_length=30)),
                ('create_time', models.CharField(default='0', help_text='创建时间', max_length=30)),
                ('update_time', models.CharField(default='0', help_text='修改时间', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='p_product_child',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_name', models.CharField(help_text='产品名称', max_length=30)),
                ('p_id', models.IntegerField(help_text='父ID')),
                ('create_time', models.CharField(default='0', help_text='创建时间', max_length=30)),
                ('update_time', models.CharField(default='0', help_text='修改时间', max_length=30)),
            ],
        ),
    ]
