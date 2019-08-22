# Generated by Django 2.0.7 on 2019-08-21 08:21

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
            name='Homework',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('contents', models.FileField(upload_to='homework/')),
                ('due_date', models.CharField(max_length=255, null=True)),
                ('video_clip_name_1', models.CharField(max_length=255, null=True)),
                ('video_clip_link_1', models.CharField(max_length=255, null=True)),
                ('video_clip_name_2', models.CharField(max_length=255, null=True)),
                ('video_clip_link_2', models.CharField(max_length=255, null=True)),
                ('video_clip_name_3', models.CharField(max_length=255, null=True)),
                ('video_clip_link_3', models.CharField(max_length=255, null=True)),
                ('quetions_image', models.ImageField(null=True, upload_to='homework/')),
                ('is_active', models.IntegerField(default=0)),
                ('Course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='courses.Course')),
            ],
        ),
        migrations.CreateModel(
            name='HomeworkTraker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(null=True)),
                ('start_time_video_1', models.DateTimeField(null=True)),
                ('start_time_video_2', models.DateTimeField(null=True)),
                ('start_time_video_3', models.DateTimeField(null=True)),
                ('end_time', models.DateTimeField(null=True)),
                ('Homework', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='homework.Homework')),
                ('Student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Student')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='homeworktraker',
            unique_together={('Student', 'Homework')},
        ),
        migrations.AlterUniqueTogether(
            name='homework',
            unique_together={('title', 'Course')},
        ),
    ]
