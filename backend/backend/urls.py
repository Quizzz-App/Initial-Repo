from django.conf.urls.static import static
from django.urls import path, include, re_path
from authenticationSystem import views
from adminSystem.views import getSiteAnalytics, continueTransaction
from django.conf import settings
from django.contrib import admin
from django.views.static import serve


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name= 'index'),
    path('about-us', views.aboutUP, name= 'about-us'),
     path('features', views.featuresPage, name= 'features'),
    path('accounts/', include('authenticationSystem.urls')),
    path('payment/', include('paymentSystem.urls')),
    path('ref/', include('referralSystem.urls')),
    path('quizz/', include('questionSystem.urls')),
    path('site-analytics', getSiteAnalytics, name='site-analytics'),
    path('verify-transaction/', continueTransaction, name= 'verify-transaction'),
    path('542b0993-3d6d-450c-89c0-191d6ad5fca6/admin-dev/', include('adminSystem.urls')),
    re_path(r'^media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$',serve,{'document_root':settings.STATIC_ROOT}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
