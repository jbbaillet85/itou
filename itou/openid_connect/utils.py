from itou.utils import constants as global_constants


def init_user_nir_from_session(request, user):
    existing_subscription_data = request.session.get(global_constants.ITOU_SESSION_JOB_SEEKER_SIGNUP_KEY)
    if existing_subscription_data:
        user.jobseeker_profile.nir = existing_subscription_data["nir"]
        user.jobseeker_profile.lack_of_nir_reason = ""
        user.jobseeker_profile.save(update_fields=["nir", "lack_of_nir_reason"])
        request.session.pop(global_constants.ITOU_SESSION_JOB_SEEKER_SIGNUP_KEY)

    # TODO(calum): job_seeker_nir is a depreciated cache key, remove the second condition in a few days
    existing_nir = request.session.get(global_constants.ITOU_SESSION_NIR_KEY)
    if existing_nir:
        user.jobseeker_profile.nir = existing_nir
        user.jobseeker_profile.lack_of_nir_reason = ""
        user.jobseeker_profile.save(update_fields=["nir", "lack_of_nir_reason"])
        request.session.pop(global_constants.ITOU_SESSION_NIR_KEY)