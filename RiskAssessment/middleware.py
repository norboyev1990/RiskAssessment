from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin

class CurrentAppMiddleware(MiddlewareMixin):
    def process_view(self, request, *args, **kwargs):
        if request.POST.get('current_month'):
            request.session['data_month'] = request.POST.get('current_month')
            HttpResponseRedirect(request.path_info)

        if request.user.is_authenticated and 'data_month' not in request.session:
            request.session['data_month'] = "2020-08"

        namespace = request.resolver_match.namespace
        request.current_app = namespace if namespace else None

        current_month = request.session['data_month'] if 'data_month' in request.session else None
        request.current_month = current_month
