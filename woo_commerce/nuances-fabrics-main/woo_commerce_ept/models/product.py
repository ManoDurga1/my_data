# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api
import json


class ProductProduct(models.Model):
    _inherit = 'product.product'

    woo_regular_price = fields.Float(string="Online Regular Price")
    woo_sale_price = fields.Float(string="Online Sale Price")
    woo_stock_available = fields.Float(string="Stock Quantity")
    is_website = fields.Boolean(string="Is Website Product", default=False , readonly="1")

    @api.model
    def update_queue_prices(self, instance):
        """
        Updates the product's woo_sale_price and woo_regular_price and woo_stock_available in product.product
        using the values from woo.product.data.queue.line.ept after syncing.
        """
        queue_lines = self.env['woo.product.data.queue.line.ept'].search([
            ('woo_instance_id', '=', instance.id),
            ('state', '=', 'done')
        ])

        for queue_line in queue_lines:
            try:
                synced_data = json.loads(queue_line.woo_synced_data or "{}")
                woo_product_name = synced_data.get("name", "").strip()
                woo_sku = synced_data.get("sku", "").strip()
                print("SKU", woo_sku)
                print("p name", woo_product_name)
                regular_price = float(synced_data.get("regular_price", 0.0))
                sale_price = float(synced_data.get("sale_price", 0.0))
                stock_qty = float(synced_data.get("stock_quantity") or 0.0)
                print(regular_price)
                print(sale_price)
                print(stock_qty)
                product = self.env['product.product'].search([
                    '|',
                    ('default_code', '=', woo_sku),
                    ('name', '=', woo_product_name)], limit=1)
                if product:
                    product.write({
                        'woo_regular_price': regular_price,
                        'woo_sale_price': sale_price,
                        # 'qty_available': qty_available,
                        'woo_stock_available' : stock_qty,
                        'is_website' : True,
                        # 'standard_price' : regular_price,
                        # 'list_price' : sale_price,
                    })
                    if product.type == 'product':  # Use 'type' instead of 'detailed_type'
                        # Method 1: Use Inventory Adjustment
                        self.env['stock.quant'].with_context(inventory_mode=True).create({
                            'product_id': product.id,
                            'location_id': self.env.ref('stock.stock_location_stock').id,
                            'inventory_quantity_auto_apply': stock_qty,
                        })
            except (json.JSONDecodeError, ValueError) as e:
                print(f"Error parsing JSON for queue line {queue_line.id}: {e}")
        return True

    def _compute_woo_product_count(self):
        woo_product_obj = self.env['woo.product.product.ept']
        for product in self:
            woo_products = woo_product_obj.search([('product_id', '=', product.id)])
            product.woo_product_count = len(woo_products) if woo_products else 0

    woo_product_count = fields.Integer(string='# Sales Count', compute='_compute_woo_product_count')
    image_url = fields.Char(size=600, string='Image URL')

    def write(self, vals):
        """
        This method use to archive/active woo product base on odoo product.
        @author: Maulik Barad on Date 21-May-2020.
        """
        if 'active' in vals.keys():
            woo_product_product_obj = self.env['woo.product.product.ept']
            for product in self:
                woo_product = woo_product_product_obj.search([('product_id', '=', product.id)])
                if vals.get('active'):
                    woo_product = woo_product_product_obj.with_context(active_test=False).search(
                        [('product_id', '=', product.id), ('active', '=', False)])
                woo_product.write({'active': vals.get('active')})
        return super(ProductProduct, self).write(vals)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    woo_regular_price = fields.Float(related="product_variant_ids.woo_regular_price", store=True,string="Woo Regular Price")
    woo_sale_price = fields.Float(related="product_variant_ids.woo_sale_price", store=True, string="Woo Sale Price")
    woo_stock_available = fields.Float(related="product_variant_ids.woo_stock_available", store=True, string="Woo Stock Quantity")
    is_website = fields.Boolean(related="product_variant_ids.is_website",string="Is Website Product",store=True)

    def write(self, vals):
        """
        This method use to archive/unarchive woo product templates base on odoo product templates.
        :parameter: self, vals
        :return: res
        @author: Haresh Mori @Emipro Technologies Pvt. Ltd on date 09/12/2019.
        :Task id: 158502
        """
        if 'active' in vals.keys():
            woo_product_template_obj = self.env['woo.product.template.ept']
            for template in self:
                woo_templates = woo_product_template_obj.search([('product_tmpl_id', '=', template.id)])
                if vals.get('active'):
                    woo_templates = woo_product_template_obj.search([('product_tmpl_id', '=', template.id),
                                                                     ('active', '=', False)])
                woo_templates.write({'active': vals.get('active')})
        res = super(ProductTemplate, self).write(vals)
        return res

    def _compute_woo_template_count(self):
        woo_product_template_obj = self.env['woo.product.template.ept']
        for template in self:
            woo_templates = woo_product_template_obj.search([('product_tmpl_id', '=', template.id)])
            template.woo_template_count = len(woo_templates) if woo_templates else 0

    woo_template_count = fields.Integer(string='# Sales', compute='_compute_woo_template_count')
