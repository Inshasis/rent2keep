// Copyright (c) 2023, Hidayatali and contributors
// For license information, please see license.txt

// frappe.ui.form.on('Rental Voucher', {
//     refresh: function(frm) {
//         if(cur_frm.doc.payment_schedule.length === 0){
//                 frm.add_custom_button(__('EMI Calculator'), function() {
//                     if(frm.doc.start_date && frm.doc.end_date){
//                         frappe.call({
//                             method: 'rent2keep_addon.rent2keep_addon.doctype.rental_voucher.rental_voucher.date_invoice_cycle',
//                             args: {
//                                 "start_date": frm.doc.start_date,
//                                 "end_date": frm.doc.end_date
            
//                             },
//                             callback: function(r) {
//                                 console.log(r);
//                                 cur_frm.clear_table("payment_schedule");
//                                 cur_frm.refresh_fields("payment_schedule");
//                                 for (let i = 0; i < r.message.length; i++) {
            
//                                     var childTable = cur_frm.add_child("payment_schedule");
//                                     childTable.date = r.message[i];
//                                     childTable.amount = cur_frm.doc.instalment_amount;
            
//                                     cur_frm.refresh_fields("payment_schedule");
            
            
//                                 }
//                             }
//                         });
//                     }
//                     else{
//                         msgprint("Please Check Start Date and End Date ");
//                     }
//                 }).css({ 'background-color': '#2490ef', 'color': 'white' });
            
            
//         }
//     }
// });

frappe.ui.form.on('Rental Payment Schedule', {
	create_sales_invoice:function(frm,cdt,cdn){
		var d = locals[cdt][cdn];
		frappe.call({
            method:"rent2keep_addon.rent2keep_addon.doctype.rental_voucher.rental_voucher.auto_create_sales_invoice",
            args:{
                doc:cur_frm.doc
            },
            callback:function(r){
                console.log(r);
                frappe.model.set_value(cdt, cdn, 'is_sales_invoice',1);
                frm.save();
                frm.reload();
            }
            
        });
	}
});
