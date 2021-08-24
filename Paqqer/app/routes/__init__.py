from app.routes.abm.buyorders import abm_buyorder
from app.routes.abm.deposit import abm_deposit 
from app.routes.abm.providers import abm_providers 


from app.routes.abm.products import abm_products
from app.routes.abm.receiptorders import abm_receiptorder


from app.routes.inbound.putaway import putaway
from app.routes.inbound.receiveorder import receive_order

from app.routes.environ.main import main




routes = [
    abm_buyorder, abm_deposit, abm_products, abm_receiptorder, abm_providers,
    putaway, receive_order, main 
]