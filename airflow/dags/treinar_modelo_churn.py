"""DAG orientada a dados: roda quando a Gold de features é atualizada."""

from datetime import datetime

from airflow.sdk import Asset, dag, task

GOLD_FEATURES = Asset("s3://gold/ml/features_clientes.parquet")


@dag(
    dag_id="treinar_modelo_churn",
    schedule=[GOLD_FEATURES],
    start_date=datetime(2026, 10, 1),
    catchup=False,
    tags=["curso", "ml"],
)
def treinar_modelo_churn():

    @task
    def treinar():
        import subprocess

        subprocess.run(
            ["python", "/opt/airflow/curso/scripts/13_treinar_churn.py"], check=True
        )

    treinar()


treinar_modelo_churn()
