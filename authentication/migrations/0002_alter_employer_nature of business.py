# Generated by Django 3.2.6 on 2022-04-10 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employer',
            name='Nature of Business',
            field=models.CharField(help_text='Ex. FastFood, IT, BPO', max_length=255),
        ),
    ]
