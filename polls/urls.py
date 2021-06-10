from django.urls import path
from polls.views import animal, answers, answer_form, get_name, hello, index, polls, poll_form, questions, question_form
from polls.views import PollView, PollTemplateView, PollListView, PollFormView
from polls.views import QuestionView, QuestionTemplateView, QuestionListView, QuestionFormView
from polls.views import AnswerView, AnswerTemplateView, AnswerListView, AnswerFormView
from polls.views import AnswerFormMethodView, PollFormMethodView, QuestionFormMethodView
from polls.views import AnswerCreateView, PollCreateView, QuestionCreateView
from polls.views import AnswerDetailView, PollDetailView, QuestionDetailView
from polls.views import AnswerGenericDetailsView, PollGenericDetailsView, QuestionGenericDetailsView
from polls.views import QuestionUpdateView, QuestionGenericUpdateView, QuestionDeleteView
from polls.views import PollUpdateView, PollGenericUpdateView, PollDeleteView
from polls.views import AnswerUpdateView, AnswerGenericUpdateView, AnswerDeleteView

# urlpatterns = [
#     path('hello/', hello)
# ]

app_name = "polls"
urlpatterns = [
    path('', index, name='index'),
    path('hello/<str:s0>/', hello),
    path('animals/', animal),
    path('polls/', polls, name='polls'),
    path('questions/', questions, name='questions'),
    path('answers/', answers, name='answers'),
    path('polls-class/', PollView.as_view(), name='polls-class'),
    path('polls-template/', PollTemplateView.as_view(), name='polls-template'),
    path('polls-list/', PollListView.as_view(), name='polls-list'),
    path('answers-class/', AnswerView.as_view(), name='answers-class'),
    path('answers-template/', AnswerTemplateView.as_view(), name='answers-template'),
    path('answers-list/', AnswerListView.as_view(), name='answers-list'),
    path('questions-class/', QuestionView.as_view(), name='questions-class'),
    path('questions-template/', QuestionTemplateView.as_view(), name='questions-template'),
    path('questions-list/', QuestionListView.as_view(), name='questions-list'),
    path('my-name-form/', get_name),
    path('my-poll-form/', poll_form),
    path('my-question-form/', question_form),
    path('my-answer-form/', answer_form),
    path('my-question-form-view/', QuestionFormView.as_view(), name='my-question-form-view'),
    path('my-poll-form-view/', PollFormView.as_view(), name='my-poll-form-view'),
    path('my-answer-form-view/', AnswerFormView.as_view(), name='my-answer-form-view'),
    path('my-poll-form-method-view/', PollFormMethodView.as_view(), name='my-poll-form-method-view'),
    path('my-question-form-method-view/', QuestionFormMethodView.as_view(), name='my-question-form-method-view'),
    path('my-answer-form-method-view/', AnswerFormMethodView.as_view(), name='my-answer-form-method-view'),
    path('question-create-view/', QuestionCreateView.as_view(), name='question-create-view'),
    path('poll-create-view/', PollCreateView.as_view(), name='poll-create-view'),
    path('answer-create-view/', AnswerCreateView.as_view(), name='answer-create-view'),
    path('question-detail-view/<pk>/', QuestionDetailView.as_view(), name='question-detail-view'),
    path('poll-detail-view/<pk>/', PollDetailView.as_view(), name='poll-detail-view'),
    path('answer-detail-view/<pk>/', AnswerDetailView.as_view(), name='answer-detail-view'),
    path('question-generic-view/<pk>/', QuestionGenericDetailsView.as_view(), name='question-generic-view'),
    path('poll-generic-view/<pk>/', PollGenericDetailsView.as_view(), name='poll-generic-view'),
    path('answer-generic-view/<pk>/', AnswerGenericDetailsView.as_view(), name='answer-generic-view'),
    path('question-update-view/<pk>/', QuestionUpdateView.as_view(), name='question-update-view'),
    path('question-generic-update-view/<pk>/', QuestionGenericUpdateView.as_view(), name='question-generic-update-view'),
    path('question-delete-view/<pk>/', QuestionDeleteView.as_view(), name='question-delete-view'),
    path('poll-update-view/<pk>/', PollUpdateView.as_view(), name='poll-update-view'),
    path('poll-generic-update-view/<pk>/', PollGenericUpdateView.as_view(), name='poll-generic-update-view'),
    path('poll-delete-view/<pk>/', PollDeleteView.as_view(), name='poll-delete-view'),
    path('answer-update-view/<pk>/', AnswerUpdateView.as_view(), name='answer-update-view'),
    path('answer-generic-update-view/<pk>/', AnswerGenericUpdateView.as_view(), name='answer-generic-update-view'),
    path('answer-delete-view/<pk>/', AnswerDeleteView.as_view(), name='answer-delete-view')
]
