import calendar
import datetime
import locale
import xlwt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as logout_user
from django.utils.translation import activate
from mokletspp_backend.models import CustomUserAkun, Spp, Pembayaran, Siswa, Petugas
from mokletsppfix.settings import LOGIN_URL


@login_required(login_url=LOGIN_URL)
def generate_laporan(request):
    user_authenticated = CustomUserAkun.objects.get(id_user=request.user.id_user)
    if user_authenticated.role == "admin" or user_authenticated.role == "petugas":
        response = HttpResponse(content_type='application/ms-excel')
        name_file = f"Data_Pembayaran_{datetime.datetime.now()} "
        response['Content-Disposition'] = f'attachment; filename="{name_file}.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet("Pembayaran")
        row_start = 0
        font_style = xlwt.easyxf('font: bold 1')
        columns = ["No", "Tahun Spp", "Bulan Spp", "Jumlah Yang Dibayar", "Nominal SPP"
            , "NISN", "Status", "Tanggal Bayar"]
        for col_num in range(len(columns)):
            ws.write(row_start, col_num, columns[col_num], font_style)

        font_style = xlwt.XFStyle()
        rows = Pembayaran.objects.all()
        for row in rows:
            row_start += 1
            ws.write(row_start, 0, row_start, font_style)
            ws.write(row_start, 1, row.spp.tahun, font_style)
            ws.write(row_start, 2, row.spp.bulan, font_style)
            ws.write(row_start, 3, row.jumlah_bayar, font_style)
            ws.write(row_start, 4, row.spp.nominal, font_style)
            ws.write(row_start, 5, row.siswa.nisn, font_style)
            ws.write(row_start, 6, row.status, font_style)
            ws.write(row_start, 7, str(row.tgl_bayar), font_style)
        wb.save(response)
        return response
    else:
        return render(dashboard)


@login_required(login_url=LOGIN_URL)
def dashboard(request):
    user = CustomUserAkun.objects.get(id_user=request.user.id_user)
    data = {'authenticated': user}
    return render(request, 'dashboard.html', data)


def auth_page(request):
    data = {}
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username and password is not None:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(dashboard)

    return render(request, 'login.html', data)


@login_required(login_url=LOGIN_URL)
def add_user(request):
    data = {}
    return render(request, 'registeruser_form.html', data)


def logout(request):
    logout_user(request)
    return redirect(auth_page)


@login_required(login_url=LOGIN_URL)
def edit_user(request, id_user):
    user_authenticated = CustomUserAkun.objects.get(id_user=request.user.id_user)
    data = {'authenticated': user_authenticated}
    if user_authenticated.role == "admin":
        user_data = CustomUserAkun.objects.get(id_user=id_user)
        data['user'] = user_data
        return render(request, 'edituser_form.html', data)
    else:
        return redirect(dashboard)


@login_required(login_url=LOGIN_URL)
def show_user(request):
    user_data = CustomUserAkun.objects.get(id_user=request.user.id_user)
    if user_data.role == "admin":
        all_user = CustomUserAkun.objects.all()
        data = {"authenticated": user_data, "user": all_user}
        return render(request, 'show_user.html', data)
    else:
        data = {"authenticated": user_data, "user": None}
        return render(request, 'show_user.html', data)


@login_required(login_url=LOGIN_URL)
def add_spp(request):
    user = CustomUserAkun.objects.get(id_user=request.user.id_user)
    locale.setlocale(locale.LC_ALL, 'id_ID')
    activate("id")
    now_date = datetime.datetime.now()
    data_month = filter(None, calendar.month_name)
    range_year = range(2010, 2099)
    data = {"months": data_month, "date_now": now_date, "range_year": range_year, "authenticated": user}
    return render(request, 'addspp_form.html', data)


@login_required(login_url=LOGIN_URL)
def show_spp(request):
    data_user = CustomUserAkun.objects.get(id_user=request.user.id_user)
    data = {'authenticated': data_user}
    if data_user.role == "admin" or data_user.role == "petugas":
        try:
            all_spp = Spp.objects.all()
            data['spp'] = all_spp
        except Exception as e:
            print(e)
            data['spp'] = None
    return render(request, 'show_spp.html', data)


@login_required(login_url=LOGIN_URL)
def edit_spp(request, spp_id):
    user = CustomUserAkun.objects.get(id_user=request.user.id_user)
    data_spp = Spp.objects.get(id_spp=spp_id)
    locale.setlocale(locale.LC_ALL, 'id_ID')
    activate("id")
    now_date = datetime.datetime.now()
    data_month = list(filter(None, calendar.month_name))
    range_year = range(2010, 2099)
    data = {'authenticated': user, "spp": data_spp, "months": data_month, "date_now": now_date,
            "range_year": range_year, 'selected_month': data_month[data_spp.bulan - 1]}

    return render(request, 'editspp_form.html', data)


@login_required(login_url=LOGIN_URL)
def add_pembayaran(request):
    user = CustomUserAkun.objects.get(id_user=request.user.id_user)
    if user.role == 'siswa':
        list_idspp = []
        siswa = Siswa.objects.get(user=user)
        pembayaran_angsuran = Pembayaran.objects.filter(siswa=siswa).filter(status="dikonfirmasi")
        for x in pembayaran_angsuran:
            list_idspp.append(x.spp.id_spp)
        all_spp = Spp.objects.exclude(id_spp__in=list_idspp)
        data = {'authenticated': user, "spp": all_spp}
        return render(request, 'addpembayaran_form.html', data)
    else:
        all_siswa = Siswa.objects.all()
        all_spp = Spp.objects.all()
        data = {'authenticated': user, "spp": all_spp, "siswa": all_siswa}
        return render(request, 'addpembayaran_form.html', data)


@login_required(login_url=LOGIN_URL)
def show_pembayaran(request):
    user = CustomUserAkun.objects.get(id_user=request.user.id_user)
    data = {'authenticated': user}
    if user.role == "siswa":
        try:
            siswa = Siswa.objects.get(user=user)
            pembayaran_angsuran = Pembayaran.objects.filter(siswa=siswa)
            data['pembayaran'] = pembayaran_angsuran
            return render(request, 'show_pembayaran.html', data)
        except Exception as e:
            print(e)
            data['pembayaran'] = None
            return render(request, 'show_pembayaran.html', data)
    else:
        pembayaran_angsuran = Pembayaran.objects.all()
        data['pembayaran'] = pembayaran_angsuran
        return render(request, 'show_pembayaran.html', data)


@login_required(login_url=LOGIN_URL)
def show_petugas(request):
    user = CustomUserAkun.objects.get(id_user=request.user.id_user)
    data = {'authenticated': user}
    if user.role == "admin":
        petugas = Petugas.objects.all()
        data['petugas'] = petugas
        return render(request, 'showpetugas.html', data)
    else:
        return redirect(dashboard)


@login_required(login_url=LOGIN_URL)
def edit_petugas(request, id_petugas):
    user = CustomUserAkun.objects.get(id_user=request.user.id_user)
    data = {'authenticated': user}
    if user.role == "admin":
        petugas = Petugas.objects.get(id_petugas=id_petugas)
        data['petugas'] = petugas
        return render(request, 'editpetugas_form.html', data)
    else:
        return redirect(dashboard)


@login_required(login_url=LOGIN_URL)
def show_siswa(request):
    user = CustomUserAkun.objects.get(id_user=request.user.id_user)
    data = {'authenticated': user}
    if user.role == "admin" or user.role == "petugas":
        siswa = Siswa.objects.all()
        data['siswa'] = siswa
        return render(request, 'showsiswa.html', data)
    else:
        return redirect(dashboard)


@login_required(login_url=LOGIN_URL)
def add_siswa(request):
    user = CustomUserAkun.objects.get(id_user=request.user.id_user)
    data = {'authenticated': user}
    if user.role == "siswa":
        return render(request, 'add_siswa.html', data)
    else:
        return redirect(dashboard)


@login_required(login_url=LOGIN_URL)
def add_petugas(request):
    user = CustomUserAkun.objects.get(id_user=request.user.id_user)
    data = {'authenticated': user}
    if user.role == "petugas" or user.role == "admin":
        return render(request, 'addpetugas.html', data)
    else:
        return redirect(dashboard)

@login_required(login_url=LOGIN_URL)
def edit_siswa(request, nisn):
    user = CustomUserAkun.objects.get(id_user=request.user.id_user)
    data = {'authenticated': user}
    if user.role == "admin":
        petugas = Siswa.objects.get(nisn=nisn)
        data['siswa'] = petugas
        return render(request, 'editsiswa_form.html', data)
    else:
        return redirect(dashboard)
