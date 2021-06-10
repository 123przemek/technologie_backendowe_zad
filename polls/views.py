from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, TemplateView, FormView, CreateView, DetailView
from django.urls import reverse_lazy, reverse

from polls.models import Answer, Poll, Question
from polls.forms import NameForm, PollForm, QuestionForm, AnswerForm
from polls.forms import QuestionModelForm, PollModelForm, AnswerModelForm
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import FormView, ListView, TemplateView, CreateView, DetailView, UpdateView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test

from polls.models import Answer, Poll, Question
from polls.forms import AnswerForm, NameForm, PollForm, QuestionForm
from polls.forms import QuestionModelForm
# Create your views here.

# def hello(request):
#     year = request.GET.get('year', '')
#     return HttpResponse(f'Hello, world! {year}')

def username_contains_i(user):
    return 'i' in user.username

class UsernameContainsIMixin(UserPassesTestMixin):
    def test_func(self):
        return 'i' in self.request.user.username

class UsernameStartsWithCapitalMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.username[0].isupper()

class UsernameMaxLength5Mixin(UserPassesTestMixin):
    def test_func(self):
        return len(self.request.user.username) <= 5

def response_hello(request):
    return HttpResponseRedirect(reverse("polls:index"))

@login_required(login_url='/login/')  #nadpisuje url domyslny ustawiony w settings.py
# dzieki temu niezalogowany uzytkownik nie bedzie miec dostepu do tego widoku
def hello(request, s0):
    s1 = request.GET.get('s1', '')
    return render(
        request, template_name='hello.html',
        context={'adjectives': [s0, s1, 'beautiful', 'wonderful']}
    )

@user_passes_test(username_contains_i)
def animal(request):
    animals = request.GET.get("animals", "")
    return render(
        request, template_name='my_template.html',
        context={"animals": animals.split(",")}
    )

def polls(request):
    return render(
        request,
        template_name='polls.html',
        context={'polls': Poll.objects.all()}
    )

def questions(request):
    return render(
        request,
        template_name='questions.html',
        context={'questions': Question.objects.all()}
    )

def answers(request):
    return render(
        request,
        template_name='answers.html',
        context={'answers': Answer.objects.all()}
    )

@permission_required("polls.view_question")
def index(request):
    return render(
        request,
        template_name='index.html'
    )

#tworzenie metody w klasie
class PollView(View):
    def get(self, request):
        return render(
            request,
            template_name='polls.html',
            context={'polls': Poll.objects.all()}
        )

#jeszcze szybszy sposob by wygenerowac templatke
class PollTemplateView(TemplateView):
    template_name = 'polls.html'
    extra_context = {'polls': Poll.objects.all()}

#jeszcze prostszy sposob, gdzie przekazuje tylko jaka templatka, jaki model i on pod spodem tworzy
#zmienna object_list do ktorej wpadaja wszystkie elementy danej tabeli
#zeby to dzialalo, musze dodatkowo w polls.html zmienic {% for poll in polls %} na
# {% for poll in object_list %}
class PollListView(PermissionRequiredMixin, UsernameContainsIMixin, ListView):
    permission_required = ("polls.view_poll")
    template_name = 'polls.html'
    model = Poll

class AnswerView(View):
    def get(self, request):
        return render(
            request,
            template_name='answers.html',
            context={'answers': Answer.objects.all()}
        )

class AnswerTemplateView(TemplateView):
    template_name = 'answers.html'
    extra_context = {'answers': Answer.objects.all()}

class AnswerListView(PermissionRequiredMixin, UsernameMaxLength5Mixin, ListView):
    permission_required = ("polls.view_answer")
    template_name = 'answers.html'
    model = Answer

class QuestionView(View):
    def get(self, request):
        return render(
            request,
            template_name='questions.html',
            context={'questions': Question.objects.all()}
        )

class QuestionTemplateView(TemplateView):
    template_name = 'questions.html'
    extra_context = {'questions': Question.objects.all()}

class QuestionListView(LoginRequiredMixin, PermissionRequiredMixin, UsernameStartsWithCapitalMixin, ListView):
    login_url = "/polls/answers" #nadpisuje url domyslny ustawiony w settings.py
    permission_required = ("polls.view_question")
    template_name = 'questions.html'
    model = Question

#Formularze

def get_name(request):
    form = NameForm(request.POST or None) #formularz trzeba nakarmic danymi
    if request.method == "POST":
        if form.is_valid():
            return HttpResponse('IT WORKED')
    return render(
        request,
        template_name='form.html',
        context={'form': form}
    )

def poll_form(request):
    form = PollForm(request.POST or None) #formularz trzeba nakarmic danymi
    if form.is_valid():
        name = form.cleaned_data['name']
        Poll.objects.create(name=name)
        return HttpResponse('IT WORKED')
    return render(
        request,
        template_name='form.html',
        context={'form': form}
    )

def question_form(request):
    form = QuestionForm(request.POST or None) #formularz trzeba nakarmic danymi
    if form.is_valid():
        question_text = form.cleaned_data['question_text']
        poll = form.cleaned_data['poll']
        Question.objects.create(question_text=question_text, poll=poll)
        return HttpResponse('IT WORKED')
    return render(
        request,
        template_name='form.html',
        context={'form': form}
    )

def answer_form(request):
    form = AnswerForm(request.POST or None) #formularz trzeba nakarmic danymi
    if form.is_valid():
        answer_text = form.cleaned_data['answer_text']
        question = form.cleaned_data['question']
        Answer.objects.create(answer_text=answer_text, question=question)
        return HttpResponse('IT WORKED')
    return render(
        request,
        template_name='form.html',
        context={'form': form}
    )

class QuestionFormView(FormView):
    template_name = 'form.html'
    form_class = QuestionModelForm
    success_url = reverse_lazy("polls:index")

    #to ponizej jest rownowazne z def question_form(request)
    #czyli przenosimy tu logike z funkcji do klasy i jest to lepsze rozwiazanie
    def form_valid(self, form):
        result = super().form_valid(form)
        question_text = form.cleaned_data['question_text']
        poll = form.cleaned_data['poll']
        Question.objects.create(question_text=question_text, poll=poll)
        return result

    def form_invalid(self, form):
        result = super().form_invalid(form)

class PollFormView(FormView):
    template_name = 'form.html'
    form_class = PollModelForm
    success_url = reverse_lazy("polls:index")

    # to ponizej jest rownowazne z def poll_form(request)
    # czyli przenosimy tu logike z funkcji do klasy i jest to lepsze rozwiazanie
    def form_valid(self, form):
        result = super().form_valid(form)
        name = form.cleaned_data['name']
        Poll.objects.create(name=name)
        return result

    def form_invalid(self, form):
        result = super().form_invalid(form)

class AnswerFormView(FormView):
    template_name = 'form.html'
    form_class = AnswerModelForm
    success_url = reverse_lazy("polls:index")

    #to ponizej jest rownowazne z def answer_form(request)
    #czyli przenosimy tu logike z funkcji do klasy i jest to lepsze rozwiazanie
    def form_valid(self, form):
        result = super().form_valid(form)
        answer_text = form.cleaned_data['answer_text']
        question = form.cleaned_data['question']
        Answer.objects.create(answer_text=answer_text, question=question)
        return result

    def form_invalid(self, form):
        result = super().form_invalid(form)

#rozbicie wyswietlania formularza i wysylania wprowadzonych danych na dwie funkcje
class PollFormMethodView(View):
    #wyswietlanie pustego formularza form=PollForm()
    def get(self, request):
        form = PollForm()
        return render(
            request,
            template_name="form.html",
            context={"form": form}
        )

    #wyslanie wypelnionego formularza
    def post(self, request):
        form = PollForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            Poll.objects.create(name=name)
            return HttpResponseRedirect(reverse("polls:index"))
        return render(
            request,
            template_name="form.html",
            context={"form": form}
        )


class QuestionFormMethodView(View):
    def get(self, request):
        form = QuestionForm()
        return render(
            request,
            template_name="form.html",
            context={"form": form}
        )

    def post(self, request):
        form = QuestionForm(request.POST)
        if form.is_valid():
            question_text = form.cleaned_data['question_text']
            poll = form.cleaned_data['poll']
            Question.objects.create(question_text=question_text, poll=poll)
            return HttpResponseRedirect(reverse("polls:index"))
        return render(
            request,
            template_name="form.html",
            context={"form": form}
        )

class AnswerFormMethodView(View):
    def get(self, request):
        form = AnswerForm()
        return render(
            request,
            template_name="form.html",
            context={"form": form}
        )

    def post(self, request):
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer_text = form.cleaned_data['answer_text']
            question = form.cleaned_data['question']
            Answer.objects.create(answer_text=answer_text, question=question)
            return HttpResponseRedirect(reverse("polls:index"))
        return render(
            request,
            template_name="form.html",
            context={"form": form}
        )

class QuestionCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ("polls.add_question")
    model = Question
    template_name = 'form.html'
    fields = '__all__'
    success_url = reverse_lazy('polls:index')

class PollCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ("polls.add_poll")
    model = Poll
    template_name = 'form.html'
    fields = '__all__'
    success_url = reverse_lazy('polls:index')

class AnswerCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ("polls.add_answer")
    model = Answer
    template_name = 'form.html'
    fields = '__all__'
    success_url = reverse_lazy('polls:index')

class QuestionDetailView(View):
    #pk to id obiektu ktory chce zobaczyc
    def get(self, request, pk):
        obj = get_object_or_404(Question, pk=pk)
        return render(
            request,
            template_name='question.html',
            context={'question': obj}
        )

class PollDetailView(View):
    #pk to id obiektu ktory chce zobaczyc
    def get(self, request, pk):
        obj = get_object_or_404(Poll, pk=pk)
        return render(
            request,
            template_name='poll.html',
            context={'poll': obj}
        )

class AnswerDetailView(View):
    #pk to id obiektu ktory chce zobaczyc
    def get(self, request, pk):
        obj = get_object_or_404(Answer, pk=pk)
        return render(
            request,
            template_name='answer.html',
            context={'answer': obj}
        )

class QuestionGenericDetailsView(PermissionRequiredMixin, DetailView):
    permission_required = ("polls.view_question")
    model = Question
    template_name = 'question.html'

class PollGenericDetailsView(PermissionRequiredMixin, DetailView):
    permission_required = ("polls.view_poll")
    model = Poll
    template_name = 'poll.html'

class AnswerGenericDetailsView(PermissionRequiredMixin, DetailView):
    permission_required = ("polls.view_answer")
    model = Answer
    template_name = 'answer.html'

class QuestionUpdateView(View):

    def get(self, request, pk):
        form = QuestionForm()
        return render(
            request,
            template_name='form.html',
            context={"form": form}
        )

    def post(self, request, pk):
        form = QuestionForm(request.POST or None)
        if form.is_valid():
            q = get_object_or_404(pk=pk)
            q.question_text = form.cleaned_data["question_text"]
            q.poll = form.cleaned_data["poll"]
            q.save()
            return HttpResponseRedirect(reverse("polls:index"))
        return render(
            request,
            template_name='form.html',
            context={"form": form}
        )

class QuestionGenericUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ("polls.change_question")
    model = Question
    fields = ("question_text")
    template_name = "form.html"
    success_url = reverse_lazy("polls:index")

class QuestionDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ("polls.delete_question")
    model = Question
    template_name = "question_delete_form.html"
    success_url = reverse_lazy("polls:index")

class PollUpdateView(View):

    def get(self, request, pk):
        form = PollForm()
        return render(
            request,
            template_name='form.html',
            context={"form": form}
        )

    def post(self, request, pk):
        form = PollForm(request.POST or None)
        if form.is_valid():
            p = get_object_or_404(pk=pk)
            p.name = form.cleaned_data["name"]
            p.save()
            return HttpResponseRedirect(reverse("polls:index"))
        return render(
            request,
            template_name='form.html',
            context={"form": form}
        )

class PollGenericUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ("polls.change_poll")
    model = Poll
    fields = ("name")
    template_name = "form.html"
    success_url = reverse_lazy("polls:index")

class PollDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ("polls.delete_poll")
    model = Poll
    template_name = "poll_delete_form.html"
    success_url = reverse_lazy("polls:index")

class AnswerUpdateView(View):

    def get(self, request, pk):
        form = AnswerForm()
        return render(
            request,
            template_name='form.html',
            context={"form": form}
        )

    def post(self, request, pk):
        form = AnswerForm(request.POST or None)
        if form.is_valid():
            a = get_object_or_404(pk=pk)
            a.answer_text = form.cleaned_data["answer_text"]
            a.question = form.cleaned_data["question"]
            a.save()
            return HttpResponseRedirect(reverse("polls:index"))
        return render(
            request,
            template_name='form.html',
            context={"form": form}
        )

class AnswerGenericUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ("polls.change_answer")
    model = Answer
    fields = ("answer_text")
    template_name = "form.html"
    success_url = reverse_lazy("polls:index")

class AnswerDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ("polls.delete_answer")
    model = Answer
    template_name = "answer_delete_form.html"
    success_url = reverse_lazy("polls:index")


