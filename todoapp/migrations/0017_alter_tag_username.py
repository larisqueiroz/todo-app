# Generated by Django 5.0.3 on 2024-05-03 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0016_alter_card_finished'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='username',
            field=models.CharField(blank=True, default=None, max_length=20, null=True),
        ),
    ]
