from project import db
from project.com.vo.DriverVO import DriverVO
from project.com.vo.VehicleVO import VehicleVO
from project.com.vo.UserVO import UserVO


class BookingVO(db.Model):
    __tablename__ = 'bookingmaster'
    bookingId = db.Column('bookingId', db.Integer, primary_key=True, autoincrement=True)
    bookingStartDate = db.Column('bookingStartDate', db.DATE)
    bookingReturnDate = db.Column('bookingReturnDate', db.DATE)
    bookingExpectedReturnDate = db.Column('bookingExpectedReturnDate', db.DATE)
    bookingDriver = db.Column('bookingDriver', db.String(100))
    bookingVehicle = db.Column('bookingVehicle', db.String(100))
    bookingVehicleStartKm = db.Column('bookingVehicleStartKm', db.String(100))
    bookingVehicleEndKm = db.Column('bookingVehicleEndKm', db.String(100))
    bookingDeliverAddress = db.Column('bookingDeliverAddress', db.String(100))
    bookingAmount = db.Column('bookingAmount', db.Integer)
    bookingDiscount = db.Column('bookingDiscount', db.Integer)
    bookingStatus = db.Column('bookingStatus',db.String(100))
    bookingCancelRole = db.Column('bookingCancelRole',db.String(100))
    booking_DriverId = db.Column('booking_DriverId', db.Integer, db.ForeignKey(DriverVO.driverId))
    booking_VehicleId = db.Column('booking_VehicleId', db.Integer, db.ForeignKey(VehicleVO.vehicleId))
    booking_UserId = db.Column('booking_UserId', db.Integer, db.ForeignKey(UserVO.userId))

    def as_dict(self):
        return {
            'bookingId': self.bookingId,
            'bookingStartDate': self.bookingStartDate,
            'bookingReturnDate': self.bookingReturnDate,
            'bookingExpectedReturnDate': self.bookingExpectedReturnDate,
            'bookingDriver': self.bookingDriver,
            'bookingVehicle': self.bookingVehicle,
            'bookingVehicleStartKm': self.bookingVehicleStartKm,
            'bookingVehicleEndKm': self.bookingVehicleEndKm,
            'bookingDeliverAddress': self.bookingDeliverAddress,
            'bookingAmount': self.bookingAmount,
            'bookingDiscount': self.bookingDiscount,
            'bookingStatus': self.bookingStatus,
            'bookingCancelRole': self.bookingCancelRole,
            'booking_DriverId': self.booking_DriverId,
            'booking_VehicleId': self.booking_VehicleId,
            'booking_UserId': self.booking_UserId,
        }


db.create_all()