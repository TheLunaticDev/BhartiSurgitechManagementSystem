from django.contrib.auth.models import Group

def user_groups(request):
    if request.user.is_authenticated:
        return {
            'is_manager': request.user.groups.filter(name='Manager').exists(),
            'is_employee': request.user.groups.filter(name='Employee').exists(),
        }
    return {
        'is_manager': False,
        'is_employee': False,
    }