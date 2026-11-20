"""
DAG pipeline_medallion — Bronze → Silver → Gold, de ponta a ponta.

ingestão (BronzeWriter) → contrato da Bronze (Pandera) → freshness → dbt build (Cosmos) → manutenção Iceberg
"""
import os
from datetime import datetime, timedelta
from pathlib import Path

from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import Asset, dag, task
from cosmos import DbtTaskGroup, ExecutionConfig, ProfileConfig, ProjectConfig, RenderConfig
from cosmos.constants import LoadMode, TestBehavior

PROJETO = Path(os.getenv("CURSO_HOME", "/opt/airflow/curso"))
DBT_DIR = PROJETO / "dbt_project"
DBT_BIN = os.getenv("DBT_BIN", "/opt/airflow/dbt_venv/bin/dbt")
PY_BIN = os.getenv("PY_BIN", "python")

GOLD_RECEITA = Asset("s3://gold/analytics/receita_mensal.parquet")
GOLD_FEATURES = Asset("s3://gold/ml/features_clientes.parquet")


def alertar_falha(context):
    """Callback de falha: em produção, enviar para Slack/Teams/e-mail."""
    ti = context["task_instance"]
    print(f"🚨 ALERTA: {ti.dag_id}.{ti.task_id} falhou (tentativa {ti.try_number}). Log: {ti.log_url}")


default_args = {
    "owner": "time-dados",
    "on_failure_callback": alertar_falha,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "retry_exponential_backoff": True,
    "execution_timeout": timedelta(minutes=30),
}

profile_config = ProfileConfig(
    profile_name="curso_ed",
    target_name=os.getenv("DBT_TARGET", "dev"),
    profiles_yml_filepath=DBT_DIR / "profiles.yml",
)


@dag(
    dag_id="pipeline_medallion",
    description="Ingestão, qualidade e transformação Bronze→Silver→Gold",
    schedule="0 6 * * *",                 # todo dia às 06:00 (UTC)
    start_date=datetime(2026, 10, 1),
    catchup=False,
    max_active_runs=1,
    default_args=default_args,
    tags=["curso", "medallion", "dbt"],
)
def pipeline_medallion():

    ingestao_bronze = BashOperator(
        task_id="ingestao_bronze_writer",
        bash_command=f"cd {PROJETO} && {PY_BIN} scripts/9_reingerir_com_particionamento.py",
    )

    contrato_bronze = BashOperator(
        task_id="contrato_bronze_pandera",
        bash_command=f"cd {PROJETO} && {PY_BIN} scripts/15_validar_bronze.py",
    )

    freshness = BashOperator(
        task_id="dbt_source_freshness",
        bash_command=f"cd {DBT_DIR} && {DBT_BIN} deps && {DBT_BIN} source freshness --profiles-dir .",
        pool="duckdb_pool",
    )

    transformacao = DbtTaskGroup(
        group_id="dbt_medallion",
        project_config=ProjectConfig(DBT_DIR),
        profile_config=profile_config,
        execution_config=ExecutionConfig(dbt_executable_path=DBT_BIN),
        render_config=RenderConfig(
            load_method=LoadMode.DBT_LS,
            test_behavior=TestBehavior.AFTER_EACH,   # testa cada modelo logo após construí-lo
        ),
        operator_args={
            "install_deps": True,          # roda dbt deps (dbt_utils) antes de cada comando
            "pool": "duckdb_pool",         # DuckDB aceita UM escritor por vez
        },
    )

    @task(outlets=[GOLD_RECEITA, GOLD_FEATURES])
    def publicar_gold():
        """Marca os assets Gold como atualizados (dispara DAGs consumidoras)."""
        print("Gold publicada: receita_mensal e features_clientes")

    manutencao_iceberg = BashOperator(
        task_id="manutencao_iceberg",
        bash_command=f"cd {PROJETO} && {PY_BIN} scripts/16_manutencao_iceberg.py",
        trigger_rule="all_done",           # roda mesmo se algo acima falhar
    )

    ingestao_bronze >> contrato_bronze >> freshness >> transformacao >> publicar_gold() >> manutencao_iceberg


pipeline_medallion()