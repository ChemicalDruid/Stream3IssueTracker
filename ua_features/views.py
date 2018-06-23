# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from .models import Subject, UaFeature, Post, Vote
from django.shortcuts import redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.template.context_processors import csrf
from .forms import UaFeatureForm, PostForm
from django.forms import formset_factory


# Create your views here.

def uafeatures(request):
    return render(request, 'forum/uafeatures.html', {'subjects': Subject.objects.all()})


def features(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)
    return render(request, 'forum/features.html', {'subject': subject})


@login_required
def new_feature(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)

    if request.method == "POST":
        feature_form = UaFeatureForm(request.POST)
        post_form = PostForm(request.POST)

        feature_valid = feature_form.is_valid() and post_form.is_valid()

        feature = save_feature(feature_form, post_form, subject, request.user)
        messages.success(request, "You have created a new feature!")
        return redirect(reverse('feature', args=[feature.pk]))

    else:
        feature_form = UaFeatureForm()
        post_form = PostForm()

    args = {
        'feature_form': feature_form,
        'post_form': post_form,
        'subject': subject
    }

    args.update(csrf(request))

    return render(request, 'forum/feature_form.html', args)


def feature(request, feature_id):
    feature_ = get_object_or_404(UaFeature, pk=feature_id)
    args = {'feature': feature_}
    args.update(csrf(request))
    return render(request, 'forum/feature.html', args)


def save_feature(feature_form, post_form, subject, user):
    feature = feature_form.save(commit=False)
    feature.subject = subject
    feature.user = user
    feature.save()

    post = post_form.save(commit=False)
    post.user = user
    post.feature = feature
    post.save()
    return feature

    subject.save()


@login_required
def new_post(request, feature_id):
    feature = get_object_or_404(UaFeature, pk=feature_id)

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(False)
            post.feature = feature
            post.user = request.user
            post.save()

            messages.success(request, "Your post has been added to the feature!")

            return redirect(reverse('feature', args={feature.pk}))
    else:
        form = PostForm()

    args = {
        'form': form,
        'form_action': reverse('new_feature_post', args={feature.id}),
        'button_text': 'Update Post'
    }
    args.update(csrf(request))

    return render(request, 'forum/post_form.html', args)


@login_required
def edit_post(request, feature_id, post_id):
    feature = get_object_or_404(UaFeature, pk=feature_id)
    post = get_object_or_404(Post, pk=post_id)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "You have updated your feature!")

            return redirect(reverse('feature', args={feature.pk}))
    else:
        form = PostForm(instance=post)

    args = {
        'form': form,
        'form_action': reverse('edit_feature_post', kwargs={"feature_id": feature.id, "post_id": post.id}),
        'button_text': 'Update Post'
    }
    args.update(csrf(request))

    return render(request, 'forum/post_form.html', args)


@login_required
def delete_post(request, feature_id, post_id):
    post = get_object_or_404(Post, pk=post_id)
    feature_id = post.feature.id
    post.delete()

    messages.success(request, "Your post was deleted!")

    return redirect(reverse('feature', args={feature_id}))


@login_required
def feature_vote(request, feature_id, subject_id):
    feature = UaFeature.objects.get(id=feature_id)

    vote = feature.feature_votes.filter(user=request.user)
    if vote:
        messages.error(request, "You have already upvoted this feature!")
        return redirect(reverse('feature', args={feature_id}))
    else:
        feature.feature_votes_count += 1
        feature.save()
        Vote.objects.create(feature=feature, user=request.user)
        return redirect(reverse('feature', args={feature_id}))
