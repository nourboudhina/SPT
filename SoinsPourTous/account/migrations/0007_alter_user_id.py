# Generated by Django 5.0.4 on 2024-05-07 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_alter_user_date_naiss_alter_user_nationalite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False, unique=True),
        ),
    ]
