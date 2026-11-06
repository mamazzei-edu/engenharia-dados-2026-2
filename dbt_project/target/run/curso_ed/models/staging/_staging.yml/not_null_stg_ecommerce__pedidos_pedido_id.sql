
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select pedido_id
from "lakehouse"."staging"."stg_ecommerce__pedidos"
where pedido_id is null



  
  
      
    ) dbt_internal_test