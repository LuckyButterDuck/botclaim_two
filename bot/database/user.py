from sqlalchemy import Column, VARCHAR, String, select
from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker

from bot.database import BaseModel


class User(BaseModel):
    __tablename__ = 'users_id'

    user_id = Column(VARCHAR(10), unique=True, nullable=False, primary_key=True)
    user_name = Column(String)


async def add_user_from_malling(
        session_maker,
        user_name,
        user_id
):
    async with session_maker() as session:
        async with session.begin():
            user = User(user_id=user_id, user_name=user_name)
            try:
                result = await session.execute(select(User).where(User.user_id == user_id))
                if result.fetchone() is not None:
                    return 'Вы уже нажимали /start'
                else:
                    print('confirm add')
                    session.add(user)
            except:
                return


async def get_users(session_maker: sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            prompt = f'SELECT * FROM users_id'
            users = await session.execute(text(prompt))
            return users.fetchall()
