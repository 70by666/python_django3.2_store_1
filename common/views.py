from django.urls import reverse_lazy


class CommonContextMixin:
    title = None
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        
        return context


class ReverseProfileMixin:
    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.request.user.id,))
