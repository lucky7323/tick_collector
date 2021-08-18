import os
import pathlib
import boto3
import telegram
from dotenv import load_dotenv
from distutils.util import strtobool
from loguru import logger
from glob import glob


def upload(file_path, file_name, telegram_bot=None):
    access_key = os.getenv('aws_access_key')
    secret_key = os.getenv('aws_secret_key')
    bucket = os.getenv('s3_bucket')
    bucket_path = os.getenv('s3_bucket_path')
    chat_id = os.getenv("telegram_chat_id")

    s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    try:
        s3.upload_file(file_path, bucket, f"{bucket_path}{file_name}")
        msg = f"S3 Upload Successful: {file_path} -> s3://{bucket}/{bucket_path}"
        logger.info(msg)
        if telegram_bot is not None:
            telegram_bot.sendMessage(chat_id=chat_id, text=msg)
    except Exception as e:
        logger.error(e)
        if telegram_bot is not None:
            telegram_bot.sendMessage(chat_id=chat_id, text=f"{e}: Failed to Upload {file_path}")
        return False
    return True


if __name__ == "__main__":
    load_dotenv()

    if bool(strtobool(os.getenv("use_s3", "False"))):
        data_dir = os.path.join(pathlib.Path().resolve(), 'data/')
        log_dir = os.path.join(pathlib.Path().resolve(), 'logs/')

        logger.add(f"{log_dir}s3.log", rotation="1 month", compression="zip")

        use_telegram = bool(strtobool(os.getenv("use_telegram", "False")))
        tel_bot = telegram.Bot(token=os.getenv("telegram_token")) if use_telegram else None

        data_path_list = glob(f"{data_dir}*.zip")
        for data_path in data_path_list:
            data_name = data_path.split(data_dir)[1]
            if upload(data_path, data_name, tel_bot):
                os.remove(data_path)
