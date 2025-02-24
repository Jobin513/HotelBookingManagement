# Generated by Django 5.1.6 on 2025-02-17 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_number', models.CharField(max_length=50)),
                ('type', models.CharField(choices=[('Single', 'Single'), ('Double', 'Double'), ('Suite', 'Suite')], max_length=50)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('Available', 'Available'), ('Booked', 'Booked'), ('Under Maintenance', 'Under Maintenance')], max_length=50)),
                ('capacity', models.PositiveIntegerField()),
                ('created_by', models.CharField(blank=True, max_length=100, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_changed_by', models.CharField(blank=True, max_length=100, null=True)),
                ('last_changed_date', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
