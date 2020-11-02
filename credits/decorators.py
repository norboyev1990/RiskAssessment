from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse


def group_required(*group_names):
    """
    Requires user membership in at least one of the groups passed in.

    """

    def in_groups(u):
        if u.is_authenticated:
            if u.is_superuser or bool(u.groups.filter(name__in=group_names)):
                return True
        return False

    return user_passes_test(in_groups, login_url='/page_403/', redirect_field_name=None)

def teacher_required(function=None):

    def _function(request, *args, **kwargs):
        if not request.user.is_authenticated:
            if not request.user.is_superuser and not bool(request.user.groups.filter(name__in='')):
                messages.info(request, 'Custom message to user')
                return HttpResponseRedirect(reverse('page_404'))
        return function(request, *args, **kwargs)

    return _function