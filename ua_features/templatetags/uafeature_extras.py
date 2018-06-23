import arrow
from django import template
from django.core.urlresolvers import reverse

register = template.Library()


@register.filter
def get_total_subject_posts(subject):
    total_posts = 0
    for feature in subject.features.all():
        total_posts += feature.feature_posts.count()
    return total_posts


@register.filter
def started_time(created_at):
    return arrow.get(created_at).humanize()


@register.simple_tag
def last_posted_user_name(feature):
    last_post = feature.feature_posts.all().order_by('created_at').last()
    return last_post.user.username


@register.simple_tag
def user_vote_button(feature, subject, user):
    vote = feature.feature_votes.filter(user_id=user.id).first()

    if not vote:
        if user.is_authenticated():
            link = """
            <div class="col-md-3 btn-vote"> 
            <a href="%s" class="btn btn-default btn-sm">
              {{feature.paypal_form.sandbox}}
            </a>
            </div>""" % reverse('cast_feature_vote',
                                kwargs={'feature_id': feature.id, 'subject_id': feature.subject_id})

            return link

    return ""


@register.simple_tag
def vote_tally(feature):
    feature.feature_votes_count += 1

    return ""


@register.filter
def vote_count(subject):
    count = subject.feature_votes.count()
    if count == 0:
        return 0
    total_votes = subject.feature_votes.count()
    return total_votes
