
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="ShopHome"),
    path('about/', views.about, name="AboutUs"),
    path('contact/', views.contact, name="ContactUs"),
    path('tracker/', views.tracker, name="TrackingStatus"),
    path('search/', views.search, name="Search"),
    path('products/', views.productView, name="AllProducts"),
    path('products/<int:myid>/', views.productView, name="ProductView"),
    path('checkout/', views.checkout, name="checkout"),
    path("policy/", views.policy, name="Policy"),
    path(
        "jazzcash-response/", views.jazzcash_response, name="jazzcash_response"
    ),
    # Easypaisa callback route (passes gateway="easypaisa" to the view)
    path(
        "easypaisa-response/",
        views.jazzcash_response,
        {"gateway": "easypaisa"},
        name="easypaisa_response",
    ),
path('shop/mock-jazzcash-gateway/', views.mock_jazzcash_view, name='mock_jazzcash'),
]
