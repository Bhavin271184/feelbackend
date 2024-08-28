from rest_framework import serializers
from .models import *

class CategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = '__all__'


class BlogSerializer(serializers.ModelSerializer):

    class Meta: 
        model = Blog
        fields = '__all__'



class HeroOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroOffer
        fields = '__all__'


class GalleryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Galleryimage
        fields = ['id', 'name', 'image', 'created_at']
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
    category = serializers.PrimaryKeyRelatedField(queryset=CategoryModel.objects.all(), write_only=True)
    category_details = CategoryModelSerializer(source='categories', read_only=True)  # Match with the model's field name
    
    class Meta:
        model = ServiceItem
        fields = ['id', 'title', 'description', 'image','categories', 'logo', 'category', 'category_details', 'created_at']

    def create(self, validated_data):
        categories = validated_data.pop('category')  # Extract categories from validated_data
        service_item = ServiceItem.objects.create(categories=categories, **validated_data)
        return service_item
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
        fields = ['id', 'name', 'description','url', 'mul_images','uploaded_images','slug','logo','created_at']

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


class SubcategoryModelSerializerForService(serializers.ModelSerializer):
    # category = serializers.PrimaryKeyRelatedField(queryset=CategoryModel.objects.all(), write_only=True)
    # category_details = CategoryModelSerializer(source='category', read_only=True)

    class Meta:
        model = SubcategoryModel
        fields = ['id', 'name', 'priority',]


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


class ChildCategoryModelSerializerForService(serializers.ModelSerializer):

    class Meta:
        model = ChildCategoryModel
        fields = ['id', 'name', 'priority',]


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
        return ChildCategoryModelSerializerForService(obj.childcategory).data

    def get_subcategory_data(self, obj):
        # You need to define a serializer for ChildCategoryModel if you want to use it
        return SubcategoryModelSerializerForService(obj.subcategory).data

    def create(self, validated_data):
        # Perform custom logic here if needed
        return super().create(validated_data)

class ServicesuserSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(queryset=CategoryModel.objects.all(), required=False, allow_null=True)
    subcategory = serializers.PrimaryKeyRelatedField(queryset=SubcategoryModel.objects.all(), required=False, allow_null=True)
    childcategory = serializers.PrimaryKeyRelatedField(queryset=ChildCategoryModel.objects.all(), required=False, allow_null=True)
    
    class Meta:
        model = Services
        fields = [
            'id', 
            'categories',  # Only the ID will be returned
            'subcategory',  # Only the ID will be returned
            'childcategory',  # Only the ID will be returned
            'service_name', 
            'description', 
            'price', 
            'image', 
            'status', 
            'priority', 
            'created_at'
        ]

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


class BookingAWTSerializer(serializers.Serializer):
    is_register = serializers.BooleanField()
    mobile_number = serializers.CharField(max_length=15)
    email = serializers.EmailField(required=False)
    first_name = serializers.CharField(max_length=100, required=False)
    last_name = serializers.CharField(max_length=100, required=False)
    birth_date = serializers.DateField(required=False, allow_null=True)
    anniversary_date = serializers.DateField(required=False, allow_null=True)
    gender = serializers.ChoiceField(choices=[('M', 'Male'), ('F', 'Female')], required=False)
    service_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=True
    )
    appointment_date = serializers.DateField(required=True)
    expectedStartTime = serializers.CharField(max_length=4, required=False)
    expectedEndTime = serializers.CharField(max_length=4, required=False)

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
            required_fields = ['email', 'first_name', 'last_name', 'gender']
            for field in required_fields:
                if not data.get(field):
                    raise serializers.ValidationError(f"{field} is required when 'is_register' is False.")

        subtotals = []
        total = 0
        service_fetching_errors = []

        for service_servid in data['service_ids']:
            service = Services.objects.filter(servid=service_servid).first()
            if service:
                subtotals.append(service.price)
                total += service.price
            else:
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
        representation['service_ids'] = [str(service_id) for service_id in instance['service_ids']]
        
        return representation


class BookingACSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=15)
    email = serializers.EmailField(required=False)
    first_name = serializers.CharField(max_length=100, required=False)
    last_name = serializers.CharField(max_length=100, required=False)
    birth_date = serializers.DateField(required=False, allow_null=True)
    anniversary_date = serializers.DateField(required=False, allow_null=True)
    gender = serializers.ChoiceField(choices=[('M', 'Male'), ('F', 'Female')], required=False)
    category = serializers.CharField(max_length=100, required=False, allow_blank=True)
    referral_type = serializers.CharField(max_length=100, required=False, allow_blank=True)

    def validate(self, data):
        # Ensure required fields are present
        for field in ['first_name', 'last_name', 'email', 'gender']:
            if not data.get(field):
                raise serializers.ValidationError(f"{field} is required.")
        return data

    def to_representation(self, instance):
        # Modify the representation to match the required AC param structure
        return {
            "mobile_number": instance['mobile_number'],
            "email": instance['email'],
            "first_name": instance['first_name'],
            "last_name": instance['last_name'],
            "birth_date": instance.get('birth_date', "").strftime("%Y-%m-%d") if instance.get('birth_date') else "",
            "anniversary_date": instance.get('anniversary_date', "").strftime("%Y-%m-%d") if instance.get('anniversary_date') else "",
            "gender": instance['gender'],
            "appointment_date": datetime.now().strftime("%Y-%m-%d"),  # Example current date
            "category": instance.get('category', "Regular"),  # Default value
            "referral_type": instance.get('referral_type', "Friend")  # Default value
        }