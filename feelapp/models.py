import os
from uuid import uuid4
from django.db import models
from django.utils import timezone
from django.core.files.storage import default_storage
from cloudinary.models import CloudinaryField
from django.urls import reverse
from django.contrib.postgres.fields import ArrayField
from django.db.models import UniqueConstraint
import os
from uuid import uuid4
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.core.files.storage import default_storage


# Create your models here.

def category_image_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid4()}.webp'
    return os.path.join('category_images', filename)


class CategoryModel(models.Model):
    catid=models.IntegerField(default=0)
    name = models.CharField(max_length=100, unique=True)
    # slug = models.SlugField()
    priority = models.IntegerField(default=0)
    image_url = models.ImageField(blank=True, null=True, default='', upload_to=category_image_upload_path, storage=default_storage)
    created_at = models.DateTimeField(default=timezone.now)
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('deactive', 'Deactive'),
    ]
    
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active',
    )
    slug = models.SlugField(unique=True, default="", max_length=255, editable=False)  # 'editable=False' ensures the slug is not directly modifiable in forms

    def save(self, *args, **kwargs):
        # Set the slug to be the same as the category name, but formatted
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

def blog_image_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid4()}.webp'
    return os.path.join('blog_images', filename)

class Blog(models.Model):
    title = models.CharField(max_length=255,unique=True)
    content = models.TextField()
    image_blog = models.ImageField(upload_to=blog_image_upload_path, blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True, default='')
    meta_title = models.CharField(max_length=255, blank=True, null=True, default='')
    meta_description = models.TextField(blank=True, null=True, default='')
    meta_keywords = models.CharField(max_length=255, blank=True, null=True, default='')
    slug = models.SlugField(unique=True)
    hashtags = ArrayField(models.CharField(max_length=200), blank=True, default=list)
    read_time = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    def __str__(self) -> str:
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Blog, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
    
def national_hero_offer_image(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid4()}.{ext}'
    return os.path.join('nationalhero', filename)

def national_mobile_hero_offer_image(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid4()}.{ext}'
    return os.path.join('nationalhero', filename)

class HeroOffer(models.Model):
    image = models.ImageField(upload_to=national_hero_offer_image, blank=True, null=True)
    mobile_image = models.ImageField(upload_to=national_mobile_hero_offer_image, blank=True, null=True)

    priority = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

# ===================================================================

class HairCategory(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.name

def default_hairservice_time():
    return {
        "hours": 0,
        "minutes": 0,
        "seatings": 0,
    }

class HairService(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(HairCategory, on_delete=models.CASCADE, related_name='services')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    gender = models.CharField(max_length=50, blank=True, null=True)
    service_time = models.JSONField(default=default_hairservice_time, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class MassageCategory(models.Model):
    TYPE_CHOICES = [
        ('classic', 'Classic'),
        ('executive', 'Executive')
    ]
    
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['name', 'type'], name='unique_name_type')
        ]


    def __str__(self):
        return self.name

def default_massageservice_time():
    return {
        "hours": 0,
        "minutes": 0,
        "seatings": 0,
    }

class MassageService(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    name = models.CharField(max_length=255)
    category = models.ForeignKey(MassageCategory, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    service_time = models.JSONField(default=default_massageservice_time, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class UnisexCategory(models.Model):
    CHOICES = [
        ('makeup', 'Makeup'),
        ('nail art', 'Nail Art'),
        ('skin', 'Skin'),
        ('aesthetic skin care', 'Aesthetic Skin Care'),
        ('package', 'Package'),
    ]

    name = models.CharField(max_length=255)
    choice = models.CharField(max_length=20, choices=CHOICES)
    created_at = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'choice'], name='unique_name_choice')
        ]

def default_unisexservice_time():
    return {
        "hours": 0,
        "minutes": 0,
        "seatings": 0,
    }

class UnisexService(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(UnisexCategory, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    gender = models.CharField(max_length=10, blank=True, null=True)
    service_time = models.JSONField(default=default_unisexservice_time, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class ServiceItem(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='service_items/', null=True, blank=True)
    logo = models.ImageField(upload_to='service_logo/', null=True, blank=True)  
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title or 'No Title'


# ===============================================================================


def brand_mul_image_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid4()}.webp'
    return os.path.join('salon_mul_images', filename)

class BrandAndProduct(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True,default="")
    logo = models.ImageField(upload_to='service_logo/', null=True, blank=True)  
    created_at = models.DateTimeField(default=timezone.now)

    
    def __str__(self):
        return self.name

class BrandAndProductMulImage(models.Model):
    brand = models.ForeignKey(BrandAndProduct, on_delete=models.CASCADE, related_name = "mul_images")

    image = models.ImageField(upload_to=brand_mul_image_upload_path, default="", null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

# ==============================================================================================================

# class GoogleReview(models.Model):
#     review_id = models.CharField(max_length=255, unique=True)
#     reviewer_name = models.CharField(max_length=255)
#     review_text = models.TextField()
#     rating = models.IntegerField()
#     review_time = models.DateTimeField()

#     def __str__(self):
#         return self.reviewer_name


# ==============================================================================================================


class SubcategoryModel(models.Model):
    subid=models.IntegerField(default=0)
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    priority = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.name

class ChildCategoryModel(models.Model):
    childid=models.IntegerField(default=0)
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubcategoryModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    priority = models.IntegerField(default=0)  # Add priority field
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name



# def default_service_time():
#     return {
#         "hours": 0,
#         "minutes": 0,
#         "seatings": 0,
#     }

def service_image(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid4()}.{ext}'
    return os.path.join('service', filename)

class Services(models.Model):
    servid=models.IntegerField(default=0)
    categories = models.ForeignKey(CategoryModel, on_delete=models.CASCADE,null=True,blank=True)
    subcategory = models.ForeignKey(SubcategoryModel, on_delete=models.CASCADE,null=True,blank=True)
    childcategory = models.ForeignKey(ChildCategoryModel, on_delete=models.CASCADE,null=True,blank=True)  # No default here
    service_name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    price = models.FloatField()
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    # gender = models.CharField(max_length=255)
    STATUS_CHOICES = [
        ('true', 'True'),
        ('false', 'False'),
    ]
    
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='',
    )
    priority = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)


# ==============================================================================================================



class ProductService(models.Model):
    service_name = models.CharField(max_length=255)
    service_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    subtotal_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    appointment_date = models.DateField()
    comment = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.subtotal_price = self.service_price * self.quantity
        super(ProductService, self).save(*args, **kwargs)


class Customer(models.Model):
    is_register = models.BooleanField(default=False)
    mobile_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    anniversary_date = models.DateField(blank=True, null=True)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female')
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)