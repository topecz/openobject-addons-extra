# -*- encoding: utf-8 -*-
#################################################################################
#                                                                               #
#    sale_picking_reservation for OpenERP                                       #
#    Copyright (C) 2011 Akretion Sébastien BEAU <sebastien.beau@akretion.com>   #
#                                                                               #
#    This program is free software: you can redistribute it and/or modify       #
#    it under the terms of the GNU Affero General Public License as             #
#    published by the Free Software Foundation, either version 3 of the         #
#    License, or (at your option) any later version.                            #
#                                                                               #
#    This program is distributed in the hope that it will be useful,            #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of             #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the              #
#    GNU Affero General Public License for more details.                        #
#                                                                               #
#    You should have received a copy of the GNU Affero General Public License   #
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.      #
#                                                                               #
#################################################################################

from osv import osv, fields
import netsvc


class stock_picking(osv.osv):
    
    _inherit = "stock.picking"

    _columns = {
        'reserved': fields.boolean('Reserved Picking', readonly=True),
    }

    _defaults = {
        'reserved': lambda *a: False,
    }

    
    def action_reserve(self, cr, uid, ids, context=None):
        """ Reserved picking.
        @return: True
        """
        self.write(cr, uid, ids, {'reserved' : True})
        todo = []
        for picking in self.browse(cr, uid, ids, context=context):
            for r in picking.move_lines:
                if r.state == 'draft':
                    todo.append(r.id)

        #self.log_picking(cr, uid, ids, context=context)

        todo = self.action_explode(cr, uid, todo, context)
        if len(todo):
            #make a fake confirmation in order to impact the virtual stock level
            self.pool.get('stock.move').write(cr, uid, todo, {'state': 'confirmed'}, context=context)
        return True

stock_picking()
