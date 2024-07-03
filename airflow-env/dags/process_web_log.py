# Libraries Import
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

# DAG Argument
default_args = {
    'owner': 'Hisham',
    'start_date': days_ago(0),
    'email': ['hisham.e.hassan@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False, 
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

# DAG Definition
dag = DAG(
    dag_id='process_web_log',
    default_args=default_args,
    description='extract web logs from server into compressed file',
    schedule_interval=timedelta(days=1),
)

PATH = '~/Desktop/Airflow/airflow-env/dags/capstone'

# Task Definition

extract_data = BashOperator(
    task_id='extract',
    bash_command=f'cut -d " " -f 1 {PATH}/accesslog.txt > {PATH}/extracted_data.txt',
    dag=dag,
)

transform_data = BashOperator(
    task_id='transform',
    bash_command=f'grep -v "198.46.149.143" {PATH}/extracted_data.txt > {PATH}/transformed_data.txt',
    dag=dag
)

load_data = BashOperator(
    task_id='load',
    bash_command=f'tar -cvf {PATH}/weblog.tar {PATH}/transformed_data.txt',
    dag=dag
)

# Pipelines
extract_data >> transform_data >> load_data