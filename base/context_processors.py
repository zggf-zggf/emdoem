from .utils import get_categories


def load_categories(request):
    categories = get_categories()
    return {'categories': categories}
