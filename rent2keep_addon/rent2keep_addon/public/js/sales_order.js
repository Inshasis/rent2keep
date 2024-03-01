// Copyright (c) 2023, Hidayatali and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sales Order', {
    refresh: function(frm) {
        frm.add_custom_button(__('Create Rental Voucher'), function() {
            frappe.call({
                method: "rent2keep_addon.rent2keep_addon.doctype.sales_order.create_rental_voucher",
                args: {
                    doc: frm.doc,
                }
            });
        }).css({ 'background-color': '#2490ef', 'color': 'white' });
    }
});