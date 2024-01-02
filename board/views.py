from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .models import Note
from .forms import NoteForm


def board_index(request):
    # Upload note
    if request.method == "POST":
        note_form = NoteForm(request.POST)
        if note_form.is_valid():
            note = note_form.save(commit=False)
            note.user = request.user
            note.date_created = timezone.now()
            note.save()

    # Get note from database and display
    notes = Note.objects.all()

    # Render with context
    context = {'notes': notes}
    return render(request, 'board/board-index.html', context)

@login_required(login_url='common:login')
def board_delete(request, id):
    target_data = Note.objects.get(id=id)

    # Process delete only if user matches or user is staff
    if target_data.user == request.user or request.user.is_staff:
        # Delete data from database and redirect to index
        target_data.delete()
        return redirect('board:index')

    # Respond to (403)Forbidden if user does not match
    return HttpResponse(status=403)