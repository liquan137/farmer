# Generated by Django 2.2.6 on 2019-10-12 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_p_message_contact_auth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='p_message_contact',
            name='auth',
            field=models.IntegerField(default=1, help_text='封禁 1：正常 2：封禁'),
        ),
    ]