from osv import fields, osv

class purchase_order(osv.osv):
    _inherit = "purchase.order"

    def _has_supplier_direct_delivery(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for id in ids:
            cr.execute('select id from purchase_order_line where is_supplier_direct_delivery=true and order_id=%d' % id)
            results = cr.fetchone()
            if results and len(results) > 0:
                res[id] = True
            else:
                res[id] = False
        return res
    
    _columns = {
        'has_supplier_direct_delivery': fields.function(_has_supplier_direct_delivery, method=True, type='boolean', string="Has Supplier Direct Delivery", store=True, select=1),
    }
    
    #we re-attach the move to the sale order line        
    def action_picking_create(self, cr, uid, ids, *args):
        super(purchase_order, self).action_picking_create(cr, uid, ids, args)
        for order in self.browse(cr, uid, ids):
            for order_line in order.order_line:
                if order_line.is_supplier_direct_delivery:
                    for move in order_line.move_ids:
                        self.pool.get('stock.picking').write(cr, uid, move.picking_id.id, {'is_supplier_direct_delivery': True, 'sale_id':order_line.sale_order_line.order_id.id})
                        self.pool.get('stock.move').write(cr, uid, move.id, {'sale_line_id':  order_line.sale_order_line.id})
    
purchase_order()


class purchase_order_line(osv.osv):
    _inherit = "purchase.order.line"
    
    def _get_partner_address_id(self, cr, uid, ids, field_name, arg, context={}):
        result = {}
        for rec in self.browse(cr, uid, ids, context):
            result[rec.id] = (rec.sale_order_line and rec.sale_order_line.order_id.partner_shipping_id.id) or False
        return result
    
    _columns = {
        #'partner_address_id': fields.function(_get_partner_address_id, method=True, type='many2one', relation='res.partner.address', string='Address'),
        'sale_order_line':fields.many2one('sale.order.line', 'Related Sale Order Line', required=False),
        'sale_order': fields.related('sale_order_line', 'order_id', type='many2one', relation='sale.order', string='Related Sale Order'),
        'partner_address_id': fields.related('sale_order_line', 'order_id', 'partner_shipping_id', type='many2one', relation='res.partner.address', string='Shipping address'),
        'is_supplier_direct_delivery': fields.boolean('Is Direct Delivery?'),
        'move_ids': fields.one2many('stock.move', 'purchase_line_id', 'Moves'),
    }
    
purchase_order_line()