class SimpleBackend(object):

    def pages_for_user(self, user_obj):
        """returns a list of IDs for UrlNodes the user can see

        This simple implementation assumes all user can see all UrlNodes
        """
        from fluent_pages.models import UrlNode
        if not hasattr(user_obj, '_fluent_pages_node_cache'):
            # build the cache of pages this user can see
            all_pks = tuple(UrlNode.objects.values_list('pk', flat=True))
            user_obj._fluent_pages_node_cache = all_pks
        return user_obj._fluent_pages_node_cache
