from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "Apilix admin"
admin.site.site_title = "Apilix admin"
admin.site.index_title = "Hub management"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("catalog.urls")),
    path("api-auth/", include("rest_framework.urls")),  # login/logout for the browsable API
]
