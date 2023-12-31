# Generated by Django 4.2.4 on 2023-08-08 10:48

from django.db import migrations, models
import newsapp.articles.models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='header_image',
            field=models.ImageField(blank=True, default='img_1_horizontal.jpg', null=True, upload_to='images/', validators=[newsapp.articles.models.MaxImageSizeValidator(5)]),
        ),
    ]
