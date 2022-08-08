from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from .forms import TicketForm, ReviewForm
from .models import UserFollows, Ticket, Review
from authentication.models import User
from django.db.models import Q
from django.contrib import messages
from django.db.utils import IntegrityError
from itertools import chain


class TicketView(View):
    template_name = 'blog/ticket.html'
    form_class = TicketForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('posts')
        return render(request, self.template_name, context={'form': form})


class ReviewView(View):
    template_name = 'blog/review.html'
    review_form = ReviewForm
    ticket = Ticket

    def get(self, request, id):
        ticket = get_object_or_404(Ticket, id=id)
        form = self.review_form()
        return render(request, self.template_name, context={'ticket': ticket, 'form': form})

    def post(self, request, id):
        form = self.review_form(request.POST)
        ticket = get_object_or_404(Ticket, id=id)
        if form.is_valid():
            review = form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            ticket.has_review = True
            ticket.save()
            return redirect("posts")
        return render(request, self.template_name, context={'ticket': ticket, 'form': form})


class TicketReviewView(View):
    template_name = 'blog/ticket_review.html'
    ticket_form = TicketForm
    review_form = ReviewForm

    def get(self, request):
        form_ticket = self.ticket_form()
        form_review = self.review_form()
        return render(request, self.template_name, context={'form_ticket': form_ticket, 'form_review': form_review})

    def post(self, request):
        form_ticket = self.ticket_form(request.POST, request.FILES)
        form_review = self.review_form(request.POST)
        if all([form_ticket.is_valid(), form_review.is_valid()]):
            ticket = form_ticket.save(commit=False)
            ticket.user = request.user
            ticket.has_review = True
            ticket.save()
            review = form_review.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            return redirect('posts')
        return render(request, self.template_name, context={'form_ticket': form_ticket, 'form_review': form_review})


class PostView(View):
    tickets = Ticket
    reviews = Review
    template_name = 'blog/post.html'

    def get(self, request):
        tickets_user = self.tickets.objects.filter(Q(user=request.user))
        reviews_user = self.reviews.objects.filter(Q(user=request.user))

        tickets_user_reviews_user = sorted(chain(tickets_user, reviews_user),
                                           key=lambda obj: obj.time_created,
                                           reverse=True)

        return render(request, self.template_name, context={'tickets_user': tickets_user,
                                                            'tickets_user_reviews_user': tickets_user_reviews_user})


class TicketUpdateView(View):
    template_name = 'blog/ticket_update.html'
    ticket = Ticket
    ticket_form = TicketForm

    def get(self, request, id):
        ticket = self.ticket.objects.get(id=id)
        form = self.ticket_form(instance=ticket)
        return render(request, self.template_name, context={'form': form})

    def post(self, request, id):
        ticket = self.ticket.objects.get(id=id)
        form = self.ticket_form(request.POST, instance=ticket)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('posts')
        return render(request, self.template_name, context={'form': form})


class TicketDeleteView(View):
    template_name = 'blog/ticket_delete.html'
    ticket = Ticket
    ticket_form = TicketForm

    def get(self, request, id):
        ticket = self.ticket.objects.get(id=id)
        form = self.ticket_form(instance=ticket)
        return render(request, self.template_name, context={'form': form})

    def post(self, request, id):
        ticket = self.ticket.objects.get(id=id)
        ticket.delete()
        return redirect('posts')


class ReviewUpdateView(View):
    template_name = 'blog/review_update.html'
    review = Review
    review_form = ReviewForm

    def get(self, request, id):
        review = self.review.objects.get(id=id)
        form = self.review_form(instance=review)
        return render(request, self.template_name, context={'form': form})

    def post(self, request, id):
        review = self.review.objects.get(id=id)
        form = self.review_form(request.POST, instance=review)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('posts')
        return render(request, self.template_name, context={'form': form})


class ReviewDeleteView(View):
    template_name = 'blog/review_delete.html'
    review = Review
    review_form = ReviewForm

    def get(self, request, id):
        review = self.review.objects.get(id=id)
        form = self.review_form(instance=review)
        return render(request, self.template_name, context={'form': form})

    def post(self, request, id):
        review = self.review.objects.get(id=id)
        review.delete()
        return redirect('posts')


class UserFollowsView(View):
    template_name = 'blog/follow.html'
    user_follow = UserFollows
    user = User

    def get(self, request):
        following = self.user_follow.objects.filter(user=request.user.id)
        followers = self.user_follow.objects.filter(followed_user=request.user.id)
        return render(request, self.template_name, context={"following": following, "followers": followers})

    def post(self, request):
        following = self.user_follow.objects.filter(user=request.user.id)
        followers = self.user_follow.objects.filter(followed_user=request.user.id)
        user_connect = request.user
        user_followed = request.POST["following"]
        if request.POST:

            if str(user_connect) == user_followed:
                messages.error(request, "Impossible de se suivre")
                return redirect('follow')

            try:
                user = self.user.objects.get(username=user_followed)
                follow = self.user_follow()
                follow.user = user_connect
                follow.followed_user = user
                follow.save()
                messages.success(request, f"{user_followed} Ajouté")

            except IntegrityError:
                messages.error(request, f"Vous êtes deja abonné à {user_followed}")

        return render(request, self.template_name, context={"following": following, "followers": followers})


def delete_follow(request, id):
    user = get_object_or_404(User, id=id)
    remove_user = UserFollows.objects.get(user=request.user.id, followed_user=user)
    remove_user.delete()
    messages.success(request, f" {user} retiré")
    return redirect("follow-test")


class FluxViews(View):
    template_name = 'blog/flux.html'

    def get(self, request):
        users_followers = UserFollows.objects.filter(user=request.user)
        users = []
        for user in users_followers:
            users.append(user.followed_user)

        tickets = Ticket.objects.filter((Q(user=request.user) | Q(user__in=users)))
        reviews = Review.objects.filter(Q(user=request.user) | Q(user__in=users))
        tickets_reviews = sorted(chain(tickets, reviews), key=lambda obj: obj.time_created, reverse=True)

        return render(request, self.template_name, context={'tickets_reviews': tickets_reviews})
