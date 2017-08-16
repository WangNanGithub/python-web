# -*- coding: utf-8 -*-

import oss2
import os
from config import oss_info
from log import logger


# 从OSS下载文件
def download(file_path):
    # 阿里认证
    access_key_id = os.getenv('OSS_TEST_ACCESS_KEY_ID', oss_info['ACCESS_KEY_ID'])
    access_key_secret = os.getenv('OSS_TEST_ACCESS_KEY_SECRET', oss_info['ACCESS_KEY_SECRET'])
    bucket_name = os.getenv('OSS_TEST_BUCKET', oss_info['BUCKET'])
    endpoint = os.getenv('OSS_TEST_ENDPOINT', oss_info['ENDPOINT'])
    bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)

    # 检查文件在系统中是否存在
    exist = bucket.object_exists(file_path)
    if exist:
        result = bucket.get_object(file_path)
        content = b''
        for chunk in result:
            content += chunk
        return content
    else:
        logger.info('object not exist, file path : %s' % file_path)
        return None

