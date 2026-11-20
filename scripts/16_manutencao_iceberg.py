"""Manutenção das tabelas Iceberg: expiração de snapshots antigos (retenção + LGPD)."""

import os
from datetime import datetime, timedelta, timezone

from pyiceberg.catalog.sql import SqlCatalog

PROJETO = os.getenv("CURSO_HOME", ".")
catalog = SqlCatalog(
    "curso_lakehouse",
    **{
        "uri": f"sqlite:///{PROJETO}/data/iceberg_catalog/catalog.db",
        "warehouse": "s3://silver",
        "s3.endpoint": "http://" + os.getenv("MINIO_ENDPOINT", "localhost:9000"),
        "s3.access-key-id": os.getenv("MINIO_ACCESS_KEY", "minioadmin"),
        "s3.secret-access-key": os.getenv("MINIO_SECRET_KEY", "minioadmin123"),
        "s3.region": "us-east-1",
    },
)
limite = datetime.now(timezone.utc) - timedelta(
    days=int(os.getenv("ICEBERG_RETENCAO_DIAS", "7"))
)

for identificador in catalog.list_tables("bronze_processado"):
    tabela = catalog.load_table(identificador)
    antes = len(tabela.snapshots())
    # O snapshot atual nunca é expirado; os anteriores ao limite saem dos metadados
    tabela.maintenance.expire_snapshots().older_than(limite).commit()
    tabela = catalog.load_table(identificador)
    print(f"{'.'.join(identificador)}: {antes} → {len(tabela.snapshots())} snapshots")
