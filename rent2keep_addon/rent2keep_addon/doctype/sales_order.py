#Copyright (c) 2023, Hidayatali and contributors
#For license information, please see license.txt

import json
import frappe
from frappe.utils import add_to_date
from datetime import datetime

@frappe.whitelist(allow_guest=True)
def create_rental_voucher(doc):
        doc = json.loads(doc)
        instalment_type,instalments,instalment_amount = frappe.db.get_value('Enquiry', {'name': doc.get("custom_enquiry")}, ['instalment_type','instalments','instalment_amount'])

    #Create Sales Order
        so_to_rv = frappe.get_list('Rental Voucher', fields=['sales_order'])
        check = {'sales_order': doc.get("name")}    

        if instalment_type == "weekly":
                dy = instalments * 7
                end_date = add_to_date(doc.get("delivery_date"), days=dy, as_string=True)
        
        elif instalment_type == "biweekly":
                dy = instalments * 14
                end_date = add_to_date(doc.get("delivery_date"), days=dy, as_string=True)
        else:
                dy = instalments * 30.5
                end_date = add_to_date(doc.get("delivery_date"), days=dy, as_string=True)

        if check not in so_to_rv:
                create_so_to_rv = frappe.get_doc({
                        "doctype": "Rental Voucher",
                        "sales_order": doc.get("name"),
                        "start_date": doc.get("delivery_date"),
                        "end_date":end_date,
                        "total_qty": doc.get("total_qty"),
                        "total_amount": doc.get("total"),
                        "total_taxes_and_charges":doc.get("total_taxes_and_charges"),
                        "in_words":doc.get("in_words"),
                        "grand_total":doc.get("grand_total"),
                        "rounded_total":doc.get("rounded_total"),
                        "instalment_type":instalment_type,
                        "total_instalments":instalments,
                        "instalment_amount":instalment_amount

                })
                for itm in doc.get('items'):
                        create_so_to_rv.append("items",{
                                'item_code':itm.get('item_code'),
                                'item_name':itm.get('item_name'),
                                'qty':itm.get('qty'),
                                "rate": itm.get('rate'),
                                "amount": itm.get('amount'),


                        })
                for tax in doc.get('taxes'):    
                        create_so_to_rv.append("taxes",{
                                'charge_type':tax.get("charge_type"),
                                'account_head':tax.get("account_head"),
                                'rate':tax.get("rate"),
                                "tax_amount":tax.get("tax_amount"),
                                "total":tax.get("total")

                        })

                create_so_to_rv.insert()
                create_so_to_rv.save()
                frappe.msgprint("Rental Voucher Created Successfully")
        
        else:
                frappe.msgprint("Rental Voucher Already Created!")