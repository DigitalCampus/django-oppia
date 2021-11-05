from django.contrib import messages


class MessagesDelegate(object):

    def __init__(self, request=None):
        self.request = request


    def warning(self, message, extra_tags='', fail_silently=False):
        if self.request:
            messages.warning(self.request, message, extra_tags=extra_tags, fail_silently=fail_silently)
        else:
            print(message)


    def info(self, message, extra_tags='', fail_silently=False):
        if self.request:
            messages.info(self.request, message, extra_tags=extra_tags, fail_silently=fail_silently)
        else:
            print(message)