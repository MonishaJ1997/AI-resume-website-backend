from django.db import models


class LandingImage(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="landing/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    



    from django.db import models

class Job(models.Model):
    company = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    description = models.TextField()
    work_location = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class JobApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    resume = models.FileField(upload_to="resumes/")
    message = models.TextField(blank=True)

    def __str__(self):
        return self.name



        from django.db import models

class Blog(models.Model):

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to="blog_images/")
    desc = models.TextField()

    def __str__(self):
        return self.title



from django.db import models

class Template(models.Model):

    name = models.CharField(max_length=100)
    price = models.IntegerField()
    image = models.ImageField(upload_to="templates/")

    def __str__(self):
        return self.name
    


from django.db import models

class Logo(models.Model):
    image = models.ImageField(upload_to="logos/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Website Logo"


from django.db import models

class FeatureIcon(models.Model):
    name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to="feature_icons/")

    def __str__(self):
        return self.name