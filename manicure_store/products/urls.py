from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path("", index, name="index"),
    path("products/", products, name="products"),
    path("contacts/", contacts, name="contacts"),
    path("category/<int:category_id>", products, name="category"),
    path("page/<int:page>", products, name="paginator"),
    path("basket/add/<int:product_id>/", basket_add, name="basket_add"),
    path("basket/remove/<int:basket_id>/", basket_remove, name="basket_remove"),
    path("basket/", basket_views, name="basket"),
    path("send/", send_data_mail, name="send_mail"),




]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)