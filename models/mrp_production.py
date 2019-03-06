# -*- coding: utf-8 -*-
# Copyright 2018 Iterativo - Rubén Bravo <rubenred18@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class MrpProduction(models.Model):
    _name = "mrp.production"
    _inherit = 'mrp.production'

    sale_line_id = fields.Many2one(
        comodel_name='sale.order.line',
        string='Sale Line',
        related='procurement_group_id.sale_line_id'
    )
