from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from .forms import QuestionForm, AnswerForm
from .models import Question, Answer, Like

def question_list_view(request):
    context = {}
    query = request.GET.get('q')
    questions = Question.objects.all().order_by('-created_at')
    if query:
        questions = questions.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    context['questions'] = questions
    context['query'] = query
    return render(request, 'questions.html', context)


def question_detail_view(request, pk, slug):
    question = get_object_or_404(Question, pk=pk, slug=slug)
    answers = question.answers.annotate(num_likes=Count('likes')).order_by('-num_likes', 'created_at')
    for answer in answers:
        answer.liked_by_author = answer.likes.filter(user=question.user, liked_by_author=True).exists()
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
            return redirect('forum:question_list')
    else:
        form = QuestionForm()
    return render(request, 'ask_question.html', {'form': form})

@login_required
def answer_question_view(request, pk, slug):
    if not request.user.is_authenticated:
        return redirect('authentication:login')
    question = get_object_or_404(Question, pk=pk, slug=slug)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.user = request.user
            answer.question = question
            answer.save()
            return redirect('forum:question_detail', pk=pk, slug=slug)
    else:
        form = AnswerForm()
    return render(request, 'answer_question.html', {'form': form, 'question': question})

@login_required
def like_answer_view(request, answer_id):
    if not request.user.is_authenticated:
        return redirect('authentication:login')
    
    answer = get_object_or_404(Answer, pk=answer_id)
    like, created = Like.objects.get_or_create(user=request.user, answer=answer)
    if request.user == answer.question.user:
        like.liked_by_author = True
        like.save()
    if not created:
        like.delete()
    return redirect('forum:question_detail', pk=answer.question.pk, slug=answer.question.slug)