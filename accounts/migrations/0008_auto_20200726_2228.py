# Generated by Django 3.0.7 on 2020-07-27 03:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20200726_2225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='equipo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='equipo', to='accounts.Equipment'),
        ),
    ]