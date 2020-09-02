# Generated by Django 3.0.7 on 2020-09-02 04:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Videos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', models.FileField(blank=True, null=True, upload_to='videos/%Y/%m/%d/')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Order')),
            ],
        ),
        migrations.RemoveField(
            model_name='images',
            name='orderimages',
        ),
        migrations.AddField(
            model_name='images',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/%Y/%m/%d/'),
        ),
        migrations.DeleteModel(
            name='Video',
        ),
    ]