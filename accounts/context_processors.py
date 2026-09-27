def user_admin_status(request):
    """Expose a safe admin boolean to templates without touching missing FarmerProfiles."""
    user = getattr(request, 'user', None)
    if not user or not getattr(user, 'is_authenticated', False):
        return {'user_is_admin': False}

    try:
        profile = user.farmer_profile
    except Exception:
        profile = None

    return {
        'user_is_admin': bool(user.is_staff or (profile is not None and profile.role == 'admin')),
    }
