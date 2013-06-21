# oppia/api/serializers.py
import json

from tastypie.serializers import Serializer

class PrettyJSONSerializer(Serializer):
    json_indent = 4

    def to_json(self, data, options=None):
        options = options or {}
        data = self.to_simple(data, options)
        return json.dumps(data,
                sort_keys=True, ensure_ascii=False, indent=self.json_indent)

class UserJSONSerializer(Serializer):     
    json_indent = 4

    def to_json(self, data, options=None):
        options = options or {}
        data = self.to_simple(data, options)
        if 'objects' in data:
            data['users'] = data['objects']
            del data['objects']
        return json.dumps(data,
                sort_keys=True, ensure_ascii=False, indent=self.json_indent)
          
class CourseJSONSerializer(Serializer):

    def to_json(self, data, options=None):
        options = options or {}
        data = self.to_simple(data, options)
    
        if 'objects' in data:
            data['courses'] = data['objects']
            del data['objects']

        return json.dumps(data,  sort_keys=True)

class ModuleJSONSerializer(Serializer):

    def to_json(self, data, options=None):
        options = options or {}
        data = self.to_simple(data, options)
    
        if 'objects' in data:
            data['modules'] = data['objects']
            del data['objects']

        return json.dumps(data,  sort_keys=True)

class ScorecardJSONSerializer(Serializer):

    def to_json(self, data, options=None):
        options = options or {}
        data = self.to_simple(data, options)
    
        if 'objects' in data:
            data['scorecards'] = data['objects']
            del data['objects']

        return json.dumps(data,  sort_keys=True)

class TagJSONSerializer(Serializer):
    json_indent = 4
    def to_json(self, data, options=None):
        options = options or {}
        data = self.to_simple(data, options)
    
        if 'objects' in data:
            data['tags'] = data['objects']
            del data['objects']
            for t in data['tags']:
                del t['courses'] 
        
        if 'courses' in data:
            new_courses = []
            for m in data['courses']:
                new_courses.append(m['course'])
            del data['courses']
            data['courses'] = new_courses
        return json.dumps(data, sort_keys=True, ensure_ascii=False)