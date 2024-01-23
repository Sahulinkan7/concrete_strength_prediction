pipeline{
    agent any
    stages{
        stage("clone cement_strength_prediction_app code"){
            steps{
                echo "======== cloning from github ========"
                git url:"https://github.com/Sahulinkan7/concrete_strength_prediction.git",branch:"main"
            }
            post{
                always{
                    echo "======== post execution of cloning code ========"
                }
                success{
                    echo "======== github cloning executed successfully ========"
                }
                failure{
                    echo "======== github cloning execution failed ========"
                }
            }
        }
        stage("Building the code : building docker image "){
            steps{
                echo "======== Building docker image for the application ========"
                sh "docker build -t concretestrength ."
            }
            post{
                always{
                    echo "======== post execution of docker image building ========"
                }
                success{
                    echo "======== docker image build successfully  ========"
                }
                failure{
                    echo "======== docker image building failed ========"
                }
            }
        }
        stage("pushing image to docker hub"){
            steps{
                echo "pushing the image to docker hub"
                withCredentials([usernamePassword(credentialsId:"dockerHub",passwordVariable:"dockerHubpass",usernameVariable:"dockerHubuser")]){
                    sh "docker tag concretestrength ${env.dockerHubuser}/concretestrength:latest"
                    sh "docker login -u ${env.dockerHubuser} -p ${env.dockerHubpass}"
                    sh "docker push ${env.dockerHubuser}/concretestrength:latest"
                }
            }
            post{
                success{
                    echo "Image pushed to dockerhub registry."
                }
            }
        }
        stage (" pull image from dockerhub and run on slave node")
        {
            agent{
                label 'slave'
            }
            steps{
                echo "running concrete_strength_prediction app container in aws slave node"
                sh "docker-compose up -d"
            }
            post{
                success{
                    echo "======== container running in 8000 port of slave node========"
                }
                failure{
                    echo "======== docker container is not running ========"
                }
            }
        }
    }
    post{
        always{
            echo "========always========"
        }
        success{
            echo "========pipeline executed successfully ========"
        }
        failure{
            echo "========pipeline execution failed========"
        }
    }
}