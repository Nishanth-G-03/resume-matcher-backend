from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ResumeMatcher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resume_matches')
    resume= models.FileField(upload_to='resumes/')
    job_description=models.TextField()
    match_score=models.FloatField(null=True, blank=True)
    uploaded_at=models.DateTimeField(auto_now_add=True)
    resume_text=models.TextField(blank=True)  # To store the extracted text from the resume
