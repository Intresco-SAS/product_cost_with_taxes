# -*- encoding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):

    _inherit = "product.template"

    standard_price_with_taxes = fields.Float(
        'Costo con Impuesto', compute='_compute_standard_price_with_taxes',
        digits='Product Price', groups="base.group_user")

    @api.onchange('last_purchase_price', 'supplier_taxes_id')
    def _onchange_product_cost_taxes(self):
        for product in self:
            product._compute_standard_price_with_taxes()

    def _compute_standard_price_with_taxes(self):
        for product in self:
            product.standard_price_with_taxes = 0.0
            if product.supplier_taxes_id:
                taxes = product.supplier_taxes_id[0].compute_all(product.last_purchase_price, product.cost_currency_id, 1, product=product, partner=False)
                # price_subtotal = taxes['total_excluded']
                price_subtotal_incl = taxes['total_included']
                product.standard_price_with_taxes = price_subtotal_incl
