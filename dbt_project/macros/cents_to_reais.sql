{% macro cents_to_reais(coluna, casas_decimais=2) -%}
    {#- Converte um valor inteiro em centavos para reais (decimal com 2 casas).
        Uso: {{ cents_to_reais('valor_centavos') }} -#}
    cast(round(cast({{ coluna }} as decimal(18, 2)) / 100, {{ casas_decimais }}) as decimal(16, {{ casas_decimais }}))
{%- endmacro %}