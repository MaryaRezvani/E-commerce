# Generated by Django 4.2 on 2024-08-14 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_otpcode"),
    ]

    operations = [
        migrations.AlterField(
            model_name="otpcode",
            name="created",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
