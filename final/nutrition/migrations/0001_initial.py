# Generated by Django 3.0.9 on 2021-04-30 06:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='NutritionEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=128)),
                ('category', models.CharField(choices=[('-------', '-------'), ('Breakfast', 'Breakfast'), ('Lunch', 'Lunch'), ('Dinner', 'Dinner'), ('Snack', 'Snack'), ('Other', 'Other')], max_length=128)),
                ('calories', models.IntegerField()),
                ('calories_goal', models.IntegerField()),
                ('grand_calories', models.IntegerField(null=True)),
                ('protein', models.IntegerField(blank=True, null=True)),
                ('fats', models.IntegerField(blank=True, null=True)),
                ('carbs', models.IntegerField(blank=True, null=True)),
                ('date', models.DateField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
