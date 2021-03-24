from django.urls import include, path
from . import views

urlpatterns = [
    path(r'login', views.auth_page, name="Login"),
    path(r'logout', views.logout, name="Logout"),
    path(r'dashboard', views.dashboard, name="Dashboard"),
    path(r'dashboard/add_user', views.add_user, name="Add User"),
    path(r'dashboard/add_spp', views.add_spp, name="Add SPP"),
    path(r'dashboard/show_spp', views.show_spp, name="Add SPP"),
    path(r'dashboard/edit_spp/<spp_id>',views.edit_spp,name="Get SPP"),
    path(r'dashboard/add_pembayaran', views.add_pembayaran, name="Edit SPP"),
    path(r'dashboard/show_pembayaran', views.show_pembayaran, name="Show Bayar"),
    path(r'dashboard/show_user', views.show_user, name="Show Bayar"),
    path(r'dashboard/edit_user/<id_user>', views.edit_user, name="Show Bayar"),
    path(r'dashboard/generate_laporan', views.generate_laporan, name="Generate Laporam"),
    path(r'dashboard/show_petugas', views.show_petugas, name="Show Petugas"),
    path(r'dashboard/show_siswa', views.show_siswa, name="Show Siswa"),
    path(r'dashboard/edit_petugas/<id_petugas>', views.edit_petugas, name="Edit Petugas"),
    path(r'dashboard/edit_siswa/<nisn>', views.edit_siswa, name="Edit Siswa"),
    path(r'dashboard/add_siswa', views.add_siswa, name="Add Siswa"),
    path(r'dashboard/add_petugas', views.add_petugas, name="Add Siswa"),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework_api'))
]
