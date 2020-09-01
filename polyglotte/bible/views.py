""" bible/views.py """

from django import forms
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic

from .form import VerseForm
from .models import Verse


def home(request):
    """ Home view of Polyglotte: redirect to Gn 1. """
    return redirect(reverse('bible:list', args=['Gn', 1]))


def verses_list(request, **kwargs):
    """ Returns a list of verses. """
    # Requested verses:
    verses = Verse.objects.filter(
        book=kwargs['book'], chapter=kwargs['chapter']).order_by('verse')

    # Books:
    books = ['Gn', 'Ex', 'Lev', 'Num', 'Dt',
             'Jos', 'Jdc', 'Ru', '1 Reg', '2 Reg', '3 Reg', '4 Reg', '1 Par', '2 Par',
             'Neh', 'Esd', 'Tb', 'Jdt', 'Est',
             'Jb', 'Ps', 'Pr', 'Qo', 'Ct', 'Sap', 'Si',
             'Is', 'Jer', 'Lam', 'Ba', 'Ez', 'Dn',
             'Os', 'Jon', 'Am', 'Ab', 'Jl', 'Mi', 'Na', 'So', 'Ha', 'Ag', 'Za', 'Mal',
             '1 Ma', '2 Ma',
             'Mt', 'Mc', 'Lc', 'Jo', 'Ac',
             'Rm', '1 Co', '2 Co', 'Ga', 'Ep', 'Ph', 'Col',
             '1 Th', '2 Th', '1 Tim', '2 Tim', 'Tit', 'Phm', 'He',
             'Jc', '1 Pe', '2 Pe', '1 Jo', '2 Jo', '3 Jo', 'Judæ', 'Ap']

    # Chapters:
    chapters = []
    chapters_of_this_book = Verse.objects.filter(
        book=kwargs['book']).values('chapter')
    for item in chapters_of_this_book:
        if not item['chapter'] in chapters:
            chapters.append(item['chapter'])

    return render(request, 'bible/list.html', {
        'verses': verses,
        'books': books,
        'chapters': chapters,
        'current_book': kwargs['book'],
        'current_chapter': kwargs['chapter'],
    })


def search_view(request):
    """ Returns a set of verses containing a string given in parameter. """
    if request.method == 'POST':
        verses = Verse.objects.filter(
            txt_latin__icontains=request.POST['search'])[:20]

    return render(request, 'bible/search.html', {'verses': verses})


def verse_update(request, **kwargs):
    """ Form of verses. """
    verse = get_object_or_404(
        Verse, book=kwargs['book'], chapter=kwargs['chapter'], verse=kwargs['verse'])

    if request.method == 'POST':
        form_verse = VerseForm(request.POST, instance=verse)
        if form_verse.is_valid:
            form_verse.save()
            return redirect(reverse('bible:list', kwargs={'book': kwargs['book'], 'chapter': kwargs['chapter']}))

    else:
        form_verse = VerseForm(instance=verse)

    return render(request, 'bible/form.html', {'form': form_verse})
