from django.shortcuts import render,HttpResponseRedirect
from django.urls import reverse
from src.pipeline.trainngpipeline import Trainpipeline
from django.contrib import messages
def homepage(request):
    return render(request,"home.html")

def train_model(request):
    try:
        if request.method=='POST':
            tr=Trainpipeline()
            if tr.is_running_pipeline:
                messages.success(request,"pipeline is already running ")
                return HttpResponseRedirect(reverse('train_model'))
            else:
                tr.run_pipeline()
                messages.success(request,"pipeline started running")
        return render(request,"train_model.html")
    except Exception as e:
        raise e