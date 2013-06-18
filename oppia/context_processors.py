# oppia/context_processors.py
from oppia.models import Points, Award

def get_points(request):
    if not request.user.is_authenticated():
        return {'points': 0, 'badges':0 }
    else:
        points = Points.get_userscore(request.user)
        if points is None:
            points = 0
        badges = Award.get_userawards(request.user)
        if badges is None:
            badges = 0
    return {'points': points, 'badges':badges }
