from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404,render
#from django.http import Http404
from django.urls import reverse
from django.views import generic
#from django.shortcuts import render, HttpResponse
#from django.template import loader

from . models import Choice, Question

# Create your views here.
class IndexView(generic.ListView):
	template_name = 'pols/index.html'
	context_object_name = 'latest_question_list'

	def get_queryset(self):
		return Question.objects.filter(pub_date_lte = timzone.now()).order_by('-pub_date')[:5]
		#return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
	model = Question
	template_name = 'pols/detail.html'
	def get_queryset(self):
		return Question.objects.filter(pub_date_lte = timezone.now())

class ResultsView(generic.DetailView):
	model = Question
	template_name = 'pols/results.html'


def index(request):
	latest_question_list = Question.objects.order_by('-pub_date')[:5]
	#template = loader.get_template('pols/index.html')
	context = {
		'latest_question_list' : latest_question_list,
	}
	return render(request, 'pols/index.html', context)
	#output = ', '.join([q.question_text for q in latest_question_list])
	#return HttpResponse(output)
	#return HttpResponse(template.render(context, request))
	#return HttpResponse("Hello, world. You're at the polls index.")
	
def detail(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'pols/detail.html', {'question': question})
	#try:
	#	question = Question.objects.get(pk=question_id)
	#except Question.DoesNotExist:
	#	raise Http404("Question does not exist")
	#return render(request, 'pols/detail.html', {'question': question})
	#return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'pols/results.html', {'question': question})
	#response = "You're looking at the results of question %s."
	#return HttpResponse(response % question_id)

def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.Choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		return render(request, 'pols/detail.html', {
			'question': question,
			'error_message': "you didn't select a choice.", 
			})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		return HttpResponseRedirect(reverse('pols:results', args=(question.id,)))
		#return HttpResponse("You're voting on question %s." % question_id)
