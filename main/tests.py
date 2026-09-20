from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Education, Experience


class MainTest(TestCase):
    def setUp(self):
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
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Part-Time")
        self.assertContains(response, "Sedang berlangsung")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "Selesai")
        self.assertNotContains(response, "Sedang berlangsung")

    def test_create_experience(self):
        response = self.client.post(
            reverse("main:create_experience"),
            {
                "title": "Software Engineer Intern",
                "description": "Bikin fitur baru.",
                "category": "Internship",
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Experience.objects.filter(title="Software Engineer Intern").exists())

    def test_update_experience(self):
        response = self.client.post(
            reverse("main:update_experience", args=[self.experience.id]),
            {
                "title": "Asisten Dosen PBP (Updated)",
                "description": self.experience.description,
                "category": self.experience.category,
            }
        )
        self.assertEqual(response.status_code, 302)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Asisten Dosen PBP (Updated)")

    def test_delete_experience(self):
        response = self.client.post(
            reverse("main:delete_experience", args=[self.experience.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Experience.objects.count(), 0)

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



class EducationTest(TestCase):
    def setUp(self):
        # Skenario 1: Berjalan & ada IPK (Data Anda)
        self.education = Education.objects.create(
            institution="Universitas Indonesia",
            degree="S1 Ilmu Komputer",
            gpa="4.00",
            started_at="2024-08-01",
        )
        # Skenario 2: Lulus & tanpa IPK
        self.education_completed = Education.objects.create(
            institution="SMAN 1 Surakarta",
            degree="SMA",
            gpa=None,
            started_at="2021-07-01",
            ended_at="2024-05-01",
        )

    def test_education_url_is_accessible(self):
        response = self.client.get(reverse("main:show_education"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "education.html")

    def test_education_data_in_response(self):
        response = self.client.get(reverse("main:show_education"))

        self.assertContains(response, self.education.institution)
        self.assertContains(response, self.education.degree)
        self.assertContains(response, self.education.gpa)

    def test_empty_education_page(self):
        Education.objects.all().delete()
        response = self.client.get(reverse("main:show_education"))

        self.assertContains(response, "Belum ada riwayat pendidikan yang ditambahkan.")

    def test_education_navbar_link_on_main(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertContains(response, f'href="{reverse("main:show_education")}"')

    def test_education_model_properties(self):
        self.assertEqual(str(self.education), "S1 Ilmu Komputer - Universitas Indonesia")
        self.assertTrue(self.education.is_current)
        self.assertFalse(self.education_completed.is_current)

    def test_completed_education_data_in_response(self):
        response = self.client.get(reverse("main:show_education"))
        
        # Memastikan skenario lulus dirender dengan benar
        self.assertContains(response, self.education_completed.institution)
        self.assertContains(response, "Lulus")
        
        # Memastikan blok IPK tidak muncul (atau tidak me-render teks 'None')
        self.assertNotContains(response, '<span class="edu-timeline__gpa-value">None</span>')