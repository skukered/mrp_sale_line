# -*- coding: utf-8 -*-
# Copyright 2018 Iterativo - Rubén Bravo <rubenred18@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models, api
from odoo.tools import float_compare
from odoo.exceptions import UserError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.multi
    def _action_launch_procurement_rule(self):
        precision = self.env['decimal.precision'].precision_get(
            'Product Unit of Measure'
        )
        errors = []
        for line in self:
            if line.state != 'sale' or not line.product_id.type in ('consu',
                                                                    'product'):
                continue
            qty = line._get_qty_procurement()
            if float_compare(qty, line.product_uom_qty,
                             precision_digits=precision) >= 0:
                continue

            group_id = self.env['procurement.group'].create({
                'name': line.order_id.name,
                'move_type': line.order_id.picking_policy,
                'sale_id': line.order_id.id,
                'sale_line_id': line.id,
                'partner_id': line.order_id.partner_shipping_id.id,
            })
            line.order_id.procurement_group_id = group_id

            values = line._prepare_procurement_values(group_id=group_id)
            product_qty = line.product_uom_qty - qty

            procurement_uom = line.product_uom
            quant_uom = line.product_id.uom_id
            get_param = self.env['ir.config_parameter'].sudo().get_param
            if procurement_uom.id != quant_uom.id and get_param(
                'stock.propagate_uom'
            ) != '1':
                product_qty = line.product_uom._compute_quantity(
                    product_qty, quant_uom, rounding_method='HALF-UP'
                )
                procurement_uom = quant_uom

            try:
                self.env['procurement.group'].run(
                    line.product_id, product_qty,
                    procurement_uom,
                    line.order_id.partner_shipping_id.property_stock_customer,
                    line.name, line.order_id.name, values
                )
            except UserError as error:
                errors.append(error.name)
        if errors:
            raise UserError('\n'.join(errors))
        return True
