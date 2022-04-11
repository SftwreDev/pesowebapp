# Generated by Django 3.2.6 on 2022-04-10 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaseModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('Status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], max_length=255)),
            ],
        ),
    ]
