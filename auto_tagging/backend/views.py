from django.shortcuts import render
from tagPredictor import getTags
from .models import tagResult

# Create your views here.
def index(request):
    return render(request, 'index.html')

def result(request):
   res=tagResult()
   res.title = request.GET['title']
   res.body = request.GET['ques']

   question = res.title + " " +res.body
   res.question = question
   predicted_tags = getTags([question])

   for tags_tuple in predicted_tags:
     ftag=''
     for tag in tags_tuple:
        ftag = ftag + tag + ", "
     
     res.tags = ftag
     print(res.tags)
   return render(request, 'page2.html',{'res':res})
 

  