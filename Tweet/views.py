from django.shortcuts import render, get_object_or_404, redirect
from .models import Tweet,Comment
from .forms import TweetForm, UserRegistrationForm, CommentForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect


def index(request):
    return render(request, 'index.html')




def tweet_list(request):
    query = request.GET.get('q')
    if query:
        tweets = Tweet.objects.filter(
            Q(text__icontains=query) | Q(user__username__icontains=query)
        ).order_by('-created_add')
    else:
        tweets = Tweet.objects.all().order_by('-created_add')

    if request.method == 'POST' and request.user.is_authenticated:
        tweet_id = request.POST.get('tweet_id')
        comment_text = request.POST.get('comment')
        if tweet_id and comment_text:
            tweet = get_object_or_404(Tweet, id=tweet_id)
            Comment.objects.create(tweet=tweet, user=request.user, comment_text=comment_text)
            return redirect('tweet_list')

    return render(request, 'tweet_list.html', {'tweets': tweets})

@login_required
def tweet_create(request):
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()  # FIXED
            return redirect('tweet_list')
    else:
        form = TweetForm()
    return render(request, 'tweet_form.html', {'form': form})


@login_required
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()  # FIXED
            return redirect('tweet_list')
    else:
        form = TweetForm(instance=tweet)
    return render(request, 'tweet_form.html', {'form': form})


@login_required
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == "POST":
        tweet.delete()
        return redirect('tweet_list')
    return render(request, 'tweet_confirm_delete.html', {'tweet': tweet})


def register(request):
    if request.method=='POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request,user)
            return redirect('tweet_list')
    else:
        form = UserRegistrationForm()
 
    return render( request, 'registration/register.html', {'form': form})


@login_required
def like_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    if request.user in tweet.likes.all():
        tweet.likes.remove(request.user)
    else:
        tweet.likes.add(request.user)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
@login_required
def tweet_comments_view(request, tweet_id):
    tweet = Tweet.objects.get(id=tweet_id)
    comments = tweet.comment_set.all().order_by('-created_at')  # or whatever your related_name is
    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.tweet = tweet
            comment.user = request.user  # Make sure user is logged in
            comment.save()
            return redirect('tweet_comments', tweet_id=tweet_id)

    comments = Comment.objects.filter(tweet=tweet)
    return render(request, 'tweet_comments.html', {'tweet': tweet, 'comments': comments})

   

