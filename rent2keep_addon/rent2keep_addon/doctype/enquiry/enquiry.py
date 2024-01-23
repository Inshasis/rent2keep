# Copyright (c) 2023, Hidayatali and contributors
# For license information, please see license.txt

import json
import frappe
from frappe.model.document import Document

class Enquiry(Document):
	pass



@frappe.whitelist(allow_guest=True)
def so_create(doc):
	doc = json.loads(doc)

	# Create customer
	customer_list = frappe.get_list('Customer', fields=['custom_email'])
	check = {'custom_email': doc.get("email_address")}
	if check not in customer_list:
		customer = frappe.get_doc({
			"doctype": "Customer",
			"customer_name": doc.get("first_name")+''+doc.get("last_name"),
			"customer_group": 'Individual',
			"customer_type": 'Individual',
			"territory":'Canada',
			"custom_email":doc.get("email_address")
		})
		customer.insert()

	#Create Sales Order
	sales_order = frappe.get_list('Sales Order', fields=['custom_enquiry'])
	check = {'custom_enquiry': doc.get("name")}

	cus_name = frappe.db.get_value('Customer', {'custom_email': doc.get("email_address")}, ['name'])

	if check not in sales_order:
		sales_order_cr = frappe.get_doc({
			"doctype": "Sales Order",
			"customer": cus_name,
			"custom_enquiry": doc.get("name"),
			"delivery_date":frappe.utils.today()

		})
		sales_order_cr.append("items",{
			'item_code':doc.get("item_code"),
			'item_name':doc.get("item_code"),
			'qty':'1',
			'rate':doc.get("total_amount")

		})
		sales_order_cr.insert()
		sales_order_cr.save()
		frappe.msgprint("SO Create Successfull")
	
	else:
		frappe.msgprint("Alreday Created!")
