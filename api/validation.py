# oppia/api/validation.py
import json

from oppia.models import Tracker

from tastypie.validation import Validation


class TrackerValidation(Validation):
    def is_valid(self, bundle, request=None):

        errors = {}
        if bundle.data \
                and 'type' in bundle.data \
                and bundle.data['type'] == 'search':
            # if the tracker is a search, we check that the needed values \
            # are present
            json_data = json.loads(bundle.data['data'])
            if 'query' not in json_data or 'results_count' not in json_data:
                errors['search'] = 'You must include the search term and the \
                                    results count'

        # check this tracker hasn't already been submitted (based on the UUID)
        try:
            json_data = json.loads(bundle.data['data'])
            if 'uuid' in json_data:
                bundle.obj.uuid = json_data['uuid']
                uuids = Tracker.objects.filter(uuid=bundle.obj.uuid)
                if uuids.count() > 0:
                    errors['uuid'] = 'This UUID has already been submitted'
        except json.JSONDecodeError: # invalid json
            pass
        except KeyError:
            pass
        except TypeError: # json_data is none
            pass

        return errors
