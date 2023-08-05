"""Authorization logic."""

from typing import List

from schematools.contrib.django.models import Profile


def profiles_for_scopes(required_scopes: Iterable[str]) -> List[Profile]:
    """Returns a list of profiles from the database
    that match a required set of scopes.

    The scopes of each returned profile are a subset of the given scopes.
    """
    required_scopes = frozenset(required_scopes)
    profiles = set()
    for profile in Profile.objects.all():
        scopes = profile.get_scopes()
        if not scopes:
            profiles.add(profile)
        elif scopes <= 
            if hasattr(self.request, "is_authorized_for"):
                if self.request.is_authorized_for(*scopes):
                    profiles.add(profile)

    return profiles
