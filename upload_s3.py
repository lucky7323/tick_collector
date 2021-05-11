import os
import json
import argparse
import boto3
import telegram
from pathlib import Path
from loguru import logger
from glob import glob


def upload(file_path, file_name, config, s3_logger, telebot=None):
    access_key = config['AWS_ACCESS_KEY']
    secret_key = config['AWS_SECRET_KEY']
    bucket = config['S3_BUCKET']
    bucket_path = config['S3_BUCKET_PATH']
    chat_id = config['TELEGRAM_CHAT_ID']

    s3 = boto3.client('s3', aws_access_key_id=access_key,
                      aws_secret_access_key=secret_key)
    try:
        s3.upload_file(file_path, bucket, f"{bucket_path}{file_name}")
        msg = f"S3 Upload Successful: {file_path} -> s3://{bucket}/{bucket_path}"
        s3_logger.info(msg)
        if telebot is not None:
            telebot.sendMessage(chat_id=chat_id, text=msg)
    except Exception as e:
        s3_logger.error(e)
        if telebot is not None:
            telebot.sendMessage(chat_id=chat_id, text=f"{e}: Failed to Upload {file_path}")
        return False
    return True


def set_logger(log_dir):
    logger.add(f"{log_dir}" + "s3.log", rotation="1 month", compression="zip",
               filter=lambda record: record["extra"]["task"] == "s3")


def get_config(path):
    config = {}
    with open(path) as f:
        config = json.load(f)
    return config


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--log_dir", type=str, help="log directory path", default="./logs/")
    parser.add_argument("--data_dir", type=str, help="data directory path", default="./data/")
    parser.add_argument("--config", "--c", type=str, help="configuration file path", default="./config.json")
    parser.add_argument("--remove", "--rm", action='store_true', help="remove data after uploading to S3")
    parser.add_argument("--telegram", "--telebot", action='store_true', help="enable telegram alarm message")
    args = parser.parse_args()

    set_logger(args.log_dir)
    config = get_config(args.config)
    s3_logger = logger.bind(task="s3")
    telebot = None

    if args.telegram:
        telebot = telegram.Bot(token=config['TELEGRAM_TOKEN'])

    if not args.remove:
        Path(f"{args.data_dir}/uploaded").mkdir(parents=True, exist_ok=True)

    file_list = glob(f"{args.data_dir}*.zip")
    for f in file_list:
        name = f.split(args.data_dir)[1]
        if upload(f, name, config, s3_logger, telebot):
            if args.remove:
                os.remove(f)
            else:
                os.replace(f, f"{args.data_dir}uploaded/{name}")

