import io, boto3, pandas as pd
from datetime import datetime, timezone

s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:9000",
    aws_access_key_id="minioadmin",
    aws_secret_access_key="minioadmin123",
    region_name="us-east-1",
)
ruim = pd.DataFrame(
    {
        "id_pedido": [3_000_001, 3_000_002],
        "id_cliente": [10, 20],
        "id_produto": [1, 2],
        "categoria": ["Livros", "Roupas"],
        "valor_unitario": [10.0, 20.0],
        "quantidade": [1, 2],
        "valor_total": [-10.0, 40.0],
        "status_pedido": ["concluido", "extraviado"],
        "regiao": ["Sul", "Norte"],
        "data_pedido": pd.to_datetime(["2022-12-20", "2022-12-21"]),
        "avaliacao_cliente": [5, None],
        "_fonte": "teste_qualidade",
        "_ingerido_em": datetime.now(timezone.utc).isoformat(),
    }
)
agora = datetime.now()
chave = f"ecommerce_sintetico/ano={agora:%Y}/mes={agora:%m}/dia={agora:%d}/zz_invalido_{int(agora.timestamp())}.parquet"
buf = io.BytesIO()
ruim.to_parquet(buf, index=False)
s3.put_object(Bucket="bronze", Key=chave, Body=buf.getvalue())
print("Carga inválida gravada em", chave)
