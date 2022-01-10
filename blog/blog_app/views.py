# from django.core import Paginator
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Post
from .forms import EmailPostForm
from django.core.mail import send_mail
# from django.core.paginator import Paginator, EmptyPage, \
#     PageNotAnInteger
from django.views.generic import ListView

# Create your views here.


class PostListView(ListView):

    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog_app/post/list.html'

# def post_list(request):
#     object_list = Post.published.all()
#     paginator = Paginator(object_list, 3)
#     page = request.GET.get('page')
#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         # if page is not an integer deliver the first page
#         posts = paginator.page(1)
#     except EmptyPage:
#         # If page is out of range deliver last page of reults
#         posts = paginator.page(paginator.num_pages)

#     return render(request,
#                   'blog_app/post/list.html',
#                   {'page': page,
#                    'posts': posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request,
                  'blog_app/post/detail.html',
                  {'post': post})


def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        # Forms was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form field is submitted
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url)
            subject = f"{cd['name']} recommends you to  read " \
                f"{post.title}"
            message = f"Read {post.title} at {post_url} \n \n" \
                f"{cd['name']} \'s comments: {cd['comments']}"
            # Send email
            send_mail(subject, message,
                      'nuhuabdulmajid58@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog_app/post/share.html', {'post': post,
                                                        'form': form,
                                                        'sent': sent})
