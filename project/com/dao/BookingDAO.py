from project import db
from project.com.vo.BookingVO import BookingVO


class BookingDAO:

    def insertBooking(self, bookingVO):
        db.session.add(bookingVO)
        db.session.commit()

    def viewBooking(self):
        bookingList=BookingVO.query.all()
        return bookingList

    def viewUserBooking(self,userId):
        bookingList = BookingVO.query.filter_by(booking_UserId=userId).all()
        return bookingList

    def viewUserCompletedBooking(self,userId):
        bookingList = BookingVO.query.filter_by(booking_UserId=userId, bookingStatus="Completed").all()
        return bookingList

    def editBooking(self,bookingVO):
        bookingList = BookingVO.query.filter_by(bookingId=bookingVO.bookingId).all()
        return bookingList

    def updateBooking(self,bookingVO):
        db.session.merge(bookingVO)
        db.session.commit()
