from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def render_stars(rating):
    filled_star_svg = """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#007bff" class="bi bi-star-fill text-warning" viewBox="0 0 16 16">
      <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.32-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.63.283.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/>
    </svg>"""

    empty_star_svg = """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#cccccc" class="bi bi-star" viewBox="0 0 16 16">
      <path d="M2.866 14.85c-.078.444.36.791.746.593l4.39-2.256 4.389 2.256c.386.198.824-.149.746-.592l-.83-4.73 3.522-3.356c.329-.32.158-.888-.283-.95l-4.898-.696L8.001.792 5.817 5.12l-4.898.696c-.441.062-.612.63-.283.95l3.522 3.356-.83 4.73zM8 12.026l-3.688 1.897.694-3.946L1.338 6.765l3.952-.561L8 2.223l1.71 3.98 3.952.561-2.668 2.561.694 3.946L8 12.026z"/>
    </svg>"""

    stars = ""
    for i in range(1, 6):
        if i <= rating:
            stars += filled_star_svg
        else:
            stars += empty_star_svg
    return mark_safe(stars)


