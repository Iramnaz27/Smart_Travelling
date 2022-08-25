from flask import request, render_template, redirect, url_for
from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession, session
from project.com.dao.VehicleDAO import VehicleDAO
from project.com.vo.VehicleVO import VehicleVO

from werkzeug.utils import secure_filename
import os
from datetime import datetime

UPLOAD_FOLDER6 = 'project/static/assets/vehicleImage/'

app.config['UPLOAD_FOLDER6'] = UPLOAD_FOLDER6


@app.route('/admin/loadVehicle', methods=['GET'])
def adminLoadVehicle():
    try:
        if adminLoginSession() == 'admin':
            return render_template('admin/addVehicle.html')
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/insertVehicle', methods=['POST'])
def adminInsertVehicle():
    try:
        if adminLoginSession() == 'admin':
            print(1)
            vehicleType = request.form['vehicleType']
            vehicleDescription = request.form['vehicleDescription']
            vehicleColor = request.form['vehicleColor']
            vehicleCapacity = request.form['vehicleCapacity']
            vehiclePriceperkm = request.form['vehiclePriceperkm']
            vehiclePrice = request.form['vehiclePrice']
            vehicleExtraDayPrice = request.form['vehicleExtraDayPrice']
            vehicleNumberplate = request.form['vehicleNumberplate']
            vehicleCurrentkm = request.form['vehicleCurrentkm']
            vehicleStatus = 'Active'
            vehicleFlag = 1
            print(2)
            if not secure_filename(request.files['file'].filename).endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                msg = 'Image is not a valid format file'
                return render_template('admin/addVehicle.html', error=msg)

            else:
                print(3)
                
                print(4)
                vehicleVO = VehicleVO()
                vehicleDAO = VehicleDAO()

                vehicleVO.vehicleType = vehicleType
                vehicleVO.vehicleDescription = vehicleDescription
                vehicleVO.vehicleColor = vehicleColor
                vehicleVO.vehicleCapacity = vehicleCapacity
                vehicleVO.vehiclePriceperkm = vehiclePriceperkm
                vehicleVO.vehiclePrice = vehiclePrice
                vehicleVO.vehicleExtraDayPrice = vehicleExtraDayPrice
                vehicleVO.vehicleNumberplate = vehicleNumberplate
                vehicleVO.vehicleCurrentkm = vehicleCurrentkm
                vehicleVO.vehicleStatus = vehicleStatus
                vehicleVO.vehicleFlag = vehicleFlag

                print(5)
                file = request.files['file']
                print(file)

                vehicleVO.vehicleFileName = secure_filename(file.filename)

                print(vehicleVO.vehicleFileName)

                vehicleVO.vehicleFilePath = os.path.join(app.config['UPLOAD_FOLDER6'])
                print(vehicleVO.vehicleFilePath)

                file.save(os.path.join(vehicleVO.vehicleFilePath, vehicleVO.vehicleFileName))

                print("done",file)

                vehicleDAO.insertVehicle(vehicleVO)


                os.rename(vehicleVO.vehicleFilePath + vehicleVO.vehicleFileName,
                          vehicleVO.vehicleFilePath + str(vehicleVO.vehicleId) +
                          os.path.splitext(vehicleVO.vehicleFileName)[-1])

                vehicleVO.vehicleFileName = str(vehicleVO.vehicleId) + os.path.splitext(vehicleVO.vehicleFileName)[-1]

                print(vehicleVO.vehicleFileName)

                vehicleVO.vehicleFilePath = vehicleVO.vehicleFilePath.replace("project", "..")

                vehicleDAO.updateVehicle(vehicleVO)


                return redirect(url_for('adminViewVehicle'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/viewVehicle', methods=['GET'])
def adminViewVehicle():
    try:
        if adminLoginSession() == 'admin':
            vehicleDAO = VehicleDAO()
            vehicleVOList = vehicleDAO.viewVehicle()
            print("__________________", vehicleVOList)
            return render_template('admin/viewVehicle.html', vehicleVOList=vehicleVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/editVehicle', methods=['POST'])
def adminEditVehicle():
    try:
        if adminLoginSession() == 'admin':
            vehicleVO = VehicleVO()
            vehicleDAO = VehicleDAO()
            vehicleId = request.form['vehicleId']
            vehicleVO.vehicleId = vehicleId
            vehicleVOList = vehicleDAO.editVehicle(vehicleVO)
            print(vehicleVOList)
            return render_template('admin/editVehicle.html', vehicleVOList=vehicleVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/updateVehicle', methods=['POST'])
def adminUpdateVehicle():
    try:
        if adminLoginSession() == 'admin':

            vehicleId = request.form['vehicleId']
            vehicleType = request.form['vehicleType']
            vehicleDescription = request.form['vehicleDescription']
            vehicleColor = request.form['vehicleColor']
            vehicleCapacity = request.form['vehicleCapacity']
            vehiclePriceperkm = request.form['vehiclePriceperkm']
            vehiclePrice = request.form['vehiclePrice']
            vehicleExtraDayPrice = request.form['vehicleExtraDayPrice']
            vehicleNumberplate = request.form['vehicleNumberplate']
            vehicleCurrentkm = request.form['vehicleCurrentkm']

            vehicleVO = VehicleVO()
            vehicleDAO = VehicleDAO()

            vehicleVO.vehicleId = vehicleId

            vehicleVOList = vehicleDAO.editVehicle(vehicleVO)

            file = request.files['file']
            print(file)

            vehicleFileName = secure_filename(file.filename)

            if vehicleFileName == '':
                vehicleFileName = vehicleVOList[0].vehicleFileName

            if not vehicleFileName.endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                msg = 'Image is not a valid format file'
                return render_template('admin/editVehicle.html', vehicleVOList=vehicleVOList, error=msg)

            else:
                vehicleVO.vehicleType = vehicleType
                vehicleVO.vehicleDescription = vehicleDescription
                vehicleVO.vehicleColor = vehicleColor
                vehicleVO.vehicleCapacity = vehicleCapacity
                vehicleVO.vehiclePriceperkm = vehiclePriceperkm
                vehicleVO.vehiclePrice = vehiclePrice
                vehicleVO.vehicleExtraDayPrice = vehicleExtraDayPrice
                vehicleVO.vehicleNumberplate = vehicleNumberplate
                vehicleVO.vehicleCurrentkm = vehicleCurrentkm

                if vehicleFileName != vehicleVOList[0].vehicleFileName:
                    vehicleVO.vehicleFileName = secure_filename(file.filename)
                    print(vehicleVO.vehicleFileName)
                    vehicleVO.vehicleFilePath = os.path.join(app.config['UPLOAD_FOLDER6'])
                    os.remove(vehicleVO.vehicleFilePath + vehicleVOList[0].vehicleFileName)
                    file.save(os.path.join(vehicleVO.vehicleFilePath, vehicleVO.vehicleFileName))
                    os.rename(vehicleVO.vehicleFilePath + vehicleVO.vehicleFileName,
                              vehicleVO.vehicleFilePath + str(vehicleVO.vehicleId) +
                              os.path.splitext(vehicleVO.vehicleFileName)[-1])
                    vehicleVO.vehicleFileName = str(vehicleVO.vehicleId) + os.path.splitext(vehicleVO.vehicleFileName)[-1]
                    print(vehicleVO.vehicleFileName)
                    vehicleVO.vehicleFilePath = vehicleVO.vehicleFilePath.replace("project", "..")

                vehicleDAO.updateVehicle(vehicleVO)

                return redirect(url_for('adminViewVehicle'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)
        
@app.route('/admin/deleteVehicle', methods=['POST'])
def adminDeleteVehicle():
    try:
        if adminLoginSession() == 'admin':
            vehicleVO = VehicleVO()
            vehicleDAO = VehicleDAO()
            vehicleId = request.form['vehicleId']
            vehicleVO.vehicleId = vehicleId
            vehicle = vehicleDAO.deleteVehicle(vehicleVO)
            path = vehicle.vehicleFilePath.replace("..", "project") + vehicle.vehicleFileName
            os.remove(path)
            return redirect(url_for('adminViewVehicle'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)

@app.route('/admin/activateVehicle', methods=['POST'])
def adminActivateVehicle():
    try:
        if adminLoginSession() == 'admin':
            vehicleId = request.form['vehicleId']
            vehicleStatus = 'Active'

            vehicleVO = VehicleVO()
            vehicleDAO = VehicleDAO()

            vehicleVO.vehicleId = vehicleId
            vehicleVO.vehicleStatus = vehicleStatus

            vehicleDAO.updateVehicle(vehicleVO)

            return redirect(url_for('adminViewVehicle'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/blockVehicle', methods=['POST'])
def adminBlockVehicle():
    try:
        if adminLoginSession() == 'admin':
            vehicleId = request.form['vehicleId']
            vehicleStatus = 'Inactive'

            vehicleVO = VehicleVO()
            vehicleDAO = VehicleDAO()

            vehicleVO.vehicleId = vehicleId
            vehicleVO.vehicleStatus = vehicleStatus

            vehicleDAO.updateVehicle(vehicleVO)

            return redirect(url_for('adminViewVehicle'))

        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)
