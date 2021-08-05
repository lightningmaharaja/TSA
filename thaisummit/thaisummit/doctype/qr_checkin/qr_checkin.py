# -*- coding: utf-8 -*-
# Copyright (c) 2021, TEAMPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import add_days
from datetime import datetime

class QRCheckin(Document):
    def after_insert(self):
        if self.qr_shift == "2":
            if frappe.db.exists("QR Checkin",{'employee':self.employee,'qr_shift':'1','shift_date':self.shift_date}):
                frappe.db.set_value("QR Checkin",self.name,'ot',1)
                self.get_bio_checkins()
        if self.qr_shift == "3":
            if frappe.db.exists("QR Checkin",{'employee':self.employee,'qr_shift':'2','shift_date':self.shift_date}):
                frappe.db.set_value("QR Checkin",self.name,'ot',1)
                self.get_bio_checkins()
        # if self.qr_shift == "1":
        #     shift_date = add_days(self.shift_date,-1)
        #     if frappe.db.exists("QR Checkin",{'employee':self.employee,'qr_shift':'3','shift_date':shift_date}):
        #         frappe.db.set_value("QR Checkin",self.name,'ot',1)
        #         self.get_bio_checkins()
        #     if frappe.db.exists("QR Checkin",{'employee':self.employee,'qr_shift':'PP2','shift_date':shift_date}):
        #         frappe.db.set_value("QR Checkin",self.name,'ot',1)
        #         self.get_bio_checkins()

    def get_bio_checkins(self):
        if not frappe.db.exists("Overtime Request",{'ot_date':self.shift_date,'employee':self.employee,'shift':self.qr_shift}):
            ot = frappe.new_doc('Overtime Request')
            ot.employee = self.employee
            ot.department = self.department
            ot.ot_date = self.shift_date
            ot.shift = self.qr_shift
            shift_start = frappe.db.get_value('Shift Type',self.qr_shift,"start_time")
            shift_start_time = datetime.strptime(str(shift_start), '%H:%M:%S')
            qr_shift = datetime.strptime(str(self.created_date), '%Y-%m-%d')
            ot.from_time = datetime.combine(qr_shift,shift_start_time.time())
            ot.to_time = ""
            ot.total_hours = ""
            ot.total_wh = ""
            ot.ot_hours = ""
            ot.save(ignore_permissions=True)
            frappe.db.commit()