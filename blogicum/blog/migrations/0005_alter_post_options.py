# Generated by Django 5.1.1 on 2025-07-24 21:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_alter_post_author_alter_post_pub_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('title',), 'verbose_name': 'публикация', 'verbose_name_plural': 'Публикации'},
        ),
    ]
