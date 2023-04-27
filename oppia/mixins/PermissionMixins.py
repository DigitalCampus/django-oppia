from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from oppia.models import Participant, Course


class ObjectPermissionRequiredMixin(LoginRequiredMixin):
    """
    Checks that the current user has permission to access this object, raising a PermissionDenied if not.
    For this, the object to check against is obtained from the self.object attribute from SingleObjectMixin,
    so this mixin must be put **after** the view that inherits from that one
    """

    def has_object_permission(self, obj):
        raise NotImplementedError(
            '{} is missing the implementation of the has_object_permission() method.'.format(self.__class__.__name__)
        )

    def get_object(self, *args, **kwargs):
        obj = super().get_object(*args, **kwargs)
        if not self.has_object_permission(obj):
            return self.handle_no_permission()
        return obj


class CanViewUserDetailsMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Verify that the current user can view details of another user. For this, the other user pk is get from
    the URL kwargs. If it is not defined with the SingleObjectMixin `pk_url_kwarg`, the specific kwarg
    can be set under the CVB that uses this mixin on the `user_url_kwarg` property
    """
    user_url_kwarg = None

    def test_func(self):
        if self.user_url_kwarg is not None:
            user_kwarg = self.user_url_kwarg
        else:
            user_kwarg = self.pk_url_kwarg if hasattr(self, 'pk_url_kwarg') else None
        user_pk = int(self.kwargs[user_kwarg]) if user_kwarg in self.kwargs else None

        if self.request.user.is_staff or (self.request.user.id == int(user_pk)):
            # If the user is staff or is the user itself, always can see the details
            return True

        # The logged in user can see other user details if they are a teacher in a course attended by that user
        courses_teached_by = Course.objects.filter(
            coursecohort__cohort__participant__user__pk=user_pk,
            coursecohort__cohort__participant__role=Participant.STUDENT) \
            .filter(
            coursecohort__cohort__participant__user=self.request.user,
            coursecohort__cohort__participant__role=Participant.TEACHER) \

        return courses_teached_by.exists()


class CanEditUserMixin(ObjectPermissionRequiredMixin):
    """
    Verify that the current user can edit the current view user.
    """
    def has_object_permission(self, obj):
        return self.request.user.is_staff or (self.request.user.id == obj.pk)
