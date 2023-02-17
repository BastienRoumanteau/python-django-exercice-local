from django.urls import path, include

from rest_framework import routers
from sales import urls as salesUrl


router = routers.DefaultRouter(trailing_slash=False)

urlpatterns = [
    path(
        "v1/",
        include(
            [
                path("", include(router.urls)),
                # path('api-auth/', include('rest_framework.urls')),
                path("sales/", include(salesUrl))
            ]
        ),
    )
]
