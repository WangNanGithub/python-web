# -*- coding: UTF-8 -*-
import pandas as pd

reg = pd.read_csv(r'C:\Users\Administrator\Desktop\reg.csv', encoding='utf-8')
req = pd.read_csv(r'C:\Users\Administrator\Desktop\req.csv', encoding='utf-8')

print reg.head()
print req.head()

merge_after = pd.merge(reg, req, left_on=(u'日期', u'渠道'), right_on=(u'日期', u'渠道'), how='outer')
merge_after = merge_after.fillna(0)
print merge_after.head()

merge_after.to_excel(r'C:\Users\Administrator\Desktop\0701-0817.xls', sheet_name='Sheet1', index=False, engine='xlsxwriter')
