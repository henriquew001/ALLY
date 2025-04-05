from django.shortcuts import render
from django.utils.translation import gettext as _

def about_view(request):
    return render(request, 'about/about.html', {'title': _('About Us')})
