from sqlalchemy import Column, ForeignKey, Integer, Text

from .abstract_model import AbstractBaseModel


class Donation(AbstractBaseModel):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text, nullable=True)

    def __repr__(self):
        if self.comment is None:
            return f'Пожертвование от {self.user_id} с комментарием: {self.comment}!'
        return f'Пожертвование от {self.user_id}!'