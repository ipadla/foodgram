# Generated by Django 2.2.28 on 2022-07-28 16:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_auto_20220728_1632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipefavorites',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorited', to='recipes.Recipe'),
        ),
    ]