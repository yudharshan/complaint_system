from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    id_number = models.CharField(max_length=20, unique=True)
    is_student = models.BooleanField(default=True)
    is_staff_member = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username

class Complaint(models.Model):
    COMPLAINT_TYPES = (
        ('hostel', 'Hostel'),
        ('mess', 'Mess'),
        ('faculty', 'Faculty'),
        ('library', 'Library'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    )
    
    LIBRARY_ISSUES = (
        ('wifi', 'WiFi Issue'),
        ('book_not_found', 'Book Not Found'),
        ('other', 'Other'),
    )
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    complaint_type = models.CharField(max_length=20, choices=COMPLAINT_TYPES)
    description = models.TextField()
    severity = models.IntegerField(choices=[(i, str(i)) for i in range(1, 11)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    # Hostel specific fields
    room_number = models.CharField(max_length=10, blank=True, null=True)
    
    # Faculty specific fields
    department = models.CharField(max_length=100, blank=True, null=True)
    faculty_name = models.CharField(max_length=100, blank=True, null=True)
    
    # Library specific fields
    library_issue_type = models.CharField(max_length=20, choices=LIBRARY_ISSUES, blank=True, null=True)
    book_name = models.CharField(max_length=200, blank=True, null=True)
    
    def __str__(self):
        return f"{self.get_complaint_type_display()} complaint by {self.user.username}"