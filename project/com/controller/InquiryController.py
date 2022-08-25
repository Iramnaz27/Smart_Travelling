from flask import request, render_template, redirect, url_for
from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession, session
from project.com.controller.MainController import loadContact
from project.com.dao.InquiryDAO import InquiryDAO
from project.com.vo.InquiryVO import InquiryVO

from datetime import datetime

import smtplib
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


@app.route('/core/insertInquiry', methods=['POST'])
def coreInsertInquiry():
    try:
        inquiryEmail = request.form['inquiryEmail']
        inquirySubject = request.form['inquirySubject']
        inquiryMessage = request.form['inquiryMessage']
        
        inquiryVO = InquiryVO()
        inquiryDAO = InquiryDAO()
        
        inquiryVO.inquiryEmail = inquiryEmail
        inquiryVO.inquirySubject = inquirySubject
        inquiryVO.inquiryMessage = inquiryMessage
        inquiryVO.inquiryDate = datetime.now().date()

        inquiryDAO.insertInquiry(inquiryVO)

        return redirect(url_for('loadContact'))
    except Exception as ex:
        print(ex)

@app.route('/admin/viewInquiry', methods=['GET'])
def adminViewInquiry():
    try:
        if adminLoginSession() == 'admin':
            inquiryDAO = InquiryDAO()
            inquiryVOList = inquiryDAO.viewInquiry()
            print("__________________", inquiryVOList)
            return render_template('admin/viewInquiry.html', inquiryVOList=inquiryVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)

@app.route('/admin/loadInquiryReply', methods=['POST'])
def adminLoadInquiryReply():
    try:
        if adminLoginSession() == 'admin':
            inquiryVO = InquiryVO()
            inquiryDAO = InquiryDAO()
            inquiryId = request.form['inquiryId']
            inquiryVO.inquiryId = inquiryId
            inquiryVO = inquiryDAO.viewInquiryById(inquiryVO)
            print("__________________", inquiryVO)
            return render_template('admin/inquiryReply.html', inquiryVO=inquiryVO)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)        

@app.route('/admin/insertInquiryReply', methods=['POST'])
def adminInsertInquiryReply():
    try:
        if adminLoginSession() == 'admin':
            inquiryId = request.form['inquiryId']
            inquiryEmail = request.form['inquiryEmail']
            inquiryReply = request.form['inquiryReply']

            sender = "smarttraveling2021@gmail.com"
            receiver = inquiryEmail
            msg = MIMEMultipart()
            msg['From'] = sender
            msg['To'] = receiver
            msg['Subject'] = request.form['inquirySubject']
            msg.attach(MIMEText("HI,\nThis mail is in response to your inquiry on Smart Travelling Portal.\n\n" + inquiryReply, 'plain'))
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender, "smart2020")
            text = msg.as_string()
            server.sendmail(sender, receiver, text)
            server.quit()

            inquiryVO = InquiryVO()
            inquiryDAO = InquiryDAO()

            inquiryVO.inquiryId = inquiryId
            inquiryVO.inquiryReply = inquiryReply

            inquiryDAO.updateReply(inquiryVO)

            return redirect(url_for('adminViewInquiry'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)

