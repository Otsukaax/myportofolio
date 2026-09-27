from django.urls import path

from main.views import (
    show_main,
    show_experience,
    show_education,
    create_education,
    delete_education,
    get_education_json,
    create_experience,
    update_experience,
    delete_experience,
    get_experience_json,
    register,
    login_user,
    logout_user,
    toggle_experience_star,
    toggle_education_star,
)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("education/", show_education, name="show_education"),
    path("education/add/", create_education, name="create_education"),
    path("education/<uuid:education_id>/delete/", delete_education, name="delete_education"),
    path("api/education/", get_education_json, name="get_education_json"),
    path("experience/add/", create_experience, name="create_experience"),
    path("experience/<uuid:experience_id>/update/", update_experience, name="update_experience"),
    path("experience/<uuid:experience_id>/delete/", delete_experience, name="delete_experience"),
    path("api/experience/", get_experience_json, name="get_experience_json"),
    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path("experience/<uuid:experience_id>/star/", toggle_experience_star, name="toggle_experience_star"),
    path("education/<uuid:education_id>/star/", toggle_education_star, name="toggle_education_star"),
]
