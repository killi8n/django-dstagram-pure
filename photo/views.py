from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView

from photo.models import Photo


@login_required
def post_list(request):
    objects = Photo.objects.all()
    return render(request, 'photo/list.html', {'photos': objects})

class UploadView(LoginRequiredMixin ,CreateView):
    model = Photo
    fields = ['title', 'text', 'photo', 'tag']
    template_name = 'photo/upload.html'

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        if form.is_valid():
            form.instance.save()
            return redirect(reverse('photo:photo_detail', kwargs={'pk': form.instance.id}))
        else:
            return self.render_to_response({'form': form})


class DetailView(LoginRequiredMixin, DetailView):
    model = Photo

class DeleteView(LoginRequiredMixin, DeleteView):
    model = Photo
    success_url = '/'

    def get(self, request, *args, **kwargs):
        object = self.get_object()
        if object.author != request.user:
            messages.warning(request, "You do not have permissions for deleting this photo")
            return HttpResponseRedirect(object.get_absolute_url())
        else:
            return super(DeleteView, self).get(request, *args, **kwargs)

@receiver(post_delete, sender=Photo)
def post_delete(sender, instance, **kwargs):
    storage, path = instance.photo.storage, instance.photo.path
    if path != '.' and path != 'photos/' and path != 'photos/.':
        storage.delete(path)


class UpdateView(LoginRequiredMixin, UpdateView):
    model = Photo
    fields = ['title', 'text', 'photo', 'tag']
    template_name = 'photo/update.html'

    def get_success_url(self):
        return reverse('photo:photo_detail', kwargs={'pk': self.object.id})



