import datetime

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core import serializers
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

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
    experience_list = Experience.objects.all()

    if title_query:
        experience_list = experience_list.filter(title__icontains=title_query)

    experience_json = serializers.serialize("json", experience_list, use_natural_foreign_keys=True)
    return HttpResponse(experience_json, content_type="application/json")


def show_experience(request):
    json_response = get_experience_json(request)

    deserialized_experiences = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    experience_list = [exp_entry.object for exp_entry in deserialized_experiences]
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Azka Nur Jauhar",
        "experience_list": experience_list,
        "title_query": title_query,
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


@login_required(login_url="/login/")
def update_experience(request, experience_id):
    if not request.user.is_superuser:
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
    education_list = Education.objects.all()

    if search_query:
        education_list = education_list.filter(institution__icontains=search_query)

    education_json = serializers.serialize("json", education_list, use_natural_foreign_keys=True)
    return HttpResponse(education_json, content_type="application/json")


def show_education(request):
    json_response = get_education_json(request)

    deserialized_educations = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    education_list = [education_entry.object for education_entry in deserialized_educations]
    education_list.sort(key=lambda education_entry: education_entry.started_at, reverse=True)
    institution_query = request.GET.get("institution", "").strip()

    context = {
        "name": "Azka Nur Jauhar",
        "education_list": education_list,
        "institution_query": institution_query,
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
