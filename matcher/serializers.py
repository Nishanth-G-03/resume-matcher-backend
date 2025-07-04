from rest_framework import serializers
from .models import ResumeMatcher

class ResumeMatcherSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeMatcher
        fields=['id', 'resume', 'job_description', 'match_score', 'uploaded_at','resume_text']
        read_only_fields=['match_score', 'uploaded_at','resume_text']