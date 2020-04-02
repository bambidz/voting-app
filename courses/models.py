import datetime
from django.db import models
from django.urls import reverse

class Course(models.Model):
    YEAR_CHOICES = []
    for r in range(2016, (datetime.datetime.now().year + 2)):
        YEAR_CHOICES.append((r, r))

    SEMESTER_CHOICES = [('Spring', 'Spring'), ('Summer', 'Summer'),
                        ('Fall', 'Fall'), ('Winter', 'Winter'),
                        ]

    title = models.CharField(max_length=255, blank=True)
    year = models.IntegerField('year', choices=YEAR_CHOICES,
                               default=datetime.datetime.now().year)
    semester = models.CharField(choices=SEMESTER_CHOICES, max_length=6,
                                default='spring')
    goal = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title}: {self.semester}, {self.year}"

    def get_absolute_url(self):
        return reverse('courses:lecture_list', kwargs={'course_pk': self.pk})


class Lecture(models.Model):
    order = models.IntegerField(default=0)
    contents = models.TextField(blank=True)
    goal = models.TextField(blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['order', ]

    def get_absolute_url(self):
        from onlineclasses.models import Video
        video_set = Video.objects.filter(lecture = self, index = 1)
        if not video_set:
            return
        video = video_set.first()
        return reverse('onlineclasses:detail', kwargs={'lecture_pk': self.pk, 'pk':video.pk})

    def __str__(self):
        return f"Lecture {self.order} ({self.course.title})"


class Section(models.Model):
    section_no = models.IntegerField(default=41)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.section_no} ({self.course.title}, {self.course.year})"


class Group(models.Model):
    group_no = models.IntegerField(default=1)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, default=41)
    tmp_no = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.group_no} in {self.section}"
