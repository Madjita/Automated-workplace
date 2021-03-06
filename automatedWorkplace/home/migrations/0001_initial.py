# Generated by Django 2.0.1 on 2018-05-22 06:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TableAutomatedWorkstation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('about', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='TableDevice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nameDevice', models.TextField()),
                ('name', models.TextField()),
                ('ip', models.CharField(max_length=50)),
                ('serial', models.TextField()),
                ('mode', models.CharField(max_length=100)),
                ('IdWorkstation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.TableAutomatedWorkstation')),
            ],
        ),
    ]
