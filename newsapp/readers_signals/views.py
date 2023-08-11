from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View

from newsapp.readers_signals.forms import SignalForm


# Create your views here.
class SubmitSignalView(View):
    template_name = 'base/signals.html'  # Create this template path
    success_template_name = 'base/success.html'

    def get(self, request, *args, **kwargs):
        form = SignalForm()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = SignalForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, self.success_template_name)
        context = {'form': form}
        return render(request, self.template_name, context)

