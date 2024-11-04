from django.contrib import admin
from .models import *
# Register your models here.



@admin.register(Extra_quick_replays)
class Extra_quick_replaysAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Extra_quick_replays._meta.fields]


class AnswerInline(admin.StackedInline):
    model = AutoMessageQuestion
    fields = ('question',)
    extra = 1

@admin.register(AutoMessage)
class AutoMessageAdmin(admin.ModelAdmin):
    list_display = ['parent_message', 'answer']
    inlines = [AnswerInline]
    
    def save_model(self, request, obj, form, change):
        # save the parent message object first
        super().save_model(request, obj, form, change)
        
        # create and save a new question object under the parent message
        if not change: # only if this is a new parent message
            new_question = AutoMessageQuestion(q_id=obj, question=obj.parent_message)
            new_question.save()

admin.site.register(AutoMessageQuestion)


class LinkAnswerInline(admin.StackedInline):
    model = AutoLinkMessageQuestion
    fields = ('question',)
    extra = 1

@admin.register(AutoLinkMessage)
class AutoLinkMessageAdmin(admin.ModelAdmin):
    list_display = ['parent_message', 'title']
    inlines = [LinkAnswerInline]
    
    def save_model(self, request, obj, form, change):
        # save the parent message object first
        super().save_model(request, obj, form, change)
        
        # create and save a new question object under the parent message
        if not change: # only if this is a new parent message
            new_question = AutoLinkMessageQuestion(q_id=obj, question=obj.parent_message)
            new_question.save()

admin.site.register(AutoLinkMessageQuestion)


class ButtonLinkAnswerInline(admin.StackedInline):
    model = ButtonLinkMessageQuestion
    fields = ('question',)
    extra = 1
class AdditionalBtnLinkInline(admin.TabularInline):
    model = AdditionalBtnLink
    fields = ('button_link', 'button_name',)
    extra = 1

@admin.register(ButtonLinkMessage)
class ButtonLinkMessageAdmin(admin.ModelAdmin):
    list_display = ['parent_message', 'text']
    inlines = [ButtonLinkAnswerInline, AdditionalBtnLinkInline]
    
    def save_model(self, request, obj, form, change):
        # save the parent message object first
        super().save_model(request, obj, form, change)
        
        # create and save a new question object under the parent message
        if not change: # only if this is a new parent message
            new_question = ButtonLinkMessageQuestion(q_id=obj, question=obj.parent_message)
            new_question.save()

admin.site.register(ButtonLinkMessageQuestion)


