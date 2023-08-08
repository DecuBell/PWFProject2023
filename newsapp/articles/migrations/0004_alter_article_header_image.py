# Generated by Django 4.2.4 on 2023-08-08 13:17

from django.db import migrations, models
import newsapp.articles.models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_alter_article_header_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='header_image',
            field=models.ImageField(blank=True, default='images/img_1_horizontal.jpg', null=True, upload_to='static/images/', validators=[newsapp.articles.models.MaxImageSizeValidator(5)]),
        ),
    ]
