# Generated by Django 4.1.5 on 2023-01-31 13:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=50),
        ),
        migrations.CreateModel(
            name='BookSellerUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.CharField(default='Book Seller', max_length=255)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_bookseller', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'BookSeller',
                'verbose_name_plural': 'BookSellers',
            },
        ),
    ]
