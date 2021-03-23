from django.db import models
from django.contrib.auth.models import AbstractUser
from mokletsppfix import settings
# Create your models here.


class CustomUserAkun(AbstractUser):
    id_user = models.AutoField(primary_key=True)
    role = models.CharField(blank=True, max_length=255)

    class Meta:
        db_table = "tb_user"


class Petugas(models.Model):
    id_petugas = models.AutoField(primary_key=True)
    nama_petugas = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey(CustomUserAkun, on_delete=models.CASCADE, blank=True, default="")

    class Meta:
        db_table = "tb_petugas"


class Spp(models.Model):
    id_spp = models.AutoField(primary_key=True)
    tahun = models.IntegerField(blank=True)
    bulan = models.IntegerField(blank=True)
    nominal = models.IntegerField(blank=True)
    petugas = models.ForeignKey(Petugas, on_delete=models.SET(""), default="")

    class Meta:
        db_table = "tb_spp"


class Siswa(models.Model):
    nisn = models.CharField(max_length=255,primary_key=True)
    nis = models.CharField(max_length=255, blank=True)
    nama_siswa = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey(CustomUserAkun, on_delete=models.CASCADE, blank=True, default="")

    class Meta:
        db_table = "tb_siswa"


class Pembayaran(models.Model):
    id_pembayaran = models.AutoField(primary_key=True)
    siswa = models.ForeignKey(Siswa, on_delete=models.SET(""), blank=True, default="")
    tgl_bayar = models.DateTimeField(auto_now=True)
    jumlah_bayar = models.IntegerField(blank=True)
    status = models.CharField(max_length=255, default='menunggu')
    spp = models.ForeignKey(Spp, on_delete=models.CASCADE, blank=True, default="")
    bukti_bayar = models.FileField(upload_to=settings.MEDIAUPLOAD_URL, blank=True)

    class Meta:
        db_table = "tb_pembayaran"

