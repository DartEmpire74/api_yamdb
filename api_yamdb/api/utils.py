from django.shortcuts import get_object_or_404

from reviews.models import Title


def get_title_model(title_id: int) -> Title:
    return get_object_or_404(Title, id=title_id)
