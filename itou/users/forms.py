from itou.users.models import JobSeekerProfile


class JobSeekerProfileFieldsMixin:
    """Mixin to add JobSeekerProfile's fields to an User ModelForm"""

    PROFILE_FIELDS = []

    def __init__(self, *args, instance, **kwargs):
        profile_initial = {}
        if instance:
            for field in self.PROFILE_FIELDS:
                profile_initial[field] = getattr(instance.jobseeker_profile, field)
        initial = kwargs.pop("initial", {})
        super().__init__(*args, instance=instance, initial=profile_initial | initial, **kwargs)
        for field in self.PROFILE_FIELDS:
            self.fields[field] = JobSeekerProfile._meta.get_field(field).formfield()

    def save(self, commit=True):
        user = super().save(commit=commit)
        for field in self.PROFILE_FIELDS:
            setattr(user.jobseeker_profile, field, self.cleaned_data[field])
        if commit:
            user.jobseeker_profile.save(update_fields=self.PROFILE_FIELDS)