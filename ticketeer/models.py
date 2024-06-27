import datetime
from django.db import models

from kanban_backend import settings

class TicketeerTask(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('urgent', 'Urgent'),
    ]

    STATUS_CHOICES = [
        ('urgent', 'Urgent'),
        ('todo', 'To Do'),
        ('inProgress', 'In Progress'),
        ('done', 'Done'),
    ]

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=200)
    content = models.TextField(max_length=500)
    date = models.DateField(default=datetime.date.today)
    prio = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='low')
    done = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='todo')
    doTime = models.IntegerField(default=0)  # This field stores time in minutes or any other unit you prefer

    def __str__(self):
        return f'({self.id}) {self.title}'