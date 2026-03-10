from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Prefetch
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DeleteView, UpdateView

from common.mixin import CheckUserIsOwner
from pets.forms import PetForm
from pets.models import Pet
from photos.models import Photo


# def pet_add(request):
#     form = PetForm(request.POST or None)
#     if request.method == 'POST' and form.is_valid():
#         form.save()
#         return redirect('accounts:details', pk=1)
#     context = {'form': form}
#     return render(request, 'pets/pet-add-page.html', context)

class PetAddView(CreateView):
    model = Pet
    form_class = PetForm
    template_name = 'pets/pet-add-page.html'

    def get_success_url(self):
        return reverse('accounts:details', kwargs={'pk': self.object.user.pk})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


def pet_details(request, username, pet_slug):
    pet = Pet.objects.prefetch_related(Prefetch('photo_set', queryset=Photo.objects.prefetch_related(
    'tagged_pets', 'like_set'
    ))).get(slug=pet_slug)

    context = {'pet': pet}
    return render(request, 'pets/pet-details-page.html', context)

# def pet_edit(request, username, pet_slug):
#     pet = Pet.objects.get(slug=pet_slug)
#     form = PetForm(request.POST or None, instance=pet)
#     if request.method == 'POST' and form.is_valid():
#         instance = form.save()
#         return redirect('pets:details', username='username', pet_slug=instance.slug)
#     context = {'form': form,
#                'pet': pet}
#     return render(request, 'pets/pet-edit-page.html', context)

class PetEditView(CheckUserIsOwner, UpdateView):
    model = Pet
    form_class = PetForm
    slug_url_kwarg = 'pet_slug'
    template_name = 'pets/pet-edit-page.html'

    def test_func(self):
        return self.request.user == self.get_object().user

    def get_success_url(self):
        return reverse('pets:details', kwargs={'username': self.object.user.username, 'pet_slug': self.object.slug})


class PetDeleteView(DeleteView):
    model = Pet
    form_class = PetForm
    slug_url_kwarg = 'pet_slug'
    template_name = 'pets/pet-delete-page.html'

    def get_success_url(self):
        return reverse('accounts:details', kwargs={'pk': self.object.user.pk})

    def get_initial(self):
        return self.object.__dict__


# def pet_delete(request, username, pet_slug):
#     pet = Pet.objects.get(slug=pet_slug)
#     form = PetForm(request.POST or None, instance=pet)
#     if request.method == 'POST' and form.is_valid():
#         pet.delete()
#         return redirect('accounts:details', pk=1)
#     context = {'form': form,
#                'pet': pet}
#
#     return render(request, 'pets/pet-delete-page.html', context)