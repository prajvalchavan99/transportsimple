from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import QuestionForm, AnswerForm
from .models import Question, Answer, Like

def question_list_view(request):
    questions = Question.objects.all().order_by('-created_at')
    return render(request, 'questions.html', {'questions': questions})

def question_detail_view(request, pk):
    question = get_object_or_404(Question, pk=pk)
    answers = question.answers.all()
    return render(request, 'question_detail.html', {
        'question': question,
        'answers': answers
    })

@login_required
def ask_question_view(request):
    form = QuestionForm()
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()
            return redirect('question_list')
    else:
        form = QuestionForm()
    return render(request, 'ask_question.html', {'form': form})

@login_required
def answer_question_view(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.user = request.user
            answer.question = question
            answer.save()
            return redirect('question_detail', pk=pk)
    else:
        form = AnswerForm()
    return render(request, 'answer_question.html', {'form': form, 'question': question})

@login_required
def like_answer_view(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    like, created = Like.objects.get_or_create(user=request.user, answer=answer)
    if not created:
        like.delete()
    return redirect('question_detail', pk=answer.question.pk)