
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select pedido_id
from "lakehouse"."intermediate"."int_pedidos__deduplicados"
where pedido_id is null



  
  
      
    ) dbt_internal_test