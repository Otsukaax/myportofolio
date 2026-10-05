import datetime

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core import serializers
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from main.forms import EducationForm, ExperienceForm
from main.models import Education, Experience, Mahasiswa


def show_main(request):
    last_login = request.COOKIES.get("last_login", "Belum ada sesi login / Cookie tidak ditemukan")
    context = {
        "name": "Azka Nur Jauhar",
        "npm": "2506612410",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "Second-year CS Student at Universitas Indonesia. Passionate about AI, Machine "
            "Learning, and Software Engineering."
        ),
        "mahasiswa_list": Mahasiswa.objects.all(),
        "last_login": last_login,
    }
    return render(request, "index.html", context)


def get_experience_json(request):
    title_query = request.GET.get("title", "").strip()
    experiences = Experience.objects.prefetch_related('starred_by').all()

    if title_query:
        experiences = experiences.filter(title__icontains=title_query)

    # Konstruksi data JSON secara manual agar bisa menyisipkan logika Star
    data = []
    for exp in experiences:
        starred_users = exp.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        starred_by_names = ", ".join([u.username for u in starred_users])
        data.append({
            "pk": str(exp.id),
            "fields": {
                "title": exp.title,
                "description": exp.description,
                "category": exp.category,
                "category_display": exp.get_category_display(),
                "thumbnail": exp.thumbnail,
                "is_ongoing": exp.is_ongoing,
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })
    return JsonResponse(data, safe=False)


def show_experience(request):
    title_query = request.GET.get("title", "").strip()
    is_editor = request.user.groups.filter(name='Editor').exists() if request.user.is_authenticated else False

    context = {
        "name": "Azka Nur Jauhar",
        "title_query": title_query,
        "is_editor": is_editor,
        "form": ExperienceForm(),
    }
    return render(request, "experience.html", context)


@login_required(login_url="/login/")
def create_experience(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    form = ExperienceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pengalaman baru berhasil ditambahkan!")
        return redirect("main:show_experience")

    context = {
        "name": "Azka Nur Jauhar",
        "form": form,
    }
    return render(request, "experience_form.html", context)


@require_POST
def create_experience_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan pengalaman."},
            status=403,
        )
    form = ExperienceForm(request.POST)
    if form.is_valid():
        experience = form.save()
        return JsonResponse(
            {"message": "Pengalaman berhasil ditambahkan.", "pk": str(experience.id)},
            status=201,
        )
    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)


@login_required(login_url="/login/")
def update_experience(request, experience_id):
    if not (request.user.is_superuser or request.user.groups.filter(name='Editor').exists()):
        raise PermissionDenied
    experience_item = get_object_or_404(Experience, pk=experience_id)
    form = ExperienceForm(request.POST or None, instance=experience_item)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pengalaman berhasil diperbarui!")
        return redirect("main:show_experience")

    context = {
        "name": "Azka Nur Jauhar",
        "form": form,
        "is_update": True,
    }
    return render(request, "experience_form.html", context)


@login_required(login_url="/login/")
def delete_experience(request, experience_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    experience_item = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        experience_item.delete()
        messages.success(request, "Pengalaman berhasil dihapus!")
        return redirect("main:show_experience")

    return redirect("main:show_experience")


def get_education_json(request):
    search_query = request.GET.get("institution", "").strip()

    # Menggunakan prefetch_related agar hemat query database
    educations = Education.objects.prefetch_related('starred_by').all()
    if search_query:
        educations = educations.filter(institution__icontains=search_query)

    # Urutkan berdasarkan waktu mulai terbaru
    educations = educations.order_by('-started_at')

    # Konstruksi data JSON secara manual agar bisa menyisipkan logika Star
    data = []
    for edu in educations:
        starred_users = edu.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        starred_by_names = ", ".join([u.username for u in starred_users])

        data.append({
            "pk": str(edu.id),
            "fields": {
                "institution": edu.institution,
                "degree": edu.degree,
                "gpa": str(edu.gpa) if edu.gpa is not None else None,
                "started_at": str(edu.started_at),
                "ended_at": str(edu.ended_at) if edu.ended_at else None,
                "is_current": edu.is_current,
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })

    return JsonResponse(data, safe=False)


def show_education(request):
    institution_query = request.GET.get("institution", "").strip()
    is_editor = request.user.groups.filter(name='Editor').exists() if request.user.is_authenticated else False

    context = {
        "name": "Azka Nur Jauhar",
        "institution_query": institution_query,
        "is_editor": is_editor,
        "form": EducationForm(),
    }
    return render(request, "education.html", context)


@login_required(login_url="/login/")
def create_education(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    form = EducationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Riwayat pendidikan baru berhasil ditambahkan!")
        return redirect("main:show_education")

    context = {
        "name": "Azka Nur Jauhar",
        "form": form,
    }
    return render(request, "education_form.html", context)


@require_POST
def create_education_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan riwayat pendidikan."},
            status=403,
        )
    form = EducationForm(request.POST)
    if form.is_valid():
        education_entry = form.save()
        return JsonResponse(
            {"message": "Riwayat pendidikan berhasil ditambahkan!", "pk": str(education_entry.id)},
            status=201,
        )
    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)


@login_required(login_url="/login/")
def delete_education(request, education_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    education_item = get_object_or_404(Education, pk=education_id)

    if request.method == "POST":
        education_item.delete()
        messages.success(request, "Riwayat pendidikan berhasil dihapus!")
        return redirect("main:show_education")

    return redirect("main:show_education")


def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "Azka Nur Jauhar",
        "form": form,
    }
    return render(request, "register.html", context)


def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        response = redirect("main:show_main")
        response.set_cookie("last_login", str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        return response

    context = {
        "name": "Azka Nur Jauhar",
        "form": form,
    }
    return render(request, "login.html", context)


def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie("last_login")
    return response


@login_required(login_url="/login/")
def toggle_experience_star(request, experience_id):
    experience_item = get_object_or_404(Experience, pk=experience_id)
    if request.method == "POST":
        if request.user in experience_item.starred_by.all():
            experience_item.starred_by.remove(request.user)
        else:
            experience_item.starred_by.add(request.user)
    return redirect("main:show_experience")


@login_required(login_url="/login/")
def toggle_education_star(request, education_id):
    education_item = get_object_or_404(Education, pk=education_id)
    if request.method == "POST":
        if request.user in education_item.starred_by.all():
            education_item.starred_by.remove(request.user)
        else:
            education_item.starred_by.add(request.user)
    return redirect("main:show_education")
