# Generated by Django 3.2 on 2021-04-12 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0003_car'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Car',
        ),
        migrations.AddField(
            model_name='userfile',
            name='size',
            field=models.CharField(default=0, max_length=10),
            preserve_default=False,
        ),
    ]
