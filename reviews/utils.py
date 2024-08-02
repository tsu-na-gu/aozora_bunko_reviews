from django.http import QueryDict

from user_account.models import SearchHistory
from django.utils.html import escape
from urllib.parse import urlencode, parse_qs


def keep_latest_page_param(query_params):
    if isinstance(query_params, str):
        query_params = parse_qs(query_params)
    elif not isinstance(query_params, dict):
        query_params = query_params.dict()

    query_params_copy = query_params.copy()
    if 'page' in query_params_copy:
        page_values = query_params_copy.pop('page')
        if isinstance(page_values, list):
            query_params_copy['page'] = page_values[0]
        else:
            query_params_copy['page'] = page_values

    return urlencode(query_params, doseq=True)

class SearchHistoryManager:
    def save_search_history(self, user, request):
        if user.is_authenticated:
            query_params = request.GET.copy()

            if 'page' in query_params:
                return

            search_url = escape(request.build_absolute_uri())
            search_term = escape(urlencode(query_params))
            SearchHistory.objects.create(
                user=user,
                search_term=search_term,
                search_url=search_url
            )
            self.limit_search_history(user)

    def limit_search_history(self, user):
        user_search_history = SearchHistory.objects.filter(user=user).order_by('-searched_at')
        if user_search_history.count() > 20:
            for history in user_search_history[20:]:
                history.delete()

