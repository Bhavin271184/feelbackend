from django.shortcuts import render
from django.utils import timezone
from django.http import JsonResponse
from django.db import transaction
from django.db.models import Q, Max, F

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ValidationError

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny

from .models import *
from .serializers import *
from .permissions import IsAuthenticatedForPostPatchDelete

import requests
import json
from datetime import datetime, time
from urllib.parse import urlencode


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
            queryset = queryset.filter(created_at__range=(start_date, end_date))
        elif start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        elif end_date:
            queryset = queryset.filter(created_at__lte=end_date)

        queryset = queryset.order_by('priority')

        return queryset


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
        slug = self.request.GET.get('slug')

        if slug:
            queryset = queryset.filter(slug=slug)

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

        queryset = queryset.order_by('priority')
        
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

    # Extract start_date and end_date from the request
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

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

    models_to_count = [
        (CategoryModel, 'Total Category'),
        (Services, 'Total Services'),
        (Blog, 'Total Blog'),
        (HeroOffer, 'Total HeroOffer'),
        (BrandAndProduct, 'Total Product'),
        (ServiceItem, 'Total Service Page'),
        (SubcategoryModel, 'Total Subcategory'),
        (ChildCategoryModel, 'Total ChildCategory'),
    ]

    for model, custom_name in models_to_count:
        queryset = model.objects.all()
        
        if start_date and end_date:
            queryset = queryset.filter(created_at__range=(start_date, end_date))
        elif start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        elif end_date:
            queryset = queryset.filter(created_at__lte=end_date)

        count = queryset.count()
        result[custom_name] = count

    return JsonResponse(result)

class GalleryimageListCreateAPIView(generics.ListCreateAPIView):
    queryset = Galleryimage.objects.all().order_by('-created_at')
    serializer_class = GalleryImageSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedForPostPatchDelete]

class GalleryimageRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Galleryimage.objects.all()
    serializer_class = GalleryImageSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedForPostPatchDelete]


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
        category_slug = self.request.query_params.get('category_slug', None)

        if category_slug:
            try:
                category = CategoryModel.objects.get(slug=category_slug)
                queryset = queryset.filter(categories=category)
            except CategoryModel.DoesNotExist:
                queryset = queryset.none()
                
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

class SubcategoryModelListCreateView(generics.ListCreateAPIView):
    queryset = SubcategoryModel.objects.all()
    serializer_class = SubcategoryModelSerializer
    permission_classes = [IsAuthenticatedForPostPatchDelete]

    def get_queryset(self):
        queryset = SubcategoryModel.objects.filter(category__status='active')
        category_id = self.request.query_params.get('category_id')  # Filter by category ID

        if category_id:
            queryset = queryset.filter(category__id=category_id)

        category_slug = self.request.query_params.get('category_slug')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

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


class ChildCategoryModelListCreateView(generics.ListCreateAPIView):
    serializer_class = ChildCategoryModelSerializer
    permission_classes = [IsAuthenticatedForPostPatchDelete]

    def get_queryset(self):
        queryset = ChildCategoryModel.objects.all()  # Define the base queryset here

        subcategory_id = self.request.query_params.get('subcategory_id')  # Filter by subcategory ID
        if subcategory_id:
            queryset = queryset.filter(subcategory__id=subcategory_id)

        category_slug = self.request.query_params.get('category_slug')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
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




class ServiceSetPagination(PageNumberPagination):
    page_size = 20  # Number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 100

class ServicesListCreateView(generics.ListCreateAPIView):
    queryset = Services.objects.all()
    serializer_class = ServicesSerializer
    permission_classes = [IsAuthenticatedForPostPatchDelete]
    pagination_class = ServiceSetPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        
        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')
        slug = self.request.GET.get('slug')  # Get the slug from the request
        search_query = self.request.GET.get('search')
        search_type = self.request.GET.get('search_type')

        if slug:
            # Adjust this filter to correctly reflect your model relationships
            queryset = queryset.filter(
                Q(childcategory__subcategory__category__slug=slug) |
                Q(subcategory__category__slug=slug) |
                Q(categories__slug=slug)
            )

        if search_query and search_type:
            if search_type == 'service_name':
                queryset = queryset.filter(Q(service_name__icontains=search_query))
            elif search_type == 'category':
                queryset = queryset.filter(Q(categories__name__icontains=search_query))
            elif search_type == 'subcategory':
                queryset = queryset.filter(Q(subcategory__name__icontains=search_query))
            elif search_type == 'childcategory':
                queryset = queryset.filter(Q(childcategory__name__icontains=search_query))
            elif search_type == 'servid':
                # Ensure search_query is a valid integer for servid search
                try:
                    servid_query = int(search_query)
                    queryset = queryset.filter(servid=servid_query)
                except ValueError:
                    # If search_query is not an integer, skip the servid filter
                    pass


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

        queryset = queryset.order_by('priority')

        return queryset.order_by('priority')

    def perform_create(self, serializer):
        childcategory = serializer.validated_data.get('childcategory')

        if childcategory:
            # If childcategory is provided, calculate the new priority
            max_priority = Services.objects.filter(childcategory=childcategory).aggregate(Max('priority'))['priority__max'] or 0
            new_priority = max_priority + 1
            # Save with the calculated priority
            serializer.save(priority=new_priority)
        else:
            # If childcategory is not provided, save without modifying priority
            serializer.save()

class AdminServiceSearch(generics.ListAPIView):
    search_fields = ['service_name']
    queryset = Services.objects.all()
    serializer_class = ServicesSerializer
    permission_classes = [IsAuthenticatedForPostPatchDelete]
    pagination_class = ServiceSetPagination

class ServicesRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Services.objects.all()
    serializer_class = ServicesSerializer
    permission_classes = [IsAuthenticatedForPostPatchDelete]

    def perform_update(self, serializer):
        childcategory = serializer.validated_data.get('childcategory')

        if childcategory:
            max_priority = Services.objects.filter(childcategory=childcategory).aggregate(Max('priority'))['priority__max'] or 0
            new_priority = max_priority + 1
            serializer.save(priority=new_priority)
        else:
            serializer.save()

class ServicesuserListCreateView(generics.ListCreateAPIView):
    queryset = Services.objects.all()
    serializer_class = ServicesuserSerializer
    permission_classes = [permissions.AllowAny]  


    def get_queryset(self):
        queryset = super().get_queryset()
        
        category_slug = self.request.query_params.get('category_slug')
        
        if category_slug:
            # Filter the services based on the category slug
            queryset = queryset.filter(categories__slug=category_slug)
    
        return queryset.order_by('priority')

    def perform_create(self, serializer):
        serializer.save()


class BaseNormalPriorityUpdateView(generics.UpdateAPIView):
    field_name = 'priority'  # Default field name for priority
    permission_classes = [IsAuthenticatedForPostPatchDelete]


    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        new_priority = request.data.get(self.field_name)

        if new_priority is not None:
            new_priority = int(new_priority)

            if new_priority >= 0:  # Check if the priority is non-negative
                with transaction.atomic():
                    max_priority = self.get_max_priority()

                    if new_priority > max_priority:
                        new_priority = max_priority

                    self.update_priority(instance, new_priority, self.field_name)
                    serializer = self.get_serializer(instance)
                    return Response(serializer.data)
            else:
                return Response({"detail": f"{self.field_name.capitalize()} must be a non-negative integer."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": f"{self.field_name.capitalize()} is required in the request data."}, status=status.HTTP_400_BAD_REQUEST)

    def get_max_priority(self):
        max_priority = self.queryset.aggregate(Max(self.field_name))[f'{self.field_name}__max']
        return max_priority if max_priority is not None else 0

    def update_priority(self, instance, new_priority, field_name):
        with transaction.atomic():
            # Lock the rows based on the field_name
            items = self.queryset.select_for_update().all()

            old_priority = getattr(instance, field_name)

            # Temporarily set the priority of the instance to the new_priority
            setattr(instance, field_name, new_priority)
            instance.save(update_fields=[field_name])

            if new_priority < old_priority:
                # If the object is moving up in priority, increment the priorities of the objects with lesser or equal priority
                objects_to_update = items.filter(**{f'{field_name}__lt': old_priority, f'{field_name}__gte': new_priority}).order_by('-' + field_name)
                objects_to_update.update(**{field_name: F(field_name) + 1})

            elif new_priority > old_priority:
                # If the object is moving down in priority, decrement the priorities of the objects in between
                objects_to_update = items.filter(**{f'{field_name}__gt': old_priority, f'{field_name}__lte': new_priority}).order_by(field_name)
                objects_to_update.update(**{field_name: F(field_name) - 1})

            # Set the priority of the instance to the new_priority
            setattr(instance, field_name, new_priority)
            instance.save(update_fields=[field_name])



class ServicesPriorityUpdateView(BaseNormalPriorityUpdateView):
    queryset = Services.objects.all()
    serializer_class = ServicesSerializer
    field_name = 'priority' 


class HeroOfferPriorityUpdateView(BaseNormalPriorityUpdateView):
    queryset = HeroOffer.objects.all()
    serializer_class = HeroOfferSerializer
    field_name = 'priority'  


def add_30_minutes(time_str):
    if len(time_str) != 4:
        raise ValueError('Time must be in HHMM format')

    hours = int(time_str[:2])
    minutes = int(time_str[2:])

    minutes += 30

    if minutes >= 60:
        minutes -= 60
        hours += 1

    if hours >= 24:
        hours = 0

    return f"{hours:02d}{minutes:02d}"
class BookingAWTView(generics.ListCreateAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = BookingAWTSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Handle customer creation or update
            if serializer.validated_data.get('is_register'):
                customer = Customer.objects.filter(mobile_number=serializer.validated_data['mobile_number']).first()
                if not customer:
                    return Response({'error': 'Customer with this mobile number does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                customer_data = {
                    'mobile_number': serializer.validated_data['mobile_number'],
                    'email': serializer.validated_data.get('email', ''),
                    'first_name': serializer.validated_data.get('first_name', ''),
                    'last_name': serializer.validated_data.get('last_name', ''),
                    'birth_date': serializer.validated_data.get('birth_date', None),
                    'anniversary_date': serializer.validated_data.get('anniversary_date', None),
                    'gender': serializer.validated_data.get('gender', ''),
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
                service = Services.objects.filter(servid=service_servid).first()
                if service:
                    services.append({
                        'service_id': service_servid,
                        'service_name': service.service_name,
                        'price': float(service.price)
                    })
                    total += service.price
                else:
                    service_fetching_errors.append(f"Service with servid {service_servid} does not exist.")

            if service_fetching_errors:
                return Response({'service_errors': service_fetching_errors}, status=status.HTTP_400_BAD_REQUEST)
            
            expected_start_time = serializer.validated_data.get('expectedStartTime', "")
            expected_end_time = add_30_minutes(expected_start_time)

            # Prepare the CRM API parameters with transformed service IDs
            param_data = {
                "clientInDate": serializer.validated_data['appointment_date'].strftime("%d/%m/%Y %H:%M"),
                "waitCode": "S",
                "waitTimeCode": "S",
                "comments": "",
                "bookedDate": serializer.validated_data['appointment_date'].strftime("%d/%m/%Y"),
                "expectedStartTime": expected_start_time,
                "expectedEndTime": expected_end_time,
                "clientId": serializer.validated_data['mobile_number'],
                "employeeId1": "0"
            }
            print(param_data)
            # Dynamically assign service IDs to the param_data
            for i, service_id in enumerate(service_ids, start=1):
                param_data[f"serviceId{i}"] = str(service_id)

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
                    'is_register': serializer.validated_data.get('is_register', ''),
                    'mobile_number': customer.mobile_number,
                    'email': customer.email,
                    'first_name': customer.first_name,
                    'last_name': customer.last_name,
                    'birth_date': customer.birth_date.strftime("%d/%m/%Y 00:00") if customer.birth_date else None,
                    'anniversary_date': customer.anniversary_date.strftime("%d/%m/%Y 00:00") if customer.anniversary_date else None,
                    'gender': customer.gender
                },
                'appointment_date': serializer.validated_data['appointment_date'].strftime("%Y-%m-%d"),
                'expectedStartTime': serializer.validated_data.get('expectedStartTime', ''),
                'expectedEndTime': serializer.validated_data.get('expectedEndTime', ''),
                'services': services,
                'total': float(total),  # Convert Decimal to float
                'crm_url': crm_url
            }

            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookingACView(generics.ListCreateAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = BookingACSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data

            # Prepare customer data
            customer_data = {
                'mobile_number': validated_data.get('mobile_number'),
                'email': validated_data.get('email'),
                'first_name': validated_data.get('first_name'),
                'last_name': validated_data.get('last_name'),
                'birth_date': validated_data.get('birth_date'),
                'anniversary_date': validated_data.get('anniversary_date'),
                'gender': validated_data.get('gender'),
            }

            # Create or update customer
            customer, created = Customer.objects.update_or_create(
                mobile_number=validated_data['mobile_number'],
                defaults=customer_data
            )

            # Prepare CRM API parameters
            ac_param_data = {
                "clientId": validated_data['mobile_number'],
                "firstName": validated_data.get('first_name', ""),
                "lastName": validated_data.get('last_name', ""),
                "email": validated_data.get('email', ""),
                "mobileNumber": validated_data['mobile_number'],
                "gender": validated_data.get('gender', ""),
                "category": validated_data.get('category', "Regular"),
                "referralType": validated_data.get('referral_type', "Friend")
            }
            ac_encoded_params = urlencode({"Param": json.dumps(ac_param_data)})

            crm_ac_url = f"http://app.salonspa.in/book/bridge.ashx?key=gangatsw&cmd=AC&{ac_encoded_params}"

            # Send data to CRM API
            try:
                crm_ac_response = requests.get(crm_ac_url)
                crm_ac_response.raise_for_status()
            except requests.RequestException as e:
                return Response({'error': f'Failed to send data to CRM (AC): {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            print(customer.anniversary_date)
            print(customer.birth_date)
            # Prepare and return the response data
            response_data = {
                'customer': {
                    'id': customer.id,
                    'mobile_number': customer.mobile_number,
                    'email': customer.email,
                    'first_name': customer.first_name,
                    'last_name': customer.last_name,
                    'gender': customer.gender
                },
                'crm_ac_url': crm_ac_url
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ContactUsListCreateView(generics.ListCreateAPIView):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer
    permission_classes = [AllowAny]


import csv
import pandas as pd
from rest_framework.views import APIView
from django.utils.encoding import smart_str
from django.http import HttpResponse
from django.db import transaction
from rest_framework.parsers import MultiPartParser


class ServicesExportCSVView(APIView):
    permission_classes = [AllowAny]  # Allow access to all users
    
    def get(self, request, *args, **kwargs):
        queryset = Services.objects.all()
        serializer = ServicesSerializer(queryset, many=True)

        # Access the fields of the base serializer (not the ListSerializer)
        fields = [field for field in serializer.child.fields]  # Access child fields
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="services.csv"'
        
        writer = csv.writer(response)
        writer.writerow(fields)  # Write header row

        for item in serializer.data:
            writer.writerow([item.get(field) for field in fields])  # Write data rows

        return response


class ServicesImportCSVView(APIView):
    parser_classes = [MultiPartParser]
    authentication_classes = []  # Remove authentication if needed
    permission_classes = []      # Remove permission requirements if needed

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        if not file:
            return JsonResponse({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

        uploaded_data = []  # List to hold successfully processed data
        failed_data = []    # List to hold data that failed

        try:
            with transaction.atomic():
                # Remove BOM if present
                file_content = file.read()
                if file_content[:3] == b'\xef\xbb\xbf':  # Check for BOM (UTF-8 with BOM)
                    file_content = file_content[3:]  # Remove BOM
                csv_file = file_content.decode('utf-8').splitlines()
                reader = csv.DictReader(csv_file)

                childcategory_is_nullable = False  # Flag to track if childcategory can be null

                # First pass through the file to check for any null childcategory
                for row in reader:
                    childcategory = row.get('childcategory')
                    if not childcategory:  # If the childcategory is empty or null
                        childcategory_is_nullable = True
                # Reset the reader since we've already read it once
                file.seek(0)
                reader = csv.DictReader(csv_file)

                for row in reader:
                    service_name = row.get('service_name')
                    price = row.get('price')
                    servid = row.get('servid')

                    # Ensure `id` or foreign keys are not empty or invalid
                    childcategory = row.get('childcategory') if childcategory_is_nullable else row.get('childcategory') or None
                    subcategory = row.get('subcategory')
                    categories = row.get('categories')

                    # Ensure that `id` fields are not empty strings or invalid
                    try:
                        childcategory = int(childcategory) if childcategory else None
                        subcategory = int(subcategory) if subcategory else None
                        categories = int(categories) if categories else None
                    except ValueError:
                        failed_data.append(row)  # Add the current row to failed data
                        continue  # Skip this row and continue with the next one

                    # Attempt to find existing service
                    service = Services.objects.filter(
                        service_name=service_name,
                        price=price,
                        servid=servid,
                        childcategory_id=childcategory,
                        subcategory_id=subcategory,
                        categories_id=categories
                    ).first()

                    serializer_data = {
                        'service_name': service_name,
                        'price': price,
                        'servid': servid,
                        'childcategory': childcategory,
                        'subcategory': subcategory,
                        'categories': categories,
                        'priority': row.get('priority', 0),
                        'description': row.get('description', ''),
                        'image': row.get('image', None)
                    }

                    if service:
                        # Update existing service
                        serializer = ServicesSerializer(service, data=serializer_data, partial=True)
                    else:
                        # Create a new service
                        serializer = ServicesSerializer(data=serializer_data)

                    if serializer.is_valid():
                        saved_service = serializer.save()  # Save the service and get the saved object
                        uploaded_data.append(serializer.data)  # Add the saved data to the response list
                    else:
                        failed_data.append(row)  # Add the current row to failed data if serializer fails
                        continue  # Skip this row and continue with the next one

            # Return the uploaded data and any failed data in the response
            return JsonResponse({
                'status': 'Import successful',
                'uploaded_data': uploaded_data,
                'failed_data': failed_data
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            # If an error occurs, return the data that was uploaded up to that point along with the error
            return JsonResponse({
                'error': str(e),
                'uploaded_data': uploaded_data,
                'failed_data': failed_data
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)