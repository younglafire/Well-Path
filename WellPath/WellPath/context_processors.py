from typing import Dict
from django.conf import settings


def feature_flags(request) -> Dict[str, bool]:
    """Expose selected feature flags to all templates.

    Example usage in template:
        {% if FEATURE_FLAGS.ENABLE_GPT5_FOR_ALL_CLIENTS %}
            <!-- GPT-5 specific UI -->
        {% endif %}
    """
    return {
        "FEATURE_FLAGS": settings.FEATURE_FLAGS,
    }
