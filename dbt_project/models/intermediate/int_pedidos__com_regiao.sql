-- Pedidos da Silver enriquecidos com a região (seed) e com o valor em centavos.
-- Sistemas de pagamento costumam guardar valores como INTEIROS em centavos, para
-- evitar erros de arredondamento; a macro cents_to_reais converte de volta.
with pedidos as (
    select
        pedido_id,
        cliente_id,
        regiao,
        status_pedido,
        valor_total,
        cast(round(valor_total * 100) as bigint)    as valor_total_centavos
    from {{ ref('int_pedidos__enriquecidos') }}
),

regioes as (
    select * from {{ ref('regioes') }}
)

select
    p.pedido_id,
    p.cliente_id,
    p.regiao,
    r.sigla_regiao,
    r.nome_regiao,
    p.status_pedido,
    p.valor_total_centavos,
    {{ cents_to_reais('p.valor_total_centavos') }}  as valor_total_reais,
    p.valor_total
from pedidos p
left join regioes r using (regiao)