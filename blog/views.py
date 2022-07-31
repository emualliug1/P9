from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from .forms import TicketForm, ReviewForm
from .models import UserFollows, Ticket, Review
from authentication.models import User
from django.db.models import Q
from django.contrib import messages
from django.db.utils import IntegrityError




@login_required
def home(request):
    template_name = 'blog/home.html'
    tickets = Ticket.objects.all()
    reviews = Review.objects.all()
    return render(request, template_name, context={'tickets': tickets, 'reviews': reviews})


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
            return redirect('home')
        return render(request, self.template_name, context={'form': form})


class ReviewView(View):
    template_name = 'blog/review.html'
    form_class = ReviewForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('home')
        return render(request, self.template_name, context={'form': form})


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
            ticket.save()
            review = form_review.save(commit=False)
            review.ticket = ticket
            review.ticket.has_review = True
            review.user = request.user
            review.save()
            return redirect('home')
        return render(request, self.template_name, context={'form_ticket': form_ticket, 'form_review': form_review})


class PostView(View):
    tickets = Ticket
    reviews = Review
    template_name = 'blog/post.html'

    def get(self, request):
        tickets_user = self.tickets.objects.filter(Q(user=request.user))
        reviews_user = self.reviews.objects.filter(Q(user=request.user))
        #tickets_date = sorted(tickets_user, key=itemgetter(time_created), reverse=True)
        #reviews_date = sorted(reviews_user, key=itemgetter(time_created), reverse=True)
        return render(request, self.template_name, context={'tickets_user': tickets_user, 'reviews_user': reviews_user})


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

    def get(self, request):
        following_users = self.user_follow.objects.filter(user=request.user.id)
        users_followers = self.user_follow.objects.filter(followed_user=request.user.id)
        return render(request, "blog/follow.html", context={"following": following_users, "followers": users_followers})

    def post(self, request):
        following_users = self.user_follow.objects.filter(user=request.user.id)
        users_followers = self.user_follow.objects.filter(followed_user=request.user.id)
        if request.POST:
            user = User.objects.get(username=request.POST["following"])

            if str(request.user) == request.POST["following"]:
                messages.error(request, "Impossible de se suivre")
                return redirect('follow')

            try:
                follow = self.user_follow()
                follow.user = request.user
                follow.followed_user = user
                follow.save()
                messages.success(request, f"{request.POST['following']} Ajouté")

            except IntegrityError:
                messages.error(request, f"Vous êtes deja abonné à {user}")

            except request.POST.DoesNotExist:
                messages.error(request, f"n'existe pas")
                return redirect('follow')

            return redirect("follow")

        return render(request, "blog/follow.html", context={"following": following_users, "followers": users_followers})


def delete_follow(request, id):

    user = get_object_or_404(User, id=id)
    remove_user = UserFollows.objects.get(user=request.user.id, followed_user=user)
    remove_user.delete()
    messages.success(request, f"{user} retiré")
    return redirect("follow")




