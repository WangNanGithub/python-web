# -*- coding: UTF-8 -*-
import pandas as pd

reg = pd.read_csv(r'C:\Users\Administrator\Desktop\reg.csv', encoding='utf-8')
req = pd.read_csv(r'C:\Users\Administrator\Desktop\req.csv', encoding='utf-8')

# 合并结果
merge_after = pd.merge(reg, req, left_on=(u'日期', u'渠道'), right_on=(u'日期', u'渠道'), how='outer')
# 按列填充空值
merge_after = merge_after.fillna({u'渠道': '', u'注册数': 0, u'首贷订单数': 0})
# 排序
merge_after = merge_after.sort_values(by=[u'日期', u'渠道'])
print merge_after.head()
# 保存文件
merge_after.to_excel(r'C:\Users\Administrator\Desktop\0701-0817-4.xls', sheet_name='Sheet1', index=False, engine='xlsxwriter')
