# Generated by Django 3.2.9 on 2024-05-09 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_userdata_is_staff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
