# Generated by Django 2.2.6 on 2019-10-16 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_p_message_num'),
    ]

    operations = [
        migrations.AddField(
            model_name='p_message',
            name='m_ip',
            field=models.TextField(default='0', help_text='ip记录'),
        ),
    ]
