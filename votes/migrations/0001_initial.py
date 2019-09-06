nerated by Django 2.2.4 on 2019-09-02 20:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('courses', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('prompt', models.CharField(blank=True, max_length=255)),
                ('contents', models.ImageField(blank=True, null=True, upload_to='')),
                ('code', models.IntegerField(default=0)),
                ('is_active', models.IntegerField(default=0)),
                ('answer', models.TextField(blank=True)),
                ('correct_number', models.IntegerField(default=1)),
                ('lecture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Lecture')),
            ],
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contents', models.ImageField(blank=True, null=True, upload_to='')),
                ('vote1', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4)], null=True)),
                ('vote2', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4)], null=True)),
                ('answer1', models.CharField(max_length=255, null=True)),
                ('answer2', models.CharField(max_length=255, null=True)),
                ('v_response', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4)], default=1)),
                ('a_response', models.CharField(max_length=255, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='votes.Question')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Student')),
            ],
        ),
    ]
