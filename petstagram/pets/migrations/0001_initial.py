# Generated by Django 3.2.3 on 2021-06-14 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('cat', 'Cat'), ('dog', 'Dog'), ('parrot', 'parrot')], max_length=6)),
                ('name', models.CharField(max_length=6)),
                ('age', models.PositiveIntegerField()),
                ('description', models.TextField()),
                ('image_url', models.URLField()),
            ],
        ),
    ]