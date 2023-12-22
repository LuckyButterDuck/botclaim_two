import asyncio
import logging
import os
import pathlib

from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from sqlalchemy.engine import URL

from bot.database import create_async_engine, get_session_maker, proceed_schemas, BaseModel
from bot.main_functionality import register_user_handler, ThrotlingMiddleware


async def start_bot(logger: logging.Logger):
    logging.basicConfig(level=logging.DEBUG)
    storage = RedisStorage.from_url('redis://redis:3535/0')
    dp = Dispatcher(storage=storage)
    bot = Bot(os.getenv('token'), parse_mode='HTML')
    register_user_handler(dp)

    host = os.getenv('POSTGRES_HOST')
    port = int(os.getenv('POSTGRES_PORT')) or 0
    db_name = os.getenv('POSTGRES_DB')
    user_name = os.getenv('POSTGRES_NAME')
    password = os.getenv('POSTGRES_PASSWORD')

    #   postgres_url = f'postgresql://{user_name}:{password}@{host}:{port}/{db_name}'
    postgres_url = URL.create(
        'postgresql+asyncpg',
        host=host,
        port=port,
        username=user_name,
        database=db_name,
        password=password
    )
    async_engine = create_async_engine(postgres_url)
    session_maker = get_session_maker(async_engine)
    await proceed_schemas(async_engine, BaseModel.metadata)

    dp.message.middleware.register(ThrotlingMiddleware(storage=storage))
    await dp.start_polling(bot, session_maker=session_maker, logger=logger)


def setup_env():
    from dotenv import load_dotenv
    path = pathlib.Path(__file__).parent.parent
    dotenv_path = path.joinpath('.env')
    if dotenv_path.exists():
        load_dotenv(dotenv_path)


def main():
    logger = logging.getLogger(__name__)

    try:
        setup_env()
        asyncio.run(start_bot(logger))
        logger.info('Bot started')
    except (KeyboardInterrupt, SystemExit):
        logger.info('Bot stopped')


if __name__ == '__main__':
    main()
