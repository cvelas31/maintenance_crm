# Generated by Django 3.0.7 on 2020-07-27 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20200726_2135'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='date_closed',
            field=models.DateTimeField(null=True),
        ),
    ]