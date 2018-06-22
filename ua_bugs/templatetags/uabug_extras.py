import arrow
from django import template
from django.core.urlresolvers import reverse
 
register = template.Library()
 
@register.filter
def get_total_subject_posts(subject):
   total_posts = 0
   for bug in subject.bugs.all():
       total_posts += bug.posts.count()
   return total_posts


@register.filter
def started_time(created_at):
   return arrow.get(created_at).humanize()
 
 
@register.simple_tag
def last_posted_user_name(bug):
    last_post = bug.posts.all().order_by('created_at').last()
    return last_post.user.username


@register.simple_tag
def user_vote_button(bug, subject, user):
    vote = bug.votes.filter(user_id=user.id).first()
 
    if not vote:
        if user.is_authenticated():
            link = """
            <div class="col-md-3 btn-vote"> 
            <a href="%s" class="btn btn-default btn-sm">
              Add my vote!
            </a>
            </div>""" % reverse('cast_vote', kwargs={'bug_id' : bug.id, 'subject_id':bug.subject_id})
 
            return link
 
    return ""


@register.filter
def vote_count(subject):
   count = subject.votes.count()
   if count == 0:
       return 0
   total_votes = subject.votes.count()
   return total_votes
