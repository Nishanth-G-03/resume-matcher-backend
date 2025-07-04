import os
import docx2txt
try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .models import ResumeMatcher
from .serializers import ResumeMatcherSerializer
import spacy
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, DestroyAPIView

nlp = spacy.load("en_core_web_sm")  # Load the English NLP model

# Create your views here.
def extract_text(file):
    ext = os.path.splitext(file.name)[-1].lower()
    if ext == '.pdf':
        doc=fitz.open(stream=file.read(),filetype='pdf')
        text=" ".join([page.get_text() for page in doc])
        return text
    elif ext in ['.docx', '.doc']:
        return docx2txt.process(file)
    else:
        return ""

class ResumeMatcherView(APIView):
    parser_classes=(MultiPartParser, FormParser)

    def post(self, request):
        resume_file = request.FILES.get('resume')
        job_description = request.data.get('job_description')

        if not resume_file or not job_description:
            return Response({"error": "Resume file and job description are required."}, status=status.HTTP_400_BAD_REQUEST) 
        
        resume_text = extract_text(resume_file)
        jd_text = job_description

        # Very basic matching logic 

        # resume_words = set(resume_text.lower().split())
        # jd_words = set(jd_text.lower().split())
        # match_score=round(len(resume_words & jd_words) / len(jd_words) * 100, 2) if jd_words else 0.0

        # NLP based semantic similarity
        doc_resume = nlp(resume_text)
        doc_jd = nlp(jd_text)
        match_score = round(doc_resume.similarity(doc_jd) * 100, 2)

        match_instance = ResumeMatcher.objects.create(
            user=request.user,
            resume=resume_file,
            job_description=jd_text,
            match_score=match_score,
            resume_text=doc_resume,  # Assuming you want to store the extracted text as well
        )

        serializer = ResumeMatcherSerializer(match_instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserMatchHistoryView(ListAPIView):
    serializer_class = ResumeMatcherSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ResumeMatcher.objects.filter(user=self.request.user).order_by('-uploaded_at')
    
class DeleteMatchView(DestroyAPIView):
    queryset = ResumeMatcher.objects.all()
    serializer_class = ResumeMatcherSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

