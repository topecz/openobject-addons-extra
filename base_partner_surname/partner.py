# -*- encoding: utf-8 -*-
##############################################################################
#    
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.     
#
##############################################################################

from osv import fields, osv


class res_partner_address(osv.osv):
    _inherit = 'res.partner.address'
    _columns = {
        'first_name' : fields.char('First Name', size=128),
        'last_name' : fields.char('Last Name', size=128),
        'name' : fields.char('Name', size=128, readonly=True),
    }
    
    def write(self, cr, uid, ids, vals, context=None):
        if context is None:
            context = {}
        if isinstance(ids,list):
            ids = ids[0]
        data = self.read(cr, uid, ids, ['first_name','last_name'], context=context)
        first_name = data['first_name'] or ''
        if 'first_name' in vals:
            first_name = vals['first_name'] or ''
        
        last_name = data['last_name'] or ''
        if 'last_name' in vals:
            last_name = vals['last_name'] or ''

        if first_name or last_name:
            vals['name'] = first_name + ' ' + last_name
        return super(res_partner_address, self).write(cr, uid, ids, vals, context)

    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        first_name = ''
        last_name = ''
        if 'first_name' in vals:
            first_name = vals['first_name'] or ''
        if 'last_name' in vals:
            last_name = vals['last_name'] or ''
            
        if first_name or last_name:
            vals['name'] = first_name + ' ' + last_name
        return super(res_partner_address, self).create(cr, uid, vals, context)

    def onchange_name(self, cr, uid, id, first_name, last_name):
        res = {}
        if not first_name:
            first_name = ''
        if not last_name:
            last_name = ''
        if first_name or last_name:
            res = {'name': first_name + ' ' + last_name}
        return {'value': res}

res_partner_address()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

