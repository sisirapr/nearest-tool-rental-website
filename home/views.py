from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.exceptions import ObjectDoesNotExist
from django.template import loader
from django.urls import reverse
from django.db.models import Avg
from users.models import RequestTool
from .models import Post,Review
from .filters import PostFilter
from .forms import RateForm,RequestToolForm


# @login_required()
class PostListView(ListView):
	model = Post
	template_name = 'home.html'	#<app>/<model>_<view_type>.html
	context_object_name = 'posts'
	# ordering = ['rating'] #newst to oldest order of listing
	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		# print("----------------------------",context)
		# context['subfilter'] = Post.objects.filter(tool__icontains=PostFilter.objects.tool)
		context['filter'] = PostFilter(self.request.GET,queryset=self.get_queryset().filter(available=True))
		# availability of tool
		return context

class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	fields = ['tool', 'content','rent','rent_type','image','available']

	def form_valid(self, form):
		form.instance.owner = self.request.user
		return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['tool', 'content','rent','rent_type','image','available']
	success_url = '/accounts/mytools/'

	def form_valid(self, form):
		form.instance.owner = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.owner:
			return True
		return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	success_url = '/accounts/mytools/'

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.owner:
			return True
		return False

def about(request):
	return render(request, 'about.html',{'title': 'About'})

def Rate(request, pk):
	post = Post.objects.get(id=pk)#pk is the post id passed from url
	user = request.user
	if request.method == 'POST':
		form = RateForm(request.POST)
		if form.is_valid():
			rate = form.save(commit=False)
			rate.user = user
			rate.post = post
			rate.save()
			return HttpResponseRedirect(reverse('post-detail',args=[pk])) #post details lekk aanu thirich povuka
	else:
		form = RateForm()
	context = {
		'form': form,
		'post': post,
	}
	template = loader.get_template('rate.html')
	return HttpResponse(template.render(context,request))

@login_required()
def PostDetail(request, pk):

	if Post.objects.filter(id=pk).exists():
		post_data = Post.objects.get(id=pk)
		reviews = Review.objects.filter(post=post_data)
		review_avg = reviews.aggregate(Avg('rate'))
		review_count = reviews.count()
		post_data.rating = list(review_avg.values())[0]
		post_data.save()
		context = {
			'object':post_data,
			'reviews':reviews,
			'review_avg':review_avg,
			'review_count':review_count,
		}
		return render(request,'home/post_detail.html',context)

def RequestToolView(request, pk):
	post = Post.objects.get(id=pk)#pk is the post id passed from url
	user = request.user
	if request.method == 'POST':
		form = RequestToolForm(request.POST)
		if form.is_valid():
			req = form.save(commit=False)
			req.from_user = user
			req.to_user = post.owner
			req.post = post
			req.save()
			return HttpResponseRedirect(reverse('post-detail',args=[pk])) #post details lekk aanu thirich povuka
	else:
		form = RequestToolForm()
	context = {
		'form': form,
		'post': post,
		'from_user': user,
		'to_user' : post.owner,
	}
	template = loader.get_template('request_tool.html')
	return HttpResponse(template.render(context,request))

# def ReviewDetail(request,email,pk):#import models, choose where to
# 	user = get_object_or_404(User,email=email)#CustomUser
# 	post = Post.objects.get(id=pk)
# 	review = Review.objects.get(user=user,post=post)
# 	context = {
# 		'review': review,
# 		'post': post,
# 	}
# 	template = loader.get_template('post_review.html')
# 	return HttpResponse(template.render(context,request))

# def home(request):
	# context = {
	# 	'posts': Post.objects.all(),
	# }
	# return render(request, 'home.html', context)

# class PostDetailView(DetailView):
# 	model = Post
	# def get_context_data(self,request,*args,**kwargs):
	# 	print('————————verunnund——————',request,args,kwargs) 
	# 	context=super(PostDetailView,self).get_context_data(*args,**kwargs) one secaa
	# 	post_data = Post.objects.get(id=*args)
	# 	reviews = Review.objects.filter(post=self.object)
	# 	review_avg = reviews.aggregate(Avg('rate'))
	# 	review_count = reviews.count()
	# 	context = {
	# 		'reviews':reviews,
	# 		'review_avg':review_avg,
	# 		'review_count':review_count,
	# 	}
	# 	return render('home/post_detail.html',context)