# Generated by Django 5.0.3 on 2024-05-01 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0011_alter_tag_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='username',
            field=models.CharField(blank=True, db_default='', default=None, max_length=20, null=True),
        ),
    ]
