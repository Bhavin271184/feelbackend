from django.shortcuts import render
from rest_framework import generics, status
from .models import *
from .serializers import *
from .permissions import IsAuthenticatedForPostPatchDelete
from datetime import datetime, time
from django.utils import timezone
from django.http import JsonResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
import requests
from decimal import Decimal
from django.db.models import Q, Max



class CategoryModelListCreateView(generics.ListCreateAPIView):
    queryset = CategoryModel.objects.all()
    serializer_class = CategoryModelSerializer
    permission_classes = [IsAuthenticatedForPostPatchDelete]

    def get_queryset(self):
        queryset = super().get_queryset()

        status = self.request.query_params.get('status', 'active')  
        if status:
            queryset = queryset.filter(status=status)
        
        slug = self.request.query_params.get('slug')
        if slug:
            queryset = queryset.filter(slug=slug)
        
        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')
        # slug = self.request.GET.get('slug')

        # if slug:
        #     queryset = queryset.filter(slug=slug)

        if start_date_str:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
                start_date = timezone.make_aware(datetime.combine(start_date, time.min), timezone.get_current_timezone())  # Set time to midnight
            except ValueError:
                start_date = None
        else:
            start_date = None

        if end_date_str:
            try:
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
                end_date = timezone.make_aware(datetime.combine(end_date, time.max), timezone.get_current_timezone())  # Set time to end of the day
            except ValueError:
                end_date = None
        else:
            end_date = None

        if start_date and end_date:
            print(f"Filtering from {start_date} to {end_date}")  # Debug statement
            queryset = queryset.filter(created_at__range=(start_date, end_date))
        elif start_date:
            print(f"Filtering from {start_date} onwards")  # Debug statement
            queryset = queryset.filter(created_at__gte=start_date)
        elif end_date:
            print(f"Filtering up to {end_date}")  # Debug statement
            queryset = queryset.filter(created_at__lte=end_date)

        return queryset #hhh


class CategoryModelRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CategoryModel.objects.all()
    serializer_class = CategoryModelSerializer
    permission_classes = [IsAuthenticatedForPostPatchDelete] 

    def partial_update(self, request, *args, **kwargs):
        if 'priorities' in request.data:
            priority_data = request.data.get('priorities', [])

            if not isinstance(priority_data, list):
                return Response({'error': 'Invalid data format. Expected a list of dictionaries.'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                for item in priority_data:
                    hero_offer = HeroOffer.objects.get(id=item['id'])
                    hero_offer.priority = item['priority']
                    hero_offer.save()

                return Response({'status': 'Priorities updated successfully'}, status=status.HTTP_200_OK)

            except HeroOffer.DoesNotExist:
                return Response({'error': 'HeroOffer not found'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return super().partial_update(request, *args, **kwargs)


class BlogListCreateView(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticatedForPostPatchDelete]

    def get_queryset(self):
        queryset = super().get_queryset()
        
        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')
        # slug = self.request.GET.get('slug')

        # if slug:
        #     queryset = queryset.filter(slug=slug)

        if start_date_str:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
                start_date = timezone.make_aware(datetime.combine(start_date, time.min), timezone.get_current_timezone())  # Set time to midnight
            except ValueError:
                start_date = None
        else:
            start_date = None

        if end_date_str:
            try:
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
                end_date = timezone.make_aware(datetime.combine(end_date, time.max), timezone.get_current_timezone())  # Set time to end of the day
            except ValueError:
                end_date = None
        else:
            end_date = None

        if start_date and end_date:
            print(f"Filtering from {start_date} to {end_date}")  # Debug statement
            queryset = queryset.filter(created_at__range=(start_date, end_date))
        elif start_date:
            print(f"Filtering from {start_date} onwards")  # Debug statement
            queryset = queryset.filter(created_at__gte=start_date)
        elif end_date:
            print(f"Filtering up to {end_date}")  # Debug statement
            queryset = queryset.filter(created_at__lte=end_date)

        return queryset

class BlogRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticatedForPostPatchDelete]

class HeroOfferListCreateView(generics.ListCreateAPIView):
    queryset = HeroOffer.objects.all()
    serializer_class = HeroOfferSerializer
    permission_classes = [IsAuthenticatedForPostPatchDelete]

    def get_queryset(self):
        queryset = super().get_queryset()
        
        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')
        # slug = self.request.GET.get('slug')

        # if slug:
        #     queryset = queryset.filter(slug=slug)

        if start_date_str:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
                start_date = timezone.make_aware(datetime.combine(start_date, time.min), timezone.get_current_timezone())  # Set time to midnight
            except ValueError:
                start_date = None
        else:
            start_date = None

        if end_date_str:
            try:
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
                end_date = timezone.make_aware(datetime.combine(end_date, time.max), timezone.get_current_timezone())  # Set time to end of the day
            except ValueError:
                end_date = None
        else:
            end_date = None

        if start_date and end_date:
            print(f"Filtering from {start_date} to {end_date}")  # Debug statement
            queryset = queryset.filter(created_at__range=(start_date, end_date))
        elif start_date:
            print(f"Filtering from {start_date} onwards")  # Debug statement
            queryset = queryset.filter(created_at__gte=start_date)
        elif end_date:
            print(f"Filtering up to {end_date}")  # Debug statement
            queryset = queryset.filter(created_at__lte=end_date)

        return queryset

class HeroOfferRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HeroOffer.objects.all()
    serializer_class = HeroOfferSerializer
    permission_classes = [IsAuthenticatedForPostPatchDelete]

    def partial_update(self, request, *args, **kwargs):
        if 'priorities' in request.data:
            priority_data = request.data.get('priorities', [])

            if not isinstance(priority_data, list):
                return Response({'error': 'Invalid data format. Expected a list of dictionaries.'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                for item in priority_data:
                    hero_offer = HeroOffer.objects.get(id=item['id'])
                    hero_offer.priority = item['priority']
                    hero_offer.save()

                return Response({'status': 'Priorities updated successfully'}, status=status.HTTP_200_OK)

            except HeroOffer.DoesNotExist:
                return Response({'error': 'HeroOffer not found'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return super().partial_update(request, *args, **kwargs)

def DashboardView(request):
    result = {}

    models_to_count = [
        (CategoryModel, 'Total Category'),
        (Services, 'Total Services'),
        (Blog, 'Total Blog'),
        (HeroOffer, 'Total HeroOffer'),
        
    ]

    for model, custom_name in models_to_count:
        count = model.objects.count()
        result[custom_name] = count

    return JsonResponse(result)

# ==============================================================================================================
class HairCategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = HairCategory.objects.all()
    serializer_class = HairCategorySerializer
    permission_classes = [IsAuthenticatedForPostPatchDelete]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')
        # slug = self.request.GET.get('slug')

        # if slug:
        #     queryset = queryset.filter(slug=slug)

        if start_date_str:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
                start_date = timezone.make_aware(datetime.combine(start_date, time.min), timezone.get_current_timezone())  # Set time to midnight
            except ValueError:
                start_date = None
        else:
            start_date = None

        if end_date_str:
            try:
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
                end_date = timezone.make_aware(datetime.combine(end_date, time.max), timezone.get_current_timezone())  # Set time to end of the day
            except ValueError:
                end_date = None
        else:
            end_date = None

        if start_date and end_date:
            print(f"Filtering from {start_date} to {end_date}")  # Debug statement
            queryset = queryset.filter(created_at__range=(start_date, end_date))
        elif start_date:
            print(f"Filtering from {start_date} onwards")  # Debug statement
            queryset = queryset.filter(created_at__gte=start_date)
        elif end_date:
            print(f"Filtering up to {end_date}")  # Debug statement
            queryset = queryset.filter(created_at__lte=end_date)

        return queryset

class HairCategoryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HairCategory.objects.all()
    serializer_class = HairCategorySerializer
    permission_classes = [IsAuthenticatedForPostPatchDelete]
    
class HairServiceListCreateAPIView(generics.ListCreateAPIView):
    queryset = HairService.objects.all()
    serializer_class = HairServiceSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedForPostPatchDelete]

    def get_queryset(self):
        queryset = super().get_queryset()
        
        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')
        # slug = self.request.GET.get('slug')

        # if slug:
        #     queryset = queryset.filter(slug=slug)

        if start_date_str:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
                start_date = timezone.make_aware(datetime.combine(start_date, time.min), timezone.get_current_timezone())  # Set time to midnight
            except ValueError:
                start_date = None
        else:
            start_date = None

        if end_date_str:
            try:
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
                end_date = timezone.make_aware(datetime.combine(end_date, time.max), timezone.get_current_timezone())  # Set time to end of the day
            except ValueError:
                end_date = None
        else:
            end_date = None

        if start_date and end_date:
            print(f"Filtering from {start_date} to {end_date}")  # Debug statement
            queryset = queryset.filter(created_at__range=(start_date, end_date))
        elif start_date:
            print(f"Filtering from {start_date} onwards")  # Debug statement
            queryset = queryset.filter(created_at__gte=start_date)
        elif end_date:
            print(f"Filtering up to {end_date}")  # Debug statement
            queryset = queryset.filter(created_at__lte=end_date)

        return queryset

class HairServiceRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HairService.objects.all()
    serializer_class = HairServiceSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedForPostPatchDelete]

class MassageCategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = MassageCategory.objects.all()
    serializer_class = MassageCategorySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedForPostPatchDelete]

    def get_queryset(self):
        queryset = super().get_queryset()
        
        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')
        # slug = self.request.GET.get('slug')

        # if slug:
        #     queryset = queryset.filter(slug=slug)

        if start_date_str:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
                start_date = timezone.make_aware(datetime.combine(start_date, time.min), timezone.get_current_timezone())  # Set time to midnight
            except ValueError:
                start_date = None
        else:
            start_date = None

        if end_date_str:
            try:
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
                end_date = timezone.make_aware(datetime.combine(end_date, time.max), timezone.get_current_timezone())  # Set time to end of the day
            except ValueError:
                end_date = None
        else:
            end_date = None

        if start_date and end_date:
            print(f"Filtering from {start_date} to {end_date}")  # Debug statement
            queryset = queryset.filter(created_at__range=(start_date, end_date))
        elif start_date:
            print(f"Filtering from {start_date} onwards")  # Debug statement
            queryset = queryset.filter(created_at__gte=start_date)
        elif end_date:
            print(f"Filtering up to {end_date}")  # Debug statement
            queryset = queryset.filter(created_at__lte=end_date)

        return queryset

class MassageCategoryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MassageCategory.objects.all()
    serializer_class = MassageCategorySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedForPostPatchDelete]

class MassageServiceListCreateAPIView(generics.ListCreateAPIView):
    queryset = MassageService.objects.all()
    serializer_class = MassageServiceSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedForPostPatchDelete]

    def get_queryset(self):
        queryset = super().get_queryset()
        
        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')
        # slug = self.request.GET.get('slug')

        # if slug:
        #     queryset = queryset.filter(slug=slug)

        if start_date_str:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
                start_date = timezone.make_aware(datetime.combine(start_date, time.min), timezone.get_current_timezone())  # Set time to midnight
            except ValueError:
                start_date = None
        else:
            start_date = None

        if end_date_str:
            try:
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
                end_date = timezone.make_aware(datetime.combine(end_date, time.max), timezone.get_current_timezone())  # Set time to end of the day
            except ValueError:
                end_date = None
        else:
            end_date = None

        if start_date and end_date:
            print(f"Filtering from {start_date} to {end_date}")  # Debug statement
            queryset = queryset.filter(created_at__range=(start_date, end_date))
        elif start_date:
            print(f"Filtering from {start_date} onwards")  # Debug statement
            queryset = queryset.filter(created_at__gte=start_date)
        elif end_date:
            print(f"Filtering up to {end_date}")  # Debug statement
            queryset = queryset.filter(created_at__lte=end_date)

        return queryset

class MassageServiceRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MassageService.objects.all()
    serializer_class = MassageServiceSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedForPostPatchDelete]

class UnisexCategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = UnisexCategory.objects.all()
    serializer_class = UnisexCategorySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedForPostPatchDelete]

    def get_queryset(self):
        queryset = super().get_queryset()
        
        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')
        # slug = self.request.GET.get('slug')

        # if slug:
        #     queryset = queryset.filter(slug=slug)

        if start_date_str:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
                start_date = timezone.make_aware(datetime.combine(start_date, time.min), timezone.get_current_timezone())  # Set time to midnight
            except ValueError:
                start_date = None
        else:
            start_date = None

        if end_date_str:
            try:
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
                end_date = timezone.make_aware(datetime.combine(end_date, time.max), timezone.get_current_timezone())  # Set time to end of the day
            except ValueError:
                end_date = None
        else:
            end_date = None

        if start_date and end_date:
            print(f"Filtering from {start_date} to {end_date}")  # Debug statement
            queryset = queryset.filter(created_at__range=(start_date, end_date))
        elif start_date:
            print(f"Filtering from {start_date} onwards")  # Debug statement
            queryset = queryset.filter(created_at__gte=start_date)
        elif end_date:
            print(f"Filtering up to {end_date}")  # Debug statement
            queryset = queryset.filter(created_at__lte=end_date)

        return queryset

class UnisexCategoryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UnisexCategory.objects.all()
    serializer_class = UnisexCategorySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedForPostPatchDelete]

class UnisexServiceListCreateAPIView(generics.ListCreateAPIView):
    queryset = UnisexService.objects.all()
    serializer_class = UnisexServiceSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedForPostPatchDelete]

    def get_queryset(self):
        queryset = super().get_queryset()
        category_choice = self.request.query_params.get('category_choice', None)
        if category_choice:
            queryset = queryset.filter(category__choice=category_choice)
        
        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')
        # slug = self.request.GET.get('slug')

        # if slug:
        #     queryset = queryset.filter(slug=slug)

        if start_date_str:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
                start_date = timezone.make_aware(datetime.combine(start_date, time.min), timezone.get_current_timezone())  # Set time to midnight
            except ValueError:
                start_date = None
        else:
            start_date = None

        if end_date_str:
            try:
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
                end_date = timezone.make_aware(datetime.combine(end_date, time.max), timezone.get_current_timezone())  # Set time to end of the day
            except ValueError:
                end_date = None
        else:
            end_date = None

        if start_date and end_date:
            print(f"Filtering from {start_date} to {end_date}")  # Debug statement
            queryset = queryset.filter(created_at__range=(start_date, end_date))
        elif start_date:
            print(f"Filtering from {start_date} onwards")  # Debug statement
            queryset = queryset.filter(created_at__gte=start_date)
        elif end_date:
            print(f"Filtering up to {end_date}")  # Debug statement
            queryset = queryset.filter(created_at__lte=end_date)

        return queryset

class UnisexServiceRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UnisexService.objects.all()
    serializer_class = UnisexServiceSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedForPostPatchDelete]


class ServiceItemListCreate(generics.ListCreateAPIView):
    queryset = ServiceItem.objects.all()
    serializer_class = ServiceItemSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedForPostPatchDelete]


def get_queryset(self):
        queryset = super().get_queryset()
        
        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')
        # slug = self.request.GET.get('slug')

        # if slug:
        #     queryset = queryset.filter(slug=slug)

        if start_date_str:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
                start_date = timezone.make_aware(datetime.combine(start_date, time.min), timezone.get_current_timezone())  # Set time to midnight
            except ValueError:
                start_date = None
        else:
            start_date = None

        if end_date_str:
            try:
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
                end_date = timezone.make_aware(datetime.combine(end_date, time.max), timezone.get_current_timezone())  # Set time to end of the day
            except ValueError:
                end_date = None
        else:
            end_date = None

        if start_date and end_date:
            print(f"Filtering from {start_date} to {end_date}")  # Debug statement
            queryset = queryset.filter(created_at__range=(start_date, end_date))
        elif start_date:
            print(f"Filtering from {start_date} onwards")  # Debug statement
            queryset = queryset.filter(created_at__gte=start_date)
        elif end_date:
            print(f"Filtering up to {end_date}")  # Debug statement
            queryset = queryset.filter(created_at__lte=end_date)

        return queryset


class ServiceItemRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServiceItem.objects.all()
    serializer_class = ServiceItemSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedForPostPatchDelete]


# ==============================================================================================================

class BrandAndProductListCreate(generics.ListCreateAPIView):
    queryset = BrandAndProduct.objects.all()
    serializer_class = BrandAndProductSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedForPostPatchDelete]

    def get_queryset(self):
        queryset = super().get_queryset()
        slug = self.request.query_params.get('slug', None)
        if slug:
            queryset = queryset.filter(slug__icontains=slug)
        
        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')

        # slug = self.request.GET.get('slug')

        # if slug:
        #     queryset = queryset.filter(slug=slug)

        if start_date_str:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
                start_date = timezone.make_aware(datetime.combine(start_date, time.min), timezone.get_current_timezone())  # Set time to midnight
            except ValueError:
                start_date = None
        else:
            start_date = None

        if end_date_str:
            try:
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
                end_date = timezone.make_aware(datetime.combine(end_date, time.max), timezone.get_current_timezone())  # Set time to end of the day
            except ValueError:
                end_date = None
        else:
            end_date = None

        if start_date and end_date:
            print(f"Filtering from {start_date} to {end_date}")  # Debug statement
            queryset = queryset.filter(created_at__range=(start_date, end_date))
        elif start_date:
            print(f"Filtering from {start_date} onwards")  # Debug statement
            queryset = queryset.filter(created_at__gte=start_date)
        elif end_date:
            print(f"Filtering up to {end_date}")  # Debug statement
            queryset = queryset.filter(created_at__lte=end_date)

        return queryset


class BrandAndProductRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = BrandAndProduct.objects.all()
    serializer_class = BrandAndProductSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedForPostPatchDelete]


class MulImageListView(generics.ListAPIView):
    queryset = BrandAndProductMulImage.objects.all()
    serializer_class = MulImageSerializer

    def get_queryset(self):

        queryset = super().get_queryset()
        salon_slug = self.request.query_params.get('salon_slug',None)
        salon_id = self.request.query_params.get('salon_id',None)
        if salon_slug: 
            queryset = queryset.filter(salon__slug=salon_slug)
        if salon_id: 
            queryset = queryset.filter(salon=salon_id)

        return queryset
        # return super().get_queryset()

class MulImageView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BrandAndProductMulImage.objects.all()
    serializer_class = MulImageSerializer
    lookup_url_kwarg = 'mul_image_id'


# ==============================================================================================================

# from django.conf import settings
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# import requests
# from datetime import datetime

# class GoogleReviewsView(APIView):
#     def get(self, request, format=None):
#         # Your place ID (you can find this from Google Maps)
#         place_id = 'YOUR_PLACE_ID'

#         # Fetch reviews
#         response = requests.get(
#             f'https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={settings.GOOGLE_PLACES_API_KEY}'
#         )

#         if response.status_code == 200:
#             result = response.json().get('result', {})
#             reviews_data = result.get('reviews', [])
#             for review in reviews_data:
#                 GoogleReview.objects.update_or_create(
#                     review_id=review['author_url'],
#                     defaults={
#                         'reviewer_name': review['author_name'],
#                         'review_text': review.get('text', ''),
#                         'rating': int(review['rating']),
#                         'review_time': datetime.fromtimestamp(review['time']),
#                     }
#                 )

#             # Get all reviews from the database
#             reviews = GoogleReview.objects.all()
#             serializer = GoogleReviewSerializer(reviews, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response({'error': 'Error fetching reviews'}, status=response.status_code)

# ==============================================================================================================

class SubcategoryModelListCreateView(generics.ListCreateAPIView):
    queryset = SubcategoryModel.objects.all()
    serializer_class = SubcategoryModelSerializer
    permission_classes = [IsAuthenticatedForPostPatchDelete]

    def get_queryset(self):
        queryset = SubcategoryModel.objects.filter(category__status='active')
        category_id = self.request.query_params.get('category_id')  # Filter by category ID

        if category_id:
            queryset = queryset.filter(category__id=category_id)
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)
        
        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')
        # slug = self.request.GET.get('slug')

        # if slug:
        #     queryset = queryset.filter(slug=slug)

        if start_date_str:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
                start_date = timezone.make_aware(datetime.combine(start_date, time.min), timezone.get_current_timezone())  # Set time to midnight
            except ValueError:
                start_date = None
        else:
            start_date = None

        if end_date_str:
            try:
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
                end_date = timezone.make_aware(datetime.combine(end_date, time.max), timezone.get_current_timezone())  # Set time to end of the day
            except ValueError:
                end_date = None
        else:
            end_date = None

        if start_date and end_date:
            print(f"Filtering from {start_date} to {end_date}")  # Debug statement
            queryset = queryset.filter(created_at__range=(start_date, end_date))
        elif start_date:
            print(f"Filtering from {start_date} onwards")  # Debug statement
            queryset = queryset.filter(created_at__gte=start_date)
        elif end_date:
            print(f"Filtering up to {end_date}")  # Debug statement
            queryset = queryset.filter(created_at__lte=end_date)

        return queryset

    def perform_create(self, serializer):
        category = serializer.validated_data['category']
        if category.status == 'deactive':
            raise ValidationError("Cannot create a subcategory under a deactivated category.")
        
        # Determine the highest priority in the category and set the new priority
        max_priority = SubcategoryModel.objects.filter(category=category).aggregate(models.Max('priority'))['priority__max'] or 0
        new_priority = max_priority + 1
        
        # Save the subcategory with the new priority
        serializer.save(priority=new_priority)

class SubcategoryModelDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubcategoryModel.objects.all()
    serializer_class = SubcategoryModelSerializer
    permission_classes = [IsAuthenticatedForPostPatchDelete]

    def get_queryset(self):
        queryset = super().get_queryset()
        
        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')
        # slug = self.request.GET.get('slug')

        # if slug:
        #     queryset = queryset.filter(slug=slug)

        if start_date_str:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
                start_date = timezone.make_aware(datetime.combine(start_date, time.min), timezone.get_current_timezone())  # Set time to midnight
            except ValueError:
                start_date = None
        else:
            start_date = None

        if end_date_str:
            try:
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
                end_date = timezone.make_aware(datetime.combine(end_date, time.max), timezone.get_current_timezone())  # Set time to end of the day
            except ValueError:
                end_date = None
        else:
            end_date = None

        if start_date and end_date:
            print(f"Filtering from {start_date} to {end_date}")  # Debug statement
            queryset = queryset.filter(created_at__range=(start_date, end_date))
        elif start_date:
            print(f"Filtering from {start_date} onwards")  # Debug statement
            queryset = queryset.filter(created_at__gte=start_date)
        elif end_date:
            print(f"Filtering up to {end_date}")  # Debug statement
            queryset = queryset.filter(created_at__lte=end_date)

        return queryset

    def perform_update(self, serializer):
        category = serializer.validated_data.get('category', serializer.instance.category)
        if category.status == 'deactive':
            raise ValidationError("Cannot update a subcategory under a deactivated category.")
        
        # Get the new priority
        priority = serializer.validated_data.get('priority', None)
        if priority is not None:
            # Ensure the new priority is unique within the category
            if SubcategoryModel.objects.filter(category=category, priority=priority).exclude(id=self.kwargs['pk']).exists():
                # Adjust the priority
                max_priority = SubcategoryModel.objects.filter(category=category).aggregate(models.Max('priority'))['priority__max'] or 0
                priority = max_priority + 1
            
            # Update the priority field
            serializer.save(priority=priority)
        else:
            serializer.save()

    def perform_destroy(self, instance):
        if instance.category.status == 'deactive':
            raise ValidationError("Cannot delete a subcategory under a deactivated category.")
        instance.delete()


from rest_framework.exceptions import ValidationError


class ChildCategoryModelListCreateView(generics.ListCreateAPIView):
    serializer_class = ChildCategoryModelSerializer
    permission_classes = [IsAuthenticatedForPostPatchDelete]

    def get_queryset(self):
        queryset = ChildCategoryModel.objects.all()  # Define the base queryset here

        subcategory_id = self.request.query_params.get('subcategory_id')  # Filter by subcategory ID
        if subcategory_id:
            queryset = queryset.filter(subcategory__id=subcategory_id)

        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')

        start_date = None
        end_date = None

        if start_date_str:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
                start_date = timezone.make_aware(datetime.combine(start_date, time.min), timezone.get_current_timezone())  # Set time to midnight
            except ValueError:
                pass  # Leave start_date as None if parsing fails

        if end_date_str:
            try:
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
                end_date = timezone.make_aware(datetime.combine(end_date, time.max), timezone.get_current_timezone())  # Set time to end of the day
            except ValueError:
                pass  # Leave end_date as None if parsing fails

        if start_date and end_date:
            queryset = queryset.filter(created_at__range=(start_date, end_date))
        elif start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        elif end_date:
            queryset = queryset.filter(created_at__lte=end_date)

        return queryset

    def perform_create(self, serializer):
        category = serializer.validated_data.get('category')
        subcategory = serializer.validated_data.get('subcategory')

        if not category or not subcategory:
            raise ValidationError("Category and subcategory must be provided.")
        
        if subcategory.category != category:
            raise ValidationError("The subcategory must belong to the specified category.")

        # Set priority for the new child category
        max_priority = ChildCategoryModel.objects.filter(category=category).aggregate(models.Max('priority'))['priority__max'] or 0
        new_priority = max_priority + 1
        
        serializer.save(priority=new_priority)
        
class ChildCategoryModelDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ChildCategoryModel.objects.all()
    serializer_class = ChildCategoryModelSerializer
    permission_classes = [IsAuthenticatedForPostPatchDelete]

    def get_queryset(self):
        queryset = super().get_queryset()
        
        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')
        # slug = self.request.GET.get('slug')

        # if slug:
        #     queryset = queryset.filter(slug=slug)

        if start_date_str:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
                start_date = timezone.make_aware(datetime.combine(start_date, time.min), timezone.get_current_timezone())  # Set time to midnight
            except ValueError:
                start_date = None
        else:
            start_date = None

        if end_date_str:
            try:
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
                end_date = timezone.make_aware(datetime.combine(end_date, time.max), timezone.get_current_timezone())  # Set time to end of the day
            except ValueError:
                end_date = None
        else:
            end_date = None

        if start_date and end_date:
            print(f"Filtering from {start_date} to {end_date}")  # Debug statement
            queryset = queryset.filter(created_at__range=(start_date, end_date))
        elif start_date:
            print(f"Filtering from {start_date} onwards")  # Debug statement
            queryset = queryset.filter(created_at__gte=start_date)
        elif end_date:
            print(f"Filtering up to {end_date}")  # Debug statement
            queryset = queryset.filter(created_at__lte=end_date)

        return queryset

    def perform_update(self, serializer):
        category = serializer.validated_data.get('category', serializer.instance.category)
        subcategory = serializer.validated_data.get('subcategory', serializer.instance.subcategory)
        

        if not category or not subcategory:
            raise ValidationError("Category and subcategory must be provided.")

        # Validate if the subcategory belongs to the specified category
        if subcategory.category != category:
            raise ValidationError("The subcategory must belong to the specified category.")
        
        # Handle priority updates
        priority = serializer.validated_data.get('priority', None)
        if priority is not None:
            # Check if priority conflicts with existing priorities
            if ChildCategoryModel.objects.filter(category=category, priority=priority).exclude(id=self.kwargs['pk']).exists():
                # Adjust priority if necessary
                max_priority = ChildCategoryModel.objects.filter(category=category).aggregate(models.Max('priority'))['priority__max'] or 0
                priority = max_priority + 1
            
            serializer.save(priority=priority)
        else:
            serializer.save()

    def perform_destroy(self, instance):
        instance.delete()

from django.db.models import Max

class ServicesListCreateView(generics.ListCreateAPIView):
    queryset = Services.objects.all()
    serializer_class = ServicesSerializer
    permission_classes = [IsAuthenticatedForPostPatchDelete]

    def get_queryset(self):
        queryset = super().get_queryset()
        
        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')
        slug = self.request.GET.get('slug')  # Get the slug from the request

        if slug:
            # Adjust this filter to correctly reflect your model relationships
            queryset = queryset.filter(
                Q(childcategory__subcategory__category__slug=slug) |
                Q(subcategory__category__slug=slug) |
                Q(categories__slug=slug)
            )
        # Initialize start_date and end_date to None
        start_date = None
        end_date = None

        if start_date_str:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
                start_date = timezone.make_aware(datetime.combine(start_date, time.min), timezone.get_current_timezone())  # Set time to midnight
            except ValueError:
                start_date = None

        if end_date_str:
            try:
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
                end_date = timezone.make_aware(datetime.combine(end_date, time.max), timezone.get_current_timezone())  # Set time to end of the day
            except ValueError:
                end_date = None

        if start_date and end_date:
            queryset = queryset.filter(created_at__range=(start_date, end_date))
        elif start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        elif end_date:
            queryset = queryset.filter(created_at__lte=end_date)

        return queryset

    def perform_create(self, serializer):
        childcategory = serializer.validated_data.get('childcategory')

        # Check if the childcategory is provided
        if childcategory:
            max_priority = Services.objects.filter(childcategory=childcategory).aggregate(Max('priority'))['priority__max'] or 0
            new_priority = max_priority + 1
            serializer.save(priority=new_priority)
        else:
            # Save without setting priority if childcategory is not provided
            serializer.save()



class ServicesRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Services.objects.all()
    serializer_class = ServicesSerializer
    permission_classes = [IsAuthenticatedForPostPatchDelete]

    def perform_update(self, serializer):
        childcategory = serializer.validated_data.get('childcategory', serializer.instance.childcategory)
        
        if not childcategory:
            raise ValidationError("Child category must be provided.")

        # Handle priority updates
        priority = serializer.validated_data.get('priority', None)
        if priority is not None:
            # Check if priority conflicts with existing priorities
            if Services.objects.filter(childcategory=childcategory, priority=priority).exclude(id=self.kwargs['pk']).exists():
                max_priority = Services.objects.filter(childcategory=childcategory).aggregate(models.Max('priority'))['priority__max'] or 0
                priority = max_priority + 1
            
            serializer.save(priority=priority)
        else:
            serializer.save()

# ------------------------------------=====================================================================
from django.conf import settings
from urllib.parse import urlencode

# class BookingView(generics.ListCreateAPIView):
#     authentication_classes = []
#     permission_classes = [AllowAny]
#     serializer_class = BookingSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             # Handle customer creation or update
#             if serializer.validated_data['is_register']:
#                 try:
#                     customer = Customer.objects.get(mobile_number=serializer.validated_data['mobile_number'])
#                 except Customer.DoesNotExist:
#                     return Response({'error': 'Customer with this mobile number does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
#             else:
#                 customer_data = {
#                     'mobile_number': serializer.validated_data['mobile_number'],
#                     'email': serializer.validated_data['email'],
#                     'first_name': serializer.validated_data['first_name'],
#                     'last_name': serializer.validated_data['last_name'],
#                     'birth_date': serializer.validated_data['birth_date'],
#                     'anniversary_date': serializer.validated_data.get('anniversary_date', None),
#                     'gender': serializer.validated_data['gender'],
#                 }
#                 customer, created = Customer.objects.update_or_create(
#                     mobile_number=serializer.validated_data['mobile_number'],
#                     defaults=customer_data
#                 )

#             # Fetch service details and prepare the service data
#             total = 0
#             service_ids = serializer.validated_data['service_ids']
#             service_fetching_errors = []

#             services = []
#             for service_id in service_ids:
#                 try:
#                     service = Services.objects.get(id=service_id)
#                     services.append({
#                         'service_id': service_id,
#                         'service_name': service.service_name,
#                         'price': float(service.price)
#                     })
#                     total += service.price
#                 except Services.DoesNotExist:
#                     service_fetching_errors.append(f"Service with ID {service_id} does not exist.")

#             if service_fetching_errors:
#                 return Response({'service_errors': service_fetching_errors}, status=status.HTTP_400_BAD_REQUEST)

#             # Prepare the CRM API parameters
#             param_data = {
#                 "clientInDate": serializer.validated_data['appointment_date'].strftime("%d/%m/%Y %H:%M"),
#                 "waitCode": "S",
#                 "waitTimeCode": "S",
#                 "comments": "",
#                 "bookedDate": serializer.validated_data['appointment_date'].strftime("%d/%m/%Y"),
#                 "expectedStartTime": "1530",  # Placeholder value
#                 "expectedEndTime": "1530",  # Placeholder value
#                 "clientId": serializer.validated_data['mobile_number'],
#                 "serviceId1": "0",  # Placeholder value
#                 "employeeId1": "0"  # Placeholder value
#             }

#             # Encode the parameters into a URL-encoded string
#             encoded_params = urlencode({"Param": str(param_data).replace("'", '"')})

#             # Prepare the full CRM API URL
#             crm_url = f"http://app.salonspa.in/book/bridge.ashx?key=gangatsw&cmd=AWT&{encoded_params}"

#             # Send data to the CRM API using GET request
#             try:
#                 crm_response = requests.get(crm_url)
#                 crm_response.raise_for_status()  # Raise an exception for HTTP errors
#             except requests.RequestException as e:
#                 return Response({'error': f'Failed to send data to CRM: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#             # Prepare and return the response data
#             response_data = {
#                 'customer': {
#                     'id': customer.id,
#                     'is_register': serializer.validated_data['is_register'],
#                     'mobile_number': customer.mobile_number,
#                     'email': customer.email,
#                     'first_name': customer.first_name,
#                     'last_name': customer.last_name,
#                     'birth_date': customer.birth_date.strftime("%Y-%m-%d"),
#                     'anniversary_date': customer.anniversary_date.strftime("%Y-%m-%d") if customer.anniversary_date else None,
#                     'gender': customer.gender
#                 },
#                 'appointment_date': serializer.validated_data['appointment_date'].strftime("%Y-%m-%d"),
#                 'services': services,
#                 'total': float(total),  # Convert Decimal to float
#                 'crm_url': crm_url
#             }

#             return Response(response_data, status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class BookingView(generics.ListCreateAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = BookingSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Handle customer creation or update
            if serializer.validated_data['is_register']:
                try:
                    customer = Customer.objects.get(mobile_number=serializer.validated_data['mobile_number'])
                except Customer.DoesNotExist:
                    return Response({'error': 'Customer with this mobile number does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                customer_data = {
                    'mobile_number': serializer.validated_data['mobile_number'],
                    'email': serializer.validated_data['email'],
                    'first_name': serializer.validated_data['first_name'],
                    'last_name': serializer.validated_data['last_name'],
                    'birth_date': serializer.validated_data['birth_date'],
                    'anniversary_date': serializer.validated_data.get('anniversary_date', None),
                    'gender': serializer.validated_data['gender'],
                }
                customer, created = Customer.objects.update_or_create(
                    mobile_number=serializer.validated_data['mobile_number'],
                    defaults=customer_data
                )

            # Fetch service details and prepare the service data
            total = 0
            service_ids = serializer.validated_data['service_ids']
            service_fetching_errors = []

            services = []
            for service_servid in service_ids:
                try:
                    service = Services.objects.get(servid=service_servid)
                    services.append({
                        'service_id': service_servid,
                        'service_name': service.service_name,
                        'price': float(service.price)
                    })
                    total += service.price
                except Services.DoesNotExist:
                    service_fetching_errors.append(f"Service with servid {service_servid} does not exist.")

            if service_fetching_errors:
                return Response({'service_errors': service_fetching_errors}, status=status.HTTP_400_BAD_REQUEST)

            # Prepare the CRM API parameters
            param_data = {
                "clientInDate": serializer.validated_data['appointment_date'].strftime("%d/%m/%Y %H:%M"),
                "waitCode": "S",
                "waitTimeCode": "S",
                "comments": "",
                "bookedDate": serializer.validated_data['appointment_date'].strftime("%d/%m/%Y"),
                "expectedStartTime": "1530",  # Placeholder value
                "expectedEndTime": "1530",  # Placeholder value
                "clientId": serializer.validated_data['mobile_number'],
                "serviceId1": "0",  # Placeholder value
                "employeeId1": "0"  # Placeholder value
            }

            # Encode the parameters into a URL-encoded string
            encoded_params = urlencode({"Param": str(param_data).replace("'", '"')})

            # Prepare the full CRM API URL
            crm_url = f"http://app.salonspa.in/book/bridge.ashx?key=gangatsw&cmd=AWT&{encoded_params}"

            # Send data to the CRM API using GET request
            try:
                crm_response = requests.get(crm_url)
                crm_response.raise_for_status()  # Raise an exception for HTTP errors
            except requests.RequestException as e:
                return Response({'error': f'Failed to send data to CRM: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Prepare and return the response data
            response_data = {
                'customer': {
                    'id': customer.id,
                    'is_register': serializer.validated_data['is_register'],
                    'mobile_number': customer.mobile_number,
                    'email': customer.email,
                    'first_name': customer.first_name,
                    'last_name': customer.last_name,
                    'birth_date': customer.birth_date.strftime("%Y-%m-%d"),
                    'anniversary_date': customer.anniversary_date.strftime("%Y-%m-%d") if customer.anniversary_date else None,
                    'gender': customer.gender
                },
                'appointment_date': serializer.validated_data['appointment_date'].strftime("%Y-%m-%d"),
                'services': services,
                'total': float(total),  # Convert Decimal to float
                'crm_url': crm_url
            }

            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







# # def send_booking_request(client_data):
# #     url = 'https://app.salonspa.in/book/bridge.ashx'
# #     params = {
# #         'key': 'gangatsw',
# #         'cmd': 'AWT',
# #         'Param': {
# #             "clientInDate": client_data.get("clientInDate", ""),
# #             "waitCode": client_data.get("waitCode", "S"),
# #             "waitTimeCode": client_data.get("waitTimeCode", "S"),
# #             "comments": client_data.get("comments", ""),
# #             "bookedDate": client_data.get("bookedDate", ""),
# #             "expectedStartTime": client_data.get("expectedStartTime", ""),
# #             "expectedEndTime": client_data.get("expectedEndTime", ""),
# #             "clientId": client_data.get("clientId", ""),
# #             "serviceId1": client_data.get("serviceId1", "0"),
# #             "employeeId1": client_data.get("employeeId1", "0")
# #         }
# #     }

# #     response = requests.post(url, params=params)
    
# #     if response.status_code == 200:
# #         return response.json()
# #     else:
# #         response.raise_for_status()


# # class BookingRequestAPIView(generics.ListCreateAPIView):
# #     permission_classes = [AllowAny]

# #     # def get_queryset(self):
# #     #     return []
# #     def create(self, request, *args, **kwargs):
# #         try:
# #             client_data = request.data
# #             result = send_booking_request(client_data)
# #             print(result)
# #             return Response(result, status=status.HTTP_200_OK)
# #         except requests.HTTPError as e:
# #             return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# def send_booking_request(client_data):
#     url = 'https://app.salonspa.in/book/bridge.ashx'
#     params = {
#         'key': 'gangatsw',
#         'cmd': 'AWT',
#         'Param': {
#             "clientInDate": client_data.get("clientInDate", ""),
#             "waitCode": client_data.get("waitCode", "S"),
#             "waitTimeCode": client_data.get("waitTimeCode", "S"),
#             "comments": client_data.get("comments", ""),
#             "bookedDate": client_data.get("bookedDate", ""),
#             "expectedStartTime": client_data.get("expectedStartTime", ""),
#             "expectedEndTime": client_data.get("expectedEndTime", ""),
#             "clientId": client_data.get("clientId", ""),
#             "serviceId1": client_data.get("serviceId1", "0"),
#             "employeeId1": client_data.get("employeeId1", "0")
#         }
#     }

#     response = requests.post(url, params=params)
    
#     if response.status_code == 200:
#         return response.json()
#     else:
#         response.raise_for_status()

# class BookingRequestAPIView(generics.CreateAPIView):
#     """
#     A view that provides the create action for booking requests.
#     """
    
#     def create(self, request, *args, **kwargs):
#         try:
#             client_data = request.data
#             result = send_booking_request(client_data)
#             return Response(result, status=status.HTTP_200_OK)
#         except requests.HTTPError as e:
#             return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# class BookingView1(generics.GenericAPIView):
#     authentication_classes = []  
#     permission_classes = [AllowAny] 
    
#     def post(self, request, *args, **kwargs):
#         # Extract the data from the request
#         client_data = request.data

#         # Construct the full URL with the key and cmd parameters
#         url = 'https://app.salonspa.in/book/bridge.ashx'
#         key = 'gangatsw'  # Replace with your actual key
#         cmd = 'AWT'  # Command for adding a wait list

#         # Prepare the JSON payload for the "Param" parameter
#         param_data = {
#             "clientInDate": client_data.get("clientInDate", "09/08/2024 12:15"),
#             "waitCode": client_data.get("waitCode", "S"),
#             "waitTimeCode": client_data.get("waitTimeCode", "S"),
#             "comments": client_data.get("comments", ""),
#             "bookedDate": client_data.get("bookedDate", "09/08/2024"),
#             "expectedStartTime": client_data.get("expectedStartTime", "1530"),
#             "expectedEndTime": client_data.get("expectedEndTime", "1530"),
#             "clientId": client_data.get("clientId", "8758780504"),
#             "serviceId1": client_data.get("serviceId1", "0"),
#             "employeeId1": client_data.get("employeeId1", "0")
#         }

#         # Send the POST request to the external API
#         response = requests.post(
#             url,
#             params={'key': key, 'cmd': cmd},  # Key and command as URL parameters
#             json={'Param': param_data}  # JSON payload for the Param parameter
#         )

#         # Check the response status
#         if response.status_code == 200:
#             return Response(response.json(), status=status.HTTP_200_OK)
#         else:
#             return Response({'error': response.text}, status=response.status_code)