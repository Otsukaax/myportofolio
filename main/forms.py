from django.forms import DateInput, ModelForm, NumberInput, TextInput

from main.models import Education


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
