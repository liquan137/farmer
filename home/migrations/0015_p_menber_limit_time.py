# Generated by Django 2.2.3 on 2019-10-19 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_auto_20191019_1021'),
    ]

    operations = [
        migrations.AddField(
            model_name='p_menber',
            name='limit_time',
            field=models.CharField(default='0', help_text='记录时间', max_length=30),
        ),
    ]
