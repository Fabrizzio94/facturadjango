# Generated by Django 3.1.2 on 2020-10-22 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('factura', '0002_auto_20201020_0025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detallefactura',
            name='id_detalle',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
