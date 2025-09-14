from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Movie, Review, ReviewLike

# Create your tests here.

class ReviewLikeTestCase(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create test movie
        self.movie = Movie.objects.create(
            name='Test Movie',
            price=10,
            description='A test movie',
            image='test.jpg'
        )
        
        # Create test review
        self.review = Review.objects.create(
            comment='Great movie!',
            movie=self.movie,
            user=self.user
        )
    
    def test_like_review(self):
        """Test that a user can like a review"""
        self.client.login(username='testuser', password='testpass123')
        
        # Like the review
        response = self.client.post(
            reverse('movies.like_review', args=[self.movie.id, self.review.id])
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(ReviewLike.objects.filter(
            review=self.review, 
            user=self.user
        ).exists())
        
        # Check that like count was updated
        self.review.refresh_from_db()
        self.assertEqual(self.review.like_count, 1)
    
    def test_unlike_review(self):
        """Test that a user can unlike a review"""
        self.client.login(username='testuser', password='testpass123')
        
        # First like the review
        ReviewLike.objects.create(review=self.review, user=self.user)
        self.review.like_count = 1
        self.review.save()
        
        # Unlike the review
        response = self.client.post(
            reverse('movies.unlike_review', args=[self.movie.id, self.review.id])
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertFalse(ReviewLike.objects.filter(
            review=self.review, 
            user=self.user
        ).exists())
        
        # Check that like count was updated
        self.review.refresh_from_db()
        self.assertEqual(self.review.like_count, 0)
