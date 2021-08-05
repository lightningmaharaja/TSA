import frappe
import json
import datetime
from frappe.utils.csvutils import read_csv_content
from frappe.utils.data import format_date, get_url_to_list
from six.moves import range
from six import string_types
from frappe.utils import (getdate, cint, add_months, date_diff, add_days,
    nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime, format_date)
from datetime import datetime
from calendar import IllegalMonthError, month, monthrange
from frappe import _, msgprint
from frappe.utils import flt,get_url_to_list
from frappe.utils import cstr, cint, getdate,get_first_day, get_last_day, today
import requests
from datetime import date, timedelta,time
import calendar
from erpnext.hr.doctype.employee.employee import get_holiday_list_for_employee
# from tabulate import tabulate


def bulk_update_from_csv(filename):
    #below is the method to get file from Frappe File manager
    from frappe.utils.file_manager import get_file
    #Method to fetch file using get_doc and stored as _file
    _file = frappe.get_doc("File", {"file_name": filename})
    #Path in the system
    filepath = get_file(filename)
    #CSV Content stored as pps

    pps = read_csv_content(filepath[1])
    for pp in pps:
        date = "2021-02-28"
        print(pp[0])
        print(frappe.db.exists('Attendance',{'employee':pp[0],'attendance_date':date}))
        for p in pp:
            if p != pp[0]:
                date = add_days(date,1)
                if not frappe.db.exists('Attendance',{'attendance_date':date,'employee':pp[0]}):
                    print(date,p)
                    status = ''
                    late = 0
                    if p in ['1','2','3','PP1','PP2','1L','2L','3L','PP1L','PP2L']:
                        # print(p)
                        att = frappe.new_doc("Attendance")
                        att.employee = pp[0]
                        att.attendance_date = date
                        att.status = 'Present'
                        if p in ['1L','2L','3L','PP1L','PP2L']:
                            att.late_entry = 1
                            att.shift = p.strip('L')
                        else:
                            att.shift = p
                        att.save(ignore_permissions=True)
                        att.submit()
                        frappe.db.commit()
                    elif p in  ['A','SL','EL','CL']:
                        att = frappe.new_doc("Attendance")
                        att.employee = pp[0]
                        att.attendance_date = date
                        att.status = 'Absent'
                        att.save(ignore_permissions=True)
                        att.submit()
                        frappe.db.commit()
                        # if p != 'A':
                        #     lev = frappe.new_doc("Leave Application")
                        #     lev.employee = pp[0]
                        #     lev.from_date = date
                        #     lev.to_date = date
                        #     lev.leave_approver = 'abdulla.pi@groupteampro.com'
                        #     lev.status = 'Approved'
                        #     if p == 'SL':
                        #         lev.leave_type = 'Sick Leave'
                        #     elif p == 'EL':
                        #         lev.leave_type = 'Earned Leave'
                        #     elif p == 'CL':
                        #         lev.leave_type = 'Casual Leave'
                        #     lev.save(ignore_permissions=True)
                        #     lev.submit()
                        #     frappe.db.commit()
                    elif p == 'OD':
                        od = frappe.new_doc("Attendance Request")
                        od.employee = pp[0]
                        od.from_date = date
                        od.to_date = date
                        od.reason = 'On Duty'
                        od.save(ignore_permissions=True)
                        od.submit()
                        frappe.db.commit()


def bulk_update_from_csv1(filename):
    #below is the method to get file from Frappe File manager
    from frappe.utils.file_manager import get_file
    #Method to fetch file using get_doc and stored as _file
    _file = frappe.get_doc("File", {"file_name": filename})
    #Path in the system
    filepath = get_file(filename)
    #CSV Content stored as pps

    pps = read_csv_content(filepath[1])
    for pp in pps:
        print(pp[0],pp[1])
        if frappe.db.exists('Employee',{'name':pp[0]}):
            doc = frappe.new_doc("QR Checkin")
            doc.employee = pp[0]
            doc.qr_shift = pp[2]
            doc.qr_scan_time = pp[1]
            doc.save(ignore_permissions=True)
            frappe.db.commit()
            att = frappe.db.exists('Attendance',{'employee':pp[0],'attendance_date':pp[1]})
            if att:
                print(pp[2])
                frappe.db.set_value('Attendance',att,'qr_shift',pp[2])
                print(doc.name)
                frappe.db.set_value("QR Checkin",doc.name,'attendance',att)
                   
                    


# def update_leave_approver():
#     depts = frappe.get_all("Department")
#     for dep in depts:
#         if dep.name != 'All Departments':
#             doc = frappe.get_doc("Department",dep.name)
#             print(doc.name)
#             doc.append('leave_approvers',{
#                 'approver' : 'abdulla.pi@groupteampro.com'
#             })
#             doc.save(ignore_permissions=True)
def mail_wc_probation():
    employees =frappe.get_all("Employee",{"employment_type":"Probation","employee_type":"WC"},["date_of_joining","name","employee_name","personal_email"])
    # print(employees)
    for emp in employees:
        # print(emp)
        t=relativedelta(months=5)
        fifth_month=emp.date_of_joining+t
        # print(fifth_month)
        s=relativedelta(months=6)
        sixth_month=emp.date_of_joining+s
        # print(sixth_month)
        today=datetime.today()
        if(fifth_month<= today.date()<= sixth_month):
            # print(emp.personal_email)
            frappe.sendmail(
            recipients= emp.personal_email,
            subject='Probation Period Date',
            message="""<p>Dear Admin,</p>
            <p> Probation period end date for  %s %s employee  </p>""" % (emp.name,emp.employee_name))
def mail_wc_get_trainee():
    employees =frappe.get_all("Employee",{"employment_type":"Trainee","employee_type":"WC","designation":"Graduate Engineer Trainee"},["date_of_joining","name","employee_name","personal_email"])
    # print(employees)
    for emp in employees:
        # print(emp)
        t=relativedelta(months=11)
        eleventh_month=emp.date_of_joining+t
        # print(eleventh_month)
        s=relativedelta(months=12)
        tewlth_month=emp.date_of_joining+s
        # print(tewlth_month)
        today=datetime.today()
        if(eleventh_month<= today.date()<= tewlth_month):
            # print("hi")
            frappe.sendmail(
            recipients= emp.personal_email,
            subject='Probation Period Date' ,
            message="""<p>Dear Admin,</p>
            <p> Trainee period end date for  %s %s employee  </p>""" % (emp.name,emp.employee_name))
def mail_wc_get_probation():
    employees =frappe.get_all("Employee",{"employment_type":"Probation","employee_type":"WC","designation":"Graduate Engineer Trainee"},["date_of_joining","name","employee_name","personal_email"])
    # print(employees)
    for emp in employees:
        # print(emp)
        t=relativedelta(months=17)
        eleventh_month=emp.date_of_joining+t
        # print(eleventh_month)
        s=relativedelta(months=18)
        tewlth_month=emp.date_of_joining+s
        # print(tewlth_month)
        today=datetime.today()
        if(eleventh_month<= today.date()<= tewlth_month):
            # print("hi")
            frappe.sendmail(
            recipients=emp.personal_email,
            subject='Probation Period Date',
            message="""<p>Dear Admin,</p>
            <p> Probation period end date for  %s %s employee  </p>""" % (emp.name,emp.employee_name))

def el_leave_policy():
    employees =frappe.get_all("Employee",{"employee_type":"WC"},["name","employee_name","personal_email"])
    for emp in employees:
        print(emp.name)
        count = 0
        el = 0
        today = "2022-01-01"
        start_date = add_months(today, -12)
        end_date = add_days(today, -1)
        print(end_date)
        print(start_date)
        for att in (frappe.db.sql("""select status,attendance_date from `tabAttendance` where attendance_date between '%s' and '%s'  """ %(start_date,end_date),as_dict=True)):
            print(att)
            if (att.status == "Present"):
                count += 1
            else:
                count = 0
            # print(count)
            if count >= 20:
                el = count // 20 + el
                count = 0
                break  
        print(el)
        print(datetime.today().date())
        get_la = frappe.new_doc("Leave Allocation")
        get_la.employee = emp.name
        get_la.leave_type = "Earned Leave"
        get_la.from_date = datetime.today().date()
        get_la.to_date = add_months(datetime.today().date(), 12)
        get_la.new_leaves_allocated = (int(el))
        get_la.save(ignore_permissions = True)
        frappe.db.commit()       
def el_leave_encashment():
    employees =frappe.get_all("Employee",{"employee_type":"WC"},["name"])
    for emp in employees:
        print(emp.name)
        # if(emp.name == "TSAI0195"):
        get_le = frappe.new_doc("Leave Encashment")
        get_le.employee = emp.name
        get_le.leave_type = "Earned Leave"
        get_le.leave_period = "HR-LPR-2021-00001"
        get_le.save(ignore_permissions = True)
        frappe.db.commit()




@frappe.whitelist()   
def create_user(employee_number,employee_name):
    # frappe.errprint(employee_number)
    user = frappe.new_doc("User")
    user.email = employee_number + "@gmail.com"
    user.first_name = employee_name
    user.username = employee_number
    user.send_welcome_mail = 0
    user.new_password = "thai@1234"
    user.save(ignore_permissions = True)
    frappe.db.commit()
    return user.email

@frappe.whitelist()
def get_sap_qty():
    parts = frappe.get_all('Part Master',['mat_no','name'])
    for part in parts:
        url = "http://182.156.241.14/StockDetail/Service1.svc/GetFGQuantity"
        payload = json.dumps({
        "ItemCode": part['mat_no']
        })
        headers = {
        'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        qty = json.loads(response.text)
        if qty:
            avl_qty = qty[0]['Qty']
            frappe.set_value("Part Master",part['name'],"sap_available_quantity",avl_qty)
            frappe.set_value("Part Master",part['name'],"sap_quantity_updated_on",datetime.now())
            frappe.set_value("Part Master",part['name'],"temp_avl_qty",avl_qty)
            frappe.set_value("Part Master",part['name'],"temp_qty_updated_on",datetime.now())
    return "Successfully Updated"

@frappe.whitelist()
def deductions():
    last_mon = add_months(nowdate(),-1)
    today = nowdate()
    deduction = frappe.db.sql("""select employee, sum(amount) as total_amount from `tabDeductions` where docstatus=1 and
        MONTH(posting_date) = MONTH(%(mon)s) group by employee""",(dict(mon=last_mon)),as_dict=True)
    for ded in deduction:
        additional_salary = frappe.db.exists("Additional Salary",{"employee":ded.employee,"payroll_date":today,"salary_component":"Personal Protective Equipment","docstatus":1},["employee"])
        if not additional_salary:
            add_salary = frappe.new_doc("Additional Salary")
            add_salary.employee = ded.employee
            add_salary.salary_component = "Personal Protective Equipment"
            add_salary.amount = int(ded.total_amount)
            add_salary.payroll_date = nowdate()
            add_salary.overwrite_salary_structure_amount = "1"
            add_salary.save(ignore_permissions=True)
            add_salary.submit()
            frappe.db.commit()

@frappe.whitelist()
def change_leave_approver(employee,leave_approver):
    leave_application = frappe.db.get_all("Leave Application",{"employee":employee,"docstatus":0},["name"])
    for lev_app in leave_application:
        frappe.db.set_value('Leave Application',lev_app.name,'leave_approver',leave_approver)

@frappe.whitelist()
def change_permission_approver(employee,permission_approver):
    permission_request = frappe.db.get_all("Permission Request",{"employee":employee,"docstatus":0},["name"])
    for per_req in permission_request:
        frappe.db.set_value('Permission Request',per_req.name,'permission_approver',permission_approver)

@frappe.whitelist()
def change_od_approver(employee,od_approver):
    od_application = frappe.db.get_all("On Duty Application",{"employee":employee,"docstatus":0},["name"])
    for od_app in od_application:
        frappe.db.set_value('On Duty Application',od_app.name,'approver',od_approver)


# def employee_type():
#     emps = frappe.db.sql("select name from `tabEmployee` where name like 'V%' ")
#     print(len(emps))
#     for emp in emps:
#         print(emp[0])
#         frappe.db.set_value("Employee",emp[0],"vacant",1)




def is_weekoff(employee, date=None, raise_exception=True):
    '''Returns True if given Employee has a weekoff on the given date
    :param employee: Employee `name`
    :param date: Date to check. Will check for today if None'''

    holiday_list = get_holiday_list_for_employee(employee, raise_exception)
    if not date:
        date = today()
    if holiday_list:
        return frappe.get_all('Holiday List',dict(name=holiday_list, holiday_date=date, weekly_off=1)) and True or False

def is_holiday(employee, date=None, raise_exception=True):
    '''Returns True if given Employee has an holiday on the given date
    :param employee: Employee `name`
    :param date: Date to check. Will check for today if None'''

    holiday_list = get_holiday_list_for_employee(employee, raise_exception)
    if not date:
        date = today()
    if holiday_list:
        return frappe.get_all('Holiday List', dict(name=holiday_list, holiday_date=date,  weekly_off=0)) and True or False


def send_birthday_wish():
    birthdays =frappe.db.sql("""select name,date_of_birth,personal_email, employee_name
        from tabEmployee where day(date_of_birth) = day(%(date)s)
        and month(date_of_birth) = month(%(date)s)
        and status = 'Active'""",{"date": today()}, as_dict=True)
    print(birthdays)
    for emp in birthdays:
        print(emp.personal_email)
        if birthdays:
            frappe.sendmail(
            recipients= emp.personal_email,
            subject="Birthday Wishes",
            message="""<p> Dear %s <br> May your birthday be the start of a year filled with good luck, good health and much happiness, <br>
            We wish you an amazing year that ends with accomplishing all the great goals that you have set!</p>""" %(emp.employee_name))

@frappe.whitelist()
def send_confirmation_mail(employee_number,employee_name,personal_email,confirmation_message):
    frappe.sendmail(
    recipients= personal_email,
    subject="Birthday Wishes",
    message="""<p> Dear %s <br> 
    %s
    </p>""" %(employee_name,confirmation_message))

@frappe.whitelist()
def get_shift(emp):
    previous_month = frappe.utils.add_months(datetime.today(), -1).strftime("%Y-%m-26")
    current_month = (datetime.today()).strftime("%Y-%m-25")
    date_list = get_dates(previous_month,current_month)
    data = ''
    rh1 = '<tr>'
    rh2 = ''
    rh3 = ''
    rd1 = '<tr>'
    rd2 = ''
    rd3 = ''
    r1 = ''
    r2 = ''
    r3 = ''
    i = 1
    for date in date_list:
        if frappe.db.exists('Attendance',{'employee':emp,'attendance_date':date,'docstatus':['!=','2']}):
            att = frappe.get_doc('Attendance',{'employee':emp,'attendance_date':date,'docstatus':['!=','2']})
            # if rd1 == str(A):
            #     """<td style='color:red'> A </td>  """
            # frappe.errprint(date)
            frappe.errprint(att.shift)
            if i <= 10:
                rh1 += """<th><center>%s</center></th>"""%((datetime.strptime(date, '%Y-%m-%d').date()).strftime("%d-%b"))
                rd1 += """<td><center>%s</center></td>"""%(att.shift or 'A')
                if i == 10:
                    r1 = rh1 + '</tr>' + rd1 + '</tr>'
            elif 10 < i <= 20:
                rh2 += """<th><center>%s</center></th>"""%((datetime.strptime(date, '%Y-%m-%d').date()).strftime("%d-%b"))
                rd2 += """<td><center>%s</center></td>"""%(att.shift or 'A')
                if i == 20:
                    r2 = '<tr>' + rh2 + '</tr><tr>' + rd2 + '</tr>'
            elif 20 < i:
                rh3 += """<th><center>%s</center></th>"""%((datetime.strptime(date, '%Y-%m-%d').date()).strftime("%d-%b"))
                rd3 += """<td><center>%s</center></td>"""%(att.shift or 'A')
            i += 1
        data = "<table border='1' class='table table-bordered'>" + r1 + r2 + '<tr>' + rh3 + '</tr><tr>' + rd3 + '</tr>' +"</table>"
    return data


def get_dates(previous_month,current_month):
    """get list of date s in between from date and to date"""
    no_of_days = date_diff(add_days(current_month, 1),previous_month )
    dates = [add_days(previous_month, i) for i in range(0, no_of_days)]
    return dates


def send_mail_hr():
    """Continous absent employees for 5 days mail sent to hr """
    current_date = (datetime.today()).strftime("%Y-%m-%d")
    five_days = frappe.utils.add_days(datetime.today(), -5).strftime("%Y-%m-%d")
    print(five_days)
    print(current_date)
    get_att = frappe.db.sql(""" select employee_name,employee,count(status) as absent_count from `tabAttendance` where status ='Absent' and docstatus = '1' and attendance_date between '%s' and '%s'  group by employee""" %(five_days,current_date),as_dict =True)
    print(get_att)
    data = ''
    header = """<tr> <th>SL No </th> <th> Employee ID</th><th> Employee Name </tr>"""
    for idx,att in enumerate(get_att):
        if att.absent_count == 5 :
            data += """ <tr> <td> %s </td> <td> %s </td> <td> %s </td> </tr>""" %(idx+1,att.employee,att.employee_name)
    data = "<table border='1' class='table table-bordered'>" + header +  data +"</table>"
    frappe.sendmail(
        recipients= ['sarumathy.d@groupteampro.com'],
        subject="Absent Employees",
        message= data)

def create_leave_allocation():
    # current_date = (datetime.today()).strftime("%Y-%m-%d")
    three_days = frappe.utils.add_days(datetime.today(), -3).strftime("%Y-%m-%d")
    print(three_days)
    employees =frappe.get_all("Employee",{"status":"Active"},["name","employee_name","personal_email"])
    for emp in employees:
        # print(emp.name)
        attendance = frappe.db.get_all('Attendance',{'employee':emp.name,'attendance_date':three_days,'docstatus':'1'},["status","employee"])
        for att in attendance:
            # print(att.status)
            if att.status in ('Half Day'):
                from erpnext.hr.doctype.leave_application.leave_application import get_leave_details
                leave_balance = get_leave_details(att.employee,nowdate())
                try:
                    if (leave_balance['leave_allocation']['Casual Leave']['remaining_leaves']) > 0:
                        leave_app = frappe.new_doc("Leave Application")
                        leave_app.employee = att.employee
                        leave_app.from_date = three_days
                        leave_app.to_date = three_days
                        leave_app.leave_type = 'Casual Leave'
                        leave_app.description = 'Auto-Leave Application for Late In Entry'
                        leave_app.leave_approver = "Administrator"
                        leave_app.save(ignore_permissions=True)
                        frappe.db.commit()
                   
                    elif(leave_balance['leave_allocation']['Sick Leave']['remaining_leaves']) > 0:
                        l_app = frappe.new_doc("Leave Application")
                        l_app.employee = att.employee
                        l_app.from_date = three_days
                        l_app.to_date = three_days
                        l_app.leave_type = 'Sick Leave'
                        l_app.description = 'Auto-Leave Application for Late In Entry'
                        l_app.leave_approver = "Administrator"
                        l_app.save(ignore_permissions=True)
                        frappe.db.commit()
                    elif (leave_balance['leave_allocation']['Earned Leave']['remaining_leaves']) > 0:
                        lea_app = frappe.new_doc("Leave Application")
                        lea_app.employee = att.employee
                        lea_app.from_date = three_days
                        lea_app.to_date = three_days
                        lea_app.leave_type = 'Earned Leave'
                        lea_app.description = 'Auto-Leave Application for Late In Entry'
                        lea_app.leave_approver = "Administrator"
                        lea_app.save(ignore_permissions=True)
                        frappe.db.commit()           
                except KeyError:
                    leave_balance['leave_allocation']['Casual Leave'] = 0
                    leave_balance['leave_allocation']['Sick Leave'] = 0
                    leave_balance['leave_allocation']['Earned Leave'] = 0


def add_special_leave():
    lle = frappe.new_doc("Leave Ledger Entry")
    lle.employee = "5"
    lle.from_date = '2021-01-01'
    lle.to_date = '2021-12-31'
    lle.leave_type = 'Casual Leave'
    lle.transaction_type = 'Leave Allocation'
    lle.leaves = "10"
    lle.save(ignore_permissions=True)
    lle.submit()
    frappe.db.commit()

@frappe.whitelist()
def exceed_vehicle_load(name,vehicle_name):
    emp = frappe.db.count('Employee',{'vehicle_name':vehicle_name})
    load = frappe.db.get_value("Vehicle Management",{'name':vehicle_name},['load_capacity'])
    balance_load = int(load - emp)
    # frappe.errprint(balance_load)
    # if(emp >= load):
    #     return "Vehicle Load Exceeded"
    return emp,load

@frappe.whitelist()
def delete_shift_summary():
    ss = frappe.get_all("Shift Schedule Status Summary")
    for s in ss:
        doc = frappe.get_doc("Shift Schedule Status Summary",s.name)
        doc.delete()

@frappe.whitelist()
def mark_qr_user(user,status):
    user = frappe.get_doc('User',user)
    if status == 'Add':
        user.role_profile_name = ''
        user.add_roles('QR User')
        frappe.errprint('add')
    else:
        user.remove_roles('QR User')
        frappe.errprint('remove')
    user.save(ignore_permissions=True)

@frappe.whitelist()
def mark_qr_user_from_csv(filename):
    #below is the method to get file from Frappe File manager
    from frappe.utils.file_manager import get_file
    #Method to fetch file using get_doc and stored as _file
    _file = frappe.get_doc("File", {"file_name": filename})
    #Path in the system
    filepath = get_file(filename)
    #CSV Content stored as pps
    pps = read_csv_content(filepath[1])
    for pp in pps:
        # print(pp[0])
        userid = frappe.get_value('Employee',pp[0],'user_id')
        username = frappe.db.exists('User',userid)
        if username:
            user = frappe.get_doc('User',username)
            user.role_profile_name = ''
            user.add_roles('QR User')
            user.save(ignore_permissions=True)

# def update_qr():
#     qrs = frappe.get_all("QR Checkin",{'shift_date':'2021-05-05'},["shift_date","qr_shift","employee"])
#     for qr in qrs:
#         att = frappe.db.exists("Attendance",{'employee':qr.employee,'attendance_date':qr.shift_date})
#         print(att)
#         frappe.db.set_value("Attendance",att,"qr_shift",qr.qr_shift)
#         frappe.db.set_value("Attendance",att,"qr_scan_time",qr.qr_scan_time)

@frappe.whitelist()
def roundoff_time(time):
    time = datetime.strptime(time,'%H:%M:%S')
    if time.minute not in (0,30):
        if time.minute < 30:
            roundoff_time = time.replace(minute=0)
        elif time.minute >= 30:
            roundoff_time = time.replace(minute=30)
        roundoff_time = roundoff_time.time()
        return str(roundoff_time)

@frappe.whitelist()
def get_employee_code(user):
    emp_id = frappe.db.get_value('Employee',{'user_id':user},"name")
    return emp_id

@frappe.whitelist()
def get_ceo(department):
    ceo = frappe.db.get_value('Department',department,"ceo")
    return ceo

@frappe.whitelist()
def get_gm(department):
    gm = frappe.db.get_value('Department',department,"gm")
    return gm

@frappe.whitelist()
def get_hod(department):
    hod = frappe.db.get_value('Department',department,"hod")
    return hod

@frappe.whitelist()
def update_user_permission(user,department):
    if not frappe.db.exists("User Permission",{'user':user,'allow':"Department","for_value":department,"is_default":1}):
        default = frappe.db.exists("User Permission",{'user':user,'allow':"Department","is_default":'1'})
        if default:
            frappe.delete_doc("User Permission",default)
        up = frappe.db.exists("User Permission",{'user':user,'allow':"Department",'for_value':department})
        if up:
            doc = frappe.get_doc("User Permission",up)
            doc.is_default = 1
            doc.save(ignore_permissions=True)
        else:
            doc = frappe.new_doc("User Permission")
            doc.user = user
            doc.allow = "Department"
            doc.for_value = department
            doc.is_default = 1
            doc.save(ignore_permissions=True)

@frappe.whitelist()
def application_allowed_from(date):
    # date = datetime.strptime(date, '%Y-%m-%d').date()
    # today_date = datetime.strptime('2021-07-29', '%Y-%m-%d').date()
    # # today_date = datetime.strptime(today(), '%Y-%m-%d').date()
    # if today_date.day <= 28:
    #     last_month = add_months(today_date,-1)
    #     last_month_start = get_first_day(last_month)
    #     allowed_from = add_days(last_month_start,25)
    #     cur_month_start = get_last_day(today_date)
    #     allowed_till = add_days(cur_month_start,25)
    #     frappe.errprint(allowed_from)
    #     frappe.errprint(allowed_till)
    #     if date < allowed_from:
    #         frappe.msgprint('Application not allowed before %s'%allowed_from)
    #         return 'NO'
    #     if date > allowed_till:
    #         frappe.msgprint('Application not allowed after %s'%allowed_till)
    #         return 'NO'
    # else:
    #     cur_month_start = get_first_day(today_date)
    #     allowed_from = add_days(cur_month_start,25)
    #     month_end = get_last_day(cur_month_start)
    #     allowed_till = add_days,(month_end,25)
    #     frappe.errprint(allowed_from)
    #     frappe.errprint(allowed_till)
    #     if date < allowed_from:
    #         frappe.msgprint('Application not allowed before %s'%allowed_from)
    #         return 'NO'
    #     if date > allowed_till:
    #         frappe.msgprint('Application not allowed after %s'%allowed_till)
    #         return 'NO'
    return ''

# @frappe.whitelist()
# def update_dept():
#     employess = frappe.get_all('Employee',['department','user_id','name'])
#     for emp in employess:
#         print(emp.name)
#         if frappe.db.exists('User Permission',{'user':emp.user_id,'allow':'Department','for_value':emp.department}):
#             doc = frappe.get_doc('User Permission',{'user':emp.user_id,'allow':'Department','for_value':emp.department})
#             doc.is_default = 1
#             doc.save(ignore_permissions=True)


# def delete_dept():
#     atts = frappe.get_all('Attendance',{'Department':'TLS Dept'})
#     print(len(atts))
#     for att in atts:
#         ec = frappe.get_all('Employee Checkin',{'attendance':att.name})
#         frappe.delete_doc("Attendance",att.name)
#         # if ec:
#         #     print(ec[0])
#         #     frappe.delete_doc("Employee Checkin",ec[0].name)

# def delete_shift():
#     from_date = '2021-06-26'
#     sa_list = frappe.db.sql("select name from `tabShift Assignment` where start_date = '%s' and docstatus = 1 "%(from_date),as_dict=True)
#     if sa_list:
#         for sa in sa_list:
# @frappe.whitelist()
# def mark_att(from_date,to_date):
#     checkins = frappe.db.sql(
#         """select * from `tabEmployee Checkin` where skip_auto_attendance = 0 and date(time) between '%s' and '%s' """%(from_date,to_date),as_dict=1)
#     if checkins:
#         for c in checkins:
#             att = mark_attendance_from_checkin(c.name,c.employee,c.log_type,c.time)
#             # print(att)
#             if att:
#                 frappe.db.set_value("Employee Checkin",
#                                     c.name, "skip_auto_attendance", "1")
#         frappe.msgprint("Attendance Marked Successfully")
#         return "ok"
#     else:
#         frappe.msgprint("Attendance Already Marked")

# def mark_attendance_from_checkin(checkin,employee,log_type,time):
#     att_time = time.time()
#     att_date = time.date()
#     month_start_date = get_first_day(att_date)
#     month_end_date = get_last_day(att_date)
#     shift = ''
#     if log_type == 'IN':
#         min_in_time = ''
#         max_in_time = ''
#         min_in_time1 = datetime.strptime('06:00', '%H:%M').time()
#         max_in_time1 = datetime.strptime('10:00', '%H:%M').time()
#         min_in_time2 = datetime.strptime('14:30', '%H:%M').time()
#         max_in_time2 = datetime.strptime('18:30', '%H:%M').time()
#         min_in_time3 = datetime.strptime('00:01', '%H:%M').time()
#         max_in_time3 = datetime.strptime('03:00', '%H:%M').time()
#         min_in_timepp1 = datetime.strptime('06:00', '%H:%M').time()
#         max_in_timepp1 = datetime.strptime('10:00', '%H:%M').time()
#         min_in_timepp2 = datetime.strptime('18:00', '%H:%M').time()
#         max_in_timepp2 = datetime.strptime('22:00', '%H:%M').time()
#         late1 = datetime.strptime('08:10', '%H:%M').time()
#         late2 = datetime.strptime('16:40', '%H:%M').time()
#         late3 = datetime.strptime('01:10', '%H:%M').time()
#         latepp1 = datetime.strptime('08:10', '%H:%M').time()
#         latepp2 = datetime.strptime('20:10', '%H:%M').time()
#         late = 0
#         status = 'Present'
#         if max_in_time1 >= att_time >= min_in_time1:
#             if frappe.db.get_value('Employee',employee,"default_shift") == 'PP1':
#                 shift = 'PP1'
#             else:
#                 shift = '1'
#             min_in_time = datetime.strptime('07:00', '%H:%M').time()
#             max_in_time = datetime.strptime('09:00', '%H:%M').time()
#             if datetime.strptime('08:00', '%H:%M').time() <= att_time <= datetime.strptime('08:10', '%H:%M').time():
#                 late = 1
#             elif att_time > datetime.strptime('08:00', '%H:%M').time():
#                 status = 'Half Day'
#         elif max_in_time2 >= att_time >= min_in_time2:
#             shift = '2'
#             min_in_time = datetime.strptime('15:30', '%H:%M').time()
#             max_in_time = datetime.strptime('17:30', '%H:%M').time()
#             if datetime.strptime('16:30', '%H:%M').time() <= att_time <= datetime.strptime('16:40', '%H:%M').time():
#                 late = 1
#             elif att_time > datetime.strptime('16:30', '%H:%M').time():
#                 status = 'Half Day'
#         elif max_in_time3 >= att_time >= min_in_time3:
#             shift = '3'
#             att_date = add_days(att_date,-1)
#             min_in_time = datetime.strptime('00:01', '%H:%M').time()
#             max_in_time = datetime.strptime('02:00', '%H:%M').time()
#             if datetime.strptime('01:00', '%H:%M').time() <= att_time <= datetime.strptime('01:10', '%H:%M').time():
#                 late = 1
#             elif att_time > datetime.strptime('01:00', '%H:%M').time():
#                 status = 'Half Day'
#         elif max_in_timepp2 >= att_time >= min_in_timepp2:
#             shift = 'PP2'
#             min_in_time = datetime.strptime('19:00', '%H:%M').time()
#             max_in_time = datetime.strptime('21:00', '%H:%M').time()
#             if datetime.strptime('20:00', '%H:%M').time() <= att_time <= datetime.strptime('20:10', '%H:%M').time():
#                 late = 1
#             elif att_time > datetime.strptime('20:00', '%H:%M').time():
#                 status = 'Half Day'
#         if late == 1:
#             count = frappe.db.sql("select count(*) as count from `tabAttendance` where employee = '%s' and docstatus != 2 and late_entry =1 and attendance_date between '%s' and '%s' "%(employee,month_start_date,month_end_date),as_dict = True)
#             if count[0].count:
#                 if int(count[0].count) >= 2:
#                     status = 'Half Day'
#         if min_in_time and max_in_time:
#             if not frappe.db.exists("Attendance",{'employee':employee,'attendance_date':att_date,'docstatus': ['!=',2]}):
#                 if shift != '3':
#                     checkins = frappe.db.sql("select name,time from `tabEmployee Checkin` where employee = '%s' and log_type = 'IN' and date(time) = '%s' and time(time) between '%s' and '%s' order by time "%(employee,att_date,min_in_time,max_in_time),as_dict=True)
#                 else:
#                     yesterday = add_days(att_date,1)
#                     checkins = frappe.db.sql("select name,time from `tabEmployee Checkin` where employee = '%s' and log_type = 'IN' and date(time) = '%s' and time(time) between '%s' and '%s' order by time "%(employee,yesterday,min_in_time,max_in_time),as_dict=True)
#                 if checkins:    
#                     qr_checkin = frappe.db.sql("select name, employee,qr_shift,qr_scan_time,shift_date from `tabQR Checkin` where employee = '%s' and date(qr_scan_time) = '%s' order by qr_scan_time "%(employee,att_date),as_dict=True)
#                     att = frappe.new_doc("Attendance")
#                     att.employee = employee
#                     att.attendance_date = att_date
#                     att.shift = shift
#                     att.status = status
#                     att.late_entry = late
#                     att.in_time = checkins[0].time
#                     if qr_checkin:
#                         att.qr_shift = qr_checkin[0].qr_shift
#                         att.qr_scan_time = qr_checkin[0].qr_scan_time
#                     att.save(ignore_permissions=True)
#                     frappe.db.commit()
#                     frappe.db.set_value("Employee Checkin",checkins[0].name, "attendance", att.name)
#                     if qr_checkin:
#                         frappe.db.set_value("QR Checkin",qr_checkin[0].name, "attendance", att.name)
#                     return att
#     if log_type == 'OUT':
#         max_out = datetime.strptime('10:00', '%H:%M').time()
#         if att_time < max_out:
#             yesterday = add_days(att_date,-1)
#             checkins = frappe.db.sql("select name,time from `tabEmployee Checkin` where employee = '%s' and log_type = 'OUT' and date(time) = '%s' and time(time) < '%s' order by time "%(employee,att_date,max_out),as_dict=True)
#             att = frappe.db.exists("Attendance",{'employee':employee,'attendance_date':yesterday})
#             frappe.errprint(att)
#             if att:
#                 att = frappe.get_doc("Attendance",att)
#                 print(att.name)
#                 if not att.out_time:
#                     if att.docstatus == 0:
#                         print(att.out_time)
#                         if len(checkins) > 0:
#                             att.out_time = checkins[-1].time
#                         else:
#                             att.out_time = checkins[0].time
#                         att.save(ignore_permissions=True)
#                         att.submit()
#                         frappe.db.commit()
#                         frappe.db.set_value("Employee Checkin",checkins[0].name, "attendance", att.name)
#                         return att
#             else:
#                 att = frappe.new_doc("Attendance")
#                 att.employee = employee
#                 att.attendance_date = yesterday
#                 # att.shift_type = shift
#                 att.status = 'Absent'
#                 if len(checkins) > 0:
#                     att.out_time = checkins[-1].time
#                 else:
#                     att.out_time = checkins[0].time
#                 att.save(ignore_permissions=True)
#                 frappe.db.commit()
#                 frappe.db.set_value("Employee Checkin",checkins[0].name, "attendance", att.name)
#                 return att
#         else:
#             checkins = frappe.db.sql("select name,time,docstatus from `tabEmployee Checkin` where employee ='%s' and log_type = 'OUT' and date(time) = '%s' order by time "%(employee,att_date),as_dict=True)
#             att = frappe.db.exists("Attendance",{'employee':employee,'attendance_date':att_date})
#             if att:
#                 att = frappe.get_doc("Attendance",att)
#                 if not att.out_time:
#                     if att.docstatus == 0:
#                         if len(checkins) > 0:
#                             att.out_time = checkins[-1].time
#                         else:
#                             att.out_time = checkins[0].time
#                         att.save(ignore_permissions=True)
#                         att.submit()
#                         frappe.db.commit()
#                         frappe.db.set_value("Employee Checkin",checkins[0].name, "attendance", att.name)
#                         return att
#             else:
#                 att = frappe.new_doc("Attendance")
#                 att.employee = employee
#                 att.attendance_date = att_date
#                 # att.shift_type = shift
#                 att.status = 'Absent'
#                 if len(checkins) > 0:
#                     att.out_time = checkins[-1].time
#                 else:
#                     att.out_time = checkins[0].time
#                 att.save(ignore_permissions=True)
#                 frappe.db.commit()
#                 frappe.db.set_value("Employee Checkin",checkins[0].name, "attendance", att.name)
#                 return att


# def mark_attendance_from_checkin(checkin,employee,log_type,time):
#     att_time = time.time()
#     att_date = time.date()
#     if log_type == 'IN':
# new_doc("Attendance")
    #             attendance.update({
    #                 "employee": employee,
    #                 "status": status,
    #                 "attendance_date":log_date,
    #                 "plant":plant,
    #                 "in": att_time,
    #                 "out":"",
    #                 "total_working_hours":"",
    #                 "extra_hours":"",
    #                 "approved_ot_hours":"",
    #                 "shift": shift
    #             })
    #             attendance.save(ignore_permissions=True)
    #             frappe.db.set_value("Employee Checkin",checkin,"attendance",attendance.name)
    #             frappe.db.commit()
    #             return "ok"    
#             doc = frappe.get_doc("Shift Assignment",sa.name)
#             doc.cancel()
#         frappe.msgprint('Shift Schedule Deleted Successfully')
#     else:
#         frappe.msgprint('No Shift Schedule found')

# def bulk_ot():
#     emps = frappe.get_all("Employee",{'employee_type':"WC"},['name','user_id'])
#     for emp in emps:
#         if emp.user_id:
#             user = frappe.get_doc('User',emp.user_id)
#             user.add_roles('Bulk OT')
#             user.save(ignore_permissions=True)

# def method(filename):
#     from frappe.utils.file_manager import get_file
#     filepath = get_file(filename)
#     pps = read_csv_content(filepath[1])
#     for pp in pps:
#         print(pp[0])
#         frappe.delete_doc('QR Checkin',pp[0])

# def method():
#     # doc = frappe.get_doc('Leave Application','HR-LAP-2021-00962')
#     # doc.cancel()
#     frappe.delete_doc('Leave Application','HR-LAP-2021-00962')
#     # frappe.db.set_value('Attendance','HR-ATT-2021-165365','status','Half Day')

def bulk_mail_alerts():
    dept = frappe.get_all('Department',{'is_group':'0'})
    header = """<p>Dear sir, <br> Please find the below list of Application pending for your Approval.</p><table class='table table-bordered'> """
    link = get_url_to_list("Approval")
    view = "<table><tr><th style = 'border: 1px solid black;background-color:#ffedcc;'><center><a href='%s'>View Approval Summary</a></center></th></tr></table><br>"%(link)
    regards = "Thanks & Regards,<br>hrPRO"
    for d in dept:
        hod = frappe.db.get_value('Department',d.name,"hod")
        content = ''
        ots = ''
        miss_punch = ''
        leave_application = ''
        ots = frappe.get_all("Overtime Request",{"department":d.name,"workflow_state":"Pending for HOD"},['employee','employee_name','ot_date','ot_hours']) 
        if ots:
            content += """<table><tr><th style = 'border: 1px solid black;background-color:#ffedcc;' colspan = "5" ><center>Overtime Request</center></th></tr><tr><th style = 'border: 1px solid black'>Department</th><th style = 'border: 1px solid black'>Employee ID</th><th style = 'border: 1px solid black'>Employee Name</th><th style = 'border: 1px solid black'>OT Date</th><th style = 'border: 1px solid black'>OT Hour</th></tr>"""
            for ot in ots:
                content += '<tr><td style = "border: 1px solid black"> %s </td><td style = "border: 1px solid black"> %s </td><td style = "border: 1px solid black"> %s </td> <td style = "border: 1px solid black"> %s </td> <td style = "border: 1px solid black"> %s </td></tr>' %(d['name'],ot['employee'],ot['employee_name'],format_date(ot['ot_date']),ot['ot_hours'])
            content +='</table><br>'

        miss_punch = frappe.get_all("Miss Punch Application",{"department":d.name,"workflow_state":"Pending for HOD"},['employee','employee_name','in_time','out_time','attendance_date'])
        if miss_punch:
            content += """<table class='table table-bordered'><tr><th style = 'border: 1px solid black;background-color:#ffedcc;' colspan = "6"><center>Manual Attendance Correction</center></th></tr><tr><th style = 'border: 1px solid black'>Department</th><th style = 'border: 1px solid black'>Employee ID</th><th style = 'border: 1px solid black'>Employee Name</th><th style = 'border: 1px solid black'>Date</th><th style = 'border: 1px solid black'>IN Time</th><th style = 'border: 1px solid black'>OUT Time</th></tr>"""
            for mp in miss_punch:
                content += '<tr><td style = "border: 1px solid black"> %s </td><td style = "border: 1px solid black"> %s </td><td style = "border: 1px solid black"> %s </td> <td style = "border: 1px solid black"> %s </td><td style = "border: 1px solid black"> %s </td> <td style = "border: 1px solid black"> %s </td></tr>' %(d['name'],mp.employee,mp.employee_name,mp.attendance_date,format_datetime(mp.in_time),format_datetime(mp.out_time))
            content +='</table><br>'

        leave_application = frappe.get_all("Leave Application",{"department":d.name,"workflow_state":"Pending for HOD"},['*'])
        if leave_application:
            content += """<table class='table table-bordered'><tr><th colspan = "8" style = 'border: 1px solid black;background-color:#ffedcc;'><center>Leave Application</center></th></tr><tr><th style = 'border: 1px solid black'>Department</th><th style = 'border: 1px solid black'>Employee ID</th><th style = 'border: 1px solid black'>Employee Name</th><th style = 'border: 1px solid black'>From Date</th><th style = 'border: 1px solid black'>To Date</th><th style = 'border: 1px solid black'>Leave Type</th><th style = 'border: 1px solid black'>Session</th><th style = 'border: 1px solid black'>Reason</th></tr>"""
            for leave in leave_application:
                content += '<tr><td style = "border: 1px solid black"> %s </td><td style = "border: 1px solid black"> %s </td><td style = "border: 1px solid black"> %s </td><td style = "border: 1px solid black"> %s </td> <td style = "border: 1px solid black"> %s </td><td style = "border: 1px solid black"> %s </td> <td style = "border: 1px solid black"> %s </td> <td style = "border: 1px solid black"> %s </td></tr>' %(d['name'],leave.employee,leave.employee_name,format_date(leave.from_date),format_date(leave.to_date),leave.leave_type,leave.session,leave.description)
            content +='</table><br>'
        
        if ots or miss_punch or leave_application:
            print(d.name)
            if hod:
                frappe.sendmail(
                recipients=[hod,"subash.p@groupteampro.com",'mohan.pan@thaisummit.co.in'],
                subject='Reg.List of pending Approvals',
                message = header+content+view+regards)

# @frappe.whitelist()
# def update_approver(dept,hod,gm,ceo,hr_gm):
#     leave_application = frappe.db.get_all("Leave Application",{"department":dept,"docstatus":0},["name",])
#     for lev_app in leave_application:
#         frappe.db.set_value('Leave Application',lev_app.name,'leave_approver',leave_approver)

# @frappe.whitelist()
# def change_permission_approver(employee,permission_approver):
#     permission_request = frappe.db.get_all("Permission Request",{"employee":employee,"docstatus":0},["name"])
#     for per_req in permission_request:
#         frappe.db.set_value('Permission Request',per_req.name,'permission_approver',permission_approver)

# @frappe.whitelist()
# def change_od_approver(employee,od_approver):
#     od_application = frappe.db.get_all("On Duty Application",{"employee":employee,"docstatus":0},["name"])
#     for od_app in od_application:
#         frappe.db.set_value('On Duty Application',od_app.name,'approver',od_approver)