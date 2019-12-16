# quiz/api/serializers.py
import json
from tastypie.serializers import Serializer


class QuizAttemptJSONSerializer(Serializer):
    json_indent = 0

    def to_json(self, data, options=None):
        options = options or {}
        data = self.to_simple(data, options)
        if 'responses' in data:
            del data['responses']
        return json.dumps(data,
                          sort_keys=True,
                          ensure_ascii=False,
                          indent=self.json_indent)
