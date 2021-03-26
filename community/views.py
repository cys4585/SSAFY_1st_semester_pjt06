from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_safe, require_POST, require_http_methods
from .forms import ReviewForm, CommentForm
from django.contrib.auth import get_user_model
from .models import Review, Comment
from django.contrib.auth.decorators import login_required


# Create your views here.
@require_safe
def index(request):
    reviews = Review.objects.order_by('-pk')
    context = {
        'reviews':reviews,
    }
    return render(request, 'community/index.html', context)

# Review 작성 
@login_required
@require_http_methods(['POST', 'GET'])
def create(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)    # table에는 저장되지 않는 save
                review.user = request.user          # form에서 user 정보를 입력하지 않기 때문에, request에서 user 정보를 꺼내서 넣어준다.
                review.save()
                return redirect('community:index')
        else:
            form = ReviewForm()
        context = {
            'form':form,
        }
        return render(request, 'community/form.html', context)
    return redirect('community:index')


@require_safe
def detail(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    comments = review.comment_set.all()  # 지금 들어온 review 페이지를 참조하는 comment만 가져오는거죠.
    # comment = Comment.objects.all()   # Comment db 모든 comment 지금 들어온  review 페이지랑 상관 X
    comment_form = CommentForm()
    context = {
        'review':review,
        'comments':comments,
        'comment_form':comment_form,
    }
    return render(request, 'community/detail.html', context)

@require_POST
def create_comment(request, review_pk):
    if request.user.is_authenticated:
        review = get_object_or_404(Review, pk=review_pk)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.review = review
            comment.save()
            return redirect('community:detail', review.pk)
        context = {
            'comment_form':comment_form,
            'review':review,
        }
        return render(request, 'community/detail.html', context)
    return redirect('community:index')