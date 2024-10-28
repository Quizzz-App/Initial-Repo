from django.conf.urls.static import static
from django.urls import path, include
from authenticationSystem import views
from django.conf import settings
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name= 'index'),
    path('about-us', views.aboutUP, name= 'about-us'),
    path('accounts/', include('authenticationSystem.urls')),
    path('payment/', include('paymentSystem.urls')),
    path('ref/', include('referralSystem.urls')),
    path('quizz/', include('questionSystem.urls')),
    path('542b0993-3d6d-450c-89c0-191d6ad5fca6/admin-dev/', include('adminSystem.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
