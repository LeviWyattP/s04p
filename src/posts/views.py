from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone  
try:
    # Python 3.x
    from urllib.parse import quote_plus
except:
    # Python 2.x
    from urllib import quote_plus

# Create your views here.
from .models import Post
from .forms import PostForm


def post_create(request):

    # set permissioning
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form = PostForm(request.POST or None,
                    request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, "Successfully Created")
        return(HttpResponseRedirect(instance.get_absolut_url()))

    # this is a bad way to do it!!
    # if request.method == "POST":
    #     print(request.POST.get("content"))
    #     print(request.POST.get("title"))

    context = {
        "form": form,
        }

    return render(request, "post_form.html", context)


def post_detail(request, id=None):

    instance = get_object_or_404(Post, id=id)
    if instance.draft or instance.publish > timezone.now().date():
        if not request.user.is_staff or not request.user.is_superuser:
            raise(Http404)
    share_string = quote_plus(instance.content)
    context = {
        "title": instance.title,
        "instance": instance,
    }

    return render(request, "post_detail.html", context)


def post_list(request):
    today = timezone.now().date()
    queryset_list = Post.objects.active()
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all()
    paginator = Paginator(queryset_list, 5)  # Show 5 entries per page

    page_request_var = "page"
    page = request.GET.get(page_request_var)

    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context = {
        "object_list": queryset,
        "title": "List",
        "page_request_var": page_request_var,
        "today":today,
        }

    return render(request, 'post_list.html', context)


def post_update(request, id=None):

    # set permissioning
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    instance = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None,
                    request.FILES or None,
                    instance=instance)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Item Sucessfully Saved",
                         extra_tags='test_tags')
        return(HttpResponseRedirect(instance.get_absolut_url()))
    
    context = {
        "title": instance.title,
        "instance": instance,
        "form": form,
    }

    return render(request, "post_form.html", context)


def post_delete(request):

    instance = get_object_or_404(Post, id=id)
    instance.delete()
    messages.success(request, "Sucessfully Deleted")
    return(redirect("posts:list"))


def post_home(request):

    return HttpResponse("<h1>Hello</h1>")


def posts_home(request):

    return HttpResponse("<h1>Hello</h1>")

