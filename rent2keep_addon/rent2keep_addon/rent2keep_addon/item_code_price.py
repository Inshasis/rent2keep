
import frappe

@frappe.whitelist( allow_guest=True )
def get_item_instalment_rate(item_code):
    # item_price = frappe.get_doc('Item Price', [{'price_list': "Standard Selling"},{'item_code': item_code}])

    item_price = frappe.db.sql("""select * from `tabItem Price` where item_code ="{0}" and price_list ="Standard Selling" """.format(item_code),as_dict = True)[0]
    
    return item_price