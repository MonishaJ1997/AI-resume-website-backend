from rest_framework.views import APIView
from rest_framework.response import Response
from .models import LandingImage
from .serializers import LandingImageSerializer


class LandingImageView(APIView):

    def get(self, request):
        images = LandingImage.objects.all()
        serializer = LandingImageSerializer(images, many=True, context={"request": request})
        return Response(serializer.data)
    



from rest_framework import generics
from .models import Job, JobApplication
from .serializers import JobSerializer, JobApplicationSerializer


class JobListView(generics.ListAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer


class JobDetailView(generics.RetrieveAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer


class JobApplyView(generics.CreateAPIView):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer



from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Blog
from .serializers import BlogSerializer

@api_view(['GET'])
def blog_list(request):

    blogs = Blog.objects.all().order_by('-date')

    serializer = BlogSerializer(blogs, many=True)

    return Response(serializer.data)



from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Template
from .serializers import TemplateSerializer

@api_view(["GET"])
def get_templates(request):

    templates = Template.objects.all()
    serializer = TemplateSerializer(templates, many=True)

    return Response(serializer.data)



from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Logo
from .serializers import LogoSerializer

@api_view(['GET'])
def get_logo(request):
    logo = Logo.objects.last()
    serializer = LogoSerializer(logo)
    return Response(serializer.data)



from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import FeatureIcon
from .serializers import FeatureIconSerializer

@api_view(['GET'])
def feature_icons(request):
    icons = FeatureIcon.objects.all()
    serializer = FeatureIconSerializer(icons, many=True)
    return Response(serializer.data)


# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pdfplumber
from docx import Document
import re

@csrf_exempt
def upload_resume(request):
    if request.method == "POST" and request.FILES.get("resume"):
        resume_file = request.FILES["resume"]
        file_name = resume_file.name.lower()

        extracted_data = {
            "firstName": "",
            "surname": "",
            "email": "",
            "phone": "",
            "profession": "",
            "skills": ["", "", "", ""],
            "experience": [],
            "education": [],
            "summary": ""
        }

        # Extract text
        text = ""
        if file_name.endswith(".pdf"):
            with pdfplumber.open(resume_file) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
        elif file_name.endswith(".docx"):
            doc = Document(resume_file)
            text = "\n".join([p.text for p in doc.paragraphs])
        else:
            return JsonResponse({"error": "Unsupported file type"}, status=400)

        lines = [line.strip() for line in text.split("\n") if line.strip()]

        # --- Extract contact info ---
        email_match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", text)
        phone_match = re.search(r"\b\d{10}\b", text)
        name_match = re.search(r"^([A-Z][a-z]+)\s([A-Z][a-z]+)", text, re.MULTILINE)

        if name_match:
            extracted_data["firstName"] = name_match.group(1)
            extracted_data["surname"] = name_match.group(2)
        if email_match:
            extracted_data["email"] = email_match.group(0)
        if phone_match:
            extracted_data["phone"] = phone_match.group(0)

        # --- Extract profession/title ---
        # Look for first non-empty line after name
        for line in lines:
            if line and not any(char.isdigit() for char in line) and line != extracted_data["firstName"] + " " + extracted_data["surname"]:
                extracted_data["profession"] = line
                break

        # --- Extract skills ---
        skills_section = []
        for i, line in enumerate(lines):
            if re.search(r"Skills|Technical Skills|Technologies", line, re.I):
                # Next few lines contain skills
                for j in range(1, 5):
                    if i+j < len(lines):
                        skills_section.append(lines[i+j])
                break
        skills_text = " ".join(skills_section).replace("•", ",")
        skills_list = [s.strip() for s in re.split(r",|;", skills_text) if s.strip()][:4]
        for i in range(len(skills_list)):
            extracted_data["skills"][i] = skills_list[i]

        # --- Extract summary / objective ---
        summary_lines = []
        for i, line in enumerate(lines):
            if re.search(r"Summary|Objective|Profile", line, re.I):
                # Take next 1-3 lines
                summary_lines = lines[i+1:i+4]
                break
        extracted_data["summary"] = " ".join(summary_lines)

        # --- Extract experience ---
        exp_sections = []
        for i, line in enumerate(lines):
            if re.search(r"Experience|Work History|Employment", line, re.I):
                # Take next few lines as experience
                for j in range(i+1, min(i+10, len(lines))):
                    if lines[j]:
                        exp_sections.append(lines[j])
                break
        # Map experience as list of objects with placeholder fields
        extracted_data["experience"] = [{"employer": "", "jobTitle": "", "startMonth": "", "startYear": "", "endMonth": "", "endYear": "", "experienceDesc": exp} for exp in exp_sections]

        # --- Extract education ---
        edu_sections = []
        for i, line in enumerate(lines):
            if re.search(r"Education|Academic Background|Qualifications", line, re.I):
                for j in range(i+1, min(i+10, len(lines))):
                    if lines[j]:
                        edu_sections.append(lines[j])
                break
        extracted_data["education"] = [{"school": "", "university": "", "degree": line, "month": "", "year": ""} for line in edu_sections]

        return JsonResponse(extracted_data)

    return JsonResponse({"error": "No file uploaded"}, status=400)






import json
import cohere
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# Initialize Cohere client
co = cohere.ClientV2(api_key=settings.COHERE_API_KEY)


# Cohere AI function
def cohere_chat(prompt):
    try:
        response = co.chat(
            model="command-a-03-2025",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ]
        )

        return response.message.content[0].text

    except Exception as e:
        print("🔥 Cohere AI ERROR:", e)
        return "AI error occurred"


# API view for React chatbot
@csrf_exempt
def ai_chat(request):

    if request.method == "POST":

        try:
            data = json.loads(request.body)
            message = data.get("message")

            if not message:
                return JsonResponse({
                    "reply": "Please enter a question."
                })

            # Ask Cohere AI
            reply = cohere_chat(
                f"You are a career assistant. Answer clearly: {message}"
            )

            return JsonResponse({
                "reply": reply
            })

        except Exception as e:
            print("API ERROR:", e)

            return JsonResponse({
                "reply": "⚠️ Server error"
            })

    return JsonResponse({
        "reply": "Invalid request"
    })