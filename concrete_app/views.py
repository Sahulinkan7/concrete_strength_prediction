from django.shortcuts import render
from .forms import Predictionform,Predictionfileform
from .models import Modelpredictions
# Create your views here.

def homepage(request):
    try:
        return render(request,"core/home.html")
    except Exception as e:
        raise e
    
def model_training(request):
    try:
        return render(request,"core/model_trainer.html")
    except Exception as e:
        raise e
    
def model_prediction(request):
    try:
        if request.method=="POST":
            fm=Predictionform(data=request.POST)
            if fm.is_valid():
                fm.save()
                # cement=fm.cleaned_data['cement']
                # blast_furnace_slag=fm.cleaned_data['blast_furnace_slag']
                # fly_ash=fm.cleaned_data['fly_ash']
                # water = fm.cleaned_data['water']
                # print(cement,blast_furnace_slag,fly_ash,water)
        else:
            fm=Predictionform()
        
        return render(request,"core/prediction.html",{'form':fm})
    except Exception as e:
        raise e
    
def see_predictions(request):
    try:
        predictions = Modelpredictions.objects.all()
        return render(request,"core/all_predictions.html", {'predictions': predictions})
    except Exception as e:
        raise e