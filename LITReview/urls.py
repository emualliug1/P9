"""LITReview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import blog.views
from django.contrib.auth.views import LogoutView
import authentication.views
import blog.views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', authentication.views.LoginPageView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/', authentication.views.ChangePassword.as_view(), name='password-change'),
    path('change-password/done/', authentication.views.ChangePasswordDone.as_view(), name='password-change-done'),
    path('signup/', authentication.views.SignupPageView.as_view(), name='signup'),
    path('ticket/', blog.views.TicketView.as_view(), name='ticket'),
    path('ticket/<int:id>/review/', blog.views.ReviewView.as_view(), name='review'),
    path('ticket-review/', blog.views.TicketReviewView.as_view(), name='ticket-review'),
    path('posts/', blog.views.PostView.as_view(), name='posts'),
    path('ticket/<int:id>/update/', blog.views.TicketUpdateView.as_view(), name='ticket-update'),
    path('ticket/<int:id>/delete/', blog.views.TicketDeleteView.as_view(), name='ticket-delete'),
    path('review/<int:id>/update/', blog.views.ReviewUpdateView.as_view(), name='review-update'),
    path('review/<int:id>/delete/', blog.views.ReviewDeleteView.as_view(), name='review-delete'),
    path('follow/', blog.views.UserFollowsView.as_view(), name='follow'),
    path('follow/<int:id>/delete/', blog.views.delete_follow, name='delete-follow'),
    path('follow_test/', blog.views.UserFollowsView.as_view(), name='follow-test'),
    path('flux/', blog.views.FluxViews.as_view(), name='flux'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
