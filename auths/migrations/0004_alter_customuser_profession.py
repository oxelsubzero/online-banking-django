# Generated by Django 4.2.7 on 2023-11-05 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auths', '0003_alter_customuser_revenu'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profession',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
