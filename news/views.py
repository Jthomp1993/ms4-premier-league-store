from django.shortcuts import (
    render, redirect, get_object_or_404, reverse,)
from django.contrib import messages
from .models import News, Comments
from .forms import CommentForm

from django.contrib.auth.decorators import login_required


def view_news(request):
    """ A view to render the news page """
    news = News.objects.all()

    context = {
        'news': news,
    }

    return render(request, 'news/news.html', context)


def news_detail(request, news_id):
    """ A view to render the news detail page """
    news = get_object_or_404(News, pk=news_id)
    comments = Comments.objects.filter(news=news_id)
    comment_form = CommentForm(data=request.POST)

    context = {
        'news': news,
        'comments': comments,
        'comment_form': comment_form,
    }

    return render(request, 'news/news_detail.html', context)


@login_required
def add_comment(request, news_id):
    """ A view to add a comment to a news article """
    news = get_object_or_404(News, pk=news_id)
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        comments = Comments.objects.filter(news=news_id)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.user = request.user
            new_comment.news = news
            new_comment.save()
            messages.success(request, 'Your comment has been added!')
            return redirect(reverse('news_detail', args=[news.id]))
        else:
            messages.error(
                request, 'Failed to add your comment. \
                    Please ensure that the form is valid.')
    else:
        comment_form = CommentForm()

    template = 'news/news_detail.html'

    context = {
        'news': news,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
    }

    return render(request, template, context)


@login_required
def edit_comment(request, news_id, comment_id):
    """ A view to edit a comment """
    news = get_object_or_404(News, pk=news_id)
    comment = get_object_or_404(Comments, news=news, pk=comment_id)
    if request.user == comment.user:
        if request.method == 'POST':
            comment_form = CommentForm(request.POST, instance=comment)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.user = request.user
                new_comment.news = news
                new_comment.save()
                messages.success(request, 'Your comment has been updated!')
                return redirect('news_detail', news_id)
            else:
                messages.error(request, 'Unable to update your comment. Please ensure that the \
                form is valid before submitting')

                return redirect('news_detail', news_id)
        else:
            comment_form = CommentForm(instance=comment)
            context = {
                'comment_form': comment_form,
            }
            return render(request, 'news/edit_comment.html', context)
    else:
        return redirect('news_detail', news_id)


@login_required
def delete_comment(request, news_id, comment_id):
    """ A view to delete a comment """
    news = get_object_or_404(News, pk=news_id)
    comment = get_object_or_404(Comments, news=news, pk=comment_id)

    if request.user == comment.user:
        comment.delete()
        messages.success(request, 'Your comment has been deleted!')

    return redirect('news_detail', news_id)


# Sources of guidance used to create this code

# https://djangocentral.com/creating-comments-system-with-django/
# https://github.com/machikolacey/composermlacey/blob/master/products/views.py
