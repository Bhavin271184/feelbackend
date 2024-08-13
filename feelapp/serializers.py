from rest_framework import serializers
from .models import *
from .admin import *

class CategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = '__all__'


class BlogSerializer(serializers.ModelSerializer):

    class Meta: 
        model = Blog
        fields = '__all__'

    # def validate(self, data):
    #     """
    #     Check that the title and slug are unique during PATCH requests.
    #     """
    #     request = self.context.get('request')
    #     if request and request.method == 'PATCH':
    #         blog_id = self.instance.id
    #         title = data.get('title')
    #         slug = data.get('slug')

    #         # Validate title uniqueness if it has changed
    #         if title and title != self.instance.title:
    #             if Blog.objects.filter(title=title).exclude(id=blog_id).exists():
    #                 raise serializers.ValidationError({'title': 'Blog with this title already exists.'})

    #         # Validate slug uniqueness if it has changed
    #         if slug and slug != self.instance.slug:
    #             if Blog.objects.filter(slug=slug).exclude(id=blog_id).exists():
    #                 raise serializers.ValidationError({'slug': 'Blog with this slug already exists.'})

    #     return data

    # def update(self, instance, validated_data):
    #     """
    #     Update and return an existing `Blog` instance, given the validated data.
    #     """
    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)

    #     instance.save()
    #     return instance



class HeroOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroOffer
        fields = '__all__'

# ============================================
class HairCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = HairCategory
        fields = ['id', 'name','created_at']

class HairServiceSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=HairCategory.objects.all())  # Accepts category ID

    class Meta:
        model = HairService
        fields = ['id', 'name', 'category', 'price', 'gender', 'service_time', 'description','created_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = HairCategorySerializer(instance.category).data  # Provide full category data
        return representation


class MassageCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MassageCategory
        fields = ['id', 'name', 'type','created_at']


class MassageServiceSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=MassageCategory.objects.all())
    category_type = serializers.SerializerMethodField()
    class Meta:
        model = MassageService
        fields = ['id', 'name', 'category', 'price', 'gender', 'service_time', 'description', 'created_at','category_type']

    def get_category_type(self, obj):
        return obj.category.type

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = MassageCategorySerializer(instance.category).data  # Provide full category data
        return representation


class UnisexCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UnisexCategory
        fields = ['id', 'name', 'choice','created_at']


class UnisexServiceSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=UnisexCategory.objects.all())
    category_choice = serializers.SerializerMethodField()

    class Meta:
        model = UnisexService
        fields = ['id', 'name', 'category', 'price', 'gender', 'service_time', 'description', 'created_at', 'category_choice']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = UnisexCategorySerializer(instance.category).data  # Provide full category data
        return representation

    def get_category_choice(self, obj):
        # Assuming 'choice' is a field in UnisexCategory
        return obj.category.choice if obj.category else None


class ServiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceItem
        fields = ['id', 'title', 'description', 'image','logo','created_at']


# ========================================================================================

class MulImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandAndProductMulImage
        fields = ['id', 'brand', 'image','created_at']


class BrandAndProductSerializer(serializers.ModelSerializer):
    mul_images = MulImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child = serializers.ImageField(max_length = 1000000, allow_empty_file = False, use_url = False),
        write_only=True,required=False)
    class Meta:
        model = BrandAndProduct
        fields = ['id', 'name', 'description', 'mul_images','uploaded_images','slug','logo','created_at']

    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', None)
        instance = BrandAndProduct.objects.create(**validated_data)
        
        if uploaded_images:
            for image in uploaded_images:
                BrandAndProductMulImage.objects.create(brand=instance, image=image)
        
        return instance

# ==============================================================================================================

# class GoogleReviewSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = GoogleReview
#         fields = '__all__'

# ==============================================================================================================

class SubcategoryModelSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=CategoryModel.objects.all(), write_only=True)
    category_details = CategoryModelSerializer(source='category', read_only=True)

    class Meta:
        model = SubcategoryModel
        fields = ['id', 'name', 'category', 'subid','category_details', 'priority','created_at']


    def validate_category(self, value):
        if value.status == 'deactive':
            raise serializers.ValidationError("Subcategory cannot be created because the associated category is deactive.")
        return value

class ChildCategoryModelSerializer(serializers.ModelSerializer):
    # Use PrimaryKeyRelatedField for category and subcategory to handle IDs in POST/PUT requests
    category = serializers.PrimaryKeyRelatedField(queryset=CategoryModel.objects.all())
    subcategory = serializers.PrimaryKeyRelatedField(queryset=SubcategoryModel.objects.all())
    
    # Include SubcategoryModelSerializer to show full subcategory details in GET requests
    subcategory_data = SubcategoryModelSerializer(source='subcategory', read_only=True)

    class Meta:
        model = ChildCategoryModel
        fields = ['id', 'category', 'subcategory', 'childid','name', 'priority', 'subcategory_data', 'created_at']

class ServicesSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(queryset=CategoryModel.objects.all(),required=False, allow_null=True)
    subcategory = serializers.PrimaryKeyRelatedField(queryset=SubcategoryModel.objects.all(),required=False, allow_null=True)
    childcategory = serializers.PrimaryKeyRelatedField(queryset=ChildCategoryModel.objects.all(),required=False, allow_null=True)
    
    # Include ChildCategoryModelSerializer to show full childcategory details in GET requests
    childcategory_data = serializers.SerializerMethodField()
    subcategory_data = serializers.SerializerMethodField()


    class Meta:
        model = Services
        fields = ['id', 'categories','price','image','description','servid','subcategory', 'childcategory', 'service_name', 'priority', 'subcategory_data','childcategory_data', 'created_at']

    def get_childcategory_data(self, obj):
        # You need to define a serializer for ChildCategoryModel if you want to use it
        return ChildCategoryModelSerializer(obj.childcategory).data

    def get_subcategory_data(self, obj):
        # You need to define a serializer for ChildCategoryModel if you want to use it
        return SubcategoryModelSerializer(obj.subcategory).data

    def create(self, validated_data):
        # Perform custom logic here if needed
        return super().create(validated_data)

# ==============================================================================================================

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
    
    def validate(self, data):
        if data['is_register']:
            if not Customer.objects.filter(mobile_number=data['mobile_number']).exists():
                raise serializers.ValidationError("Customer with this mobile number does not exist.")
        return data

class ProductServiceSerializer(serializers.ModelSerializer):
    service_id = serializers.IntegerField(write_only=True)
    service_type = serializers.ChoiceField(choices=['hair', 'massage', 'unisex'], write_only=True)
    service_name = serializers.CharField(read_only=True)
    service_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    quantity = serializers.IntegerField()
    subtotal_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    appointment_date = serializers.DateField()
    comment = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = ProductService
        fields = ['service_id', 'service_type', 'service_name', 'service_price', 'quantity', 'subtotal_price', 'appointment_date', 'comment']

    def create(self, validated_data):
        service_id = validated_data.pop('service_id')
        service_type = validated_data.pop('service_type')

        # Fetch the service details based on service_type and service_id
        if service_type == 'hair':
            service = HairService.objects.get(id=service_id)
        elif service_type == 'massage':
            service = MassageService.objects.get(id=service_id)
        elif service_type == 'unisex':
            service = UnisexService.objects.get(id=service_id)
        else:
            raise serializers.ValidationError("Invalid service type.")

        validated_data['service_name'] = service.name
        validated_data['service_price'] = service.price
        validated_data['subtotal_price'] = validated_data['service_price'] * validated_data['quantity']
        
        return super().create(validated_data)

class ServiceDetailSerializer(serializers.Serializer):
    service_name = serializers.CharField()
    service_type = serializers.ChoiceField(choices=['unisex', 'massage', 'hair'])
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    quantity = serializers.IntegerField()

# class BookingSerializer(serializers.Serializer):
#     is_register = serializers.BooleanField()
#     mobile_number = serializers.CharField(max_length=15)
#     email = serializers.EmailField(required=False)
#     first_name = serializers.CharField(max_length=100, required=False)
#     last_name = serializers.CharField(max_length=100, required=False)
#     birth_date = serializers.DateField(required=False)
#     anniversary_date = serializers.DateField(required=False)
#     gender = serializers.ChoiceField(choices=[('M', 'Male'), ('F', 'Female')], required=False)
#     service_ids = serializers.ListField(
#         child=serializers.IntegerField(),
#         required=True
#     )
#     appointment_date = serializers.DateField(required=True)

#     def validate(self, data):
#         # Fetch or validate customer based on `is_register`
#         if data['is_register']:
#             customer = Customer.objects.filter(mobile_number=data['mobile_number']).first()
#             if customer:
#                 data.update({
#                     'email': customer.email,
#                     'first_name': customer.first_name,
#                     'last_name': customer.last_name,
#                     'birth_date': customer.birth_date,
#                     'anniversary_date': customer.anniversary_date,
#                     'gender': customer.gender
#                 })
#             else:
#                 raise serializers.ValidationError("Customer with this mobile number does not exist.")
#         else:
#             required_fields = ['email', 'first_name', 'last_name', 'birth_date', 'gender']
#             for field in required_fields:
#                 if not data.get(field):
#                     raise serializers.ValidationError(f"{field} is required when 'is_register' is False.")

#         subtotals = []
#         total = 0
#         service_fetching_errors = []

#         for service_id in data['service_servid']:
#             try:
#                 # Fetch the service based on ID
#                 service = Services.objects.get(id=service_id)
#                 subtotals.append(service.price)
#                 total += service.price
#             except Services.DoesNotExist:
#                 service_fetching_errors.append(f"Service with ID {service_id} does not exist.")

#         if service_fetching_errors:
#             raise serializers.ValidationError({"service_errors": service_fetching_errors})

#         # Add calculated subtotals and total to the validated data
#         data['subtotals'] = subtotals
#         data['total'] = total

#         return data

#     def to_representation(self, instance):
#         # Modify the representation to include `appointment_date` outside the services array
#         representation = super().to_representation(instance)

#         # Add the appointment_date to the top level
#         representation['appointment_date'] = instance['appointment_date']
        
#         # Remove appointment_date from each service if present
#         for service in representation.get('services', []):
#             service.pop('appointment_date', None)
        
#         return representation




class BookingSerializer(serializers.Serializer):
    is_register = serializers.BooleanField()
    mobile_number = serializers.CharField(max_length=15)
    email = serializers.EmailField(required=False)
    first_name = serializers.CharField(max_length=100, required=False)
    last_name = serializers.CharField(max_length=100, required=False)
    birth_date = serializers.DateField(required=False)
    anniversary_date = serializers.DateField(required=False)
    gender = serializers.ChoiceField(choices=[('M', 'Male'), ('F', 'Female')], required=False)
    service_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=True
    )
    appointment_date = serializers.DateField(required=True)

    def validate(self, data):
        # Fetch or validate customer based on `is_register`
        if data['is_register']:
            customer = Customer.objects.filter(mobile_number=data['mobile_number']).first()
            if customer:
                data.update({
                    'email': customer.email,
                    'first_name': customer.first_name,
                    'last_name': customer.last_name,
                    'birth_date': customer.birth_date,
                    'anniversary_date': customer.anniversary_date,
                    'gender': customer.gender
                })
            else:
                raise serializers.ValidationError("Customer with this mobile number does not exist.")
        else:
            required_fields = ['email', 'first_name', 'last_name', 'birth_date', 'gender']
            for field in required_fields:
                if not data.get(field):
                    raise serializers.ValidationError(f"{field} is required when 'is_register' is False.")

        subtotals = []
        total = 0
        service_fetching_errors = []

        for service_servid in data['service_ids']:
            try:
                # Fetch the service based on `servid`
                service = Services.objects.get(servid=service_servid)
                subtotals.append(service.price)
                total += service.price
            except Services.DoesNotExist:
                service_fetching_errors.append(f"Service with servid {service_servid} does not exist.")

        if service_fetching_errors:
            raise serializers.ValidationError({"service_errors": service_fetching_errors})

        # Add calculated subtotals and total to the validated data
        data['subtotals'] = subtotals
        data['total'] = total

        return data

    def to_representation(self, instance):
        # Modify the representation to include `appointment_date` outside the services array
        representation = super().to_representation(instance)

        # Add the appointment_date to the top level
        representation['appointment_date'] = instance['appointment_date']
        
        # Remove appointment_date from each service if present
        for service in representation.get('services', []):
            service.pop('appointment_date', None)
        
        return representation