# Generated by Django 5.0 on 2024-02-04 06:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_coupon_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='wallet',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.payementwallet'),
        ),
    ]
