// Copyright (c) 2023, Hidayatali and contributors
// For license information, please see license.txt


//Total Amount Calculation
frappe.ui.form.on('Enquiry',  {
    refresh: function(frm) {
        if(cur_frm.doc.total_amount === 0){
            let inst_amt = cur_frm.doc.instalments * cur_frm.doc.instalment_amount;
            cur_frm.set_value("total_amount",inst_amt);
            frm.save();
        }
    }
}); 


//Total Saving Calculation
frappe.ui.form.on("Enquiry", "refresh", function(frm) {
    frm.add_custom_button(__("Calculation"), function() {
        
        let inc = cur_frm.doc.type_of_gov_benefit_or_other_income + cur_frm.doc.income_pf;
        let exp = cur_frm.doc.household_expenses_pf + cur_frm.doc.rentmortgage_pf + cur_frm.doc.car_pf + cur_frm.doc.phone_pf + cur_frm.doc.health_insurance_pf + cur_frm.doc.food_pf + cur_frm.doc.loans_pf + cur_frm.doc.other_expenses_pf + cur_frm.doc.other_rentals_pf;
        
        cur_frm.set_value("total_income",inc);
        cur_frm.set_value("total_expenses",exp);
        
        let tot_saving = cur_frm.doc.total_income - cur_frm.doc.total_expenses;
        cur_frm.set_value("total_saving",tot_saving);
        
        frm.save();
        
    }).addClass("btn-warning").css({'background-color':'#2490ef','color':'white','font-weight': 'normal'});

    frm.add_custom_button(__("Convert into SO"), function() {
        frappe.call({
        method: "rent2keep_addon.rent2keep_addon.doctype.enquiry.enquiry.so_create",
        args:{
            doc:cur_frm.doc,
        },
        callback:function(r){
            console.log("*************** Sales Order Created *******************");
        }
        });
        
    }).addClass("btn-warning").css({'background-color':'#A62F03','color':'white','font-weight': 'normal'});
});


