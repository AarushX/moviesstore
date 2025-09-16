from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review, ReviewLike
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
# Create your views here.


def index(request):
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()
    template_data = {}
    template_data['title'] = 'Movies'
    template_data['movies'] = movies
    return render(request, 'movies/index.html',
                    {'template_data': template_data})

def show(request, id):
    movie = Movie.objects.get(id=id)
    
    # Get sorting parameter
    sort_by = request.GET.get('sort', 'date')  # Default to date
    
    # Get non-hidden reviews with like counts
    reviews = Review.objects.filter(movie=movie, is_hidden=False).select_related('user')
    
    # Apply sorting
    if sort_by == 'user':
        reviews = reviews.order_by('user__username')
    else:  # Default to date
        reviews = reviews.order_by('-date')
    
    # Get user's likes for this movie's reviews
    user_likes = set()
    if request.user.is_authenticated:
        user_likes = set(ReviewLike.objects.filter(
            review__in=reviews, 
            user=request.user
        ).values_list('review_id', flat=True))
    
    template_data = {}
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['reviews'] = reviews
    template_data['user_likes'] = user_likes
    template_data['sort_by'] = sort_by
    return render(request, 'movies/show.html',
                  {'template_data': template_data})

@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment'] != '':
        movie = Movie.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment']
        review.movie = movie
        review.user = request.user
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)
    
@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)
    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'movies/edit_review.html',
            {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)
    
@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id,
        user=request.user)
    review.delete()
    return redirect('movies.show', id=id)

@login_required
@require_POST
def report_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id, movie_id=id)
    # Anyone authenticated can report; hide it immediately
    review.is_hidden = True
    review.save(update_fields=['is_hidden'])
    messages.success(request, 'Thanks for reporting. The review has been hidden and will be reviewed by admins.')
    return redirect('movies.show', id=id)

@login_required
@require_POST
def like_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    like, created = ReviewLike.objects.get_or_create(
        review=review, 
        user=request.user
    )
    
    if created:
        # Update like count
        review.like_count += 1
        review.save()
        return JsonResponse({'liked': True, 'like_count': review.like_count})
    else:
        return JsonResponse({'liked': False, 'like_count': review.like_count})

@login_required
@require_POST
def unlike_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    try:
        like = ReviewLike.objects.get(review=review, user=request.user)
        like.delete()
        # Update like count
        review.like_count = max(0, review.like_count - 1)
        review.save()
        return JsonResponse({'liked': False, 'like_count': review.like_count})
    except ReviewLike.DoesNotExist:
        return JsonResponse({'liked': False, 'like_count': review.like_count})