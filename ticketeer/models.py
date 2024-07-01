import datetime
from django.db import models
from kanban_backend import settings
from django.core.validators import MinLengthValidator, MaxLengthValidator

class TicketeerTask(models.Model):
    """
    Model representing a task in the Ticketeer application.
    Attributes:
        author: ForeignKey to the user who created the task.
        title: Title of the task (max length 100).
        subtitle: Subtitle or brief description of the task (max length 200).
        content: Detailed content or description of the task (max length 500).
        date: Date when the task was created (default is today's date).
        prio: Priority of the task, chosen from predefined choices ('low', 'medium', 'urgent').
        status: Current status of the task, chosen from predefined choices ('urgent', 'todo', 'inProgress', 'done').
        doTime: Estimated time required to complete the task, stored in minutes (default is 0).

    Methods:
        __str__: String representation of the task, displaying its ID and title.
    """

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
    title = models.CharField(max_length=100, validators=[MinLengthValidator(3)])
    subtitle = models.CharField(max_length=200, validators=[MaxLengthValidator(10)])
    content = models.TextField(max_length=500, validators=[MinLengthValidator(10)])
    date = models.DateField(default=datetime.date.today)
    prio = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='low')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='todo')
    doTime = models.IntegerField(default=0)  # This field stores time in minutes

    def __str__(self):
        """
        String representation of the task.
        Returns:
            str: String containing the task ID and title.
        """
        return f'({self.id}) {self.title}'
