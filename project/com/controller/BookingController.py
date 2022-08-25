from flask import request, render_template, redirect, url_for
from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession, session
from project.com.dao.BookingDAO import BookingDAO
from project.com.vo.BookingVO import BookingVO

from project.com.dao.DriverDAO import DriverDAO
from project.com.vo.DriverVO import DriverVO

from project.com.dao.VehicleDAO import VehicleDAO
from project.com.vo.VehicleVO import VehicleVO

from project.com.dao.DiscountDAO import DiscountDAO
from project.com.vo.DiscountVO import DiscountVO

from project.com.dao.UserDAO import UserDAO
from project.com.vo.UserVO import UserVO

from datetime import datetime

import smtplib
import string

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

d={}

@app.route('/user/loadBooking', methods=['GET'])
def userLoadBooking():
    try:
        if adminLoginSession() == 'user':
            return render_template('user/addBooking.html')
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)
    
@app.route('/user/confirmBooking', methods=['POST'])
def userConfirmBooking():
    try:
        if adminLoginSession() == 'user':
            bookingStartDate = request.form['bookingStartDate']
            bookingExpectedReturnDate = request.form['bookingExpectedReturnDate']
            bookingVehicle = request.form['bookingVehicle']
            bookingDriver = request.form['bookingDriver']
            bookingDeliverAddress = request.form['bookingDeliverAddress']
            bookingVehicleMinCapacity = request.form['bookingVehicleMinCapacity']

            bookingStartDate = datetime.strptime(bookingStartDate, '%Y-%m-%d')
            bookingExpectedReturnDate = datetime.strptime(bookingExpectedReturnDate, '%Y-%m-%d')

            print(bookingStartDate)
            print(bookingExpectedReturnDate)
            print(bookingVehicle)
            print(bookingDriver)
            print(bookingDeliverAddress)

            
            userList = UserVO.query.filter_by(user_LoginId=session["session_loginId"]).all()
            for user in userList:
                userId = user.userId

            dd={}

            dd["bookingStartDate"]=bookingStartDate
            dd["bookingExpectedReturnDate"]=bookingExpectedReturnDate            
            dd["bookingDeliverAddress"]=bookingDeliverAddress

            bookingList = BookingVO.query.filter_by(booking_UserId=userId,bookingCancelRole="User").all()

            if bookingStartDate>=bookingExpectedReturnDate:
                msg = 'Return Date must be greater than Booking Date'
                return render_template('user/addBooking.html', error=msg)

            if bookingDriver=="Yes" and bookingVehicle=="Yes":
                driverDAO = DriverDAO()
                driverVOList = driverDAO.viewActiveDriver()
                if not driverVOList:
                    msg = 'No Driver Available...\nPlease try again later!'
                    return render_template('user/addBooking.html', error=msg)   
                vehicleDAO = VehicleDAO()
                vehicleVOList = vehicleDAO.viewActiveVehicle(bookingVehicleMinCapacity)
                if not vehicleVOList:
                    msg = 'No Vehicle of your queried Capacity Available...\nPlease try again later!'
                    return render_template('user/addBooking.html', error=msg)
                driverVO=driverVOList[0]
                vehicleVO=vehicleVOList[0]
                discountDAO = DiscountDAO()
                discountVO = discountDAO.viewDiscount()
                userVOList = UserVO.query.filter_by(user_LoginId=session["session_loginId"]).all()
                userVO = userVOList[0]
                print(1)
                if discountVO:
                    if userVO.userDiscountStatus:
                        #userVO.userDiscountStatus=0
                        #userDAO = UserDAO()
                        #userDAO.updateUser(userVO)
                        print(2)
                        discountNewcustomer = discountVO.discountNewcustomer if discountVO.discountExpireDateForNewCustomer >= datetime.now().date() else 0
                        discountAllcustomer = discountVO.discountAllcustomer if discountVO.discountExpireDateForAllCustomer >= datetime.now().date() else 0
                        discount = max(discountNewcustomer, discountAllcustomer)
                    else:
                        print(3)
                        discountOldcustomer = discountVO.discountOldcustomer if discountVO.discountExpireDateForOldCustomer >= datetime.now().date() else 0
                        discountAllcustomer = discountVO.discountAllcustomer if discountVO.discountExpireDateForAllCustomer >= datetime.now().date() else 0
                        discount = max(discountOldcustomer, discountAllcustomer)
                else:
                    discount = 0
                print(4)
                extraCharges=vehicleVO.vehiclePriceperkm
                print(5)
                print(bookingExpectedReturnDate.toordinal()-bookingStartDate.toordinal())
                if len(bookingList)>=6:
                    discount = 0
                estimatedCharges= (1 - (discount//100))*((vehicleVO.vehiclePrice + driverVO.driverPrice)*(bookingExpectedReturnDate.toordinal()-bookingStartDate.toordinal()))
                print(6)
                dd["bookingDiscount"]=discount
                d[userId]=dd
                return render_template('user/confirmBooking.html', vehicleVO=vehicleVO, driverVO=driverVO, estimatedCharges=estimatedCharges, extraCharges=extraCharges, discount=discount)

            elif bookingDriver=="Yes":
                driverDAO = DriverDAO()
                driverVOList = driverDAO.viewActiveDriver()
                if not driverVOList:
                    msg = 'No Driver Available...\nPlease try again later!'
                    return render_template('user/addBooking.html', error=msg)   
                driverVO=driverVOList[0]
                discountDAO = DiscountDAO()
                discountVO = discountDAO.viewDiscount()
                userVOList = UserVO.query.filter_by(user_LoginId=session["session_loginId"]).all()
                userVO = userVOList[0]
                print(1)
                if discountVO:
                    if userVO.userDiscountStatus:
                        #userVO.userDiscountStatus=0
                        #userDAO = UserDAO()
                        #userDAO.updateUser(userVO)
                        print(2)
                        discountNewcustomer = discountVO.discountNewcustomer if discountVO.discountExpireDateForNewCustomer >= datetime.now().date() else 0
                        discountAllcustomer = discountVO.discountAllcustomer if discountVO.discountExpireDateForAllCustomer >= datetime.now().date() else 0
                        discount = max(discountNewcustomer, discountAllcustomer)
                    else:
                        print(3)
                        discountOldcustomer = discountVO.discountOldcustomer if discountVO.discountExpireDateForOldCustomer >= datetime.now().date() else 0
                        discountAllcustomer = discountVO.discountAllcustomer if discountVO.discountExpireDateForAllCustomer >= datetime.now().date() else 0
                        discount = max(discountOldcustomer, discountAllcustomer)
                else:
                    discount = 0
                print(4)
                print(5)
                print(bookingExpectedReturnDate.toordinal()-bookingStartDate.toordinal())
                if len(bookingList)>=6:
                    discount = 0
                estimatedCharges= (1 - (discount//100))*((driverVO.driverPrice)*(bookingExpectedReturnDate.toordinal()-bookingStartDate.toordinal()))
                print(6)
                dd["bookingDiscount"]=discount
                d[userId]=dd
                return render_template('user/confirmBooking.html',driverVO=driverVO, estimatedCharges=estimatedCharges, discount=discount)

            elif bookingVehicle=="Yes":
                vehicleDAO = VehicleDAO()
                vehicleVOList = vehicleDAO.viewActiveVehicle(bookingVehicleMinCapacity)
                if not vehicleVOList:
                    msg = 'No Vehicle of your queried Capacity Available...\nPlease try again later!'
                    return render_template('user/addBooking.html', error=msg)
                vehicleVO=vehicleVOList[0]
                discountDAO = DiscountDAO()
                discountVO = discountDAO.viewDiscount()
                userVOList = UserVO.query.filter_by(user_LoginId=session["session_loginId"]).all()
                userVO = userVOList[0]
                print(1)
                if discountVO:
                    if userVO.userDiscountStatus:
                        #userVO.userDiscountStatus=0
                        #userDAO = UserDAO()
                        #userDAO.updateUser(userVO)
                        print(2)
                        discountNewcustomer = discountVO.discountNewcustomer if discountVO.discountExpireDateForNewCustomer >= datetime.now().date() else 0
                        discountAllcustomer = discountVO.discountAllcustomer if discountVO.discountExpireDateForAllCustomer >= datetime.now().date() else 0
                        discount = max(discountNewcustomer, discountAllcustomer)
                    else:
                        print(3)
                        discountOldcustomer = discountVO.discountOldcustomer if discountVO.discountExpireDateForOldCustomer >= datetime.now().date() else 0
                        discountAllcustomer = discountVO.discountAllcustomer if discountVO.discountExpireDateForAllCustomer >= datetime.now().date() else 0
                        discount = max(discountOldcustomer, discountAllcustomer)
                else:
                    discount = 0
                print(4)
                extraCharges=vehicleVO.vehiclePriceperkm
                print(5)
                print(bookingExpectedReturnDate.toordinal()-bookingStartDate.toordinal())
                if len(bookingList)>=6:
                    discount = 0
                estimatedCharges= (1 - (discount//100))*((vehicleVO.vehiclePrice)*(bookingExpectedReturnDate.toordinal()-bookingStartDate.toordinal()))
                print(6)
                dd["bookingDiscount"]=discount
                d[userId]=dd
                return render_template('user/confirmBooking.html',vehicleVO=vehicleVO, estimatedCharges=estimatedCharges, extraCharges=extraCharges, discount=discount)

            else:
                msg = 'Either Vehicle or Driver should be Rented'
                return render_template('user/addBooking.html', error=msg)

        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)

@app.route('/user/insertBooking', methods=['POST'])
def userInsertBooking():
    try:
        if adminLoginSession() == 'user':
            print(request.form)

            print(d)

            userList = UserVO.query.filter_by(user_LoginId=session["session_loginId"]).all()
            for user in userList:
                userVo = user
                userId = user.userId

            bookingVO = BookingVO()
            bookingDAO = BookingDAO()

            if request.form["typee"]=="reject":
                return redirect(url_for('userViewBooking')) 

            bookingVO.bookingStartDate = d[userId]["bookingStartDate"]
            bookingVO.bookingExpectedReturnDate = d[userId]["bookingExpectedReturnDate"]
            bookingVO.bookingDeliverAddress = d[userId]["bookingDeliverAddress"]
            bookingVO.bookingDiscount = d[userId]["bookingDiscount"]
            bookingVO.booking_UserId = userId

            if "driverId" in request.form:
                bookingVO.booking_DriverId = request.form["driverId"]
                bookingVO.bookingDriver = "Yes"

                driverVO = DriverVO.query.get(bookingVO.booking_DriverId)
                driverDAO=DriverDAO()
                if driverVO.driverStatus == "Occupied":
                    msg = 'Try Again ...'
                    return render_template('user/addBooking.html', error=msg)
                driverVO.driverStatus = "Occupied"

                sender = "smarttraveling2021@gmail.com"

                receiver = driverVO.driverEmail

                msg = MIMEMultipart()

                msg['From'] = sender
                msg['To'] = receiver

                msg['Subject'] = "Smart Travelling Confirmed Booking"

                if "vehicleId" in request.form:
                    msg.attach(MIMEText("Hii, you have a confirmed booking from "+str(bookingVO.bookingStartDate)+" to "+str(bookingVO.bookingExpectedReturnDate) +".      Address: "+bookingVO.bookingDeliverAddress+".     Contact:"+userVo.userMobile+".            You need to take a Vehicle from Company's premise.",'plain'))
                else:
                    msg.attach(MIMEText("Hii, you have a confirmed booking from "+str(bookingVO.bookingStartDate)+" to "+str(bookingVO.bookingExpectedReturnDate) +".      Address: "+bookingVO.bookingDeliverAddress+".     Contact:"+userVo.userMobile+".            Please reach there by yourself.",'plain'))

                server = smtplib.SMTP('smtp.gmail.com', 587)

                server.starttls()

                server.login(sender, "smart2020")

                text = msg.as_string()

                server.sendmail(sender, receiver, text)

                server.quit()

                driverVO.driverFlag =0

                driverDAO.updateDriver(driverVO)

            else:
                bookingVO.bookingDriver = "No"
                
            if "vehicleId" in request.form:
                bookingVO.booking_VehicleId = request.form["vehicleId"]
                bookingVO.bookingVehicle = "Yes"
                vehicleVO = VehicleVO.query.get(bookingVO.booking_VehicleId)
                bookingVO.bookingVehicleStartKm = vehicleVO.vehicleCurrentkm

                vehicleDAO = VehicleDAO()
                if vehicleVO.vehicleStatus == "Occupied":
                    msg = 'Try Again ...'
                    return render_template('user/addBooking.html', error=msg)
                vehicleVO.vehicleStatus="Occupied"
                vehicleVO.vehicleFlag=0
                vehicleDAO.updateVehicle(vehicleVO)

            else:
                bookingVO.bookingVehicle = "No"

            bookingVO.bookingStatus = "InProcess"

            userVo.userDiscountStatus=0
            userDAO = UserDAO()
            userDAO.updateUser(userVo)

            bookingDAO.insertBooking(bookingVO)

            return redirect(url_for('userViewBooking'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)

@app.route('/user/viewBooking', methods=['GET'])
def userViewBooking():
    try:
        if adminLoginSession() == 'user':
            userList = UserVO.query.filter_by(user_LoginId=session["session_loginId"]).all()
            for user in userList:
                userId = user.userId
            bookingDAO = BookingDAO()
            bookingVOList = bookingDAO.viewUserBooking(userId)
            for bookingVO in bookingVOList:
                if bookingVO.bookingDriver=="Yes":
                    driverVO = DriverVO.query.get(bookingVO.booking_DriverId)
                    bookingVO.driverName = driverVO.driverName
                    bookingVO.driverMobile = driverVO.driverMobile
                if bookingVO.bookingVehicle == "Yes":
                    vehicleVO = VehicleVO.query.get(bookingVO.booking_VehicleId)
                    bookingVO.vehicleType = vehicleVO.vehicleType
                    bookingVO.vehicleNumberplate = vehicleVO.vehicleNumberplate
            print("__________________", bookingVOList)
            return render_template('user/viewBooking.html', bookingVOList=bookingVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)

@app.route('/admin/viewBooking', methods=['GET'])
def adminViewBooking():
    try:
        if adminLoginSession() == 'admin':
            bookingDAO = BookingDAO()
            bookingVOList = bookingDAO.viewBooking()
            for bookingVO in bookingVOList:
                if bookingVO.bookingDriver=="Yes":
                    driverVO = DriverVO.query.get(bookingVO.booking_DriverId)
                    bookingVO.driverName = driverVO.driverName
                    bookingVO.driverMobile = driverVO.driverMobile
                if bookingVO.bookingVehicle == "Yes":
                    vehicleVO = VehicleVO.query.get(bookingVO.booking_VehicleId)
                    bookingVO.vehicleType = vehicleVO.vehicleType
                    bookingVO.vehicleNumberplate = vehicleVO.vehicleNumberplate
            print("__________________", bookingVOList)
            return render_template('admin/viewBooking.html', bookingVOList=bookingVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)

@app.route('/user/cancelBooking', methods=['POST'])
def userCancelBooking():
    try:
        if adminLoginSession() == 'user':
            bookingId = request.form["bookingId"]
            
            bookingVO = BookingVO.query.get(bookingId)

            if bookingVO.bookingStartDate<=datetime.now().date():
                msg = 'Cannot be Cancelled on/after Booking Date'
                bookingDAO = BookingDAO()
                bookingVOList = bookingDAO.viewUserBooking(bookingVO.booking_UserId)
                for bookingVO in bookingVOList:
                    if bookingVO.bookingDriver=="Yes":
                        driverVO = DriverVO.query.get(bookingVO.booking_DriverId)
                        bookingVO.driverName = driverVO.driverName
                        bookingVO.driverMobile = driverVO.driverMobile
                    if bookingVO.bookingVehicle == "Yes":
                        vehicleVO = VehicleVO.query.get(bookingVO.booking_VehicleId)
                        bookingVO.vehicleType = vehicleVO.vehicleType
                        bookingVO.vehicleNumberplate = vehicleVO.vehicleNumberplate
                print("__________________", bookingVOList)
                return render_template('user/viewBooking.html',bookingVOList=bookingVOList, error=msg)

            if bookingVO.bookingVehicle=="Yes":
                vehicleVO = VehicleVO.query.get(bookingVO.booking_VehicleId)
                vehicleDAO = VehicleDAO()
                vehicleVO.vehicleStatus="Active"
                vehicleDAO.updateVehicle(vehicleVO)     

            if  bookingVO.bookingDriver == "Yes":
                driverVO = DriverVO.query.get(bookingVO.booking_DriverId)
                driverDAO=DriverDAO()
                driverVO.driverStatus = "Active"
                driverDAO.updateDriver(driverVO)

                sender = "smarttraveling2021@gmail.com"

                receiver = driverVO.driverEmail

                msg = MIMEMultipart()

                msg['From'] = sender
                msg['To'] = receiver

                msg['Subject'] = "Smart Travelling Cancelled Booking"

                msg.attach(MIMEText("Hii, you have a cancelled booking from "+str(bookingVO.bookingStartDate)+" to "+str(bookingVO.bookingExpectedReturnDate) +".",'plain'))

                server = smtplib.SMTP('smtp.gmail.com', 587)

                server.starttls()

                server.login(sender, "smart2020")

                text = msg.as_string()

                server.sendmail(sender, receiver, text)

                server.quit()           

            bookingVO.bookingCancelRole = "User"
            bookingVO.bookingStatus = "Cancelled"

            bookingDAO = BookingDAO()
            bookingDAO.updateBooking(bookingVO)

            return redirect(url_for('userViewBooking'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)

@app.route('/admin/cancelBooking', methods=['POST'])
def adminCancelBooking():
    try:
        if adminLoginSession() == 'admin':
            bookingId = request.form["bookingId"]
            
            bookingVO = BookingVO.query.get(bookingId)

            if bookingVO.bookingStartDate<=datetime.now().date():
                msg = 'Cannot be Cancelled on/after Booking Date'
                bookingDAO = BookingDAO()
                bookingVOList = bookingDAO.viewBooking()
                for bookingVO in bookingVOList:
                    if bookingVO.bookingDriver=="Yes":
                        driverVO = DriverVO.query.get(bookingVO.booking_DriverId)
                        bookingVO.driverName = driverVO.driverName
                        bookingVO.driverMobile = driverVO.driverMobile
                    if bookingVO.bookingVehicle == "Yes":
                        vehicleVO = VehicleVO.query.get(bookingVO.booking_VehicleId)
                        bookingVO.vehicleType = vehicleVO.vehicleType
                        bookingVO.vehicleNumberplate = vehicleVO.vehicleNumberplate
                print("__________________", bookingVOList)
                return render_template('admin/viewBooking.html',bookingVOList=bookingVOList, error=msg)

            if bookingVO.bookingVehicle=="Yes":
                vehicleVO = VehicleVO.query.get(bookingVO.booking_VehicleId)
                vehicleDAO = VehicleDAO()
                vehicleVO.vehicleStatus="Active"
                vehicleDAO.updateVehicle(vehicleVO)     

            if  bookingVO.bookingDriver == "Yes":
                driverVO = DriverVO.query.get(bookingVO.booking_DriverId)
                driverDAO=DriverDAO()
                driverVO.driverStatus = "Active"
                driverDAO.updateDriver(driverVO)     

                sender = "smarttraveling2021@gmail.com"

                receiver = driverVO.driverEmail

                msg = MIMEMultipart()

                msg['From'] = sender
                msg['To'] = receiver

                msg['Subject'] = "Smart Travelling Cancelled Booking"

                msg.attach(MIMEText("Hii, you have a cancelled booking from "+str(bookingVO.bookingStartDate)+" to "+str(bookingVO.bookingExpectedReturnDate) +".",'plain'))

                server = smtplib.SMTP('smtp.gmail.com', 587)

                server.starttls()

                server.login(sender, "smart2020")

                text = msg.as_string()

                server.sendmail(sender, receiver, text)

                server.quit()      

            bookingVO.bookingCancelRole = "Admin"
            bookingVO.bookingStatus = "Cancelled"

            bookingDAO = BookingDAO()
            bookingDAO.updateBooking(bookingVO)

            sender = "smarttraveling2021@gmail.com"

            userVO = UserVO.query.get(bookingVO.booking_UserId)

            receiver = userVO.userEmail

            msg = MIMEMultipart()

            msg['From'] = sender
            msg['To'] = receiver

            msg['Subject'] = "Smart Travelling Cancelled Booking"

            msg.attach(MIMEText("Hii, you have a cancelled booking from "+str(bookingVO.bookingStartDate)+" to "+str(bookingVO.bookingExpectedReturnDate) +".",'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)

            server.starttls()

            server.login(sender, "smart2020")

            text = msg.as_string()

            server.sendmail(sender, receiver, text)

            server.quit()

            return redirect(url_for('adminViewBooking'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)

@app.route('/admin/closeBooking', methods=['POST'])
def adminCloseBooking():
    try:
        if adminLoginSession() == 'admin':
            bookingId = request.form["bookingId"]
            bookingReturnDate = request.form["bookingReturnDate"]
            
            bookingReturnDate = datetime.strptime(bookingReturnDate, '%Y-%m-%d')
            bookingReturnDate = datetime.date(bookingReturnDate)

            print(bookingReturnDate)

            if "bookingVehicleEndKm" in request.form:
                bookingVehicleEndKm = request.form["bookingVehicleEndKm"]

            bookingVO = BookingVO.query.get(bookingId)

            if bookingVO.bookingStartDate>datetime.now().date():
                msg = 'Cannot be Closed before Booking Date, you may cancel the booking.'
                bookingDAO = BookingDAO()
                bookingVOList = bookingDAO.viewUserBooking(bookingVO.booking_UserId)
                for bookingVO in bookingVOList:
                    if bookingVO.bookingDriver=="Yes":
                        driverVO = DriverVO.query.get(bookingVO.booking_DriverId)
                        bookingVO.driverName = driverVO.driverName
                        bookingVO.driverMobile = driverVO.driverMobile
                    if bookingVO.bookingVehicle == "Yes":
                        vehicleVO = VehicleVO.query.get(bookingVO.booking_VehicleId)
                        bookingVO.vehicleType = vehicleVO.vehicleType
                        bookingVO.vehicleNumberplate = vehicleVO.vehicleNumberplate
                print("__________________", bookingVOList)
                return render_template('admin/viewBooking.html',bookingVOList=bookingVOList, error=msg)

            
            if bookingVO.bookingDriver=="Yes" and bookingVO.bookingVehicle=="Yes":
                driverVO = DriverVO.query.get(bookingVO.booking_DriverId)
                vehicleVO = VehicleVO.query.get(bookingVO.booking_VehicleId)
                discount = bookingVO.bookingDiscount
                print(0)
                extraCharges=vehicleVO.vehiclePriceperkm * (int(bookingVehicleEndKm)-int(vehicleVO.vehicleCurrentkm))
                print(1)
                if bookingReturnDate<=bookingVO.bookingExpectedReturnDate:
                    estimatedCharges= (1 - (discount/100))*((vehicleVO.vehiclePrice + driverVO.driverPrice)*(bookingVO.bookingExpectedReturnDate.toordinal()-bookingVO.bookingStartDate.toordinal()))
                else:
                    if bookingReturnDate>datetime.now().date():
                        msg = 'Return Date cannot be more than Todays Date'
                        bookingDAO = BookingDAO()
                        bookingVOList = bookingDAO.viewUserBooking(bookingVO.booking_UserId)
                        for bookingVO in bookingVOList:
                            if bookingVO.bookingDriver=="Yes":
                                driverVO = DriverVO.query.get(bookingVO.booking_DriverId)
                                bookingVO.driverName = driverVO.driverName
                                bookingVO.driverMobile = driverVO.driverMobile
                            if bookingVO.bookingVehicle == "Yes":
                                vehicleVO = VehicleVO.query.get(bookingVO.booking_VehicleId)
                                bookingVO.vehicleType = vehicleVO.vehicleType
                                bookingVO.vehicleNumberplate = vehicleVO.vehicleNumberplate
                        print("__________________", bookingVOList)
                        return render_template('admin/viewBooking.html',bookingVOList=bookingVOList, error=msg)
                    estimatedCharges= (1 - (discount/100))*((vehicleVO.vehiclePrice + driverVO.driverPrice)*(bookingVO.bookingExpectedReturnDate.toordinal()-bookingVO.bookingStartDate.toordinal()))
                    estimatedCharges+= (vehicleVO.vehiclePrice + vehicleVO.vehicleExtraDayPrice) * (bookingReturnDate.toordinal()-bookingVO.bookingExpectedReturnDate.toordinal())
                    estimatedCharges+= (driverVO.driverPrice + driverVO.driverExtraDayPrice) * (bookingReturnDate.toordinal()-bookingVO.bookingExpectedReturnDate.toordinal())
                print(6)

            elif bookingVO.bookingDriver=="Yes":
                driverVO = DriverVO.query.get(bookingVO.booking_DriverId)
                vehicleVO = VehicleVO.query.get(bookingVO.booking_VehicleId)
                discount = bookingVO.bookingDiscount
                extraCharges = 0
                if bookingReturnDate<=bookingVO.bookingExpectedReturnDate:
                    estimatedCharges= (1 - (discount/100))*((driverVO.driverPrice)*(bookingVO.bookingExpectedReturnDate.toordinal()-bookingVO.bookingStartDate.toordinal()))
                else:
                    if bookingReturnDate>datetime.now().date():
                        msg = 'Return Date cannot be more than Todays Date'
                        bookingDAO = BookingDAO()
                        bookingVOList = bookingDAO.viewUserBooking(bookingVO.booking_UserId)
                        for bookingVO in bookingVOList:
                            if bookingVO.bookingDriver=="Yes":
                                driverVO = DriverVO.query.get(bookingVO.booking_DriverId)
                                bookingVO.driverName = driverVO.driverName
                                bookingVO.driverMobile = driverVO.driverMobile
                            if bookingVO.bookingVehicle == "Yes":
                                vehicleVO = VehicleVO.query.get(bookingVO.booking_VehicleId)
                                bookingVO.vehicleType = vehicleVO.vehicleType
                                bookingVO.vehicleNumberplate = vehicleVO.vehicleNumberplate
                        print("__________________", bookingVOList)
                        return render_template('admin/viewBooking.html',bookingVOList=bookingVOList, error=msg)
                    estimatedCharges= (1 - (discount/100))*((driverVO.driverPrice)*(bookingVO.bookingExpectedReturnDate.toordinal()-bookingVO.bookingStartDate.toordinal()))
                    estimatedCharges+= (driverVO.driverPrice + driverVO.driverExtraDayPrice) * (bookingReturnDate.toordinal()-bookingVO.bookingExpectedReturnDate.toordinal())
                print(6)

            elif bookingVO.bookingVehicle=="Yes":
                vehicleVO = VehicleVO.query.get(bookingVO.booking_VehicleId)
                discount = bookingVO.bookingDiscount
                print(0)
                extraCharges=vehicleVO.vehiclePriceperkm * (int(bookingVehicleEndKm)-int(vehicleVO.vehicleCurrentkm))
                print(1)
                if bookingReturnDate<=bookingVO.bookingExpectedReturnDate:
                    print(2)
                    estimatedCharges= (1 - (discount/100))*((vehicleVO.vehiclePrice)*(bookingVO.bookingExpectedReturnDate.toordinal()-bookingVO.bookingStartDate.toordinal()))
                else:
                    if bookingReturnDate>datetime.now().date():
                        msg = 'Return Date cannot be more than Todays Date'
                        bookingDAO = BookingDAO()
                        bookingVOList = bookingDAO.viewUserBooking(bookingVO.booking_UserId)
                        for bookingVO in bookingVOList:
                            if bookingVO.bookingDriver=="Yes":
                                driverVO = DriverVO.query.get(bookingVO.booking_DriverId)
                                bookingVO.driverName = driverVO.driverName
                                bookingVO.driverMobile = driverVO.driverMobile
                            if bookingVO.bookingVehicle == "Yes":
                                vehicleVO = VehicleVO.query.get(bookingVO.booking_VehicleId)
                                bookingVO.vehicleType = vehicleVO.vehicleType
                                bookingVO.vehicleNumberplate = vehicleVO.vehicleNumberplate
                        print("__________________", bookingVOList)
                        return render_template('admin/viewBooking.html',bookingVOList=bookingVOList, error=msg)
                    estimatedCharges= (1 - (discount/100))*((vehicleVO.vehiclePrice)*(bookingVO.bookingExpectedReturnDate.toordinal()-bookingVO.bookingStartDate.toordinal()))
                    estimatedCharges+= (vehicleVO.vehiclePrice + vehicleVO.vehicleExtraDayPrice) * (bookingReturnDate.toordinal()-bookingVO.bookingExpectedReturnDate.toordinal())
                print(6)


            if bookingVO.bookingVehicle=="Yes":
                vehicleVO = VehicleVO.query.get(bookingVO.booking_VehicleId)
                vehicleDAO = VehicleDAO()
                vehicleVO.vehicleStatus="Active"
                vehicleVO.vehicleCurrentkm = bookingVehicleEndKm
                bookingVO.bookingVehicleEndKm = bookingVehicleEndKm
                vehicleDAO.updateVehicle(vehicleVO)     

            if  bookingVO.bookingDriver == "Yes":
                driverVO = DriverVO.query.get(bookingVO.booking_DriverId)
                driverDAO=DriverDAO()
                driverVO.driverStatus = "Active"
                driverDAO.updateDriver(driverVO)     

                sender = "smarttraveling2021@gmail.com"

                receiver = driverVO.driverEmail

                msg = MIMEMultipart()

                msg['From'] = sender
                msg['To'] = receiver

                msg['Subject'] = "Smart Travelling Booking Completed"

                msg.attach(MIMEText("Hii, Thanks for completing booking from "+str(bookingVO.bookingStartDate)+" to "+str(bookingVO.bookingReturnDate) +".",'plain'))

                server = smtplib.SMTP('smtp.gmail.com', 587)

                server.starttls()

                server.login(sender, "smart2020")

                text = msg.as_string()

                server.sendmail(sender, receiver, text)

                server.quit()      

            bookingVO.bookingStatus = "Completed"
            bookingVO.bookingReturnDate = bookingReturnDate
            bookingVO.bookingAmount = estimatedCharges + extraCharges

            bookingDAO = BookingDAO()
            bookingDAO.updateBooking(bookingVO)
            print(11)
            sender = "smarttraveling2021@gmail.com"

            userVO = UserVO.query.get(bookingVO.booking_UserId)

            receiver = userVO.userEmail

            msg = MIMEMultipart()

            msg['From'] = sender
            msg['To'] = receiver

            msg['Subject'] = "Smart Travelling Booking Completed"

            msg.attach(MIMEText("Hii, Thanks for completing booking from "+str(bookingVO.bookingStartDate)+" to "+str(bookingVO.bookingReturnDate) +".         Your Charges are :             Total Rent:"+str(estimatedCharges)+"           Per Km Rent:"+str(extraCharges)+"      Charges calculated as per Expected Return Date "+str(bookingVO.bookingExpectedReturnDate),'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)

            server.starttls()

            server.login(sender, "smart2020")

            text = msg.as_string()

            server.sendmail(sender, receiver, text)

            server.quit()

            return redirect(url_for('adminViewBooking'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)

@app.route('/admin/loadCloseBooking', methods=['POST'])
def adminLoadCloseBooking():
    try:
        if adminLoginSession() == 'admin':
            bookingId = request.form["bookingId"]
            bookingVO = BookingVO.query.get(bookingId)
            return render_template('admin/closeBooking.html',bookingVO = bookingVO)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)
