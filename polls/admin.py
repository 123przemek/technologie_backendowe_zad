from django.contrib import admin
from polls.models import Poll, Question, Answer

# Register your models here.

class QuestionAdmin(admin.ModelAdmin):
    ordering = ('question_text',)   #lub ("-question_text")
    list_display = ('question_text','pub_year','poll')
    list_display_links = ('question_text',)
    list_per_page = 20
    list_filter = ('pub_date',)
    search_fields = ('question_text',)
    actions = ('cleanup_text')

    fieldsets = [
        ("General", {
            "fields": ["question_text", "pub_date"]
        }
         ),
        ("External Information", {
            "fields": ["poll", ],
            "description": "Information about related Poll"
        }
         )
    ]

    readonly_fields = ["pub_date"]

    @staticmethod
    def pub_year(obj):
        return obj.pub_date.year

    @staticmethod
    def cleanup_text(modeladmin, request, queryset):
        queryset.update(question_text='')

admin.site.register(Answer)
admin.site.register(Poll)
admin.site.register(Question, QuestionAdmin)
