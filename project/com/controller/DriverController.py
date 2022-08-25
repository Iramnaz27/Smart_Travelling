from flask import request, render_template, redirect, url_for
from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession, session
from project.com.dao.DriverDAO import DriverDAO
from project.com.vo.DriverVO import DriverVO

from werkzeug.utils import secure_filename
import os
from datetime import datetime

import smtplib
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
UPLOAD_FOLDER3 = 'project/static/assets/driverImage/'

app.config['UPLOAD_FOLDER3'] = UPLOAD_FOLDER3


@app.route('/admin/loadDriver', methods=['GET'])
def adminLoadDriver():
    try:
        if adminLoginSession() == 'admin':
            return render_template('admin/addDriver.html')
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/insertDriver', methods=['POST'])
def adminInsertDriver():
    try:
        if adminLoginSession() == 'admin':
            driverName = request.form['driverName']
            driverEmail = request.form['driverEmail']
            driverMobile = request.form['driverMobile']
            driverAddress = request.form['driverAddress']
            driverGender = request.form['driverGender']
            driverPrice = request.form['driverPrice']
            driverExtraDayPrice = request.form['driverExtraDayPrice']
            driverLicenseNumber = request.form['driverLicenseNumber']
            driverStatus = 'Active'
            driverFlag = 1

            driverVO = DriverVO()
            driverDAO = DriverDAO()

            driverVOList = driverDAO.viewDriver()
            for driver in driverVOList:
                if driver.driverEmail == driverEmail:
                    msg = 'Driver with same email already exists.'
                    return render_template('admin/addDriver.html', error=msg)

            if not secure_filename(request.files['file'].filename).endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                msg = 'Image is not a valid format file'
                return render_template('admin/addDriver.html', error=msg)

            else:
                print("1")

                sender = "smarttraveling2021@gmail.com"
                print("2")

                receiver = driverEmail
                print("3")

                msg = MIMEMultipart()
                print("4")

                msg['From'] = sender
                msg['To'] = receiver

                msg['Subject'] = "Smart Travelling"
                print("5")

                msg.attach(MIMEText("Hii, you have been registered as driver at smart_travelling portal.",'plain'))
                print("6")
                server = smtplib.SMTP('smtp.gmail.com', 587)
                print("7")    
                server.starttls()
                print("8")
                password = 'smart2020'
                print(sender, password)

                server.login(sender, password)
                print("9")
                text = msg.as_string()
                print("10")

                server.sendmail(sender, receiver, text)
                print("11")

                server.quit()
                print("2")

                driverVO.driverName = driverName
                driverVO.driverEmail = driverEmail
                driverVO.driverMobile = driverMobile
                driverVO.driverAddress = driverAddress
                driverVO.driverGender = driverGender
                driverVO.driverPrice = driverPrice
                driverVO.driverExtraDayPrice = driverExtraDayPrice
                driverVO.driverLicenseNumber = driverLicenseNumber
                driverVO.driverStatus = driverStatus
                driverVO.driverFlag = driverFlag

                file = request.files['file']
                print(file)

                driverVO.driverFileName = secure_filename(file.filename)

                print(driverVO.driverFileName)

                driverVO.driverFilePath = os.path.join(app.config['UPLOAD_FOLDER3'])

                file.save(os.path.join(driverVO.driverFilePath, driverVO.driverFileName))

                driverDAO.insertDriver(driverVO)


                os.rename(driverVO.driverFilePath + driverVO.driverFileName,
                          driverVO.driverFilePath + str(driverVO.driverId) +
                          os.path.splitext(driverVO.driverFileName)[-1])

                driverVO.driverFileName = str(driverVO.driverId) + os.path.splitext(driverVO.driverFileName)[-1]

                print(driverVO.driverFileName)

                driverVO.driverFilePath = driverVO.driverFilePath.replace("project", "..")

                driverDAO.updateDriver(driverVO)


                return redirect(url_for('adminViewDriver'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/viewDriver', methods=['GET'])
def adminViewDriver():
    try:
        if adminLoginSession() == 'admin':
            driverDAO = DriverDAO()
            driverVOList = driverDAO.viewDriver()
            print("__________________", driverVOList)
            return render_template('admin/viewDriver.html', driverVOList=driverVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/editDriver', methods=['POST'])
def adminEditDriver():
    try:
        if adminLoginSession() == 'admin':
            driverVO = DriverVO()
            driverDAO = DriverDAO()
            driverId = request.form['driverId']
            driverVO.driverId = driverId
            driverVOList = driverDAO.editDriver(driverVO)
            return render_template('admin/editDriver.html', driverVOList=driverVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/updateDriver', methods=['POST'])
def adminUpdateDriver():
    try:
        if adminLoginSession() == 'admin':

            driverId = request.form['driverId']
            driverName = request.form['driverName']
            driverEmail = request.form['driverEmail']
            driverMobile = request.form['driverMobile']
            driverAddress = request.form['driverAddress']
            driverGender = request.form['driverGender']
            driverPrice = request.form['driverPrice']
            driverExtraDayPrice = request.form['driverExtraDayPrice']
            driverLicenseNumber = request.form['driverLicenseNumber']

            driverVO = DriverVO()
            driverDAO = DriverDAO()

            driverVO.driverId = driverId

            driverVOList = driverDAO.editDriver(driverVO)

            flag=0
            if len(driverMobile)!=10:
                msg = 'Please match the requested format for Employee Mobile.'
                return render_template('admin/editDriver.html', driverVOList=driverVOList, error=msg)
            for i in driverMobile:
                print(i)
                if i not in ['1','2','3','4','5','6','7','8','9','0']:
                    flag=1
                    break
            if flag==1:
                msg = 'Please match the requested format for Employee Mobile.'
                return render_template('admin/editDriver.html', driverVOList=driverVOList, error=msg)

            file = request.files['file']
            print(file)

            driverFileName = secure_filename(file.filename)

            if driverFileName == '':
                driverFileName = driverVOList[0].driverFileName

            if not driverFileName.endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                msg = 'Image is not a valid format file'
                return render_template('admin/editDriver.html', driverVOList=driverVOList, error=msg)

            else:
                driverVO.driverName = driverName
                driverVO.driverEmail = driverEmail
                driverVO.driverMobile = driverMobile
                driverVO.driverAddress = driverAddress
                driverVO.driverGender = driverGender
                driverVO.driverPrice = driverPrice
                driverVO.driverExtraDayPrice = driverExtraDayPrice
                driverVO.driverLicenseNumber = driverLicenseNumber

                if driverFileName != driverVOList[0].driverFileName:
                    driverVO.driverFileName = secure_filename(file.filename)
                    print(driverVO.driverFileName)
                    driverVO.driverFilePath = os.path.join(app.config['UPLOAD_FOLDER3'])
                    os.remove(driverVO.driverFilePath + driverVOList[0].driverFileName)
                    file.save(os.path.join(driverVO.driverFilePath, driverVO.driverFileName))
                    os.rename(driverVO.driverFilePath + driverVO.driverFileName,
                              driverVO.driverFilePath + str(driverVO.driverId) +
                              os.path.splitext(driverVO.driverFileName)[-1])
                    driverVO.driverFileName = str(driverVO.driverId) + os.path.splitext(driverVO.driverFileName)[-1]
                    print(driverVO.driverFileName)
                    driverVO.driverFilePath = driverVO.driverFilePath.replace("project", "..")

                driverDAO.updateDriver(driverVO)

                return redirect(url_for('adminViewDriver'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)

@app.route('/admin/deleteDriver', methods=['POST'])
def adminDeleteDriver():
    try:
        if adminLoginSession() == 'admin':
            driverVO = DriverVO()
            driverDAO = DriverDAO()
            driverId = request.form['driverId']
            driverVO.driverId = driverId
            driver = driverDAO.deleteDriver(driverVO)
            path = driver.driverFilePath.replace("..", "project") + driver.driverFileName
            os.remove(path)
            return redirect(url_for('adminViewDriver'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)

@app.route('/admin/activateDriver', methods=['POST'])
def adminActivateDriver():
    try:
        if adminLoginSession() == 'admin':
            driverId = request.form['driverId']
            driverStatus = 'Active'

            driverVO = DriverVO()
            driverDAO = DriverDAO()

            driverVO.driverId = driverId
            driverVO.driverStatus = driverStatus

            driverDAO.updateDriver(driverVO)

            return redirect(url_for('adminViewDriver'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/blockDriver', methods=['POST'])
def adminBlockDriver():
    try:
        if adminLoginSession() == 'admin':
            driverId = request.form['driverId']
            driverStatus = 'Inactive'

            driverVO = DriverVO()
            driverDAO = DriverDAO()

            driverVO.driverId = driverId
            driverVO.driverStatus = driverStatus

            driverDAO.updateDriver(driverVO)

            return redirect(url_for('adminViewDriver'))

        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)
