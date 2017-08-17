# -*- coding: UTF-8 -*-

from datebase import db_util
import pandas as pd


def update_pdl_channel():
    data = pd.read_excel(ur'../resource/现金贷渠道识别号.xlsx', sheetname='Sheet3', encoding='utf-8')
    sql = """
        INSERT INTO `pdl_channels` ( `channel_no`, `name`, `channel` ) VALUES( %s, %s, %s )
    """

    sql1 = """
        SELECT `id`, `version`, `platform`, `channel`, `download_url` AS 'downloadUrl', `update_desc` AS 'updateDesc', `force_update` AS 'forceUpdate', `force_update_version` AS 'forceUpdateVersion', `create_time` AS 'createTime', `update_time` AS 'updateTime' FROM `pdl_client_update` WHERE `platform` = 'Android'
    """

    sql2 = """
        SELECT COUNT(*) AS 'no' FROM `pdl_channels` WHERE `channel` = '%s'
    """

    client_update = db_util.select(sql1)
    with db_util.open_connection() as db:
        for i in range(len(data)):
            channel = data['channel'][i]
            for j in range(len(client_update)):
                if str(data['channel'][i]).startswith(client_update['channel'][j]):
                    channel = str(data['channel'][i])[len(client_update['channel'][j]) + 1:]
                    break
            param = (int(data['channel_no'][i]), data['name'][i], channel)
            count = db_util.select(sql2 % channel, db)
            print count['no'][0]
            if count['no'][0] <= 0:
                db_util.insert(sql, param, db)

