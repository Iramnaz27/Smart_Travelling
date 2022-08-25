from flask import request, render_template, redirect, url_for
from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession, session
from project.com.dao.UserDAO import UserDAO
from project.com.vo.UserVO import UserVO
from project.com.dao.LoginDAO import LoginDAO
from project.com.vo.LoginVO import LoginVO

from werkzeug.utils import secure_filename
import os
from datetime import datetime

UPLOAD_FOLDER2 = 'project/static/assets/userImage/'

app.config['UPLOAD_FOLDER2'] = UPLOAD_FOLDER2


@app.route('/core/loadUser', methods=['GET'])
def coreLoadUser():
    try:
        return render_template('core/addUser.html')
    except Exception as ex:
        print(ex)

@app.route('/user/insertUser', methods=['POST'])
def userInsertUser():
    try:
        print("12")
        userName = request.form['userName']
        print("13")
        userEmail = request.form['userEmail']
        print("14")
        userMobile = request.form['userMobile']
        print("15")
        userAddress = request.form['userAddress']
        print("16")
        userStatus = 'Active'
        userDiscountStatus = 1
        print("45")
        loginEmail = userEmail
        loginPassword = request.form['loginPassword']

        userEmailList = UserVO.query.filter_by(userEmail=userEmail).all()

        loginEmailList = LoginVO.query.filter_by(loginEmail=loginEmail).all()

        if len(userEmailList) > 0:
            print(userEmailList)
            msg = 'User with same email already exist'
            return render_template('core/addUser.html', error=msg)

        elif len(loginEmailList) > 0:
            print(loginEmailList)
            msg = 'User with same email already exist'
            return render_template('core/addUser.html', error=msg)

        elif not secure_filename(request.files['file'].filename).endswith(
                ('.png', '.jpg', '.jpeg', '.tiff', '.bmp')):
            msg = 'Image is not a valid image file'
            return render_template('core/addUser.html', error=msg)

        else:
            loginVO = LoginVO()
            loginDAO = LoginDAO()

            userVO = UserVO()
            userDAO = UserDAO()

            loginVO.loginEmail = loginEmail
            loginVO.loginPassword = loginPassword
            loginVO.loginRole = "user"

            loginDAO.insertLogin(loginVO)

            userVO.userName = userName
            userVO.userEmail = userEmail
            userVO.userMobile = userMobile
            userVO.userAddress = userAddress
            userVO.userStatus = userStatus
            userVO.userJoiningDate = datetime.now().date()
            userVO.userDiscountStatus = userDiscountStatus

            file = request.files['file']
            print(file)

            userVO.userFileName = secure_filename(file.filename)

            userVO.userFilePath = os.path.join(app.config['UPLOAD_FOLDER2'])

            file.save(os.path.join(userVO.userFilePath, userVO.userFileName))

            os.rename(userVO.userFilePath + userVO.userFileName,
                      userVO.userFilePath + str(loginVO.loginId) + os.path.splitext(userVO.userFileName)[-1])

            userVO.userFileName = str(loginVO.loginId) + os.path.splitext(userVO.userFileName)[-1]

            print(userVO.userFileName)

            userVO.userFilePath = userVO.userFilePath.replace("project", "..")

            userVO.user_LoginId = loginVO.loginId

            userDAO.insertUser(userVO)

            msg = 'You have been registered successfully :)'

            return render_template('core/addUser.html', error=msg)
    except Exception as ex:
        print(ex)


@app.route('/user/viewProfile', methods=['GET'])
def userViewProfile():
    try:
        if adminLoginSession() == 'user':
            userVOList = UserVO.query.filter_by(user_LoginId=session["session_loginId"]).all()
            print("__________________", userVOList)
            return render_template('user/viewProfile.html', userVOList=userVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/editProfile')
def userEditProfile():
    try:
        if adminLoginSession() == 'user':

            userVOList = UserVO.query.filter_by(user_LoginId=session["session_loginId"]).all()

            print(userVOList)

            print("=======UserVOList=======", userVOList)

            print("=======type of UserVOList=======", type(userVOList))

            return render_template('user/editProfile.html', userVOList=userVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/updateUser', methods=['POST'])
def userUpdateUser():
    try:
        if adminLoginSession() == 'user':
            userId = request.form['userId']
            userName = request.form['userName']
            userMobile = request.form['userMobile']
            userAddress = request.form['userAddress']

            userVO = UserVO()
            userDAO = UserDAO()

            userVO.userId = userId

            userVOList = userDAO.editUser(userVO)

            flag = 0
            if len(userMobile) != 10:
                msg = 'Please match the requested format for User Mobile.'
                return render_template('user/editUser.html', userVOList=userVOList, error=msg)
            for i in userMobile:
                print(i)
                if i not in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
                    flag = 1
                    break
            if flag == 1:
                msg = 'Please match the requested format for User Mobile.'
                return render_template('user/editUser.html', userVOList=userVOList, error=msg)

            file = request.files['file']
            print(file)

            userFileName = secure_filename(file.filename)

            if userFileName == '':
                userFileName = userVOList[0].userFileName

            userFilePath = os.path.join(app.config['UPLOAD_FOLDER2'])

            if not userFileName.endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp')):
                msg = 'Image is not a valid image file'
                return render_template('user/editUser.html', userVOList=userVOList, error=msg)

            else:
                userVO.userName = userName
                userVO.userMobile = userMobile
                userVO.userAddress = userAddress
                userVO.userId = userId

                if userFileName != userVOList[0].userFileName:
                    path = userVOList[0].userFilePath.replace("..", "project") + userVOList[0].userFileName
                    os.remove(path)
                    userVO.userFileName = userFileName
                    userVO.userFilePath = userFilePath
                    file.save(os.path.join(userVO.userFilePath, userVO.userFileName))
                    os.rename(userVO.userFilePath + userVO.userFileName,
                              userVO.userFilePath + str(session["session_loginId"]) +
                              os.path.splitext(userVO.userFileName)[-1])
                    userVO.userFileName = str(session["session_loginId"]) + os.path.splitext(userVO.userFileName)[-1]
                    userVO.userFilePath = userVO.userFilePath.replace("project", "..")

                userDAO.updateUser(userVO)

                return redirect(url_for('userViewProfile'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)
