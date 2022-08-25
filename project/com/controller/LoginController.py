from flask import request, render_template, redirect, url_for, session
from project import app
from project.com.dao.LoginDAO import LoginDAO
from project.com.vo.LoginVO import LoginVO
from project.com.vo.UserVO import UserVO

from project.com.vo.BookingVO import BookingVO
from project.com.dao.BookingDAO import BookingDAO

from project.com.vo.VehicleVO import VehicleVO
from project.com.vo.DriverVO import DriverVO
from project.com.dao.DiscountDAO import DiscountDAO

import random

import smtplib
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from sqlalchemy import func

from datetime import datetime



@app.route('/core/loadForgotPassword', methods=['GET'])
def coreLoadForgotPassword():
    try:
        session.clear()
        print("in forgot password")
        return render_template('core/forgotPassword.html')
    except Exception as ex:
        print(ex)


@app.route('/core/generatePassword', methods=['POST'])
def coreGeneratePassword():
    try:
        session.clear()
        loginEmail = request.form['loginEmail']

        loginVO = LoginVO()

        loginDAO = LoginDAO()

        loginVO.loginEmail = loginEmail
        loginVO.loginPassword = ''.join((random.choice(string.ascii_letters + string.digits)) for x in range(8))

        loginVOList = LoginVO.query.filter_by(loginEmail=func.binary(loginVO.loginEmail)).all()

        loginDictList = [i.as_dict() for i in loginVOList]

        print(loginDictList)

        lenLoginDictList = len(loginDictList)

        if lenLoginDictList == 0:

            msg = 'Email address is not registered !'

            return render_template('core/forgotPassword.html', error=msg)

        else:

            for row1 in loginDictList:

                loginVO.loginId = row1['loginId']

                sender = "smarttraveling2021@gmail.com"

                receiver = loginVO.loginEmail

                msg = MIMEMultipart()

                msg['From'] = sender
                msg['To'] = receiver

                msg['Subject'] = "Smart Travelling Login Password"

                msg.attach(MIMEText("Hii, your password for smart_travelling portal is {}".format(loginVO.loginPassword),'plain'))

                server = smtplib.SMTP('smtp.gmail.com', 587)

                server.starttls()

                server.login(sender, "smart2020")

                text = msg.as_string()

                server.sendmail(sender, receiver, text)

                server.quit()

                loginDAO.updateLogin(loginVO)

                msg = 'Password has been sent to your registered email.'

                return render_template('core/forgotPassword.html', error=msg)

    except Exception as ex:
        print(ex)


@app.route('/admin/loadEditPassword', methods=['GET'])
def adminLoadEditPassword():
    try:
        if adminLoginSession() == 'admin':
            return render_template('admin/editPassword.html')
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)

@app.route('/admin/editPassword', methods=['POST'])
def adminEditPassword():
    try:
        if adminLoginSession() == 'admin':
            currentPassword = request.form['currentPassword']
            newPassword = request.form['newPassword']

            loginVO = LoginVO()
            loginDAO = LoginDAO()

            loginList = LoginVO.query.filter_by(loginId=session['session_loginId']).all()
            for login in loginList:
                if login.loginPassword==currentPassword:
                    loginVO.loginId = login.loginId
                    loginVO.loginPassword = newPassword
                    loginDAO.updateLogin(loginVO)
                    msg = 'Your password has been updated.'
                    return render_template('admin/editPassword.html', error=msg)
                else:
                    msg = 'Your current password is incorrect.'
                    return render_template('admin/editPassword.html', error = msg)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)

@app.route('/user/loadEditPassword', methods=['GET'])
def userLoadEditPassword():
    try:
        if adminLoginSession() == 'user':
            return render_template('user/editPassword.html')
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)

@app.route('/user/editPassword', methods=['POST'])
def userEditPassword():
    try:
        if adminLoginSession() == 'user':
            currentPassword = request.form['currentPassword']
            newPassword = request.form['newPassword']

            loginVO = LoginVO()
            loginDAO = LoginDAO()

            loginList = LoginVO.query.filter_by(loginId=session['session_loginId']).all()
            for login in loginList:
                if login.loginPassword==currentPassword:
                    loginVO.loginId = login.loginId
                    loginVO.loginPassword = newPassword
                    loginDAO.updateLogin(loginVO)
                    msg = 'Your password has been updated.'
                    return render_template('user/editPassword.html', error=msg)
                else:
                    msg = 'Your current password is incorrect.'
                    return render_template('user/editPassword.html', error = msg)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/core/loadLogin', methods=['GET'])
def coreLoadLogin():
    try:
        session.clear()
        print("in login")
        return render_template('core/login.html')
    except Exception as ex:
        print(ex)

@app.route('/core/validateLogin', methods=['POST'])
def coreValidateLogin():
    try:
        loginEmail = request.form['loginEmail']
        loginPassword = request.form['loginPassword']

        loginVO = LoginVO()
        loginDAO = LoginDAO()

        loginVO.loginEmail = loginEmail
        loginVO.loginPassword = loginPassword

        loginVOList = loginDAO.validateLogin(loginVO)

        loginDictList = [i.as_dict() for i in loginVOList]

        print(loginDictList)

        lenLoginDictList = len(loginDictList)

        if lenLoginDictList == 0:

            msg = 'Username Or Password is Incorrect !'

            return render_template('core/login.html', error=msg)

        else:

            for row1 in loginDictList:

                loginId = row1['loginId']

                loginEmail = row1['loginEmail']

                loginRole = row1['loginRole']

                print(loginRole)

                session['session_loginId'] = loginId

                session['session_loginEmail'] = loginEmail

                session['session_loginRole'] = loginRole

                session.permanent = True

                if loginRole == 'admin' :

                    session['session_loginName'] = 'Smart Travelling'

                    session['session_loginFileName'] = 'user.jpg'

                    session['session_loginFilePath'] = '../../static/assets/img'

                    return redirect(url_for('adminLoadDashboard'))

                elif loginRole == 'user' :

                    loginName,loginFileName,loginFilePath="","",""
                    userList = UserVO.query.filter_by(user_LoginId=loginId).all()
                    for user in userList:
                        loginName = user.userName
                        loginFileName = user.userFileName
                        loginFilePath = user.userFilePath

                    session['session_loginName'] = loginName

                    session['session_loginFileName'] = loginFileName

                    session['session_loginFilePath'] = loginFilePath

                    return redirect(url_for('userLoadDashboard'))

    except Exception as ex:
        print(ex)


@app.route('/admin/loadDashboard', methods=['GET'])
def adminLoadDashboard():
    try:
        if adminLoginSession() == 'admin':
            userCount = len(UserVO.query.all())
            driverCount = len(DriverVO.query.all())
            vehicleCount = len(VehicleVO.query.all())

            upcomingBookings = len(BookingVO.query.filter_by(bookingStatus="InProcess").all())
            cancelledBookings = len(BookingVO.query.filter_by(bookingStatus="Cancelled").all())
            completedBookings = len(BookingVO.query.filter_by(bookingStatus="Completed").all())
            
            discountDAO = DiscountDAO()
            discountVO = discountDAO.viewDiscount()

            if discountVO:
                discountNewcustomer = discountVO.discountNewcustomer
                discountOldcustomer = discountVO.discountOldcustomer
                discountAllcustomer = discountVO.discountAllcustomer
                discountExpireDateForNewCustomer=discountVO.discountExpireDateForNewCustomer
                discountExpireDateForOldCustomer=discountVO.discountExpireDateForOldCustomer
                discountExpireDateForAllCustomer=discountVO.discountExpireDateForAllCustomer
                if discountExpireDateForNewCustomer>=datetime.now().date():
                    pass
                else:
                    discountNewcustomer=0
                if discountExpireDateForOldCustomer>=datetime.now().date():
                    pass
                else:
                    discountOldcustomer=0
                if discountExpireDateForAllCustomer>=datetime.now().date():
                    pass
                else:
                    discountAllcustomer=0
            else:
                discountNewcustomer=0
                discountOldcustomer=0
                discountAllcustomer=0

            from project.com.controller.MainController import visitors

            return render_template('admin/index.html', upcomingBookings=upcomingBookings, cancelledBookings=cancelledBookings, completedBookings=completedBookings,userCount=userCount, driverCount=driverCount, vehicleCount=vehicleCount, discountNewcustomer=discountNewcustomer, discountOldcustomer=discountOldcustomer, discountAllcustomer=discountAllcustomer, visitors=visitors)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)

@app.route('/user/loadDashboard', methods=['GET'])
def userLoadDashboard():
    try:
        if adminLoginSession() == 'user':
            userList = UserVO.query.filter_by(user_LoginId=session["session_loginId"]).all()
            for user in userList:
                userId = user.userId
            bookingDAO = BookingDAO()
            bookingVOList = bookingDAO.viewUserCompletedBooking(userId)

            vehicleCount = len(BookingVO.query.filter_by(booking_UserId=userId, bookingVehicle="Yes", bookingDriver="No").all())
            driverCount = len(BookingVO.query.filter_by(booking_UserId=userId, bookingVehicle="No", bookingDriver="Yes").all())
            bothCounts = len(BookingVO.query.filter_by(booking_UserId=userId, bookingVehicle="Yes", bookingDriver="Yes").all())

            upcomingBookings = len(BookingVO.query.filter_by(booking_UserId=userId, bookingStatus="InProcess").all())
            cancelledBookings = len(BookingVO.query.filter_by(booking_UserId=userId, bookingStatus="Cancelled").all())
            completedBookings = len(bookingVOList)

            return render_template('user/index.html', bookingVOList=bookingVOList, upcomingBookings=upcomingBookings, cancelledBookings=cancelledBookings, completedBookings=completedBookings, vehicleCount=vehicleCount, driverCount=driverCount, bothCounts=bothCounts)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/loginSession')
def adminLoginSession():
    try:
        if 'session_loginId' and 'session_loginRole' in session:

            if session['session_loginRole'] == 'admin':
                return 'admin'

            elif session['session_loginRole'] == 'user':
                return 'user'

            print("<<<<<<<<<<<<<<<<True>>>>>>>>>>>>>>>>>>>>")

        else:

            print("<<<<<<<<<<<<<<<<False>>>>>>>>>>>>>>>>>>>>")

            return False

    except Exception as ex:
        print(ex)


@app.route("/admin/logoutSession", methods=['GET'])
def adminLogoutSession():
    try:
        session.clear()
        return redirect(url_for('coreLoadLogin'))
    except Exception as ex:
        print(ex)
