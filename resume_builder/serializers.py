from rest_framework import serializers
from .models import LandingImage


class LandingImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandingImage
        fields = "__all__"




        from rest_framework import serializers
from .models import Job, JobApplication


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = "__all__"


class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = "__all__"


from rest_framework import serializers
from .models import Blog

class BlogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Blog
        fields = "__all__"


from rest_framework import serializers
from .models import Template

class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = "__all__"



from rest_framework import serializers
from .models import Logo

class LogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logo
        fields = "__all__"



from rest_framework import serializers
from .models import FeatureIcon

class FeatureIconSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeatureIcon
        fields = "__all__"