"""Validação de contrato da Bronze (shift-left) com Pandera.
Uso: python scripts/15_validar_bronze.py  -> exit code 1 se o contrato for violado."""
import os
import sys

import duckdb
import pandas as pd
import pandera.pandas as pa
from pandera.pandas import Check, Column, DataFrameSchema

BRONZE_ROOT = os.getenv("BRONZE_ROOT", "s3://bronze")
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "localhost:9000")

# Aceita QUALQUER tipo inteiro (int32 ou int64). A largura do inteiro varia conforme
# quem gerou o Parquet: o NumPy 1.x no Windows usa int32 como padrão; no Linux, int64.
# Exigir int64 rejeitaria dados válidos; aceitar float deixaria passar 3.5 pedidos.
eh_inteiro = Check(lambda s: pd.api.types.is_integer_dtype(s), name="tipo_inteiro")

contrato_pedidos = DataFrameSchema(
    {
        "id_pedido": Column(None, [eh_inteiro, Check.gt(0)]),
        "id_cliente": Column(None, [eh_inteiro, Check.in_range(1, 100_000)]),
        "status_pedido": Column(str, Check.isin(["concluido", "cancelado", "pendente", "reembolsado"])),
        "valor_unitario": Column(float, Check.gt(0)),
        "quantidade": Column(None, [eh_inteiro, Check.in_range(1, 10)]),
        "valor_total": Column(float, Check.ge(0)),
        "avaliacao_cliente": Column(float, Check.isin([1, 2, 3, 4, 5]), nullable=True, coerce=True),
    },
    checks=[Check(lambda df: (df["valor_total"] - df["valor_unitario"] * df["quantidade"]).abs() <= 0.01,
                  name="valor_total_consistente")],
    strict=False,
)

def main() -> int:
    con = duckdb.connect()
    if BRONZE_ROOT.startswith("s3://"):
        con.execute("INSTALL httpfs; LOAD httpfs;")
        con.execute(f"""CREATE SECRET minio (TYPE s3, KEY_ID '{os.getenv("MINIO_ACCESS_KEY", "minioadmin")}',
            SECRET '{os.getenv("MINIO_SECRET_KEY", "minioadmin123")}', ENDPOINT '{MINIO_ENDPOINT}',
            URL_STYLE 'path', USE_SSL false, REGION 'us-east-1')""")
    # Valida uma amostra da carga (arquivo) mais recente
    df = con.execute(f"""
        WITH ultima_carga AS (
            SELECT * FROM read_parquet('{BRONZE_ROOT}/ecommerce_sintetico/**/*.parquet', filename = true)
            WHERE filename = (SELECT max(filename)
                              FROM read_parquet('{BRONZE_ROOT}/ecommerce_sintetico/**/*.parquet', filename = true))
        )
        SELECT * FROM ultima_carga USING SAMPLE reservoir(100000 ROWS) REPEATABLE (42)
    """).df()
    try:
        contrato_pedidos.validate(df, lazy=True)        # lazy=True: coleta TODAS as violações
    except pa.errors.SchemaErrors as erros:
        print("❌ Contrato da Bronze violado:")
        print(erros.failure_cases.groupby(["column", "check"]).size().to_string())
        return 1
    print(f"✅ Contrato da Bronze OK ({len(df):,} linhas validadas)")
    return 0

if __name__ == "__main__":
    sys.exit(main())