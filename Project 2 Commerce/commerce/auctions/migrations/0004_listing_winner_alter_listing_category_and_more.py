# Generated by Django 4.0.1 on 2022-02-11 21:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_bid'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='winner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(choices=[('BO', 'Books, Movies & Music'), ('CO', 'Collectibles & Art'), ('FA', 'Fashion'), ('OT', 'Other')], max_length=2),
        ),
        migrations.AlterField(
            model_name='listing',
            name='lister',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lister', to=settings.AUTH_USER_MODEL),
        ),
    ]
