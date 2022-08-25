from project import db
from project.com.vo.FeedbackVO import FeedbackVO
from project.com.vo.UserVO import UserVO


class FeedbackDAO:
    def insertFeedback(self, feedbackVO):
        db.session.add(feedbackVO)
        db.session.commit()

    def adminViewFeedback(self, feedbackVO):
        feedbackList = db.session.query(FeedbackVO, UserVO) \
            .join(UserVO, FeedbackVO.feedbackFrom_LoginId == UserVO.user_LoginId) \
            .filter(FeedbackVO.feedbackTo_LoginId == feedbackVO.feedbackTo_LoginId).all()
        return feedbackList

    def viewFeedback(self, feedbackVO):
        feedbackList = FeedbackVO.query.filter_by(feedbackFrom_LoginId=feedbackVO.feedbackFrom_LoginId).all()
        return feedbackList