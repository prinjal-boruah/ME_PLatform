# Generated by Django 2.1.15 on 2020-05-05 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='bill_address1',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='organization',
            name='bill_address2',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='organization',
            name='comm_address1',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='organization',
            name='comm_address2',
            field=models.TextField(),
        ),
    ]
