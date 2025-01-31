from django.urls import path
from .views import *

urlpatterns = [
    path('categories/', CategoryModelListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryModelRetrieveUpdateDestroyView.as_view(), name='category-detail'),

    path('blogs/', BlogListCreateView.as_view(), name='blog-list-create'),
    path('blogs/<int:pk>/', BlogRetrieveUpdateDestroyView.as_view(), name='blog-detail'),

    path('dashboard/', DashboardView, name='dashboard'),

    path('hero-offers/', HeroOfferListCreateView.as_view(), name='hero-offer-list-create'),
    path('hero-offers/<int:pk>/', HeroOfferRetrieveUpdateDestroyView.as_view(), name='hero-offer-detail'),

    path('gallery-image/',GalleryimageListCreateAPIView.as_view(), name='galleyimage'),
    path('gallery-image/<int:pk>/',GalleryimageRetrieveUpdateDestroyAPIView.as_view(), name='gallery-details'),

    path('haircategories/', HairCategoryListCreateAPIView.as_view(), name='haircategory-list-create'),
    path('haircategories/<int:pk>/', HairCategoryRetrieveUpdateDestroyAPIView.as_view(), name='haircategory-detail'),

    path('hairservices/', HairServiceListCreateAPIView.as_view(), name='hairservice-list-create'),
    path('hairservices/<int:pk>/', HairServiceRetrieveUpdateDestroyAPIView.as_view(), name='hairservice-detail'),

    path('massagecategories/', MassageCategoryListCreateAPIView.as_view(), name='massagecategory-list-create'),
    path('massagecategories/<int:pk>/', MassageCategoryRetrieveUpdateDestroyAPIView.as_view(), name='massagecategory-detail'),

    path('massageservices/', MassageServiceListCreateAPIView.as_view(), name='hairservice-list-create'),
    path('massageservices/<int:pk>/', MassageServiceRetrieveUpdateDestroyAPIView.as_view(), name='hairservice-detail'),

    path('unisexcategories/', UnisexCategoryListCreateAPIView.as_view(), name='unisexcategory-list-create'),
    path('unisexcategories/<int:pk>/', UnisexCategoryRetrieveUpdateDestroyAPIView.as_view(), name='unisexcategory-detail'),

    path('unisexservices/', UnisexServiceListCreateAPIView.as_view(), name='unisexservice-list-create'),
    path('unisexservices/<int:pk>/', UnisexServiceRetrieveUpdateDestroyAPIView.as_view(), name='unisexservice-detail'),

    path('service-items/', ServiceItemListCreate.as_view(), name='service-item-list-create'),
    path('service-items/<int:pk>/', ServiceItemRetrieveUpdateDestroy.as_view(), name='service-item-retrieve-update-destroy'),

    path('brands/', BrandAndProductListCreate.as_view(), name='brand-list-create'),
    path('brands/<int:pk>/', BrandAndProductRetrieveUpdateDestroy.as_view(), name='brand-retrieve-update-destroy'),
    
    path('mulimage/', MulImageListView.as_view(), name="mulimage-list"),
    path('salon/<int:salon_id>/mulimage/<int:mul_image_id>/', MulImageView.as_view(), name="salon-mul-image"),
    path('mulimage/<id>/', MulImageView.as_view(), name="mulimage"),

    path('subcategory/', SubcategoryModelListCreateView.as_view(), name='subcategory-list-create'),
    path('subcategory/<int:pk>/', SubcategoryModelDetailView.as_view(), name='subcategory-detail'),

    path('childcategory/', ChildCategoryModelListCreateView.as_view(), name='childcategory-list-create'),
    path('childcategory/<int:pk>/', ChildCategoryModelDetailView.as_view(), name='childcategory-detail'),

    path('services/', ServicesListCreateView.as_view(), name='services-list-create'),
    path('services/<int:pk>/', ServicesRetrieveUpdateDestroyView.as_view(), name='services-detail'),

    path('servicesuser/', ServicesuserListCreateView.as_view(), name='services-list-create'),
    path('search-service/', AdminServiceSearch.as_view(), name='admin-service-search'),


    path('bookingawt/', BookingAWTView.as_view(), name='booking'),
    path('bookingac/', BookingACView.as_view(), name='booking'),


    path('services/<int:pk>/update-priority/', ServicesPriorityUpdateView.as_view(), name='services-update-priority'),
    path('hero-offers/<int:pk>/update-priority/', HeroOfferPriorityUpdateView.as_view(), name='hero-offer-update-priority'),
    path('category/<int:pk>/update-priority/', CategoryPriorityUpdateView.as_view(), name='category-update-priority'),
    path('subcategory/<int:pk>/update-priority/', SubcategoryPriorityUpdateView.as_view(), name='subcategory-update-priority'),
    path('childcategory/<int:pk>/update-priority/', ChildCategoryPriorityUpdateView.as_view(), name='childcategory-update-priority'),


    path('contact-us/', ContactUsListCreateView.as_view(), name='contact_us_list_create'),

    path('services/export-csv/', ServicesExportCSVView.as_view(), name='services_export_csv'),
    path('services/import-csv/', ServicesImportCSVView.as_view(), name='services_import_csv'),

    path('titles/', TitlesListCreateView.as_view(), name='titles-list-create'),  # List all & create a title
    path('titles/<int:pk>/', TitlesRetrieveUpdateDeleteView.as_view(), name='titles-detail'),
]