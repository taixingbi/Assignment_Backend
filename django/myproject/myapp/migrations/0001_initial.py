# Generated by Django 5.2.1 on 2025-05-10 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NucleotideSequence',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('content', models.TextField()),
            ],
        ),
    ]
