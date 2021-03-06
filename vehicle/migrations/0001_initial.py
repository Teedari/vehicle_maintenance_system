# Generated by Django 3.2.7 on 2021-09-17 16:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fullname', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=10)),
                ('email', models.EmailField(blank=True, max_length=100)),
                ('address', models.TextField(blank=True, default='no address provided')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('text', models.CharField(max_length=100)),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('vehicle_year', models.CharField(blank=True, max_length=4)),
                ('vehicle_type', models.CharField(choices=[('toyota', 'Toyota'), ('nissan', 'Nissan'), ('vibe', 'Vibe'), ('v8', 'V8'), ('mercedes-benz', 'Mercedes-benz'), ('rolls', 'Rolls'), ('rolls royce', 'Rolls Royce')], max_length=15)),
                ('vehicle_make', models.CharField(max_length=100)),
                ('vehicle_model', models.CharField(max_length=100)),
                ('vehicle_number_plate', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Maintenance',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('token', models.CharField(blank=True, max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='vehicle.customer')),
                ('service', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='service', to='vehicle.service')),
            ],
        ),
        migrations.AddField(
            model_name='customer',
            name='vehicles',
            field=models.ManyToManyField(blank=True, related_name='vehicles', to='vehicle.Vehicle'),
        ),
    ]
