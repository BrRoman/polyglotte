from django import forms
from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic

from .form import VerseForm
from .models import Verse


class HomeView(generic.RedirectView):
    def get_redirect_url(self):
        return reverse('bible:list', args=['Gn', 1])


class VersesList(generic.ListView):
    template_name = 'bible/list.html'
    model = Verse

    def get_queryset(self, **kwargs):
        queryset = Verse.objects.filter(
            book=self.kwargs['book'], chapter=self.kwargs['chapter'])
        return queryset

    def get_context_data(self, ** kwargs):
        context = super().get_context_data(**kwargs)

        # Books:
        context['books'] = []
        books = Verse.objects.values('book')
        for item in books:
            if not item['book'] in context['books']:
                context['books'].append(item['book'])

        # Chapters:
        chapters = []
        verses = Verse.objects.filter(
            book=self.kwargs['book']).values('chapter')
        for item in verses:
            if not item['chapter'] in chapters:
                chapters.append(item['chapter'])
        context['chapters'] = chapters

        # Current book and chapter:
        context['current_book'] = self.kwargs['book']
        context['current_chapter'] = self.kwargs['chapter']
        return context


class VerseUpdate(generic.UpdateView):
    model = Verse
    form_class = VerseForm
    template_name = 'bible/form.html'

    def get_object(self):
        params = self.kwargs
        verse = Verse.objects.get(
            book=params['book'], chapter=params['chapter'], verse=params['verse'])
        return verse

    def form_valid(self, form):
        form.save()
        return redirect(reverse('bible:list', kwargs={'book': self.kwargs['book'], 'chapter': self.kwargs['chapter']}))
