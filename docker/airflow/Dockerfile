FROM apache/airflow:3.3.2-python3.12

USER airflow

# Dependências das tarefas Python (ingestão, validação, manutenção, ML)
RUN pip install --no-cache-dir \
      "apache-airflow==${AIRFLOW_VERSION}" \
      "astronomer-cosmos==1.15.*" \
      "duckdb==1.5.6" "pandera>=0.25" boto3 \
      "dlt[filesystem,parquet,s3]" \
      "pyiceberg[sql-sqlite,pyarrow,pandas]>=0.10" \
      scikit-learn joblib requests truststore

# dbt em venv ISOLADO (Cosmos chama este executável)
RUN python -m venv /opt/airflow/dbt_venv && \
    /opt/airflow/dbt_venv/bin/pip install --no-cache-dir \
      "dbt-core~=1.12.0" "dbt-duckdb~=1.11.0" "duckdb==1.5.6"