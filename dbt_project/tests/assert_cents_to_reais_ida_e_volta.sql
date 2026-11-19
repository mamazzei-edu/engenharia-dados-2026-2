-- Teste singular: converter para centavos e voltar com a macro não pode alterar o valor
select pedido_id, valor_total, valor_total_centavos, valor_total_reais
from {{ ref('int_pedidos__com_regiao') }}
where valor_total_reais <> valor_total