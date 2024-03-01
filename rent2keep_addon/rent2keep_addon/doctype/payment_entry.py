#Copyright (c) 2023, Hidayatali and contributors
#For license information, please see license.txt

import json
import frappe

@frappe.whitelist(allow_guest=True)
def create_rental_voucher(doc):
    doc = json.loads(doc)
    
    create_so_to_rv = frappe.get_doc({
            "doctype": "Rental Voucher",
            "sales_order": doc.get("name"),
            "start_date": doc.get("delivery_date"),
            "total_qty": doc.get("total_qty"),
            "total_amount": doc.get("total"),
            "total_taxes_and_charges":doc.get("total_taxes_and_charges"),
            "in_words":doc.get("in_words"),
            "grand_total":doc.get("grand_total"),
            "rounded_total":doc.get("rounded_total")

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