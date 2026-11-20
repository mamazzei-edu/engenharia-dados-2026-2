select
    {{ pseudonimizar('cliente_id') }} as cliente_hash,
    segmento_cliente,
    total_pedidos,
    receita_total
from {{ ref('dim_clientes') }}