# Generated by Django 2.2.6 on 2019-10-16 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_auto_20191016_2223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='p_message',
            name='m_ip',
            field=models.TextField(default='0', help_text='ip记录'),
        ),
    ]
