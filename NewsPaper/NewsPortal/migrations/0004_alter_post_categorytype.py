# Generated by Django 4.1.1 on 2022-10-20 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NewsPortal', '0003_post_categorytype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='categoryType',
            field=models.CharField(choices=[('NW', 'Новость'), ('AR', 'Статья')], default='NW', max_length=2),
        ),
    ]
