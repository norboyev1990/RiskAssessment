from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext as _

@login_required
def index(request):
    title = _("Clients")
    context = {
        "page_title": title
    }
    return render(request, 'clients/index.html', context)
