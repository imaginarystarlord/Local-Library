from django.contrib import admin

# Register your models here.
from .models import Genre,Book,BookInstance,Author,Language

admin.site.register(Genre)
# admin.site.register(Book)
# admin.site.register(BookInstance)
# admin.site.register(Author)
admin.site.register(Language)

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name','first_name','date_of_birth','date_of_death')
    fields = ['first_name','last_name',('date_of_birth','date_of_death')]


admin.site.register(Author,AuthorAdmin)
class BookInstanceInline(admin.TabularInline):
    model = BookInstance
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title','author')
    inlines = [BookInstanceInline]
    # def display_genre(self):
    #     return ', '.join(genre.name for genre in self.genre.all()[:3])
    # display_genre.short_description = 'Genre'
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book','status','borrower','due_back','id')
    list_filter = ('status','due_back')
    fieldsets = (
        (None,{
            'fields':('book','imprint','id')
        }),
        ('Availability',{
            'fields':('status','due_back','borrower')
        })
    )
