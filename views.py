from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .models import Course, Lesson, Enrollment, Question, Choice, Submission


def course_list(request):
    courses = Course.objects.all()
    return render(request, 'onlinecourse/course_list.html', {'course_list': courses})


def course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'onlinecourse/course_details_bootstrap.html', {'course': course})


def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user
    enrollment, _ = Enrollment.objects.get_or_create(user=user, course=course)
    submission = Submission.objects.create(enrollment=enrollment)
    selected_ids = request.POST.getlist('choice')
    for choice_id in selected_ids:
        choice = get_object_or_404(Choice, pk=choice_id)
        submission.choices.add(choice)
    return redirect('onlinecourse:show_exam_result', course_id=course.id, submission_id=submission.id)


def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    selected_ids = list(submission.choices.values_list('id', flat=True))
    total_score = 0
    possible_score = 0
    for question in course.question_set.all():
        possible_score += question.grade
        if question.is_get_score(selected_ids):
            total_score += question.grade
    grade = int((total_score / possible_score) * 100) if possible_score > 0 else 0
    return render(request, 'onlinecourse/exam_result_bootstrap.html', {
        'course': course,
        'selected_ids': selected_ids,
        'grade': grade
    })
