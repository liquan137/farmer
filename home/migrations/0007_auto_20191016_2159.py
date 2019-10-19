# Generated by Django 2.2.6 on 2019-10-16 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_p_menber_auth_auth'),
    ]

    operations = [
        migrations.CreateModel(
            name='p_report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(help_text='关联用户', max_length=30)),
                ('content', models.CharField(default='', help_text='举报描述', max_length=500)),
                ('contact', models.CharField(default='', help_text='联系方式', max_length=500)),
            ],
        ),
        migrations.AlterField(
            model_name='p_menber_auth',
            name='photo',
            field=models.CharField(help_text='营业许可证或者组织证明材料', max_length=800),
        ),
    ]