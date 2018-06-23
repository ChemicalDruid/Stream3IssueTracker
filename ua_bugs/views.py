# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import BugSubject, UaBug, BugPost, BugVote
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.template.context_processors import csrf
from .forms import UaBugForm, PostForm
from django.forms import formset_factory


def uabugs(request):
    return render(request, 'forum/uabugs.html', {'subjects': BugSubject.objects.all()})


def bugs(request, subject_id):
    subject = get_object_or_404(BugSubject, pk=subject_id)
    return render(request, 'forum/bugs.html', {'subject': subject})


@login_required
def new_bug(request, subject_id):
    subject = get_object_or_404(BugSubject, pk=subject_id)

    if request.method == "POST":
        bug_form = UaBugForm(request.POST)
        post_form = PostForm(request.POST)

        bug_valid = bug_form.is_valid() and post_form.is_valid()

        bug = save_bug(bug_form, post_form, subject, request.user)
        messages.success(request, "You have created a new bug!")
        return redirect(reverse('bug', args=[bug.pk]))

    else:
        bug_form = UaBugForm()
        post_form = PostForm()

    args = {
        'bug_form': bug_form,
        'post_form': post_form,
        'subject': subject
    }

    args.update(csrf(request))

    return render(request, 'forum/bug_form.html', args)


def bug(request, bug_id):
    bug_ = get_object_or_404(UaBug, pk=bug_id)
    args = {'bug': bug_}
    args.update(csrf(request))
    return render(request, 'forum/bug.html', args)


def save_bug(bug_form, post_form, subject, user):
    bug = bug_form.save(commit=False)
    bug.subject = subject
    bug.user = user
    bug.save()

    post = post_form.save(commit=False)
    post.user = user
    post.bug = bug
    post.save()
    return bug


@login_required
def new_post(request, bug_id):
    bug = get_object_or_404(UaBug, pk=bug_id)

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(False)
            post.bug = bug
            post.user = request.user
            post.save()

            messages.success(request, "Your post has been added to the bug!")

            return redirect(reverse('bug', args={bug.pk}))
    else:
        form = PostForm()

    args = {
        'form': form,
        'form_action': reverse('new_post', args={bug.id}),
        'button_text': 'Update Bug Post'
    }
    args.update(csrf(request))

    return render(request, 'forum/post_form.html', args)


@login_required
def edit_post(request, bug_id, post_id):
    bug = get_object_or_404(UaBug, pk=bug_id)
    post = get_object_or_404(BugPost, pk=post_id)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "You have updated your bug!")

            return redirect(reverse('bug', args={bug.pk}))
    else:
        form = PostForm(instance=post)

    args = {
        'form': form,
        'form_action': reverse('edit_post', kwargs={"bug_id": bug.id, "post_id": post.id}),
        'button_text': 'Update Post'
    }
    args.update(csrf(request))

    return render(request, 'forum/post_form.html', args)


@login_required
def delete_post(request, bug_id, post_id):
    post = get_object_or_404(BugPost, pk=post_id)
    bug_id = post.bug.id
    post.delete()

    messages.success(request, "Your post was deleted!")

    return redirect(reverse('bug', args={bug_id}))


@login_required
def bug_vote(request, bug_id, subject_id):
    bug = UaBug.objects.get(id=bug_id)
    vote = bug.votes.filter(user=request.user)
    if vote:
        messages.error(request, "You already upvoted this bug!")
        return redirect(reverse('bug', args={bug_id}))
    else:
        bug.bug_votes += 1
        bug.save()
        BugVote.objects.create(bug=bug, user=request.user)
        return redirect(reverse('bug', args={bug_id}))
