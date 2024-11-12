# import the libraries
from datetime import timedelta
# The DAG object; we'll need this to instantiate a DAG
from airflow.models import DAG
# Operators; you need this to write tasks!
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago



default_args = {
    'owner': 'My_Dummy_Name',
    'start_date': days_ago(0),
    'email': ['jatinzorro@gmail.com'],
    'email_on_failure':	True,
    'email_on_retry':	True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


dag = DAG(
    dag_id='ETL_toll_data',
    default_args=default_args,
    description='Apache Airflow Final Assignment',
    schedule_interval=timedelta(days=1),
)

unzip_data = BashOperator(
    task_id='unzip_data',
    bash_command='tar -xvf /home/project/airflow/dags/finalassignment/tolldata.tgz -C /home/project/airflow/dags/finalassignment',
    dag=dag,
)

extract_data_from_csv = BashOperator(
        task_id='extract_data_from_csv',
        bash_command='cut -d, -f1,2,3,4 vehicle-data.csv > csv_data.csv',
        dag=dag,
)

extract_data_from_tsv = BashOperator(
        task_id='extract_data_from_tsv',
        bash_command='cut -f5,6,7 tollplaza-data.tsv > tsv_data.csv',
        dag=dag,
    )


 extract_data_from_fixed_width = BashOperator(
        task_id='extract_data_from_fixed_width',
        bash_command='awk -F "" "{print substr(\$0, 59, 3) \",\" substr(\$0, 63, 5)}" payment-data.txt > fixed_width_data.csv',
        dag=dag,
    )

consolidate_data = BashOperator(
    task_id='consolidate_data',
    bash_command='paste -d, csv_data.csv tsv_data.csv fixed_width_data.csv > extracted_data.csv',
    dag=dag,
)

transform_data = BashOperator(
    task_id='transform_data',
    bash_command='awk -F, "{ $4=toupper($4); print $0; }" extracted_data.csv > transformed_data.csv',
    dag=dag,
)


unzip_data >> extract_data_from_csv >> extract_data_from_tsv >> extract_data_from_fixed_width >> consolidate_data >> transform_data

