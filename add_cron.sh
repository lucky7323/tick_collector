#! /bin/sh

FILE_PATH=`realpath $0`
BASE_DIR=`dirname $FILE_PATH`
CURRENT_PYTHON=`which python3`

CRON_CMD="upload_s3.py --log_dir $BASE_DIR/logs/ \
  --data_dir $BASE_DIR/data/ \
  --config $BASE_DIR/config.json \
  --rm"

(crontab -l 2>/dev/null; echo "0 0 * * * cd $BASE_DIR && $CURRENT_PYTHON $CRON_CMD") | crontab -

