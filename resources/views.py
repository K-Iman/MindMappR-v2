from django.shortcuts import render

# Leaving accessible without login_required so public users can still view emergency contacts if needed,
# though it hooks elegantly into the authenticated dashboard as well!
def resources_list(request):
    return render(request, 'resources/index.html')
