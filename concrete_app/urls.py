from django.urls import path

from . import views

urlpatterns = [
    path("",views.homepage,name="home"),
    path("model_trainer/",views.model_training,name="model_training"),
    path("model_prediction/",views.model_prediction,name="model_prediction"),
    path("all_predictions/",views.see_predictions,name="see_predictions"),
]

