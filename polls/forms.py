from django import forms
from django.core.exceptions import ValidationError
from polls.models import Poll, Question, Answer

from datetime import datetime
import pytz
utc = pytz.UTC

def capitalized_validator(value):
    if value[0].islower():
        raise ValidationError('Value must be capitalized!')

def not_capitalized_validator(value):
    if value.isupper():
        raise ValidationError('Value cannot be capitalized!')

class PastMonthField(forms.DateTimeField):
    def validate(self, value):
        super().validate(value)
        if value >= datetime.today().replace(tzinfo=utc):
            raise ValidationError('Only past dates allowed here!')

class NameForm(forms.Form):
    name = forms.CharField(max_length=128)
    birth_date = forms.DateTimeField()

class PollForm(forms.Form):
    name = forms.CharField(max_length=128)

    def clean_name(self):
        #chcemy by 'name' podane przez uzytkownika bylo zapisane w bazie danych wielkimi literami
        initial = self.cleaned_data['name']
        return initial.upper()

#pub_date mozna pominac bo dodaje sie automatycznie
class QuestionForm(forms.Form):
    question_text = forms.CharField(max_length=128, validators=[capitalized_validator])
    pub_date = PastMonthField(label="Publication Date", widget=forms.TextInput(attrs={'placeholder': 'eg.2006-10-25 14:30:59'}))
    poll = forms.ModelChoiceField(queryset=Poll.objects.all())

    # metoda 'clean' na polu (w tym wypadku polu 'question_text') zmienia wartosc jaka bedzie wyslana do bazy danych
    def clean_question_text(self):
        #chcemy by spacje zostaly zastapione znakiem *
        initial = self.cleaned_data['question_text']
        return initial.replace(" ", "*")

    # metoda 'clean' na calym formularzu a nie konkretnym polu i zmienia wartosc jaka bedzie wyslana do bazy danych
    def clean(self):
        result = super().clean()
        if result['question_text'][0] == 'A' and result['pub_date'].year < 2000:
            self.add_error('question_text', "Can't start with A")
            self.add_error('pub_date', 'Add year after 1999')
            raise ValidationError(
                "Don't put question text with A and year before 2000"
            )
        elif result['question_text'][0] == 'W' and result['pub_date'] <= datetime.today().replace(tzinfo=utc):
            raise ValidationError(
                "Don't put question text with W and past date"
            )
        return result

#date_added pomijam bo dodaje sie automatycznie
class AnswerForm(forms.Form):
    answer_text = forms.CharField(max_length=128, validators=[not_capitalized_validator])
    question = forms.ModelChoiceField(queryset=Question.objects.all())
    date_added = PastMonthField()


class QuestionModelForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = '__all__'

class PollModelForm(forms.ModelForm):

    class Meta:
        model = Poll
        fields = '__all__'

class AnswerModelForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = '__all__'

