# quiz/api/validation.py

from tastypie.validation import Validation


class QuizAttemptValidation(Validation):
    STR_NO_DATA = 'no data.'

    def is_valid(self, bundle, request=None):
        if not bundle.data:
            return {'__all__': self.STR_NO_DATA}
        errors = {}
        # check all questions actually belong to this quiz

        # check there is a response for every quiz question

        # check marks awarded are consistent with the results stored here

        return errors
