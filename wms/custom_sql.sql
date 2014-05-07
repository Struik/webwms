create or replace view web_client as
select
id, name, address, sdid
from bst.client
where is_holder='t';

create or replace view web_sku as
select
id, sku_id, name, holder_id, sdid
from bst.sku
where id>0;

create or replace view web_order as
select
o.id, o.sdid, o.display_name, o.holder_id, c.name client_name, date_utils.ctime2date(o.date_to_ship) date_to_ship, o.status
from bst.orders o
join bst.client c on c.id=o.holder_id
where o.id>0;

create or replace view web_order_detail as
select
od.id,  o.id order_id, od.line, od.sku_id, s.name sku_name, od.qty, od.planned, od.moved, od.packed, od.shiped
from bst.orders o
join bst.order_details od on od.order_id=o.id
join bst.sku s on s.id=od.sku_id
where o.id>0;

create or replace view web_incoming as
select
i.id, i.sdid, i.display_name, i.holder_id, c.name client_name, date_utils.ctime2date(i.date_to_ship) date_to_ship, i.status
from bst.incomings i
join bst.client c on c.id=i.holder_id
where i.id>0;

create or replace view web_incoming_detail as
select
rownum id,  i.id incoming_id, id.line, id.sku_id, s.name sku_name, id.qty, sum(rd.units_received) received
from bst.incomings i
join bst.incoming_details id on id.inc_id=i.id
join bst.sku s on s.id=id.sku_id
join bst.rcn_detail rd on rd.inc_id=id.inc_id
where i.id>0
group by rownum, i.id, id.line, id.sku_id, s.name, s.name, id.qty;

grant select on client to web;
grant select on sku to web;
grant select on orders to web;
grant select on order_details to web;
grant select on incomings to web;
grant select on incoming_details to web;
grant select on rcn to web;
grant select on rcn_detail to web;