from django.shortcuts import render,HttpResponseRedirect
from django.urls import reverse
from .forms import Predictionform,Predictionfileform
from .models import Modelpredictions
from src.pipeline.trainngpipeline import Trainpipeline
from django.contrib import messages
from src.logger import logging
from .models import Modeltraining,Modelpredictions
from src.pipeline.predictionpipeline import get_data_frame,Prediction

# Create your views here.

def homepage(request):
    try:
        logging.info(f"uer is on landing page .")
        return render(request,"core/home.html")
    except Exception as e:
        raise e
    
def model_training(request):
    try:
        all_experiments = Modeltraining.objects.all()
        if request.method == 'POST':
            logging.info(f"user is starting the training pipeline")
            training = Trainpipeline()
            print(training.experiment.experiment_id)
            if training.experiment.running_status:
                logging.error(f"pipeline can not be started , pipeline is already running")
                messages.error(request,f"Pipeline is already running ")
                status= f"Training is already in progress"
            else:
                logging.info(f"pipeline is about to start ")
                model_training_artifact = training.start()
                messages.success(request,f"pipeline has been started ")
                return HttpResponseRedirect(reverse("model_training"))
        else:
            logging.info(f"user is on model training page")
        return render(request,"core/model_trainer.html",{'experiments':all_experiments})
    except Exception as e:
        raise e
    
def model_prediction(request):
    try:
        if request.method=="POST":
            fm=Predictionform(data=request.POST)
            if fm.is_valid():
                datadict={}
                print(fm.cleaned_data)
                print(type(fm.cleaned_data))
                for k,v in fm.cleaned_data.items():
                    datadict[k]=int(v)
                print(datadict)
                dataframe = get_data_frame(datadict)
                logging.info(f"dataframe for prediction is \n {dataframe.head(1).to_string()}")
                predictionpipeline = Prediction()
                output = predictionpipeline.single_output_predict(dataframe)
                if output is None:
                    messages.error(request,"Model not yet trained and not available for predictions")
                    return HttpResponseRedirect(reverse("model_prediction"))
                datadict['concrete_compressive_strength'] = output[0]
                modelpreds=Modelpredictions(**datadict)
                modelpreds.save()
                logging.info(f"user clicked on predict button to predict the cement strength and the predicted value is {output[0]}")
                return render(request,"core/prediction.html",{'form':fm,'predicted_output':output[0]})
        else:
            logging.info(f"user is on prediction page")
            fm=Predictionform()
        return render(request,"core/prediction.html",{'form':fm})
    except Exception as e:
        raise e
    
def see_predictions(request):
    try:
        logging.info(f"user is visiting all prediction page")
        predictions = Modelpredictions.objects.all()
        return render(request,"core/all_predictions.html", {'predictions': predictions})
    except Exception as e:
        raise e