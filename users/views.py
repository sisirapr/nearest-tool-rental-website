from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.db.models import Q
from django.urls import reverse
from .forms import UserUpdateForm,ProfileUpdateForm,RejectNotiForm,AcceptNotiForm,StartContractForm
from home.models import Post
from .models import RequestTool,ReplayTool,Contract

# Create your views here.
@login_required()
def profile(req):
	if req.method == 'POST':
		u_form = UserUpdateForm(req.POST, instance=req.user)
		p_form = ProfileUpdateForm(req.POST, req.FILES, instance=req.user.profile)
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(req, f'Your account has been updated!')
			return redirect('profile')
	else:
		u_form = UserUpdateForm(instance=req.user)
		p_form = ProfileUpdateForm(instance=req.user.profile)

	context = {
		'u_form': u_form,
		'p_form': p_form
	}
	return render(req, 'users/profile.html', context)

def mytools(request):
	context = {
		'posts':request.user.post_set.all()
	}
	return render(request,'users/mytools.html', context)

@login_required()
def NotificationView(request):
	notis=RequestTool.objects.filter(to_user=request.user).order_by('-date') #,status=0
	context = {
		'notis':notis
	}
	return render(request,'users/notifications/notis_new.html', context)

def SendNotiView(request):
	reqs=RequestTool.objects.filter(from_user=request.user)
	reps=ReplayTool.objects.filter(from_u=request.user)
	notis=reqs.union(reps)
	if request.method == 'POST':
		id=request.POST.get('noti_id')
		RequestTool.objects.filter(id=id,status=0).delete()
		id=request.POST.get('reply_id')
		ReplayTool.objects.filter(id=id).delete()

	context = {
		'notis':notis.order_by('-date'),
	}
	return render(request,'users/notifications/notis_send.html', context)

def ReplyNotiView(request):
	if request.method == 'POST':
		id=request.POST.get('reply_id')
		ReplayTool.objects.filter(id=id).delete()
	context = {
		'replys':ReplayTool.objects.filter(to_u=request.user).order_by('-date')
	}
	return render(request,'users/notifications/notis_reply.html', context)

def RejectNotiView(request,pk):
	noti = RequestTool.objects.get(id=pk)#pk is the post id passed from url
	if request.method == 'POST':
		form = RejectNotiForm(request.POST)
		if form.is_valid():
			req = form.save(commit=False)
			req.from_u = request.user
			req.to_u = noti.from_user
			req.reply_to = noti
			req.status = 3
			req.save()
			noti.status = 2
			noti.save()
			return HttpResponseRedirect(reverse('mynotis')) #post details lekk aanu thirich povuka
	else:
		form = RejectNotiForm()
	context = {
		'form': form,
		'reply_to': noti,
		'from_u': request.user,
		'to_u' : noti.from_user,
	}
	template = loader.get_template('users/notifications/reject_notis.html')
	return HttpResponse(template.render(context,request))

def AcceptNotiView(request,pk):
	noti = RequestTool.objects.get(id=pk)#pk is the post id passed from url
	if request.method == 'POST':
		form = AcceptNotiForm(request.POST)
		if form.is_valid():
			req = form.save(commit=False)
			req.from_u = request.user
			req.to_u = noti.from_user
			req.reply_to = noti
			req.status = 4
			req.save()
			noti.status = 1
			noti.save()
			return HttpResponseRedirect(reverse('mynotis')) #post details lekk aanu thirich povuka
	else:
		form = AcceptNotiForm()
	context = {
		'form': form,
		'reply_to': noti,
		'from_u': request.user,
		'to_u' : noti.from_user,
	}
	template = loader.get_template('users/notifications/accept_notis.html')
	return HttpResponse(template.render(context,request))

def StartContractView(request,pk):
	noti = RequestTool.objects.get(id=pk)#pk is the post id passed from url
	if request.method == 'POST':
		form = StartContractForm(request.POST)
		if form.is_valid():
			req = form.save(commit=False)
			req.client = request.user
			req.owner = noti.post.owner
			req.post = noti.post
			req.total_rent = req.post.rent*req.period
			req.status = 0
			req.save()
			noti.status = 5
			noti.save()
			post = Post.objects.get(id=noti.post.id)
			post.available=False
			post.save()
			pk=req.id;
			return HttpResponseRedirect(reverse('contract-detail',args=[pk]))
	else:
		form = StartContractForm()
	context = {
		'form': form,
		'post': noti.post,
		'owner' : noti.post.owner,
	}
	template = loader.get_template('users/contracts/start_contract.html')
	return HttpResponse(template.render(context,request))

def ContractDetail(request, pk):

	if Contract.objects.filter(id=pk).exists():
		contract_data = Contract.objects.get(id=pk)
		context = {
			'object':contract_data,
		}
		return render(request,'users/contracts/contract_detail.html',context)

def ContractHistory(request):
	contracts=Contract.objects.filter(owner=request.user,status=6).order_by('-start_date')|Contract.objects.filter(client=request.user,status=6).order_by('-start_date') #,status=0
	context = {
		'contracts': contracts,
	}
	return render(request, 'users/contracts/contract_history.html', context)

def ContractsOngoing(request):
	contracts=Contract.objects.filter(owner=request.user).order_by('-start_date')|Contract.objects.filter(client=request.user).order_by('-start_date') #,status=0
	context = {
		'contracts': contracts.exclude(status=6),
	}
	return render(request, 'users/contracts/contracts_ongoing.html', context)


def Status1(request, pk):
    contract = Contract.objects.filter(pk=pk)
    contract.update(status = 1)
    context = {
    	'object':contract,
    }
    return HttpResponseRedirect(reverse('contract-detail',args=[pk]))
    # return render(request,'users/contracts/contract_detail.html',context)

def Status2(request, pk):
    contract = Contract.objects.filter(pk=pk)
    contract.update(status = 2)
    context = {
    	'object':contract,
    }
    return HttpResponseRedirect(reverse('contract-detail',args=[pk]))

def Status3(request, pk):
    contract = Contract.objects.filter(pk=pk)
    contract.update(status = 3)
    context = {
    	'object':contract,
    }
    return HttpResponseRedirect(reverse('contract-detail',args=[pk]))

def Status4(request, pk):
    contract = Contract.objects.filter(pk=pk)
    contract.update(status = 4)
    context = {
    	'object':contract,
    }
    return HttpResponseRedirect(reverse('contract-detail',args=[pk]))

def Status5(request, pk):
    contract = Contract.objects.filter(pk=pk)
    contract.update(status = 5)
    context = {
    	'object':contract,
    }
    return HttpResponseRedirect(reverse('contract-detail',args=[pk]))

def Status6(request, pk):
    contract = Contract.objects.filter(pk=pk)
    contract.update(status = 6)
    c=Contract.objects.get(id=pk)
    c.post.available=True
    c.post.save()
    context = {
    	'object':contract,
    }
    return HttpResponseRedirect(reverse('contract-detail',args=[pk]))


# def mytools(request):
# 	t_form = UserToolForm(instance=request.user.post_set)
# 	context = {
# 		'posts': t_form
# 	}
# 	return render(request, 'mytools.html', context)

# def ReadNotiView(request):
# 	notis=RequestTool.objects.filter(to_user=request.user,status=2).order_by('-date') | RequestTool.objects.filter(to_user=request.user,status=1).order_by('-date')
# 	context = {
# 		'notis':notis
# 	}
# 	return render(request,'users/notifications/notis_read.html', context)

# def SendNotiView(request):
# 	if request.method == 'POST':
# 		id=request.POST.get('noti_id')
# 		RequestTool.objects.filter(id=id,status=0).delete()
# 		id=request.POST.get('reply_id')
# 		ReplayTool.objects.filter(id=id).delete()

# 	context = {
# 		'notis':RequestTool.objects.filter(from_user=request.user).order_by('-date'),
# 		'replys':ReplayTool.objects.filter(from_u=request.user).order_by('-date')
# 	}
# 	return render(request,'users/notifications/notis_send.html', context)