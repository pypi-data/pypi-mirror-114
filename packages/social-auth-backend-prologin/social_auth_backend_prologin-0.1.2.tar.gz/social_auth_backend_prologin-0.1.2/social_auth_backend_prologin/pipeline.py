def save_all_claims_as_extra_data(
    response, storage, social=None, *_args, **_kwargs
):
    """Update user extra-data using data from provider."""
    if not social:
        return

    social.extra_data = response
    storage.user.changed(social)


def apply_upstream_security_clearances(
    storage, backend, details, social=None, user=None, *_args, **_kwargs
):
    if not user or backend.name != "prologin":
        return

    is_staff = social.extra_data.get("is_staff", False)
    is_superuser = social.extra_data.get("is_superuser", False)
    user.is_staff = is_staff
    user.is_superuser = is_superuser
    storage.user.changed(user)

def create_user(strategy, details, user=None, response=None, social=None, *args, **kwargs):
    return {
        'is_new': True,
        'user': strategy.create_user(**{
            'id': response['sub'],
            'username': response['nickname'],
            'first_name': response.get('given_name', ''),
            'last_name': response.get('family_name', ''),
            'email': response['email'],
            'is_staff': response.get('is_staff', False),
            'is_superuser': response.get('is_superuser', False),
        })
    }
