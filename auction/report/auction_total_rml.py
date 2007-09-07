##############################################################################
#
# Copyright (c) 2005 TINY SPRL. (http://tiny.be) All Rights Reserved.
#
# $Id$
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################


import pooler
import time
from report import report_sxw


class auction_total_rml(report_sxw.rml_parse):
	def __init__(self, cr, uid, name, context):
		super(auction_total_rml, self).__init__(cr, uid, name, context)
		self.localcontext.update({
			'time': time,
			'sum_taxes':self.sum_taxes,
			'sold_item':self.sold_item,
			'sum_buyer':self.sum_buyer,
			'sum_seller':self.sum_seller,
			'sum_buyer_paid':self.sum_buyer_paid,
			'sum_adj':self.sum_adj,
			'count_comm':self.count_comm,
			'sum_minadj':self.sum_minadj,
			'sum_maxadj':self.sum_maxadj,
			'sum_credit':self.sum_credit,
			'sum_debit': self.sum_debit,
			'chek_paid': self.chek_paid,
			'check_paid_seller': self.chek_paid,
			'count_take': self.count_take,
			'sum_credit_seller':self.sum_credit_seller,
			'sum_debit_buyer': self.sum_debit_buyer
		})

	def sum_taxes(self, auction_id):
		return len(self.pool.get('auction.lots').search(self.cr,self.uid,([('auction_id','=',auction_id)])))

	def sold_item(self, object):
		auct_id=object.auction_id.id
		self.cr.execute("select count(1) from auction_lots where auction_id=%d and state in ('unsold','draft') "%(auct_id))
		res = self.cr.fetchone()
		return str(res[0])


	def sum_buyer(self, auction_id):
		self.cr.execute('select count(*) from auction_lots where auction_id=%d AND ach_uid is not null'%(auction_id))
		res = self.cr.fetchone()
		return str(res[0])
	def sum_seller(self, auction_id):
		self.cr.execute('select count(*) from auction_lots where auction_id=%d AND bord_vnd_id is not null'%(auction_id))
		res = self.cr.fetchone()
		return str(res[0])

	def sum_adj(self, auction_id):
		self.cr.execute('select sum(obj_price) from auction_lots where auction_id=%d '%(auction_id))
		res = self.cr.fetchone()
		return str(res[0])

	def count_take(self, auction_id):
		self.cr.execute("select count(*) from auction_lots where auction_id=%d and ach_emp='True'"%(auction_id))
		res = self.cr.fetchone()
		return str(res[0])

	def chek_paid(self, auction_id):
		self.cr.execute("select count(1) from auction_lots where auction_id=%d and ((paid_ach='T') or (is_ok='T')) "%(auction_id))
		res = self.cr.fetchone()
		return str(res[0])
	def check_paid_seller(self, auction_id):
		self.cr.execute("select count(1) from auction_lots where auction_id=%d and paid_vnd=1 "%(auction_id))
		res = self.cr.fetchone()
		return str(res[0])

	def sum_credit(self,object):
		print "ICI CA BLOQUE"
		auct_id=object.auction_id.id
		print auct_id
		self.cr.execute("select sum(buyer_price) from auction_lots where (auction_id=%d) and (paid_ach='T')"%(auct_id,))
		res = self.cr.fetchone()
		return str(res[0] or 0)

	def sum_debit_buyer(self,object):
		auct_id=object.auction_id.id
		self.cr.execute("select sum(buyer_price) from auction_lots where auction_id=%d and paid_ach='F'"%(auct_id,))
		res = self.cr.fetchone()
		return str(res[0] or 0)

	def sum_debit(self, object):
		auct_id=object.auction_id.id
		self.cr.execute("select sum(seller_price) from auction_lots where auction_id=%d and paid_vnd='0'"%(auct_id))
		res = self.cr.fetchone()
		return str(res[0] or 0)

	def sum_credit_seller(self, object):
		auct_id=object.auction_id.id
		self.cr.execute("select sum(seller_price) from auction_lots where auction_id=%d and paid_vnd='1'"%(auct_id))
		res = self.cr.fetchone()
		return str(res[0] or 0)

	def sum_minadj(self, auction_id):
		self.cr.execute('select sum(lot_est1) from auction_lots where auction_id=%d '%(auction_id))
		res = self.cr.fetchone()
		return str(res[0])

	def sum_maxadj(self, auction_id):
		self.cr.execute('select sum(lot_est2) from auction_lots where auction_id=%d '%(auction_id))
		res = self.cr.fetchone()
		return str(res[0])

	def sum_buyer_paid(self, auction_id):
		self.cr.execute("select count(*) from auction_lots where auction_id=%d AND state = 'paid'"%(auction_id))
		res = self.cr.fetchone()
		return str(res[0])

	def count_comm(self, auction_id):
		self.cr.execute("select count(*) from auction_lots where auction_id=%d AND obj_comm is not null"%(auction_id))
		res = self.cr.fetchone()
		return str(res[0])

report_sxw.report_sxw('report.auction.total.rml', 'auction.lots', 'addons/auction/report/auction_total.rml',parser=auction_total_rml)


