# oppia/context_processors.py
import oppia
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

def get_version(request):
    version = "v" + str(oppia.VERSION[0]) + "." + str(oppia.VERSION[1]) + "." + str(oppia.VERSION[2])
    return {'version': version }
