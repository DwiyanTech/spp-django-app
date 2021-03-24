from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'petugas', views.PetugasViewSet, basename="Petugas")
router.register(r'myaccount', views.UserViewSet, basename="MyAccount")
router.register(r'pembayaran',views.PembayaranViewsets,basename="Pemabayaran")
router.register(r'siswa',views.SiswaViewSet,basename="Siswa")
router.register(r'spp',views.SppViewSet,basename="Spp")
router.register(r'users', views.AllUserViewSet, basename="User")
router.register(r'currentmyspp', views.FetchMySppViewSets, basename="MyCurrentSpp")
router.register(r'update_petugas', views.UpdatePetugasViewSet, basename="MyUpdatePetugas")
router.register(r'update_user', views.UpdateUserViewSet, basename="MyUpdateSpp")
router.register(r'update_siswa', views.UpdateSiswaViewSet, basename="MyUpdateSiswa")

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]