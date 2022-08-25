from datetime import datetime

from flask import render_template, request, url_for, redirect

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession, session
from project.com.vo.UserVO import UserVO
from project.com.dao.ComplaintDAO import ComplaintDAO
from project.com.vo.ComplaintVO import ComplaintVO


@app.route('/admin/viewComplaint', methods=['GET'])
def adminViewComplaint():
    try:
        if adminLoginSession() == 'admin':
            complaintVO = ComplaintVO()
            complaintDAO = ComplaintDAO()
            complaintVO.complaintTo_LoginId = session['session_loginId']
            complaintVOList = complaintDAO.adminViewComplaint(complaintVO)
            return render_template('admin/viewComplaint.html', complaintVOList=complaintVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)

@app.route('/admin/editComplaint', methods=['POST'])
def adminEditComplaint():
    try:
        if adminLoginSession() == 'admin':
            complaintVO = ComplaintVO()
            complaintDAO = ComplaintDAO()

            complaintVO.complaintId=request.form['complaintId']

            complaintVOList = complaintDAO.editComplaint(complaintVO)

            return render_template('admin/editComplaint.html', complaintVOList=complaintVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)

@app.route('/admin/updateComplaint', methods=['POST'])
def adminUpdateComplaint():
    try:
        if adminLoginSession() == 'admin':
            complaintVO = ComplaintVO()
            complaintDAO = ComplaintDAO()
            print('1')
            complaintVO.complaintId = request.form['complaintId']
            print('2')
            complaintVO.complaintReply = request.form['complaintReply']
            print('3')
            complaintDAO.updateComplaint(complaintVO)
            return redirect(url_for('adminViewComplaint'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)

@app.route('/user/complaint', methods=['GET'])
def userComplaint():
    try:
        if adminLoginSession() == 'user':
            complaintVO = ComplaintVO()
            complaintDAO = ComplaintDAO()

            complaintFrom_LoginId = session['session_loginId']
            complaintVO.complaintFrom_LoginId = complaintFrom_LoginId

            complaintVOList = complaintDAO.viewComplaint(complaintVO)
            print("______________", complaintVOList)

            return render_template("user/postComplaint.html", complaintVOList=complaintVOList)
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)

@app.route('/user/loadComplaint', methods=['GET'])
def userLoadComplaint():
    try:
        if adminLoginSession() == 'user':
            return render_template("user/addComplaint.html")
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/insertComplaint', methods=['POST'])
def userInsertComplaint():
    try:
        if adminLoginSession() == 'user':
            complaintSubject = request.form['complaintSubject']
            complaintDescription = request.form['complaintDescription']
            complaintReply = ''
            complaintDate = datetime.now().date()
            complaintTime = datetime.now().time()
            complaintFrom_LoginId = session['session_loginId']

            complaintVO = ComplaintVO()
            complaintDAO = ComplaintDAO()

            complaintVO.complaintTo_LoginId = 1

            complaintVO.complaintSubject = complaintSubject
            complaintVO.complaintDescription = complaintDescription
            complaintVO.complaintReply=complaintReply
            complaintVO.complaintDate = complaintDate
            complaintVO.complaintTime = complaintTime
            complaintVO.complaintFrom_LoginId = complaintFrom_LoginId

            complaintDAO.insertComplaint(complaintVO)

            return redirect(url_for('userComplaint'))
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)
