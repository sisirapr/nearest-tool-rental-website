import django_filters
from .models import Post

class PostFilter(django_filters.FilterSet):
	CHOICES = (
		('ascending','Ascending'),
		('descending','Descending')
		)

	ordering = django_filters.ChoiceFilter(label='Ordering', choices=CHOICES,method='filter_by_order')

	class Meta:
		model = Post
		fields = {
		'tool':['icontains'],
		
		}
		# 'rent':,
	def filter_by_order(self, queryset, name, value):
		expression = 'rent' if value == 'ascending' else '-rent'
		return queryset.order_by(expression)