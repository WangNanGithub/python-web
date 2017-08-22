# -*- coding:utf-8 -*-
"""
    用来保存贷后SQL
"""
# 每日到期订单
expired_daily = """
 SELECT tmp.loanDate AS '放款日期',     
     sum((CASE WHEN (tmp.paymentNum = 1 AND datediff(now(),tmp.repaymentDate)>0) THEN 1 ELSE 0 END))  AS '到期笔数1',
     sum((CASE WHEN (tmp.paymentNum = 2 AND datediff(now(),tmp.repaymentDate)>0) THEN 1 ELSE 0 END))  AS '到期笔数2',
     sum((CASE WHEN (tmp.paymentNum >= 3 AND datediff(now(),tmp.repaymentDate)>0) THEN 1 ELSE 0 END))  AS '到期笔数3+'
     FROM (  SELECT
                 (CASE WHEN (lo.due = 1 AND lo.`actual_repayment_date` IS NOT NULL AND lo.`status` = 1000 )
                  THEN datediff(lo.`actual_repayment_date`, lo.`repayment_date` )
                       WHEN (lo.due = 1 AND lo.`actual_repayment_date` IS NULL ) THEN datediff(now(),lo.repayment_date)
                       WHEN (lo.due = 1 AND lo.`actual_repayment_date` IS NOT NULL AND lo.`status` != 1000 )
                        THEN datediff(now(),lo.repayment_date)
                       ELSE '0' END) AS 'dueDays',
                     DATE_FORMAT(lo.`loan_date`,   '%y-%m-%d') AS 'loanDate',
                     lo.`repayment_date`  AS 'repaymentDate',
                 (CASE WHEN (lo.due = 1) THEN '是'
                     WHEN (lo.due = 0) THEN '否'
                     ELSE '未知' END) AS 'isDUe',
                 (SELECT COUNT(a.id) FROM pdl_loan_order a WHERE a.user_id = lo.user_id
                  AND  a.`create_time` > '2017-02-16 00:00:00' AND a.`create_time` <= lo.create_time
                   AND a.status IN (30,35,-60,-100,1000))  AS 'paymentNum'
               FROM 
                 `pdl_loan_order` lo

                WHERE lo.`create_time` >= '2017-02-16 00:00:00' AND lo.`loan_date` >= '2017-07-01'
                 AND lo.`loan_date` <=date_sub(curdate(),INTERVAL 0 DAY)
                  AND lo.`user_id` NOT IN('8688485082575304' ,'8688485139642602','8688487288128300','8688494921401201',
                  '8688496375422203','8688485081906005','8688495287722601','8688485081962305','8688493352520000',
                  '8688489997182404','8688490150744709','8688490174210505','8688490254451201','8688492163295307',
                  '8688498541093603','8688493352858707')  AND  lo.`status` IN (30,35,-60,-100,1000) ) AS tmp
     WHERE loanDate IS NOT NULL
     GROUP BY loanDate
     ORDER BY loanDate ASC;
"""

# 到期一个月以上
expired_one_month_more = """
 SELECT tmp.loanDate AS '放款月份', 
        sum((CASE WHEN (tmp.paymentNum= 1) THEN 1 ELSE 0 END))  AS '放款1',
        sum((CASE WHEN (tmp.paymentNum= 2) THEN 1 ELSE 0 END))  AS '放款2',
        sum((CASE WHEN (tmp.paymentNum >= 3) THEN 1 ELSE 0 END))  AS '放款3+',
        sum((CASE WHEN (tmp.paymentNum = 1 AND datediff(now(),tmp.repaymentDate)>30) THEN 1 ELSE 0 END))  AS '到期一个月以上笔数1',
        sum((CASE WHEN (tmp.paymentNum = 2 AND datediff(now(),tmp.repaymentDate)>30) THEN 1 ELSE 0 END))  AS '到期一个月以上笔数2',
        sum((CASE WHEN (tmp.paymentNum >= 3 AND datediff(now(),tmp.repaymentDate)>30) THEN 1 ELSE 0 END))  AS '到期一个月以上笔数3+'
FROM (  SELECT
            (CASE WHEN (lo.due = 1 AND lo.`actual_repayment_date` IS NOT NULL AND lo.`status` = 1000 )
             THEN datediff(lo.`actual_repayment_date`, lo.`repayment_date` )
                  WHEN (lo.due = 1 AND lo.`actual_repayment_date` IS NULL ) THEN datediff(now(),lo.repayment_date)
                  WHEN (lo.due = 1 AND lo.`actual_repayment_date` IS NOT NULL AND lo.`status` != 1000 )
                   THEN datediff(now(),lo.repayment_date)
                  ELSE '0' END) AS 'dueDays',
                DATE_FORMAT(lo.`loan_date`,   '%y-%m') AS 'loanDate',
                lo.`repayment_date`  AS 'repaymentDate',
            (SELECT COUNT(a.id) FROM pdl_loan_order a WHERE a.user_id = lo.user_id
             AND  a.`create_time` > '2017-02-16 00:00:00' AND a.`create_time` <= lo.create_time 
             AND a.status IN (30,35,-60,-100,1000))  AS 'paymentNum'
          FROM 
            `pdl_loan_order` lo

           WHERE lo.`create_time` >= '2017-02-16 00:00:00' AND lo.`loan_date` <=date_sub(curdate(),INTERVAL 0 DAY) 
            AND lo.`user_id` NOT IN('8688485082575304' ,'8688485139642602','8688487288128300','8688494921401201',
            '8688496375422203','8688485081906005','8688495287722601','8688485081962305','8688493352520000',
            '8688489997182404','8688490150744709','8688490174210505','8688490254451201','8688492163295307',
            '8688498541093603','8688493352858707')  AND  lo.`status` IN (30,35,-60,-100,1000) ) AS tmp
WHERE loanDate IS NOT NULL
GROUP BY loanDate
ORDER BY loanDate  ASC;
"""

# 到期
expired_all = """
 SELECT tmp.loanDate AS '放款月份', 
    sum((CASE WHEN (tmp.paymentNum= 1) THEN 1 ELSE 0 END))  AS '放款1',
    sum((CASE WHEN (tmp.paymentNum= 2) THEN 1 ELSE 0 END))  AS '放款2',
    sum((CASE WHEN (tmp.paymentNum >= 3) THEN 1 ELSE 0 END))  AS '放款3+',
    sum((CASE WHEN (tmp.paymentNum = 1 AND datediff(now(),tmp.repaymentDate)>0) THEN 1 ELSE 0 END))  AS '到期笔数1',
    sum((CASE WHEN (tmp.paymentNum = 2 AND datediff(now(),tmp.repaymentDate)>0) THEN 1 ELSE 0 END))  AS '到期笔数2',
    sum((CASE WHEN (tmp.paymentNum >= 3 AND datediff(now(),tmp.repaymentDate)>0) THEN 1 ELSE 0 END))  AS '到期笔数3+'
FROM (  SELECT
            (CASE WHEN (lo.due = 1 AND lo.`actual_repayment_date` IS NOT NULL AND lo.`status` = 1000 )
             THEN datediff(lo.`actual_repayment_date`, lo.`repayment_date` )
                  WHEN (lo.due = 1 AND lo.`actual_repayment_date` IS NULL ) THEN datediff(now(),lo.repayment_date)
                  WHEN (lo.due = 1 AND lo.`actual_repayment_date` IS NOT NULL AND lo.`status` != 1000 )
                   THEN datediff(now(),lo.repayment_date)
                  ELSE '0' END) AS 'dueDays',
                DATE_FORMAT(lo.`loan_date`,   '%y-%m') AS 'loanDate',
                lo.`repayment_date`  AS 'repaymentDate',
            (CASE WHEN (lo.due = 1) THEN '是'
                WHEN (lo.due = 0) THEN '否'
                ELSE '未知' END) AS 'isDUe',
            (SELECT COUNT(a.id) FROM pdl_loan_order a WHERE a.user_id = lo.user_id
             AND  a.`create_time` > '2017-02-16 00:00:00' AND a.`create_time` <= lo.create_time
              AND a.status IN (30,35,-60,-100,1000))  AS 'paymentNum'
          FROM 
            `pdl_loan_order` lo
           WHERE lo.`create_time` >= '2017-02-16 00:00:00' AND lo.`loan_date` <=date_sub(curdate(),INTERVAL 0 DAY) 
           AND lo.`user_id` NOT IN('8688485082575304' ,'8688485139642602','8688487288128300','8688494921401201',
            '8688496375422203','8688485081906005','8688495287722601','8688485081962305','8688493352520000',
            '8688489997182404','8688490150744709','8688490174210505','8688490254451201','8688492163295307',
            '8688498541093603','8688493352858707')  AND  lo.`status` IN (30,35,-60,-100,1000) ) AS tmp
WHERE loanDate IS NOT NULL
GROUP BY loanDate
ORDER BY loanDate ASC;
"""

# 决策订单逾期率
decision_sys_due_rate = """
          select 
              date(loan_date) AS '放款日期',
              count(*) AS '放款笔数',
              sum((case when (datediff(now(),o.`repayment_date` )>0)then 1 else 0 end )) AS '到期笔数',
              sum((case when (due = 1) then 1 else 0 end )) AS '逾期笔数',
              o.`loan_period` AS '借款期限',
              o.`review_by` AS 'review_by(0:贷前,1:决策系统,2:被拒订单分流)'
               from `pdl_decision_sys_result` pd
               LEFT JOIN `pdl_loan_order` o ON pd.`order_id` = o.`id` 
               LEFT JOIN `pdl_user_id_card` ui ON ui.`user_id` = o.`user_id`
               LEFT JOIN `pdl_user_basic` u ON o.`user_id` = u.`id` 
               where  o.create_time >= '2017-07-11' and o.status in(30,35,-60,-100,1000)
               and o.`review_by` != 0
               and o.`user_id` not in('8688485082575304' ,'8688485139642602','8688487288128300','8688487131293707',
               '8688494921401201','8688496375422203','8688485081906005','8688495287722601','8688485081962305',
               '8688493352520000','8688489997182404','8688490150744709','8688490174210505','8688490254451201',
               '8688492163295307','8688498541093603','8688493352858707')
group by date(loan_date),o.`loan_period` ,o.`review_by`  
"""

# 决策订单通过率
decision_sys_pass_rate = """
        select 
         tmp.o_time AS '申请时间',
         tmp.o_count AS '申请笔数',
         tmp.tg_count AS '通过笔数',
         concat(FORMAT((tmp.tg_count/tmp.o_count)*100,2),'%') AS '通过率',
         tmp.review_by AS 'review_by(0:贷前,1:决策系统,2:被拒订单分流)' 
     from ( select Date(o.`create_time` )AS 'o_time', count(*) AS 'o_count',
                    sum((case when(o.status in (30,35,-60,-100,1000,20,25)) then 1 else 0 end)) As 'tg_count', 
                    o.`review_by` AS 'review_by'
                    from `pdl_decision_sys_result` pd
                    LEFT JOIN `pdl_loan_order` o ON pd.`order_id` = o.`id` 
                    LEFT JOIN `pdl_user_id_card` ui ON ui.`user_id` = o.`user_id`
                    LEFT JOIN `pdl_user_basic` u ON o.`user_id` = u.`id` 
                    where o.`review_by` != 0 
                    and o.`user_id` not in('8688485082575304' ,'8688485139642602','8688487288128300','8688487131293707',
                    '8688494921401201','8688496375422203','8688485081906005','8688495287722601','8688485081962305',
                    '8688493352520000','8688489997182404','8688490150744709','8688490174210505','8688490254451201',
                    '8688492163295307','8688498541093603','8688493352858707')
                    group by Date(o.`create_time` ),o.`review_by` ) tmp
"""
