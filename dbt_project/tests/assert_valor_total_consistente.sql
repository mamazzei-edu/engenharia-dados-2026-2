select pedido_id, valor_unitario, quantidade, valor_total
from {{ ref('int_pedidos__enriquecidos') }}
where abs(valor_total - valor_unitario * quantidade) > 0.01