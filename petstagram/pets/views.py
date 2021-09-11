from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, CreateView, ListView, UpdateView, DeleteView

from petstagram.common.forms import CommentForm, CommentModelForm
from petstagram.common.models import Comment
from petstagram.pets.forms import PetForm, CommentPetForm
from petstagram.pets.models import Pet, Like


class PostOnlyView(View):
    form_class = None

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
       pass

    def form_invalid(self, form):
        pass


class ListPetsView(ListView):
    model = Pet
    template_name = 'pets/pet_list.html'
    success_url = 'list pets'


class PetDetailsView(DetailView):
    model = Pet
    template_name = 'pets/pet_detail.html'
    context_object_name = 'pet'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pet = context['pet']
        pet.likes_count = pet.like_set.count()
        is_owner = pet.user == self.request.user
        is_liked_by_user = pet.like_set.filter(user_id=self.request.user.id).exists()

        context['comment_form'] = CommentForm(initial={'pet_pk': self.object.id})
        context['pet'] = pet
        context['comments'] = pet.comment_set.all()
        context['is_owner'] = is_owner
        context['is_liked'] = is_liked_by_user

        return context


class CommentPetView(LoginRequiredMixin, View):
    form_class = CommentPetForm
    success_url = 'pet details'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        text = form.cleaned_data['comment']
        pet = Pet.objects.get(pk=self.kwargs['pk'])
        comment = Comment(
            comment=text,
            pet=pet,
            user=self.request.user
        )
        comment.save()
        return redirect('pet details', pet.id)

    def form_invalid(self, form):
        pass


class CreateLikeView(LoginRequiredMixin, View):
    like = None

    def post(self, request, *args, **kwargs):
        pet = Pet.objects.get(pk=self.request.kwargs['pk'])
        is_liked_by_user = pet.like_set.filter(user_id=self.request.user.id).first()
        if is_liked_by_user:
            is_liked_by_user.delete()
        else:
            like = Like(pet=pet,
                        user=self.request.user
                        )
            like.save()
        return redirect('pet details', pet.id)


@login_required()
def like_pet(request, pk):
    pet = Pet.objects.get(pk=pk)
    is_liked_by_user = pet.like_set.filter(user_id=request.user.id).first()
    if is_liked_by_user:
        is_liked_by_user.delete()
    else:
        like = Like(pet=pet,
                    user=request.user
                    )
        like.save()
    return redirect('pet details', pet.id)


class CreatePetView(LoginRequiredMixin, CreateView):
    model = Pet
    template_name = 'pets/pet_create.html'
    fields = ['name', 'age', 'description', 'image', 'type']
    success_url = reverse_lazy('list pets')

    def form_valid(self, form):
        pet = form.save(commit=False)
        pet.user = self.request.user
        pet.save()
        return super().form_valid(form)


class EditPetView(LoginRequiredMixin, UpdateView):
    model = Pet
    template_name = 'pets/pet_edit.html'
    form_class = PetForm
    success_url = reverse_lazy('list pets')


class DeletePetView(LoginRequiredMixin, DeleteView):
    model = Pet
    template_name = 'pets/pet_delete.html'
    success_url = reverse_lazy('list pets')




