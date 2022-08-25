from flask import request, render_template, redirect, url_for
from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession, session
from project.com.dao.DiscountDAO import DiscountDAO
from project.com.vo.DiscountVO import DiscountVO

@app.route('/admin/viewDiscount', methods=['GET'])
def adminViewDiscount():
    try:
        if adminLoginSession() == 'admin':    
            discountDAO = DiscountDAO()
            discountVO = discountDAO.viewDiscount()
            print("__________________", discountVO)
            return render_template('admin/editDiscount.html', discountVO=discountVO)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)

@app.route('/admin/updateDiscount', methods=['POST'])
def adminUpdateDiscount():
    try:
        if adminLoginSession() == 'admin':    
            discountDAO = DiscountDAO()
            discountVO = DiscountVO()
            discountVO.discountNewcustomer= request.form['discountNewcustomer']
            discountVO.discountOldcustomer= request.form['discountOldcustomer']
            discountVO.discountAllcustomer= request.form['discountAllcustomer']
            discountVO.discountExpireDateForNewCustomer= request.form['discountExpireDateForNewCustomer']
            discountVO.discountExpireDateForOldCustomer= request.form['discountExpireDateForOldCustomer']
            discountVO.discountExpireDateForAllCustomer= request.form['discountExpireDateForAllCustomer']
            discountVO.discountId=1
            discountDAO.updateDiscount(discountVO)
            return redirect(url_for('adminViewDiscount'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)




