from airflow.utils.dates import days_ago
from datetime import datetime, timedelta
from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount                     




# default_args for DAG
default_args = {
    'owner': 'dhiraj47',
    'depends_on_past': False,                   
    'email_on_failure': False,
    'email_on_retry': False,
    'start_date': days_ago(1),
}



# Creating / Declaring a DAG Object
dag = DAG(
    'ml_pipeline_dag',
    default_args=default_args,
    description='ML pipeline for Recommendation System with Docker',
    schedule_interval=None,                   
    catchup=False,
)



# First sample bash task
bash_task_test = BashOperator(
    task_id="bash_task_test",
    bash_command=""" 
    echo "Testing bash task executed successfully !!" 
    """
)



# 2nd Task
model_train_and_publish = DockerOperator(
    task_id='model_train_and_publish',
    docker_url="tcp://docker-socket-proxy:2375"
    auto_remove=True,                                 
    api_version='auto',                    
    image='recommendation_model:v1.0.0',                   
    container_name='training_recommendation_model',
    environment={                                          
        'MINIO_ENDPOINT': 'host.docker.internal:9000',
        'MINIO_ACCESS_KEY_ID': 'oUUzXjuf15DaA5pcuuuw',
        'MINIO_SECRET_ACCESS_KEY': '5ooT0EJ9mcPeiVBs4SsTYrpOMWltSiETgyabQF43',
        'MINIO_BUCKET_NAME': '47-recommendation-model',
    },
    network_mode='bridge',                          
    dag=dag,
)



# Setting Task Dependencies / Order
bash_task_test >> model_train_and_publish