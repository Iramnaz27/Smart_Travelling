from datetime import datetime

from flask import render_template, request, url_for, redirect

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession, session
from project.com.vo.UserVO import UserVO
from project.com.dao.FeedbackDAO import FeedbackDAO
from project.com.vo.FeedbackVO import FeedbackVO


@app.route('/admin/viewFeedback', methods=['GET'])
def adminViewFeedback():
    try:
        if adminLoginSession() == 'admin':
            feedbackVO = FeedbackVO()
            feedbackDAO = FeedbackDAO()
            feedbackVO.feedbackTo_LoginId = session['session_loginId']
            feedbackVOList = feedbackDAO.adminViewFeedback(feedbackVO)
            return render_template('admin/viewFeedback.html', feedbackVOList=feedbackVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)

@app.route('/user/feedback', methods=['GET'])
def userFeedback():
    try:
        if adminLoginSession() == 'user':
            feedbackDAO = FeedbackDAO()
            feedbackVO = FeedbackVO()

            feedbackFrom_LoginId = session['session_loginId']
            feedbackVO.feedbackFrom_LoginId = feedbackFrom_LoginId

            feedbackVOList = feedbackDAO.viewFeedback(feedbackVO)
            print("______________", feedbackVOList)

            return render_template("user/postFeedback.html", feedbackVOList=feedbackVOList)
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)

@app.route('/user/loadFeedback', methods=['GET'])
def userLoadFeedback():
    try:
        if adminLoginSession() == 'user':
            return render_template("user/addFeedback.html")
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/insertFeedback', methods=['POST'])
def userInsertFeedback():
    try:
        if adminLoginSession() == 'user':
            feedbackSubject = request.form['feedbackSubject']
            feedbackDescription = request.form['feedbackDescription']
            feedbackRating = request.form['feedbackRating']

            if feedbackRating =='0':
                return render_template("user/addFeedback.html", error="Ratings required!!")

            feedbackDate = datetime.now().date()
            feedbackTime = datetime.now().time()

            feedbackVO = FeedbackVO()
            feedbackDAO = FeedbackDAO()

            feedbackVO.feedbackTo_LoginId = 1

            feedbackFrom_LoginId = session['session_loginId']

            feedbackVO.feedbackSubject = feedbackSubject
            feedbackVO.feedbackDescription = feedbackDescription
            feedbackVO.feedbackRating = feedbackRating
            feedbackVO.feedbackDate = feedbackDate
            feedbackVO.feedbackTime = feedbackTime
            feedbackVO.feedbackFrom_LoginId = feedbackFrom_LoginId

            feedbackDAO.insertFeedback(feedbackVO)
            print('1')
            print('2')
            return redirect(url_for('userFeedback'))
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


