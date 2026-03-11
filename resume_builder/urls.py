from django.urls import path
from .views import LandingImageView
from .views import JobListView, JobDetailView, JobApplyView
from .views import blog_list
from .views import get_templates
from .views import get_logo
from .views import feature_icons
from .views import upload_resume
from .views import ai_chat
urlpatterns = [
    path("landing-images/", LandingImageView.as_view()),



    path("jobs/", JobListView.as_view()),
    path("jobs/<int:pk>/", JobDetailView.as_view()),
    path("apply/", JobApplyView.as_view()),
     path('blogs/', blog_list),
      path("templates/", get_templates),
      path("logo/", get_logo),
      path("feature-icons/", feature_icons),
      path('upload-resume/', upload_resume, name='upload_resume'),
      path("ai-chat/", ai_chat),
]    



   