{% macro pseudonimizar(coluna) -%}
    sha256(concat('{{ env_var("PII_SALT", "troque-este-salt") }}', cast({{ coluna }} as varchar)))
{%- endmacro %}