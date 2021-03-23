from rest_framework import viewsets, permissions, response
from . import json_response
from .serializers import *


# Create your views here.
# -- AUTH PAGE --


# --- PETUGAS PAGE ---

class UpdateUserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UpdateUserSerializers
    queryset = CustomUserAkun.objects.all()


class PetugasViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = PetugasSerializers

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return response.Response(json_response.success_response("Menambah Data Berhasil"))
        except Exception as e:
            print(e)
            return response.Response(json_response.error_response("Menambah Data Gagal"))

    def get_queryset(self):
        return Petugas.objects.all()

    def list(self, request, *args, **kwargs):
        all_petugas = Petugas.objects.all()
        user_req = self.request.user
        user = CustomUserAkun.objects.get(id_user=user_req.id_user)
        if user.role == 'admin' or user.role == 'petugas':
            serializer = PetugasSerializers(instance=all_petugas, many=True)
            return response.Response(json_response.success_response(serializer.data))
        else:
            return response.Response(json_response.deny_response("Anda Bukan Admin"))


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializers

    def get_queryset(self):
        user = self.request.user
        return CustomUserAkun.objects.filter(id_user=user.id_user)

    def list(self, request, *args, **kwargs):
        instance = request.user
        user = CustomUserAkun.objects.get(id_user=instance.id_user)
        if user is not None:
            serializer = self.get_serializer(user)
            try:
                if user.role == "admin" or user.role == "petugas":
                    data = Petugas.objects.get(user=user)
                    data_profile = {"status": "petugas", "id": data.id_petugas, "nama": data.nama_petugas}
                else:
                    data = Siswa.pbjects.get(user=user)
                    data_profile = {"status": "siswa", "id": data.id_siswa, "nama": data.nama_siswa}
            except Exception as e:
                print(e)
                data_profile = None
            data = {"user": serializer.data, "profile": data_profile}
            return response.Response(json_response.success_response(data))
        else:
            return response.Response(json_response.error_response("User Is Not Authenticated"))


class SppViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SppSerializer

    def get_queryset(self):
        return Spp.objects.all()

    def create(self, request, *args, **kwargs):
        user_req = self.request.user
        user = CustomUserAkun.objects.get(id_user=user_req.id_user)
        if user.role == "admin" or user.role == "petugas":
            try:
                petugas_data = Petugas.objects.get(user=user)
                data = {"tahun": request.data['tahun'], "bulan": request.data['bulan'],
                        "nominal": request.data['nominal'], "petugas": petugas_data.id_petugas}
                serializer = SppSerializer(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return response.Response(json_response.success_response("Menambah Data Berhasil"))
            except Exception as e:
                print(e)
                return response.Response(json_response.error_response("Menambah Data Gagal"))
        else:
            return response.Response(json_response.error_response("Anda Adalah Siswa"))

    def list(self, request, *args, **kwargs):
        user_req = self.request.user
        user = CustomUserAkun.objects.get(id_user=user_req.id_user)
        try:
            if user.role == 'admin' or user.role == 'petugas':
                spp_data = Spp.objects.all()
                serializer = SppSerializer(spp_data, many=True)
                return response.Response(json_response.success_response(serializer.data))
            else:
                return response.Response(json_response.deny_response("Anda Bukan Admin"))
        except Exception as e:
            print(e)
            return response.Response(json_response.deny_response("Gagal Mendapatkan Data"))


class SiswaViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SiswaSerializers
    queryset = Siswa.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return response.Response(json_response.success_response("Menambah Data Berhasil"))
        except Exception as e:
            print(e)
            return response.Response(json_response.error_response("Menambah Data Gagal"))

    def list(self, request, *args, **kwargs):
        get_all_siswa = Siswa.objects.all()
        serializer = SiswaSerializers(get_all_siswa, many=True)
        return response.Response(json_response.success_response(serializer.data))


class PembayaranViewsets(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PembayaranSerializers
    queryset = Pembayaran.objects.all()

    def create(self, request, *args, **kwargs):
        user = CustomUserAkun.objects.get(id_user=request.user.id_user)
        if user.role == "admin" or user.role == "petugas":
            try:
                serializer = PembayaranSerializers(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return response.Response(json_response.success_response("Menambah Data Berhasil"))
            except Exception as e:
                print(e)
                return response.Response(json_response.error_response("Menambah Data Gagal"))
        else:
            try:
                siswa = Siswa.objects.get(user=user)
                data = {'bukti_bayar': request.data['bukti_bayar'], 'siswa': siswa.nisn, 'spp': request.data['spp'],
                        'jumlah_bayar': request.data['jumlah_bayar']}
                serializer = PembayaranSerializers(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return response.Response(json_response.success_response("Menambah Data Berhasil"))
            except Exception as e:
                print(e)
                return response.Response(json_response.error_response("Menambah Data Gagal"))

    def list(self, request, *args, **kwargs):
        user_req = request.user
        user = CustomUserAkun.objects.get(id_user=user_req.id_user)
        if user.role == "admin" or user.role == "petugas":
            try:
                pembayaran = Pembayaran.objects.all()
                serializer = PembayaranSerializers(pembayaran, many=True)
                return response.Response(json_response.success_response(serializer.data))
            except Exception as e:
                print(e)
                return response.Response(json_response.deny_response("Maaf Anda Bukan Petugas"))
        else:
            siswa = Siswa.objects.get(user=user)
            pembayaran = Pembayaran.objects.filter(siswa=siswa)
            serializer = PembayaranSerializers(pembayaran, many=True)
            return response.Response(json_response.success_response(serializer.data))


class AllUserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AddUserSerializer
    queryset = CustomUserAkun.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return response.Response(json_response.success_response("Menambah Data Berhasil"))
        except Exception as e:
            print(e)
            return response.Response(json_response.error_response("Menambah Data Gagal"))

    def list(self, request, *args, **kwargs):
        user_req = request.user.id_user
        user = CustomUserAkun.objects.get(id_user=user_req)
        if user.role == "admin" or user.role == "petugas":
            all_user = CustomUserAkun.objects.all()
            serializer = UserSerializers(all_user, many=True)
            return response.Response(json_response.success_response(serializer.data))
        else:
            return response.Response(json_response.error_response("Anda Bukan Petugas"))


# --- END PETUGAS ---

# --- START SISWA ---

class FetchMySppViewSets(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SppOnlyCountPaidSerializer

    def get_queryset(self):
        return Spp.objects.all()

    def list(self, request, *args, **kwargs):
        exclude_spp = []
        total_spp = []
        total_nominal_pembayaran = []
        total_all_spp = []
        user_req = self.request.user
        user = CustomUserAkun.objects.get(id_user=user_req.id_user)
        if user.role == "siswa":
            siswa = Siswa.objects.get(user=user_req)
            pembayaran_angsuran = Pembayaran.objects.filter(siswa=siswa).exclude(status="menunggu")
            serialize_pembayaran = PembayaranSerializers(pembayaran_angsuran, many=True)
            for angsuran in pembayaran_angsuran:
                total_nominal_pembayaran.append(angsuran.jumlah_bayar)
            pembayaran = Pembayaran.objects.filter(siswa=siswa).filter(status="dikonfirmasi")
            for p in pembayaran:
                exclude_spp.append(p.spp.id_spp)
            spp = Spp.objects.exclude(id_spp__in=exclude_spp)
            spp_all = Spp.objects.all()
            for s_all in spp_all:
                total_all_spp.append(s_all.nominal)
            serializer = SppOnlyCountPaidSerializer(spp, many=True)
            for s in spp:
                total_spp.append(s.nominal)
            total = sum(total_all_spp) - sum(total_nominal_pembayaran)
            if total < 0:
                total_penjumlahan = 0
            else:
                total_penjumlahan =total
            sisa_spp = {"total_tunggakan": total_penjumlahan, "spp": serializer.data,
                        "pembayaran": serialize_pembayaran.data}
            return response.Response(json_response.success_response(sisa_spp))
        else:
            return response.Response(json_response.error_response("Anda Bukan Siswa"))
