from .models import FarmerProfile


class EnsureFarmerProfileMiddleware:
    """Create a FarmerProfile for authenticated users if it was missing."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if hasattr(request, 'user') and request.user.is_authenticated:
            try:
                request.user.farmer_profile
            except FarmerProfile.DoesNotExist:
                FarmerProfile.objects.get_or_create(user=request.user)
        return self.get_response(request)
