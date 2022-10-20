from django_filters import FilterSet
from .models import Post


class NewsFilter(FilterSet):
    class Meta:
        model = Post
        fields = {'header': ['icontains'],
                  # 'categoryType': [co],
                  'time_post': ['date__gt'],
                  }