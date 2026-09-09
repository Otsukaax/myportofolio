from django.shortcuts import render

from main.models import Experience, Mahasiswa


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


def show_experience(request):
    context = {
        "name": "Azka Nur Jauhar",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)
