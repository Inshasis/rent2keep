#Copyright (c) 2023, Hidayatali and contributors
#For license information, please see license.txt

import json
import frappe

def validate(doc,method):
    check_payment = frappe.db.get_value("Rental Payment Schedule", {'parent':doc.custom_rental_voucher,'date':doc.due_date,'amount':doc.grand_total}, 'name')
    
    #Add Sales Invoice Number In Rental Payment
    frappe.db.set_value('Rental Payment Schedule', check_payment, {
        'sales_invoice': doc.name,
        # 'is_sales_invoice':0
        })
