import json
import calendar

from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.db import IntegrityError
from .models import User, Course, Part, Task, DailyTask
from datetime import date
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta

# Create your views here.
def format_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    if hours > 0:
        return f"{hours}h {minutes:02d}m {seconds:02d}s"

    return f"{minutes}m {seconds:02d}s"


@login_required
def dashboard(request):
    today = date.today()

    all_today_tasks = DailyTask.objects.filter(
        user=request.user,
        date=today
    )

    daily_tasks = all_today_tasks.filter(
        completed=False
    )

    total_planned_seconds = sum(
        task.planned_minutes * 60 for task in all_today_tasks
    )

    total_actual_seconds = sum(
        task.actual_seconds for task in all_today_tasks
    )

    planned_time = format_time(total_planned_seconds)
    actual_time = format_time(total_actual_seconds)

    completed_tasks = DailyTask.objects.filter(
        user=request.user,
        completed=True,
        date__year=today.year,
        date__month=today.month
    )

    active_dates = set(
        task.date for task in completed_tasks
    )

    first_day = date(today.year, today.month, 1)

    days_in_month = calendar.monthrange(
        today.year,
        today.month
    )[1]

    calendar_days = [None] * first_day.weekday()

    for day_number in range(1, days_in_month + 1):
        current_day = date(
            today.year,
            today.month,
            day_number
        )

        calendar_days.append({
            "date": current_day,
            "active": current_day in active_dates
        })

    month_name = today.strftime("%B %Y")

    recent_result = DailyTask.objects.filter(
        user=request.user,
        completed=True
    ).order_by("-date", "-id").first()

    recent_result_time = None

    if recent_result:
        recent_result_time = format_time(recent_result.actual_seconds)

    return render(request, "tracker/dashboard.html", {
        "daily_tasks": daily_tasks,
        "planned_time": planned_time,
        "actual_time": actual_time,
        "active_dates": active_dates,
        "calendar_days": calendar_days,
        "month_name": month_name,
        "recent_result": recent_result,
        "recent_result_time": recent_result_time
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("dashboard"))
        else:
            return render(request, "tracker/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "tracker/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("dashboard"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "tracker/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, username, password)
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "username/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("dashboard"))
    else:
        return render(request, "tracker/register.html")

@login_required
def courses(request):
    courses = Course.objects.filter(user=request.user)
    for course in courses:
        total_parts = course.parts.count()

        completed_parts = course.parts.filter(
            completed=True
        ).count()

        if total_parts > 0:
            course.completion_percentage = round(
                (completed_parts / total_parts) * 100
            )
        else:
            course.completion_percentage = 0
    return render(request, "tracker/courses.html", {
        "courses": courses
    })

@login_required
def complete_part(request, part_id):
    if request.method == "POST":
        part = get_object_or_404(
            Part,
            id=part_id,
            course__user=request.user
        )

        part.completed = True
        part.save()

        course = part.course

        if not course.parts.filter(completed=False).exists():
            course.completed = True
            course.save()

        return JsonResponse({"success": True})

    return JsonResponse({"success": False}, status=405)

@login_required
def addCourses(request):
    if request.method == "POST":
        name = request.POST.get("name")
        resource_url = request.POST.get("resource_url")

        Course.objects.create(
            user=request.user,
            name=name,
            resource_url=resource_url
        )

        return redirect("courses")

    return render(request, "tracker/addCourses.html")

@login_required
def deleteCourse(request, course_id):
    course = Course.objects.get(id=course_id)

    if course.user == request.user:
        course.delete()

    return redirect("courses")

@login_required
def editCourse(request, course_id):
    course = Course.objects.get(id=course_id)

    if course.user != request.user:
        return redirect("courses")

    if request.method == "POST":
        course.name = request.POST.get("name")
        course.resource_url = request.POST.get("resource_url")
        course.save()

        return redirect("courses")

    return render(request, "tracker/editCourse.html", {
        "course": course
    })

@login_required
def addPart(request, course_id):

    course = Course.objects.get(id=course_id)

    if request.method == "POST":
        name = request.POST.get("name")

        Part.objects.create(
            course=course,
            name=name
        )

        return redirect("courses")

    return render(request, "tracker/addPart.html", {
        "course": course
    })

@login_required
def deletePart(request, part_id):
    parts = Part.objects.get(id=part_id)

    if parts.course.user == request.user:
        parts.delete()

    return redirect("courses")

@login_required
def editPart(request, part_id):
    part = Part.objects.get(id=part_id)

    if part.course.user != request.user:
        return redirect("courses")

    if request.method == "POST":
        part.name = request.POST.get("name")
        part.save()

        return redirect("courses")

    return render(request, "tracker/editPart.html", {
        "part": part
    })

@login_required
def revert_part(request, part_id):
    if request.method == "POST":
        part = get_object_or_404(
            Part,
            id=part_id,
            course__user=request.user
        )

        part.completed = False
        part.save()

        return JsonResponse({"success": True})

    return JsonResponse({"success": False}, status=405)

@login_required
def addTask(request, part_id):
    part = Part.objects.get(id=part_id)

    if request.method == "POST":
        name = request.POST["name"]
        resource_url = request.POST.get("resource_url")

        Task.objects.create(
            part=part,
            name=name,
            resource_url=resource_url
        )

        return redirect("courses")

    return render(request, "tracker/addTask.html", {
        "part": part
    })

@login_required
def deleteTask(request, task_id):
    task = Task.objects.get(id=task_id)

    if task.part.course.user == request.user:
        task.delete()

    return redirect("courses")

@login_required
def editTask(request, task_id):
    task = Task.objects.get(id=task_id)

    if task.part.course.user != request.user:
        return redirect("courses")

    if request.method == "POST":
        task.name = request.POST.get("name")
        task.resource_url = request.POST.get("resource_url")
        task.save()

        return redirect("courses")

    return render(request, "tracker/editTask.html", {
        "task": task
    })

@login_required
def addDailyTask(request, task_id):
    task = Task.objects.get(id=task_id)

    if task.part.course.user != request.user:
        return redirect("courses")

    if request.method == "POST":
        planned_minutes = request.POST.get("planned_minutes")

        DailyTask.objects.create(
            user=request.user,
            task=task,
            date=date.today(),
            planned_minutes=planned_minutes
        )

        return redirect("dashboard")

    return render(request, "tracker/addDailyTask.html", {
        "task": task
    })

@login_required
def updateDailyTask(request, daily_task_id):

    if request.method == "POST":
        daily_task = DailyTask.objects.get(id=daily_task_id)

        if daily_task.user != request.user:
            return JsonResponse({"error": "Unauthorized"}, status=403)

        data = json.loads(request.body)

        daily_task.actual_seconds = data.get("actual_seconds")
        daily_task.save()

        return JsonResponse({
            "message": "Time updated successfully"
        })

    return JsonResponse({
        "error": "POST request required"
    }, status=400)

@login_required
def completeDailyTask(request, daily_task_id):
    if request.method == "POST":
        daily_task = DailyTask.objects.get(
            id=daily_task_id,
            user=request.user
        )

        daily_task.completed = True
        daily_task.save()

        return JsonResponse({"success": True})

    return JsonResponse({"error": "POST request required"}, status=400)

@login_required
def history(request):
    completed_tasks = DailyTask.objects.filter(
        user=request.user,
        completed=True
    ).order_by("-date")

    for daily_task in completed_tasks:
        daily_task.planned_time = format_time(daily_task.planned_minutes * 60)
        daily_task.actual_time = format_time(daily_task.actual_seconds)

    return render(request, "tracker/history.html", {
        "completed_tasks": completed_tasks,
    })

@login_required
def revertTask(request, daily_task_id):
    daily_task = DailyTask.objects.get(
        id=daily_task_id,
        user=request.user
    )

    daily_task.completed = False
    daily_task.save()

    return JsonResponse({"success": True})

@login_required
def statistics(request):
    today = timezone.localdate()

    month_start = today.replace(day=1)

    monthly_tasks = DailyTask.objects.filter(
        user=request.user,
        date__gte=month_start,
        date__lte=today
    )

    planned_minutes = monthly_tasks.aggregate(
        total=Sum("planned_minutes")
    )["total"] or 0

    actual_seconds = monthly_tasks.aggregate(
        total=Sum("actual_seconds")
    )["total"] or 0

    planned_seconds = planned_minutes * 60

    planned_hours, remainder = divmod(planned_seconds, 3600)
    planned_mins, planned_secs = divmod(remainder, 60)

    actual_hours, remainder = divmod(actual_seconds, 3600)
    actual_mins, actual_secs = divmod(remainder, 60)

    # Daily streak
    completed_dates = set(
        DailyTask.objects.filter(
            user=request.user,
            completed=True
        ).values_list("date", flat=True)
    )

    streak = 0
    current_date = today

    while current_date in completed_dates:
        streak += 1
        current_date -= timedelta(days=1)

    most_tasks_completed = DailyTask.objects.filter(
        user=request.user,
        completed=True
    ).values("date").annotate(
        task_count=Count("id")
    ).order_by("-task_count").first()

    most_tasks = (
        most_tasks_completed["task_count"]
        if most_tasks_completed
        else 0
    )

    return render(request, "tracker/statistics.html", {
        "planned_time": f"{planned_hours}h {planned_mins}m {planned_secs:02d}s",
        "actual_time": f"{actual_hours}h {actual_mins}m {actual_secs:02d}s",
        "streak": streak,
        "most_tasks": most_tasks,
    })