from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("courses/", views.courses, name="courses"),
    path("addCourses/", views.addCourses, name="addCourses"),
    path("deleteCourse/<int:course_id>/", views.deleteCourse, name="deleteCourse"),
    path("editCourse/<int:course_id>/", views.editCourse, name="editCourse"),
    path("addPart/<int:course_id>/", views.addPart, name="addPart"),
    path("deletePart/<int:part_id>/", views.deletePart, name="deletePart"),
    path("editPart/<int:part_id>/", views.editPart, name="editPart"),
    path("addTask/<int:part_id>/", views.addTask, name="addTask"),
    path("revert-part/<int:part_id>/", views.revert_part, name="revertPart"),
    path("deleteTask/<int:task_id>/", views.deleteTask, name="deleteTask"),
    path("editTask/<int:task_id>/", views.editTask, name="editTask"),
    path("addDailyTask/<int:task_id>/", views.addDailyTask, name="addDailyTask"),
    path("updateDailyTask/<int:daily_task_id>/", views.updateDailyTask, name="updateDailyTask"),
    path("completeDailyTask/<int:daily_task_id>/", views.completeDailyTask, name="completeDailyTask"),
    path("history/", views.history, name="history"),
    path("revertTask/<int:daily_task_id>/", views.revertTask, name="revertTask"),
    path("complete-part/<int:part_id>/", views.complete_part, name="completePart"),
    path("statistics/", views.statistics, name="statistics"),
]