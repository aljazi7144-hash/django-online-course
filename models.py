from django.db import models
from django.utils.timezone import now


class Course(models.Model):
    name = models.CharField(null=False, max_length=30, default='online course')
    pub_date = models.DateField(default=now)
    description = models.CharField(max_length=500, default='')

    def __str__(self):
        return self.name


class Lesson(models.Model):
    title = models.CharField(max_length=200, default="title")
    order = models.IntegerField(default=0)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.TextField(default='')

    def __str__(self):
        return self.title


class Learner(models.Model):
    user_id = models.CharField(max_length=200, default='')
    occupation = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.user_id


class Enrollment(models.Model):
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateField(default=now)
    mode = models.CharField(max_length=15, default='audit')

    def __str__(self):
        return f"{self.learner} - {self.course}"


class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True)
    question_text = models.CharField(max_length=500)
    grade = models.IntegerField(default=50)

    def __str__(self):
        return self.question_text

    def is_get_score(self, selected_ids):
        all_answers = self.choice_set.filter(is_correct=True).count()
        selected_correct = self.choice_set.filter(is_correct=True, id__in=selected_ids).count()
        selected_incorrect = self.choice_set.filter(is_correct=False, id__in=selected_ids).count()
        if all_answers == selected_correct and selected_incorrect == 0 and all_answers > 0:
            return True
        return False


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


class Submission(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    choices = models.ManyToManyField(Choice)
    submitted_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"Submission {self.id} - {self.enrollment}"
