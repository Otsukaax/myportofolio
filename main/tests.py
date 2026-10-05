import json
from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.forms import EducationForm
from main.models import Education, Experience


class MainTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username="admin", password="password123")
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, 'id="experience-search-form"')
        self.assertContains(response, 'id="grid"')
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, 'id="empty"')

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:get_experience_json"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '"is_ongoing": false')

    def test_get_experience_json(self):
        response = self.client.get(reverse("main:get_experience_json"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Asisten Dosen PBP")

    def test_search_experience_json(self):
        Experience.objects.create(title="Data Scientist", description="AI", category="full-time")
        response = self.client.get(reverse("main:get_experience_json") + "?title=Asisten")
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Asisten Dosen PBP")
        self.assertNotContains(response, "Data Scientist")

    def test_create_experience_ajax_success(self):
        self.client.login(username="admin", password="password123")
        response = self.client.post(
            reverse("main:create_experience_ajax"),
            {
                "title": "Software Engineer Intern",
                "description": "Bikin fitur baru.",
                "category": "Internship",
            }
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Experience.objects.filter(title="Software Engineer Intern").exists())

    def test_create_experience_ajax_forbidden(self):
        response = self.client.post(
            reverse("main:create_experience_ajax"),
            {
                "title": "Software Engineer Intern",
                "description": "Bikin fitur baru.",
                "category": "Internship",
            }
        )
        self.assertEqual(response.status_code, 403)

    def test_clean_title_xss_rejected(self):
        self.client.login(username="admin", password="password123")
        response = self.client.post(
            reverse("main:create_experience_ajax"),
            {
                "title": '<img src="x" onerror="alert(1)">',
                "description": "Coba injeksi XSS",
                "category": "Internship",
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Experience.objects.filter(description="Coba injeksi XSS").exists())



class EducationTest(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username="admin_test",
            password="password123",
        )
        self.regular_user = User.objects.create_user(
            username="user_test",
            password="password123",
        )
        self.education = Education.objects.create(
            institution="Universitas Indonesia",
            degree="S1 Ilmu Komputer",
            gpa="4.00",
            started_at=date(2024, 8, 1),
            ended_at=None,
        )
        self.education_completed = Education.objects.create(
            institution="SMAN 1 Surakarta",
            degree="SMA",
            gpa=None,
            started_at=date(2021, 7, 1),
            ended_at=date(2024, 5, 1),
        )

    def test_education_url_is_accessible(self):
        response = self.client.get(reverse("main:show_education"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "education.html")
        self.assertContains(response, 'id="education-search-form"')
        self.assertContains(response, 'id="edu-timeline-container"')
        self.assertIn("form", response.context)
        self.assertIsInstance(response.context["form"], EducationForm)

    def test_empty_education_page(self):
        Education.objects.all().delete()
        response = self.client.get(reverse("main:show_education"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "education.html")
        self.assertContains(response, 'id="empty"')

    def test_education_navbar_link_on_main(self):
        response = self.client.get(reverse("main:show_main"))
        self.assertContains(response, f'href="{reverse("main:show_education")}"')

    def test_education_model_properties(self):
        self.assertEqual(str(self.education), "S1 Ilmu Komputer - Universitas Indonesia")
        self.assertTrue(self.education.is_current)
        self.assertFalse(self.education_completed.is_current)

    def test_get_education_json_structure(self):
        response = self.client.get(reverse("main:get_education_json"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")

        data = json.loads(response.content)
        self.assertEqual(len(data), 2)

        first_item = data[0]
        self.assertEqual(first_item["pk"], str(self.education.id))
        self.assertEqual(first_item["fields"]["institution"], "Universitas Indonesia")
        self.assertEqual(first_item["fields"]["degree"], "S1 Ilmu Komputer")
        self.assertTrue(first_item["fields"]["is_current"])
        self.assertEqual(first_item["fields"]["star_count"], 0)

    def test_get_education_json_search_filter(self):
        response = self.client.get(reverse("main:get_education_json"), {"institution": "Indonesia"})
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["fields"]["institution"], "Universitas Indonesia")

        response_empty = self.client.get(reverse("main:get_education_json"), {"institution": "UGM"})
        data_empty = json.loads(response_empty.content)
        self.assertEqual(len(data_empty), 0)

    def test_create_education_ajax_by_superuser_success(self):
        self.client.login(username="admin_test", password="password123")
        payload = {
            "institution": "National University of Singapore",
            "degree": "Master of Computing",
            "gpa": "3.90",
            "started_at": "2025-08-01",
            "ended_at": "",
        }
        response = self.client.post(reverse("main:create_education_ajax"), payload)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Education.objects.filter(institution="National University of Singapore").exists())

    def test_create_education_ajax_by_non_superuser_forbidden(self):
        payload = {
            "institution": "Harvard University",
            "degree": "Computer Science",
            "started_at": "2024-01-01",
        }
        # Guest
        response_guest = self.client.post(reverse("main:create_education_ajax"), payload)
        self.assertEqual(response_guest.status_code, 403)

        # Regular user
        self.client.login(username="user_test", password="password123")
        response_user = self.client.post(reverse("main:create_education_ajax"), payload)
        self.assertEqual(response_user.status_code, 403)
        self.assertFalse(Education.objects.filter(institution="Harvard University").exists())

    def test_create_education_ajax_invalid_data(self):
        self.client.login(username="admin_test", password="password123")
        payload = {
            "institution": "Oxford University",
            "degree": "Software Engineering",
            "started_at": "",
        }
        response = self.client.post(reverse("main:create_education_ajax"), payload)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertIn("errors", data)

    def test_clean_institution_and_degree_xss_rejected(self):
        self.client.login(username="admin_test", password="password123")
        response = self.client.post(
            reverse("main:create_education_ajax"),
            {
                "institution": '<img src="x" onerror="alert(1)">',
                "degree": '<script>alert("XSS")</script>',
                "started_at": "2024-01-01",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Education.objects.filter(started_at="2024-01-01").exists())

    def test_education_form_xss_cleaner(self):
        form_valid = EducationForm(data={
            "institution": '<script>alert("XSS")</script>MIT',
            "degree": "<b>Artificial Intelligence</b>",
            "started_at": "2023-01-01",
        })
        self.assertTrue(form_valid.is_valid())
        self.assertEqual(form_valid.cleaned_data["institution"], 'alert("XSS")MIT')
        self.assertEqual(form_valid.cleaned_data["degree"], "Artificial Intelligence")

        form_invalid = EducationForm(data={
            "institution": "<script></script>",
            "degree": "<div></div>",
            "started_at": "2023-01-01",
        })
        self.assertFalse(form_invalid.is_valid())
        self.assertIn("institution", form_invalid.errors)
        self.assertIn("degree", form_invalid.errors)