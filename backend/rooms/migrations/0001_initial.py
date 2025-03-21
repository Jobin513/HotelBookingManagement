# Generated by Django 5.1.6 on 2025-03-05 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('room_number', models.CharField(max_length=50, unique=True)),
                ('room_type', models.CharField(choices=[('Single', 'Single'), ('Double', 'Double'), ('Suite', 'Suite')], max_length=50)),
                ('rate', models.DecimalField(decimal_places=2, max_digits=10)),
                ('room_status', models.CharField(choices=[('Available', 'Available'), ('Booked', 'Booked'), ('Under Maintenance', 'Under Maintenance')], max_length=50)),
                ('capacity', models.PositiveIntegerField()),
                ('created_by', models.CharField(blank=True, max_length=100, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_changed_by', models.CharField(blank=True, max_length=100, null=True)),
                ('last_changed_date', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
