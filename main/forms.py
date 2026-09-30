from django.core.exceptions import ValidationError
from django.forms import DateInput, ModelForm, NumberInput, Select, TextInput, Textarea, URLInput
from django.utils.html import strip_tags

from main.models import Education, Experience


class EducationForm(ModelForm):
    class Meta:
        model = Education
        fields = [
            "institution",
            "degree",
            "gpa",
            "started_at",
            "ended_at",
        ]

        labels = {
            "institution": "Nama Institusi",
            "degree": "Jenjang / Program Studi",
            "gpa": "IPK (Opsional)",
            "started_at": "Tanggal Mulai",
            "ended_at": "Tanggal Selesai (Opsional)",
        }

        widgets = {
            "institution": TextInput(
                attrs={
                    "placeholder": "Universitas Indonesia",
                    "maxlength": 255,
                }
            ),
            "degree": TextInput(
                attrs={
                    "placeholder": "S1 Ilmu Komputer",
                    "maxlength": 255,
                }
            ),
            "gpa": NumberInput(
                attrs={
                    "placeholder": "4.00",
                    "step": "0.01",
                    "min": "0.00",
                    "max": "4.00",
                }
            ),
            "started_at": DateInput(
                attrs={
                    "type": "date",
                }
            ),
            "ended_at": DateInput(
                attrs={
                    "type": "date",
                }
            ),
        }


class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = [
            "title",
            "description",
            "category",
            "thumbnail",
            "ended_at",
        ]

        labels = {
            "title": "Posisi / Pekerjaan",
            "description": "Deskripsi Pengalaman",
            "category": "Kategori",
            "thumbnail": "URL Thumbnail (Opsional)",
            "ended_at": "Tanggal Selesai (Opsional)",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Software Engineer Intern",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Mengerjakan fitur X...",
                    "rows": 4,
                    "maxlength": "500",
                    "id": "id_description",
                }
            ),
            "category": Select(),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "https://example.com/image.png",
                }
            ),
            "ended_at": DateInput(
                attrs={
                    "type": "date",
                }
            ),
        }

    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()
        if not title:
            raise ValidationError("Nama pengalaman tidak boleh hanya berisi tag HTML.")
        return title

    def clean_description(self):
        return strip_tags(self.cleaned_data["description"]).strip()
