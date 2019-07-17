from django.shortcuts import render,get_object_or_404,redirect
from catalog.models import Book,Author,BookInstance,Genre
from django.views import generic
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from catalog.forms import RenewBookForm
from django.contrib import messages
from catalog.forms import UserRegistrationForm
# Create your views here.
def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    num_authors = Author.objects.count()

    num_visits = request.session.get('num_visits',0)
    request.session['num_visits'] = num_visits + 1
    context = {
        'num_books' : num_books,
        'num_instances' : num_instances,
        'num_instances_available' : num_instances_available,
        'num_authors' : num_authors,
        'num_visits' : num_visits,
    }

    return render(request,'index.html',context=context)

class BookListView(generic.ListView):
    model = Book
    paginate_by = 2

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 2

class AuthorDetailView(generic.DetailView):
    model = Author

from django.contrib.auth.mixins import LoginRequiredMixin


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


# Added as part of challenge!
from django.contrib.auth.mixins import PermissionRequiredMixin


class LoanedBooksAllListView(PermissionRequiredMixin, generic.ListView):
    """Generic class-based view listing all books on loan. Only visible to users with can_mark_returned permission."""
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


from django.contrib.auth.decorators import permission_required
@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request,pk):
    book_instance = get_object_or_404(BookInstance,pk=pk)

    if request.method == 'POST':

        form = RenewBookForm(request.POST)


        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewable_date']
            book_instance.save()

            return HttpResponseRedirect(reverse('all-borrowed'))
    else:
        proposed_renewable_date = datetime.date.today() +datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewable_date':proposed_renewable_date})

    context = {
    'form':form,
    'book_instance':book_instance,
    }

    return render(request,'catalog/book_renew_librarian.html',context)

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    initial = {'date_of_birth':'05/01/2019'}

class AuthorUpdate(UpdateView):
    model =Author
    fields = ['first_name','last_name','date_of_birth','date_of_death']

class AuthorDelete(DeleteView):
    model= Author
    success_url = reverse_lazy('authors')

class BookCreate(CreateView):
    model = Book
    fields = '__all__'

class BookUpdate(UpdateView):
    model = Book
    fields ='__all__'

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Account is successfully created for {username}, Login to continue !')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request,'catalog/register.html',{'form':form})
