# -*- coding: utf-8 -*-
# Copyright 2018 Iterativo - Rubén Bravo <rubenred18@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class ProcurementGroup(models.Model):
    _inherit = 'procurement.group'

    sale_line_id = fields.Many2one(
        'sale.order.line', string='Sale Line'
    )
