# oppia/quiz/api/serializers.py
import json
from tastypie.serializers import Serializer
        
class QuizJSONSerializer(Serializer):
    json_indent = 0
    def to_json(self, data, options=None):
        options = options or {}
        data = self.to_simple(data, options)
    
        if 'objects' in data:
            for o in data['objects']:
                self.format_quiz(o)
            data['quizzes'] = data['objects']
            del data['objects']
        if 'questions' in data:
            self.format_quiz(data)
        
        return json.dumps(data, sort_keys=True, ensure_ascii=False,  indent=self.json_indent)
        
    def format_quiz(self, data):
        
        qmaxscore = 0.0
        # remove intermediate quizquestion data
        for question in data['questions']:
            del question['question']['owner']
            del question['question']['resource_uri']
            if 'props' in question['question']:
                question['question']['p'] = {}
                for p in question['question']['props']:
                    try:
                        question['question']['p'][p['name']] = float(p['value'])
                    except:
                        question['question']['p'][p['name']] = p['value']
                question['question']['props'] = question['question']['p']
                del question['question']['p']
                try:
                    float(question['question']['props']['maxscore'])
                    qmaxscore = qmaxscore + float(question['question']['props']['maxscore'])
                except:
                    qmaxscore = qmaxscore
            
           # for response in question['response']:
            for r in question['question']['responses']:
                del r['question']
                del r['resource_uri']
                r['p'] = {}
                for p in r['props']:
                    r['p'][p['name']] = p['value']
                r['props'] = r['p']
                del r['p']
        # calc maxscore for quiz
        data['p'] = {}
        data['p']['maxscore'] = qmaxscore
        for p in data['props']:
            data['p'][p['name']] = p['value']
        data['props'] = data['p']
        del data['p']  
        
         
        return data  
    
class QuizAttemptJSONSerializer(Serializer):
    json_indent = 0

    def to_json(self, data, options=None):
        options = options or {}
        data = self.to_simple(data, options)
        if 'responses' in data:
            del data['responses']
        return json.dumps(data, sort_keys=True, ensure_ascii=False, indent=self.json_indent)