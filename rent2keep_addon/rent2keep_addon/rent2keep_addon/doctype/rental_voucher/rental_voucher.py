# Copyright (c) 2023, Hidayatali and contributors
# For license information, please see license.txt

import json
import frappe
from frappe.model.document import Document
from frappe.utils import today
from datetime import datetime ,timedelta, date
from dateutil import rrule

class RentalVoucher(Document):
	pass



# @frappe.whitelist()
# def date_invoice_cycle(end_date,start_date):
#     monthlylist=[]
   
#     endate=str(end_date)
#     endate_strp =datetime. strptime(endate, "%Y-%m-%d")
#     endateformating = datetime(endate_strp.year,endate_strp.month,endate_strp.day)
#     invoicing_start_date = str(start_date)
#     invoicing_strp=datetime. strptime(invoicing_start_date,"%Y-%m-%d")
#     invoce_startformating=datetime(invoicing_strp.year,invoicing_strp.month,invoicing_strp.day)
#     [monthlylist.append(monthly.date()) for monthly in rrule.rrule(rrule.MONTHLY,dtstart=invoce_startformating,until=endateformating)]
    
#     return monthlylist

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
		sales_invoice.append("items",{
			'item_code':i.get("item_code"),
			'qty':1,
			'rate':doc.get("instalment_amount"),
			'amount':doc.get("instalment_amount"),

		})

	# Taxes
	for tax in doc.get("taxes"):
		amount = doc.get("instalment_amount")
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
