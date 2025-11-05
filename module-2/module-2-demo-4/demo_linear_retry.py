from airflow import DAG
from airflow.operators.empty import EmptyOperator
from datetime import datetime, timedelta

with DAG(
    dag_id="hello_mwaa",
    start_date=datetime(2025, 1, 1),
    schedule_interval=None,
    catchup=False,
    default_args={"retries": 1, "retry_delay": timedelta(minutes=1)},
) as dag:
    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")
    start >> end
