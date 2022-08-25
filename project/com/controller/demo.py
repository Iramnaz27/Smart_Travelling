@app.route('/manager/loadEmployee', methods=['GET'])
def managerLoadEmployee():
    try:
        if adminLoginSession() == 'manager':
            return render_template('manager/addDriver.html')
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)

@app.route('/manager/insertEmployee', methods=['POST'])
def managerInsertEmployee():
    try:
        if adminLoginSession() == 'manager':
            employeeName = request.form['employeeName']
            employeeEmail = request.form['employeeEmail']
            employeeMobile = request.form['employeeMobile']
            employeeAddress = request.form['employeeAddress']
            employeeStatus = 'Inactive'

            loginEmail = employeeEmail
            loginPassword = ''.join((random.choice(string.ascii_letters + string.digits)) for x in range(8))

            loginEmailList = LoginVO.query.filter_by(loginEmail=loginEmail).all()

            if len(loginEmailList) > 0:
                print(loginEmailList)
                msg = 'User with same email already exist'
                return render_template('manager/addDriver.html', error=msg)

            elif not secure_filename(request.files['file'].filename).endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                msg = 'Image is not a valid format file'
                return render_template('manager/addDriver.html', error=msg)

            else:
                print("loginPassword=" + loginPassword)

                sender = "rs.projectmanagementsystem@gmail.com"

                receiver = loginEmail

                msg = MIMEMultipart()


                msg['From'] = sender
                msg['To'] = receiver

                msg['Subject'] = "Project Management System Login"

                msg.attach(MIMEText("Hii, your password for project_management_system portal is {}".format(loginPassword), 'plain'))

                server = smtplib.SMTP('smtp.gmail.com', 587)

                server.starttls()

                server.login(sender, "admin@projectmanagementsystem")

                text = msg.as_string()

                server.sendmail(sender, receiver, text)

                loginVO = LoginVO()
                loginDAO = LoginDAO()

                employeeVO = EmployeeVO()
                employeeDAO = EmployeeDAO()

                loginVO.loginEmail = loginEmail
                loginVO.loginPassword = loginPassword
                loginVO.loginRole = "employee"

                loginDAO.insertLogin(loginVO)

                employeeVO.employeeName = employeeName
                employeeVO.employeeEmail = employeeEmail
                employeeVO.employeeMobile = employeeMobile
                employeeVO.employeeAddress = employeeAddress
                employeeVO.employeeStatus = employeeStatus
                employeeVO.employeeJoiningDate = datetime.now().date()
                employeeVO.employeeJoiningTime = datetime.now().time()

                file = request.files['file']
                print(file)

                employeeVO.employeeFileName = secure_filename(file.filename)

                print(employeeVO.employeeFileName)

                employeeVO.employeeFilePath = os.path.join(app.config['UPLOAD_FOLDER4'])

                file.save(os.path.join(employeeVO.employeeFilePath, employeeVO.employeeFileName))

                os.rename(employeeVO.employeeFilePath + employeeVO.employeeFileName,
                          employeeVO.employeeFilePath + str(loginVO.loginId) +
                          os.path.splitext(employeeVO.employeeFileName)[-1])

                employeeVO.employeeFileName = str(loginVO.loginId) + os.path.splitext(employeeVO.employeeFileName)[-1]

                print(employeeVO.employeeFileName)

                employeeVO.employeeFileName1 = secure_filename(file.filename)

                employeeVO.employeeFilePath = employeeVO.employeeFilePath.replace("project", "..")

                managerList = ManagerVO.query.filter_by(manager_LoginId=session['session_loginId']).all()
                for manager in managerList:
                    employeeVO.employee_ManagerId = manager.managerId
                    employeeVO.employee_CompanyId = manager.manager_CompanyId

                employeeVO.employee_LoginId = loginVO.loginId

                employeeDAO.insertEmployee(employeeVO)

                server.quit()

                return redirect(url_for('managerViewEmployee'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/manager/viewEmployee', methods=['GET'])
def managerViewEmployee():
    try:
        if adminLoginSession() == 'manager':
            employeeVO = EmployeeVO()
            employeeDAO = EmployeeDAO()
            managerList = ManagerVO.query.filter_by(manager_LoginId=session['session_loginId']).all()
            for manager in managerList:
                employeeVO.employee_ManagerId = manager.managerId
            employeeVOList = employeeDAO.viewManagerEmployee(employeeVO)
            print("__________________", employeeVOList)
            return render_template('manager/viewDriver.html', employeeVOList=employeeVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/manager/deleteEmployee', methods=['POST'])
def managerDeleteEmployee():
    try:
        if adminLoginSession() == 'manager':
            employeeVO = EmployeeVO()
            employeeDAO = EmployeeDAO()
            employeeId = request.form['employeeId']
            employeeVO.employeeId = employeeId
            employeeList = employeeDAO.deleteEmployee(employeeVO)
            path = employeeList.employeeFilePath.replace("..", "project") + employeeList.employeeFileName
            os.remove(path)
            loginVO = LoginVO()
            loginDAO = LoginDAO()
            loginVO.loginId = employeeList.employee_LoginId
            loginDAO.deleteLogin(loginVO)
            return redirect(url_for('managerViewEmployee'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/manager/editEmployee', methods=['POST'])
def managerEditEmployee():
    try:
        if adminLoginSession() == 'manager':
            employeeVO = EmployeeVO()
            employeeDAO = EmployeeDAO()
            employeeId = request.form['employeeId']
            employeeVO.employeeId = employeeId
            employeeVOList = employeeDAO.editEmployee(employeeVO)
            return render_template('manager/editProfile.html', employeeVOList=employeeVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/manager/updateEmployee', methods=['POST'])
def managerUpdateEmployee():
    try:
        if adminLoginSession() == 'manager':
            employeeId = request.form['employeeId']
            employeeName = request.form['employeeName']
            employeeEmail = request.form['employeeEmail']
            employeeMobile = request.form['employeeMobile']
            employeeAddress = request.form['employeeAddress']
            employee_LoginId = request.form['employee_LoginId']

            employeeVO = EmployeeVO()
            employeeDAO = EmployeeDAO()

            employeeVO.employeeId = employeeId

            employeeVOList = employeeDAO.editEmployee(employeeVO)

            flag=0
            if len(employeeMobile)!=10:
                msg = 'Please match the requested format for Employee Mobile.'
                return render_template('manager/editProfile.html', employeeVOList=employeeVOList, error=msg)
            for i in employeeMobile:
                print(i)
                if i not in ['1','2','3','4','5','6','7','8','9','0']:
                    flag=1
                    break
            if flag==1:
                msg = 'Please match the requested format for Employee Mobile.'
                return render_template('manager/editProfile.html', employeeVOList=employeeVOList, error=msg)

            file = request.files['file']
            print(file)

            employeeFileName = secure_filename(file.filename)

            if employeeFileName == '':
                employeeFileName = employeeVOList[0].employeeFileName

            loginEmail = employeeEmail

            loginEmailList = LoginVO.query.filter_by(loginEmail=loginEmail).all()

            if len(loginEmailList) > 0 and employeeVOList[0].employeeEmail != loginEmailList[0].loginEmail:
                print(loginEmailList)
                msg = 'User with same email already exist'
                return render_template('manager/editProfile.html', employeeVOList=employeeVOList, error=msg)

            elif not employeeFileName.endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                msg = 'Image is not a valid format file'
                return render_template('manager/editProfile.html', employeeVOList=employeeVOList, error=msg)

            else:
                employeeVO.employeeName = employeeName
                employeeVO.employeeEmail = employeeEmail
                employeeVO.employeeMobile = employeeMobile
                employeeVO.employeeAddress = employeeAddress
                employeeVO.employee_LoginId = employee_LoginId

                loginVO = LoginVO()
                loginDAO = LoginDAO()

                loginVO.loginId = employee_LoginId
                loginVO.loginEmail = employeeEmail

                loginDAO.updateLogin(loginVO)

                if employeeFileName != employeeVOList[0].employeeFileName:
                    employeeVO.employeeFileName = secure_filename(file.filename)
                    print(employeeVO.employeeFileName)
                    employeeVO.employeeFilePath = os.path.join(app.config['UPLOAD_FOLDER4'])
                    os.remove(employeeVO.employeeFilePath + employeeVOList[0].employeeFileName)
                    file.save(os.path.join(employeeVO.employeeFilePath, employeeVO.employeeFileName))
                    os.rename(employeeVO.employeeFilePath + employeeVO.employeeFileName,
                              employeeVO.employeeFilePath + str(loginVO.loginId) +
                              os.path.splitext(employeeVO.employeeFileName)[-1])
                    employeeVO.employeeFileName = str(loginVO.loginId) + os.path.splitext(employeeVO.employeeFileName)[-1]
                    print(employeeVO.employeeFileName)
                    employeeVO.employeeFileName1 = secure_filename(file.filename)
                    employeeVO.employeeFilePath = employeeVO.employeeFilePath.replace("project", "..")
                    userUpdateNotification(employee_LoginId, employeeName, employeeVO.employeeFileName,employeeVO.employeeFilePath)

                employeeDAO.updateEmployee(employeeVO)

                userInsertNotification("Your profile has been updated.", employee_LoginId)

                return redirect(url_for('managerViewEmployee'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)
