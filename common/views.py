from django.views.generic import TemplateView


SERVER_VERSION = 'Current_version'


class AboutTemplateView(TemplateView):
    template_name = 'common/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['server_version'] = SERVER_VERSION

        return context
