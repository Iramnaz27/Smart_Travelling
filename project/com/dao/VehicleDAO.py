from project import db
from project.com.vo.VehicleVO import VehicleVO
from sqlalchemy import and_

class VehicleDAO:

    def insertVehicle(self, vehicleVO):
        db.session.add(vehicleVO)
        db.session.commit()

    def viewVehicle(self):
        vehicleList=VehicleVO.query.all()
        return vehicleList

    def viewActiveVehicle(self,vehicleMinCapacity):
        vehicleList=VehicleVO.query.filter(and_(VehicleVO.vehicleCapacity>=vehicleMinCapacity,VehicleVO.vehicleStatus=="Active")).all()
        return vehicleList

    def deleteVehicle(self,vehicleVO):

        vehicle = VehicleVO.query.get(vehicleVO.vehicleId)

        db.session.delete(vehicle)

        db.session.commit()

        return vehicle

    def editVehicle(self,vehicleVO):

        vehicleList = VehicleVO.query.filter_by(vehicleId=vehicleVO.vehicleId).all()

        return vehicleList

    def updateVehicle(self,vehicleVO):

        db.session.merge(vehicleVO)

        db.session.commit()
