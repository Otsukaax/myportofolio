from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from main.forms import EducationForm, ExperienceForm
from main.models import Education, Experience, Mahasiswa


def show_main(request):
    context = {
        "name": "Azka Nur Jauhar",
        "npm": "2506612410",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "Second-year CS Student at Universitas Indonesia. Passionate about AI, Machine "
            "Learning, and Software Engineering."
        ),
        "mahasiswa_list": Mahasiswa.objects.all(),
    }
    return render(request, "index.html", context)


def get_experience_json(request):
    experience_list = Experience.objects.all()
    experience_json = serializers.serialize("json", experience_list)
    return HttpResponse(experience_json, content_type="application/json")


def show_experience(request):
    json_response = get_experience_json(request)

    deserialized_experiences = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    experience_list = [exp_entry.object for exp_entry in deserialized_experiences]

    context = {
        "name": "Azka Nur Jauhar",
        "experience_list": experience_list,
    }
    return render(request, "experience.html", context)


def create_experience(request):
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


def update_experience(request, experience_id):
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


def delete_experience(request, experience_id):
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

    education_json = serializers.serialize("json", education_list)
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


def create_education(request):
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


def delete_education(request, education_id):
    education_item = get_object_or_404(Education, pk=education_id)

    if request.method == "POST":
        education_item.delete()
        messages.success(request, "Riwayat pendidikan berhasil dihapus!")
        return redirect("main:show_education")

    return redirect("main:show_education")



