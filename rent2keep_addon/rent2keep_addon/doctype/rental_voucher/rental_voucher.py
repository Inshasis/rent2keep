# Copyright (c) 2023, Hidayatali and contributors
# For license information, please see license.txt

import json
import frappe
from frappe.model.document import Document
from frappe.utils import today

class RentalVoucher(Document):
	pass


@frappe.whitelist(allow_guest=True)
def auto_create_sales_invoice(doc):
	doc = json.loads(doc)
	
	sales_invoice = frappe.get_doc({
		"doctype": "Sales Invoice",
		"custom_rental_voucher":doc.get("name"),
		"customer": doc.get("customer"),
		"disable_rounded_total":1

	})
	# Items
	for i in doc.get("items"):
		amount = doc.get("total_amount") / doc.get("total_week")
		sales_invoice.append("items",{
			'item_code':i.get("item_code"),
			'qty':1,
			'rate':amount,
			'amount':amount,

		})

	# Taxes
	for tax in doc.get("taxes"):
		amount = doc.get("total_amount") / doc.get("total_week")
		tax_amount = amount * tax.get("rate") / 100
		sales_invoice.append("taxes",{
			'charge_type':tax.get("charge_type"),
			'description':"GST @ 5.0",
			'account_head':tax.get("account_head"),
			'rate':tax.get("rate"),
			'tax_amount':tax_amount,
			'total':tax_amount,

		})	

	sales_invoice.insert()
	# sales_invoice.submit()
	sales_invoice.reload()
