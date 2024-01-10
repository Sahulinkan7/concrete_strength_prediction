from src.pipeline.trainngpipeline import Trainpipeline

def main():
    training = Trainpipeline()
    print(training.is_running_pipeline)
    if training.is_running_pipeline:
        print("pipeline already running")
        return
    else:
        training.run_pipeline()
        
if __name__=='__main__':
    main()