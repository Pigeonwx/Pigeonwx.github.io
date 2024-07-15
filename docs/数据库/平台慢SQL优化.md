# 一、背景
分析autofish应用所有Top占比慢SQL，优化他们的调用时长，提高核心逻辑的DB读写效率
# 二、问题分析
## 2.1 慢SQL的主要原因
> 导致慢SQL查询一般都是如下原因

1️⃣ 索引没有设计好
2️⃣ 语句没有写好
3️⃣ MYSQL选错索引
4️⃣ 数据量太多

## 2.2 工具与平台
慢SQL统计平台：[https://dbservice.alibaba-inc.com/performance/instance_detail?granularity=1&instance=rm-8vb1scd0i2alf2p18&ip=33.9.193.161&port=3003&region=cn-zhangjiakou&start=2024/06/24%2015:01:56&end=2024/06/24%2015:11:56&tabkeyInstance=slowsql](https://dbservice.alibaba-inc.com/performance/instance_detail?granularity=1&instance=rm-8vb1scd0i2alf2p18&ip=33.9.193.161&port=3003&region=cn-zhangjiakou&start=2024/06/24%2015:01:56&end=2024/06/24%2015:11:56&tabkeyInstance=slowsql)
分析TOP15 占比的慢SQL来源、产生原因并提供修改建议，一般从经验来看缓解慢SQL的方式有以下几种

- 表数据量级优化（表数量行超过W）:减少数据行，执行无效数据的删除
- 表索引优化：分析查询SQL，对必要字段加索引
- 业务逻辑改造：SQL语句优化
# 三、解决方案
> 由于权限关系，我只对DMS查询出来的过去30天数据分析，指标筛选范围为"或"关系

- 慢SQL日期筛选范围：2020.06.09-2020.07.09
- 1️⃣ 慢SQL指标筛选范围：风险指数不小于2.00的
- 2️⃣ 慢SQL指标筛选范围：耗时比例超过%1的
- 3️⃣ 慢SQL指标筛选范围：执行次数超过10次的
- 方法：人工审核筛选

## 慢SQL分析优化

- 筛选日期记录

[20240624~20240708]  done

### 慢SQL涉及的表格


### 慢SQL优化本地MOCK
### 表格数据准备
创建这几个表格，并根据实际情况随机插入一些数据，尽可能还原原数据表格![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2024/png/137756471/1720665366713-8db2fc08-5e66-42a5-8929-eb0c0927a82b.png#clientId=u034f9bf3-6c05-4&from=paste&height=287&id=uc5b923ff&originHeight=574&originWidth=3840&originalType=binary&ratio=2&rotation=0&showTitle=false&size=555434&status=done&style=none&taskId=u8abe0ba3-cbfa-4d17-aa5a-0affe958b05&title=&width=1920)
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2024/png/137756471/1720749435250-c23c8cf5-9405-41fd-87ec-dfa64dc58d0c.png#clientId=u98dd93dd-f542-4&from=paste&height=346&id=u7eaf29af&originHeight=692&originWidth=3786&originalType=binary&ratio=2&rotation=0&showTitle=false&size=654839&status=done&style=none&taskId=u844f0663-5061-4de4-b157-bfc0719250b&title=&width=1893)

### 治理前后效果对比
#### efd7db9e

- SQL句子
```sql
/* 2132b44c17204050600087865e1802/0.1//efd7db9e/// */
select id, gmt_create, gmt_modified, sunfire_id, plugin_id, tenant_id, name, plugin_type,push_goc, has_alarm_rule, source_type, url, compute_close, related_mtop, path, alarm_title,gmt_first_alarm, time_range, alarm_count, alarm_count_days, apps, monitor_type, manager, priority, msg, is_spe
    from sunfire_alarm
    where 1=1
        and gmt_create >= '2024-07-08 09:47:39'         
        and gmt_create <= '2024-07-08 10:17:39' 
    order by gmt_create desc
```

- 真实线上优化前性能

![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2024/png/137756471/1720663541126-a03f1df6-461b-42ee-9738-fcfc873a2f6e.png#clientId=u034f9bf3-6c05-4&from=paste&height=251&id=u887d6b29&originHeight=502&originWidth=3582&originalType=binary&ratio=2&rotation=0&showTitle=false&size=362010&status=done&style=none&taskId=u4e00af33-b590-4d2b-bd05-2207aa01401&title=&width=1791)

- 本地优化前性能![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2024/png/137756471/1720665648739-eb6eadc6-2ac5-406f-8d4c-8465a5cf7c61.png#clientId=u034f9bf3-6c05-4&from=paste&height=455&id=ubc02398a&originHeight=910&originWidth=3840&originalType=binary&ratio=2&rotation=0&showTitle=false&size=819000&status=done&style=none&taskId=u9149a3dc-d0c7-4f9e-8d67-82204c78268&title=&width=1920)

- 优化
```sql
ALTER TABLE `idle_autofish`.`sunfire_alarm` ADD INDEX `idx_gmtcreate` (`gmt_create`);
```
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2024/png/137756471/1720666024325-d1d39d70-1955-456a-85eb-d576cc69cac5.png#clientId=u034f9bf3-6c05-4&from=paste&height=179&id=u48d8f9fc&originHeight=358&originWidth=3834&originalType=binary&ratio=2&rotation=0&showTitle=false&size=296209&status=done&style=none&taskId=u42b534fc-9771-4805-85a9-bd7e87ce473&title=&width=1917)
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2024/png/137756471/1720666225189-b074a23b-c60f-4e82-8451-ff971f2b4769.png#clientId=u034f9bf3-6c05-4&from=paste&height=466&id=ufaf2bef9&originHeight=932&originWidth=3836&originalType=binary&ratio=2&rotation=0&showTitle=false&size=823895&status=done&style=none&taskId=u7bf3a9a2-926a-413b-8ad1-a924d06b297&title=&width=1918)

- 结论

可以进行
#### 68a75e19&cf28808c&8b6e0020&4cf93cf3

- SQL句子
```sql
/* ///68a75e19/// */
SELECT *
FROM sre_main_score_detail
WHERE 1 = 1
	AND main_sre_id = 911
	AND statistic_period = 'day'
	AND status = 1
	AND sub_dept_name LIKE concat('%', '淘天集团-闲鱼-闲鱼技术-算法-推荐算法', '%')
	AND DATE_FORMAT('2024-07-08 00:00:00', '%Y-%m-%d') <= DATE_FORMAT(gmt_create, '%Y-%m-%d')
	AND DATE_FORMAT('2024-07-08 23:59:59.999', '%Y-%m-%d') >= DATE_FORMAT(gmt_create, '%Y-%m-%d')
ORDER BY gmt_modified DESC
LIMIT 20;
```
```sql
/* ///cf28808c/// */
SELECT COUNT(0)
FROM sre_main_score_detail
WHERE 1 = 1
	AND main_sre_id = 911
	AND statistic_period = 'day'
	AND status = 1
	AND sub_dept_name LIKE concat('%', '淘天集团-闲鱼-闲鱼技术-渠道增长技术', '%')
	AND DATE_FORMAT('2024-07-08 00:00:00', '%Y-%m-%d') <= DATE_FORMAT(gmt_create, '%Y-%m-%d')
	AND DATE_FORMAT('2024-07-08 23:59:59.999', '%Y-%m-%d') >= DATE_FORMAT(gmt_create, '%Y-%m-%d')
```

```sql
/* ///8b6e0020/// */
SELECT *
FROM sre_main_score_detail
WHERE 1 = 1
	AND statistic_period = 'day'
	AND status = 1
	AND DATE_FORMAT('2024-07-08 00:00:00', '%Y-%m-%d') <= DATE_FORMAT(gmt_create, '%Y-%m-%d')
	AND DATE_FORMAT('2024-07-08 23:59:59.999', '%Y-%m-%d') >= DATE_FORMAT(gmt_create, '%Y-%m-%d')
ORDER BY gmt_modified DESC
LIMIT 620, 20
```

```sql
/* ///4cf93cf3/// */
SELECT COUNT(0)
FROM sre_main_score_detail
WHERE 1 = 1
	AND statistic_period = 'day'
	AND status = 1
	AND DATE_FORMAT('2024-07-08 00:00:00', '%Y-%m-%d') <= DATE_FORMAT(gmt_create, '%Y-%m-%d')
	AND DATE_FORMAT('2024-07-08 23:59:59.999', '%Y-%m-%d') >= DATE_FORMAT(gmt_create, '%Y-%m-%d')
```

- 线上优化前数据

![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2024/png/137756471/1720666440915-7a6f1be7-976e-4ba8-81c6-bec9a06dc903.png#clientId=u034f9bf3-6c05-4&from=paste&height=225&id=u5376a176&originHeight=450&originWidth=3592&originalType=binary&ratio=2&rotation=0&showTitle=false&size=337716&status=done&style=none&taskId=ufe764358-abf2-4753-bf7a-1cc5fbcf3aa&title=&width=1796)
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2024/png/137756471/1720666971779-05bbfcda-7c95-41ee-90bd-f5c2f2cadf05.png#clientId=u034f9bf3-6c05-4&from=paste&height=393&id=ucd578564&originHeight=786&originWidth=3628&originalType=binary&ratio=2&rotation=0&showTitle=false&size=603410&status=done&style=none&taskId=ub44c2166-825e-4969-b6a6-0e50219d2e7&title=&width=1814)
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2024/png/137756471/1720666920047-ec0998d8-ac54-4d75-997c-62f1f98b3a70.png#clientId=u034f9bf3-6c05-4&from=paste&height=358&id=u4f2241af&originHeight=716&originWidth=3652&originalType=binary&ratio=2&rotation=0&showTitle=false&size=563986&status=done&style=none&taskId=u0dae3f1c-e1e7-4331-beec-3e51f662722&title=&width=1826)
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2024/png/137756471/1720667003806-54dcf828-d319-4672-931c-0d41d491ac39.png#clientId=u034f9bf3-6c05-4&from=paste&height=539&id=udb9ff48d&originHeight=1078&originWidth=3624&originalType=binary&ratio=2&rotation=0&showTitle=false&size=801863&status=done&style=none&taskId=u663e5796-65f3-441f-8013-a06f1b27dac&title=&width=1812)

- 本地优化前性能
   - 68a75e19
   - cf28808c
   - 8b6e0020
   - 4cf93cf3

![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2024/png/137756471/1720709637295-4944b6fc-5396-4a68-886e-2d3bb0b24b48.png#clientId=u301b8cbd-16cc-4&from=paste&height=350&id=u4fab9267&originHeight=700&originWidth=1204&originalType=binary&ratio=2&rotation=0&showTitle=false&size=269452&status=done&style=none&taskId=ud0d264e6-c241-4528-bbb9-8596d59c801&title=&width=602)

- 优化

1. 加索引
```sql
CREATE INDEX idx_main_statisc_status_status_gmt ON sre_main_score_detail (
    main_sre_id,
    statistic_period,
    status,
    gmt_create
);
```

2. 改SQL，from_

![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2024/png/137756471/1720709667528-cc0bb420-e297-4e3e-9d6c-dbe878ca7886.png#clientId=u301b8cbd-16cc-4&from=paste&height=336&id=u1724236c&originHeight=672&originWidth=1210&originalType=binary&ratio=2&rotation=0&showTitle=false&size=274034&status=done&style=none&taskId=u35d223a9-7298-460b-ae8b-4efc8ba25de&title=&width=605)
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2024/png/137756471/1720709714201-542cd7dd-d863-4ab3-9242-0c30f8c09b68.png#clientId=u301b8cbd-16cc-4&from=paste&height=209&id=udf6e5791&originHeight=418&originWidth=3168&originalType=binary&ratio=2&rotation=0&showTitle=false&size=305065&status=done&style=none&taskId=ue2bbe87b-1273-4e20-8924-02b548c21d7&title=&width=1584)

- 结论

可行
#### d5e4572a&c7edccab

- SQL
```sql
/* ///d5e4572a/// */
SELECT COUNT(issue_id) AS count, type, user_id
	, SUM(score) AS score, MAX(date) AS end
	, MIN(date) AS begin, issue_id, url
	, name, nickname, dept_name
FROM quality_score_detail
WHERE status = '已扣除'
GROUP BY type, issue_id, user_id;
```
```sql
/* 2107c42117199221638786235e3b84/0.1//c7edccab/// */
SELECT COUNT(issue_id) AS count, type, user_id
	, SUM(score) AS score, MAX(date) AS end
	, MIN(date) AS begin, issue_id, url
	, name, nickname, dept_name
FROM quality_score_detail
GROUP BY type, issue_id, user_id
```

- 线上表现

![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2024/png/137756471/1720667438351-8de3e8ff-bb39-45ac-b833-339ab96dab33.png#clientId=u034f9bf3-6c05-4&from=paste&height=510&id=u6d32e361&originHeight=1020&originWidth=3688&originalType=binary&ratio=2&rotation=0&showTitle=false&size=788760&status=done&style=none&taskId=ua0b498fc-447e-4450-9f48-cd95b6ce60f&title=&width=1844)![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2024/png/137756471/1720667549147-c7a37a70-954f-4751-ab0a-8c4fc9864c73.png#clientId=u034f9bf3-6c05-4&from=paste&height=350&id=u5bca0466&originHeight=700&originWidth=3602&originalType=binary&ratio=2&rotation=0&showTitle=false&size=515791&status=done&style=none&taskId=u0cbe291b-9194-43f1-9c6f-db86373c56c&title=&width=1801)

- 本地优化前性能![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2024/png/137756471/1720667844272-93d0947e-9a06-4893-8c6d-77394eccb87a.png#clientId=u034f9bf3-6c05-4&from=paste&height=475&id=ud03e8b96&originHeight=950&originWidth=3696&originalType=binary&ratio=2&rotation=0&showTitle=false&size=803383&status=done&style=none&taskId=u73e4a82c-34ea-47ee-9aea-984acd5e90e&title=&width=1848)![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2024/png/137756471/1720668037412-61c60ebd-b7f5-40d3-b8a5-ec4a3f5ccce6.png#clientId=u034f9bf3-6c05-4&from=paste&height=477&id=griHU&originHeight=954&originWidth=3384&originalType=binary&ratio=2&rotation=0&showTitle=false&size=743664&status=done&style=none&taskId=ue31d62e4-18c4-4515-bbf9-3bfdc868308&title=&width=1692)

- 优化
```sql
mysql> CREATE INDEX idx_status_type_issue_user ON quality_score_detail(status, type, issue_id, user_id);
Query OK, 0 rows affected (2.69 sec)
Records: 0  Duplicates: 0  Warnings: 0

mysql> CREATE INDEX idx_type_issue_user_status ON quality_score_detail(type, issue_id, user_id, status);
Query OK, 0 rows affected (2.31 sec)
Records: 0  Duplicates: 0  Warnings: 0

mysql> CREATE INDEX idx_type_issue_user ON quality_score_detail(type, issue_id, user_id);
Query OK, 0 rows affected (1.93 sec)
Records: 0  Duplicates: 0  Warnings: 0
```

| SQL | idx_status_type_issue_user | idx_type_issue_user_status | idx_type_issue_user |
| --- | --- | --- | --- |
| d5e4572a | ![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2024/png/137756471/1720683861987-a1ef2163-5eed-481f-b157-c7341cd7a9fe.png#clientId=uddec1cb0-7863-4&from=paste&height=333&id=u5572d2d2&originHeight=666&originWidth=1038&originalType=binary&ratio=2&rotation=0&showTitle=false&size=241542&status=done&style=none&taskId=u32665844-622e-4f2c-b841-c9213c8dd9b&title=&width=519) | ![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2024/png/137756471/1720683873142-4fc8763e-511d-42c7-927d-782a54f65897.png#clientId=uddec1cb0-7863-4&from=paste&height=329&id=ucec916a8&originHeight=658&originWidth=1142&originalType=binary&ratio=2&rotation=0&showTitle=false&size=261621&status=done&style=none&taskId=uea98a71f-7029-42e3-a9e6-1b4e986b5d1&title=&width=571) | ![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2024/png/137756471/1720683892797-75f96fd3-9da5-47c0-bdf6-2dd86c4b87ac.png#clientId=uddec1cb0-7863-4&from=paste&height=169&id=ua877d68e&originHeight=337&originWidth=560&originalType=binary&ratio=2&rotation=0&showTitle=false&size=87669&status=done&style=none&taskId=u4df8c8ff-b192-423e-a3fd-19372428dd3&title=&width=280) |
| c7edccab |  |  |  |


- 结论

没法优化

#### 8a2c35ed

- SQL
```sql
/* ///8a2c35ed/// */
SELECT id, gmt_create, gmt_modified, offline_table_id, table_name
	, version, version_create_at, active, full_data_record_count, field_count
	, full_data_physical_size, full_data_logical_size
FROM idle_suezops_table_version
ORDER BY version DESC
```

- 线上表现

![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2024/png/137756471/1720684083996-fe0cade2-553c-4d52-bc92-40f963317e9c.png#clientId=uddec1cb0-7863-4&from=paste&height=366&id=u027d5aeb&originHeight=732&originWidth=3680&originalType=binary&ratio=2&rotation=0&showTitle=false&size=584735&status=done&style=none&taskId=u845de055-fa15-4898-bce3-a0bca7b35c0&title=&width=1840)

- 本地mock

![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2024/png/137756471/1720684364829-b804dcb9-ff04-4094-a6ea-71a233380dd2.png#clientId=uddec1cb0-7863-4&from=paste&height=346&id=ue9bb07c8&originHeight=692&originWidth=1200&originalType=binary&ratio=2&rotation=0&showTitle=false&size=272667&status=done&style=none&taskId=ud8ad155a-df2c-403e-bda7-2d83123cede&title=&width=600)

- 优化
```sql
ALTER TABLE `idle_autofish`.`idle_suezops_table_version` ADD INDEX `idx_version` (`version`);
```
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2024/png/137756471/1720702307175-0a6ab355-5eb8-47be-bfe4-644429a26073.png#clientId=uddec1cb0-7863-4&from=paste&height=337&id=uf9bd3869&originHeight=674&originWidth=1192&originalType=binary&ratio=2&rotation=0&showTitle=false&size=266689&status=done&style=none&taskId=uc4a1250e-1d34-45da-8606-d9d15e0d8aa&title=&width=596)

- 结论

效果不明显，可以试试，因为线上数据version可能会随机一点

#### c74bb5f4

- SQL
```sql
DELETE FROM idle_data_works_instance_record
WHERE gmt_create < date_sub(now(), INTERVAL 3 DAY)
```

- 线上表现

![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2024/png/137756471/1720703292443-24466e6b-408e-4820-86ca-c9eb7a1ac47e.png#clientId=uddec1cb0-7863-4&from=paste&height=366&id=ub0531aba&originHeight=732&originWidth=3644&originalType=binary&ratio=2&rotation=0&showTitle=false&size=537839&status=done&style=none&taskId=u6ed631e6-133c-4b33-9371-9a932b48934&title=&width=1822)

- 本地mock

![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2024/png/137756471/1720703383904-25eda450-fed6-49c0-9de1-f909be1559e8.png#clientId=uddec1cb0-7863-4&from=paste&height=324&id=uc781532d&originHeight=648&originWidth=1292&originalType=binary&ratio=2&rotation=0&showTitle=false&size=275703&status=done&style=none&taskId=ue24baf9a-e50e-4c0d-9076-185354e9882&title=&width=646)

- 优化
```sql
ALTER TABLE `idle_autofish`.`idle_data_works_instance_record` ADD INDEX `idx_gmtcreate` (`gmt_create`)
```
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2024/png/137756471/1720703992114-6110fda2-99e7-4139-b4ee-a13b26792b7e.png#clientId=uddec1cb0-7863-4&from=paste&height=297&id=u7fa1efa1&originHeight=594&originWidth=1184&originalType=binary&ratio=2&rotation=0&showTitle=false&size=226982&status=done&style=none&taskId=udd25fdfc-9248-4517-8e3e-d0bfd5c1857&title=&width=592)

- 结论

可行
#### d2620289&350508ae

- SQL
```sql
DELETE FROM autofish_cf_info
WHERE unix_timestamp(gmt_create) <= 1717322401
```
```sql
/* 212abc3617200351856431316e112f/0.1.3.1.3362155218.15.1.334325130.102.1.335131238//350508ae/// */
SELECT COUNT(0)
FROM autofish_cf_info
WHERE 1 = 1
	AND unix_timestamp(gmt_create) >= 1720034763318
	AND unix_timestamp(gmt_create) <= 1720035363318
```

- 线上表现

![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2024/png/137756471/1720704591930-c76ca77d-acae-4611-91ee-fe7f4959ba31.png#clientId=u301b8cbd-16cc-4&from=paste&height=231&id=ub75b4353&originHeight=462&originWidth=3698&originalType=binary&ratio=2&rotation=0&showTitle=false&size=353462&status=done&style=none&taskId=u3839475f-611d-4d8c-b0a5-47d546ee0ba&title=&width=1849)
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2024/png/137756471/1720704670023-9aa1cc86-9bbc-4aa8-954d-5dedc49680b2.png#clientId=u301b8cbd-16cc-4&from=paste&height=304&id=ud4f7944b&originHeight=608&originWidth=3710&originalType=binary&ratio=2&rotation=0&showTitle=false&size=469528&status=done&style=none&taskId=u80c0c673-69f8-4fc5-9a43-88df7ebde09&title=&width=1855)

- 本地MOCK

![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2024/png/137756471/1720707340349-2e919534-7983-49b1-8018-20b3b27511e4.png#clientId=u301b8cbd-16cc-4&from=paste&height=171&id=u6268fdf6&originHeight=342&originWidth=629&originalType=binary&ratio=2&rotation=0&showTitle=false&size=103291&status=done&style=none&taskId=ud7f001d2-29bf-4127-8dcc-6525e615871&title=&width=314.5)

- 优化

取消使用unix_timestamp，使用FROM_UNIXTIME，需要在xml里面改语句
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2024/png/137756471/1720707312817-f0aee5e0-36dc-4539-a1cb-6d832d6a57a6.png#clientId=u301b8cbd-16cc-4&from=paste&height=171&id=u6e932117&originHeight=342&originWidth=633&originalType=binary&ratio=2&rotation=0&showTitle=false&size=103303&status=done&style=none&taskId=ua8c426ca-fe21-47b0-97e1-d5065f2abe8&title=&width=316.5)

- 结论

可行
#### 2e0d8293&ca82ecd7&36086d4f

- SQL
```sql
/* 21054a2417200576229293380e14e7/0.1//2e0d8293/// */
SELECT id, gmt_create, gmt_modified, version, app_version
	, platform, type, utdid, category, sdk
	, method, stack_md5, page, count, is_delete
	, process_uuid, user_action, action_time, priority, uid
	, stack, is_valid
FROM app_privacy_log
WHERE 1 = 1
	AND version = '7.16.50'
	AND platform = 'iOS'
	AND priority = 'H'
	AND is_valid = 1
	AND is_delete = 0
ORDER BY priority ASC, action_time ASC
LIMIT 10000
```
```sql
/* 21054a2417200576229313381e14e7/0.1//ca82ecd7/// */
SELECT id, gmt_create, gmt_modified, version, app_version
	, platform, type, utdid, category, sdk
	, method, stack_md5, page, count, is_delete
	, process_uuid, user_action, action_time, priority, uid
	, stack, is_valid
FROM app_privacy_log
WHERE 1 = 1
	AND version = '7.16.50'
	AND platform = 'iOS'
	AND is_valid = 1
	AND priority IN ('M', 'L')
	AND is_delete = 0
ORDER BY priority ASC, action_time ASC
LIMIT 5000
```
```sql
/* 2107c42117199221606755995e3b84/0.1//36086d4f/// */
SELECT name, type, AVG(score) AS score, period
	, user_id, month, dept_id
FROM `quality_score_mirror`
WHERE dept_id IN (
	'K4366', 
	'G4481', 
	'M4679', 
	'K4367', 
	'K4368', 
	'87294', 
	'N4697', 
	'K4334', 
	'K8377', 
	'51167', 
	'G4617', 
	'K8376', 
	'47137', 
	'M4918', 
	'G4480', 
	'G4482', 
	'N5778', 
	'K4308', 
	'G6413', 
	'47138', 
	'G5882', 
	'M4680', 
	'B1346', 
	'51166', 
	'G4618', 
	'K4336', 
	'K4335', 
	'G4619', 
	'N5783', 
	'B2109', 
	'N5784', 
	'G4813', 
	'47136', 
	'69138', 
	'G4812', 
	'K4433', 
	'87295', 
	'87296', 
	'51169', 
	'37997', 
	'D0332', 
	'87297', 
	'47133', 
	'87298', 
	'M4684'
)
GROUP BY `period`, `type`
ORDER BY `period` DESC
```

- 线上表现

![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2024/png/137756471/1720705120922-7a424e24-fb9d-4f26-a8c1-3ca665f43d8d.png#clientId=u301b8cbd-16cc-4&from=paste&height=186&id=u0b3c03f6&originHeight=372&originWidth=3600&originalType=binary&ratio=2&rotation=0&showTitle=false&size=285076&status=done&style=none&taskId=ua2b3d1e3-bd8b-4e4f-96f7-25f0d0d0f7f&title=&width=1800)
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2024/png/137756471/1720705176748-3fe2de86-32a4-4a78-993d-ce13670e0c54.png#clientId=u301b8cbd-16cc-4&from=paste&height=323&id=u4581db47&originHeight=646&originWidth=3724&originalType=binary&ratio=2&rotation=0&showTitle=false&size=483094&status=done&style=none&taskId=u516260b5-3120-4d98-a834-a078aa47cd9&title=&width=1862)

- 本地MOCK

![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2024/png/137756471/1720708288054-efceec23-fa5f-4073-a0a4-15efd4153021.png#clientId=u301b8cbd-16cc-4&from=paste&height=359&id=ubc8f4a9a&originHeight=718&originWidth=1166&originalType=binary&ratio=2&rotation=0&showTitle=false&size=273133&status=done&style=none&taskId=u15b445da-619f-493d-bd85-925904f9719&title=&width=583)
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2024/png/137756471/1720708367834-08ea2d10-8203-40cb-988e-d74f8cb03cc0.png#clientId=u301b8cbd-16cc-4&from=paste&height=172&id=uc2742d9e&originHeight=344&originWidth=2852&originalType=binary&ratio=2&rotation=0&showTitle=false&size=230465&status=done&style=none&taskId=uef897ae6-5dd2-44fc-936e-4d7cbe615a2&title=&width=1426)

- 优化
```sql
ALTER TABLE `idle_autofish`.`app_privacy_log` ADD INDEX `idx_version_platform_priority_is_valid_is_delete` (`version`,  `platform`, `priority`,`is_valid`, `is_delete`)
```

- 结论

可行
## 表空间异常优化
> 这部分看碎片TOP10优化即可

| **表（点击查看）** | **表（点击查看）** | **异常内容** | **诊断时间** | **优化** |
| --- | --- | --- | --- | --- |
| +autofish_cf_info | idle_autofish | 单表碎片空间大于6G,并且碎片率大于30% free空间大小14.62G | 2024-07-09 21:15:19 | OPTIMIZETABLE |
| +app_package_analysis_info | idle_autofish | 单表碎片空间大于6G,并且碎片率大于30% free空间大小10.24G | 2024-07-09 21:15:19 | OPTIMIZETABLE |

## 空间优化-表空间占比大小TOP10

## 空间优化-表空间碎片率TOP10
## 空间优化-单行长度占比TOP10

## 空间优化-表格行数占比TOP10
## 空间优化-数据行数为0表格TOP10
| 表（点击查看） | 表空间 | 表空间占比 | 索引空间 | 数据空间 | 碎片率 | 表行数 | 平均行长 | 索引数据比 | 索引大小 | 数据大小 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| longmen_static_item_record | 112 KB | 0.00% | 96.0 KB | 16.0 KB | 0.00% | 0 | 0 B | 6 | 96 | 16 |
| log_store_query_detail | 48.0 KB | 0.00% | 32.0 KB | 16.0 KB | 0.00% | 0 | 0 B | 2 | 32 | 16 |
| entrance_graph | 48.0 KB | 0.00% | 32.0 KB | 16.0 KB | 0.00% | 0 | 0 B | 2 | 32 | 16 |
| sunfire_alarm_result | 323 MB | 0.60% | 172 MB | 151 MB | 81.39% | 0 | 0 B | 1.139072848 | 176128 | 154624 |
| miniprogram_project | 32.0 KB | 0.00% | 16.0 KB | 16.0 KB | 0.00% | 0 | 0 B | 1 | 16 | 16 |
| log_store_indicator_config | 32.0 KB | 0.00% | 16.0 KB | 16.0 KB | 0.00% | 0 | 0 B | 1 | 16 | 16 |
| log_store | 32.0 KB | 0.00% | 16.0 KB | 16.0 KB | 0.00% | 0 | 0 B | 1 | 16 | 16 |
| log_scenario | 32.0 KB | 0.00% | 16.0 KB | 16.0 KB | 0.00% | 0 | 0 B | 1 | 16 | 16 |
| autofish_testcase_ai_model | 32.0 KB | 0.00% | 16.0 KB | 16.0 KB | 0.00% | 0 | 0 B | 1 | 16 | 16 |
| newtc_attachments | 32.0 KB | 0.00% | 16.0 KB | 16.0 KB | 0.00% | 0 | 0 B | 1 | 16 | 16 |
| perf_threshold_config | 32.0 KB | 0.00% | 16.0 KB | 16.0 KB | 0.00% | 0 | 0 B | 1 | 16 | 16 |
| autofish_label_info | 32.0 KB | 0.00% | 16.0 KB | 16.0 KB | 0.00% | 0 | 0 B | 1 | 16 | 16 |
| app_duty_user | 16.0 KB | 0.00% | 0 B | 16.0 KB | 0.00% | 0 | 0 B | 0 | 0 | 16 |
| integration_collect_task | 16.0 KB | 0.00% | 0 B | 16.0 KB | 0.00% | 0 | 0 B | 0 | 0 | 16 |
| data_works_instance | 16.0 KB | 0.00% | 0 B | 16.0 KB | 0.00% | 0 | 0 B | 0 | 0 | 16 |
| autofish_execution_info | 16.0 KB | 0.00% | 0 B | 16.0 KB | 0.00% | 0 | 0 B | 0 | 0 | 16 |
| activity_process_unit | 16.0 KB | 0.00% | 0 B | 16.0 KB | 0.00% | 0 | 0 B | 0 | 0 | 16 |
| autofish_ut_meta_data | 16.0 KB | 0.00% | 0 B | 16.0 KB | 0.00% | 0 | 0 B | 0 | 0 | 16 |
| idle_qa_info | 16.0 KB | 0.00% | 0 B | 16.0 KB | 0.00% | 0 | 0 B | 0 | 0 | 16 |
| activity_dev_delivery | 16.0 KB | 0.00% | 0 B | 16.0 KB | 0.00% | 0 | 0 B | 0 | 0 | 16 |
| gitlab_webhook_proxy_table | 16.0 KB | 0.00% | 0 B | 16.0 KB | 0.00% | 0 | 0 B | 0 | 0 | 16 |
| idle_longmen_test_submit | 16.0 KB | 0.00% | 0 B | 16.0 KB | 0.00% | 0 | 0 B | 0 | 0 | 16 |
| autofish_device_info | 16.0 KB | 0.00% | 0 B | 16.0 KB | 0.00% | 0 | 0 B | 0 | 0 | 16 |
| activity_delay_log | 16.0 KB | 0.00% | 0 B | 16.0 KB | 0.00% | 0 | 0 B | 0 | 0 | 16 |
| fe_alarm_record | 16.0 KB | 0.00% | 0 B | 16.0 KB | 0.00% | 0 | 0 B | 0 | 0 | 16 |
| smart_ui_task_result_info | 16.0 KB | 0.00% | 0 B | 16.0 KB | 0.00% | 0 | 0 B | 0 | 0 | 16 |
| autofish_device_adapt_task | 16.0 KB | 0.00% | 0 B | 16.0 KB | 0.00% | 0 | 0 B | 0 | 0 | 16 |
| config_change | 16.0 KB | 0.00% | 0 B | 16.0 KB | 0.00% | 0 | 0 B | 0 | 0 | 16 |
| idle_pl_project | 16.0 KB | 0.00% | 0 B | 16.0 KB | 0.00% | 0 | 0 B | 0 | 0 | 16 |
| autofish_department_info | 16.0 KB | 0.00% | 0 B | 16.0 KB | 0.00% | 0 | 0 B | 0 | 0 | 16 |
| activity_checklist | 16.0 KB | 0.00% | 0 B | 16.0 KB | 0.00% | 0 | 0 B | 0 | 0 | 16 |
| efficiency_assistant_update_data | 16.0 KB | 0.00% | 0 B | 16.0 KB | 0.00% | 0 | 0 B | 0 | 0 | 16 |
| autofish_package_info | 16.0 KB | 0.00% | 0 B | 16.0 KB | 0.00% | 0 | 0 B | 0 | 0 | 16 |
| autofish_tracking_duration | 16.0 KB | 0.00% | 0 B | 16.0 KB | 0.00% | 0 | 0 B | 0 | 0 | 16 |
| idle_drill_search | 16.0 KB | 0.00% | 0 B | 16.0 KB | 0.00% | 0 | 0 B | 0 | 0 | 16 |
| autofish_common_attribute | 16.0 KB | 0.00% | 0 B | 16.0 KB | 0.00% | 0 | 0 B | 0 | 0 | 16 |
| mock_project | 16.0 KB | 0.00% | 0 B | 16.0 KB | 0.00% | 0 | 0 B | 0 | 0 | 16 |
| autofish_testcase_info | 16.0 KB | 0.00% | 0 B | 16.0 KB | 0.00% | 0 | 0 B | 0 | 0 | 16 |
| efficiency_assistant_auto_data | 16.0 KB | 0.00% | 0 B | 16.0 KB | 0.00% | 0 | 0 B | 0 | 0 | 16 |
| idle_quark_tag_data | 16.0 KB | 0.00% | 0 B | 16.0 KB | 0.00% | 0 | 0 B | 0 | 0 | 16 |
| activity_rule_map | 16.0 KB | 0.00% | 0 B | 16.0 KB | 0.00% | 0 | 0 B | 0 | 0 | 16 |
| activity_metrics | 16.0 KB | 0.00% | 0 B | 16.0 KB | 0.00% | 0 | 0 B | 0 | 0 | 16 |
| autofish_relation_testcase_label | 16.0 KB | 0.00% | 0 B | 16.0 KB | 0.00% | 0 | 0 B | 0 | 0 | 16 |
| java_file_data_type_analysis | 16.0 KB | 0.00% | 0 B | 16.0 KB | 0.00% | 0 | 0 B | 0 | 0 | 16 |
| activity_req_change | 16.0 KB | 0.00% | 0 B | 16.0 KB | 0.00% | 0 | 0 B | 0 | 0 | 16 |
| autofish_mtl_package | 16.0 KB | 0.00% | 0 B | 16.0 KB | 0.00% | 0 | 0 B | 0 | 0 | 16 |
| autofish_catalog_info | 16.0 KB | 0.00% | 0 B | 16.0 KB | 0.00% | 0 | 0 B | 0 | 0 | 16 |
| app_emergent_integration_apply | 16.0 KB | 0.00% | 0 B | 16.0 KB | 0.00% | 0 | 0 B | 0 | 0 | 16 |
| autofish_testcase_collection_case | 16.0 KB | 0.00% | 0 B | 16.0 KB | 0.00% | 0 | 0 B | 0 | 0 | 16 |
| mock_api_mock | 16.0 KB | 0.00% | 0 B | 16.0 KB | 0.00% | 0 | 0 B | 0 | 0 | 16 |
| activity_question_answer | 16.0 KB | 0.00% | 0 B | 16.0 KB | 0.00% | 0 | 0 B | 0 | 0 | 16 |
| autofish_testrun_user | 16.0 KB | 0.00% | 0 B | 16.0 KB | 0.00% | 0 | 0 B | 0 | 0 | 16 |
| autofish_testcase_collection | 16.0 KB | 0.00% | 0 B | 16.0 KB | 0.00% | 0 | 0 B | 0 | 0 | 16 |
| activity_inspection_task | 16.0 KB | 0.00% | 0 B | 16.0 KB | 0.00% | 0 | 0 B | 0 | 0 | 16 |
| mock_api_define | 16.0 KB | 0.00% | 0 B | 16.0 KB | 0.00% | 0 | 0 B | 0 | 0 | 16 |
| activity_put_delivery | 16.0 KB | 0.00% | 0 B | 16.0 KB | 0.00% | 0 | 0 B | 0 | 0 | 16 |
| idle_quark_beta_tag_map | 16.0 KB | 0.00% | 0 B | 16.0 KB | 0.00% | 0 | 0 B | 0 | 0 | 16 |

## 空间优化-索引数据比大于1的表格
| 表（点击查看） | 表空间 | 表空间占比 | 索引空间 | 数据空间 | 碎片率 | 表行数 | 平均行长 | 索引数据比 | 索引大小 | 数据大小 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| idle_pl_app_report | 112 KB | 0.00% | 96.0 KB | 16.0 KB | 0.00% | 51 | 321 B | 6 | 96 | 16 |
| longmen_static_item_record | 112 KB | 0.00% | 96.0 KB | 16.0 KB | 0.00% | 0 | 0 B | 6 | 96 | 16 |
| miniprogram | 80.0 KB | 0.00% | 64.0 KB | 16.0 KB | 0.00% | 13 | 1.23 KB | 4 | 64 | 16 |
| longmen_static_check_rule | 80.0 KB | 0.00% | 64.0 KB | 16.0 KB | 0.00% | 3 | 5.33 KB | 4 | 64 | 16 |
| dag | 64.0 KB | 0.00% | 48.0 KB | 16.0 KB | 0.00% | 72 | 227 B | 3 | 48 | 16 |
| assembler_biz_record | 64.0 KB | 0.00% | 48.0 KB | 16.0 KB | 0.00% | 22 | 744 B | 3 | 48 | 16 |
| miniprogram_builder_record | 64.0 KB | 0.00% | 48.0 KB | 16.0 KB | 0.00% | 8 | 2.00 KB | 3 | 48 | 16 |
| dag_event | 64.0 KB | 0.00% | 48.0 KB | 16.0 KB | 0.00% | 8 | 2.00 KB | 3 | 48 | 16 |
| smart_dw_metric_v2_dwd_workitem_status_log_ref_xy_v2 | 159 MB | 0.29% | 116 MB | 42.6 MB | 3.05% | 513252 | 87.0 B | 2.723004695 | 118784 | 43622.4 |
| sre_team_score_detail | 17.6 MB | 0.03% | 12.1 MB | 5.52 MB | 18.48% | 35292 | 163 B | 2.192028986 | 12390.4 | 5652.48 |
| odps_table_partition | 53.2 MB | 0.10% | 36.1 MB | 17.1 MB | 59.15% | 65365 | 273 B | 2.111111111 | 36966.4 | 17510.4 |
| idle_dependency_entrance | 13.6 MB | 0.03% | 9.06 MB | 4.52 MB | 22.76% | 20123 | 235 B | 2.004424779 | 9277.44 | 4628.48 |
| newtc_testsets | 48.0 KB | 0.00% | 32.0 KB | 16.0 KB | 0.00% | 35 | 468 B | 2 | 32 | 16 |
| longmen_log_sls_config | 48.0 KB | 0.00% | 32.0 KB | 16.0 KB | 0.00% | 33 | 496 B | 2 | 32 | 16 |
| idle_drill_task | 48.0 KB | 0.00% | 32.0 KB | 16.0 KB | 0.00% | 25 | 655 B | 2 | 32 | 16 |
| sre_sub_config | 48.0 KB | 0.00% | 32.0 KB | 16.0 KB | 0.00% | 24 | 682 B | 2 | 32 | 16 |
| idle_common_patrol_record | 48.0 KB | 0.00% | 32.0 KB | 16.0 KB | 0.00% | 20 | 819 B | 2 | 32 | 16 |
| idle_app_db | 48.0 KB | 0.00% | 32.0 KB | 16.0 KB | 0.00% | 14 | 1.14 KB | 2 | 32 | 16 |
| assembler | 48.0 KB | 0.00% | 32.0 KB | 16.0 KB | 0.00% | 14 | 1.14 KB | 2 | 32 | 16 |
| sre_main_config | 48.0 KB | 0.00% | 32.0 KB | 16.0 KB | 0.00% | 10 | 1.60 KB | 2 | 32 | 16 |
| assembler_template | 48.0 KB | 0.00% | 32.0 KB | 16.0 KB | 0.00% | 6 | 2.67 KB | 2 | 32 | 16 |
| miniprogram_iteration | 48.0 KB | 0.00% | 32.0 KB | 16.0 KB | 0.00% | 4 | 4.00 KB | 2 | 32 | 16 |
| idle_quark_beta_data | 48.0 KB | 0.00% | 32.0 KB | 16.0 KB | 0.00% | 2 | 8.00 KB | 2 | 32 | 16 |
| idle_quark_reactor_data | 48.0 KB | 0.00% | 32.0 KB | 16.0 KB | 0.00% | 1 | 16.0 KB | 2 | 32 | 16 |
| log_store_query_detail | 48.0 KB | 0.00% | 32.0 KB | 16.0 KB | 0.00% | 0 | 0 B | 2 | 32 | 16 |
| entrance_graph | 48.0 KB | 0.00% | 32.0 KB | 16.0 KB | 0.00% | 0 | 0 B | 2 | 32 | 16 |
| xianyu_entrance_info | 14.0 MB | 0.03% | 8.44 MB | 5.52 MB | 22.28% | 17115 | 337 B | 1.528985507 | 8642.56 | 5652.48 |
| sre_main_score_detail | 161 MB | 0.30% | 90.4 MB | 70.6 MB | 3.01% | 339272 | 218 B | 1.280453258 | 92569.6 | 72294.4 |
| longmen_static_method_entrance_record | 14.1 MB | 0.03% | 7.58 MB | 6.52 MB | 22.11% | 23476 | 291 B | 1.162576687 | 7761.92 | 6676.48 |
| sunfire_alarm_result | 323 MB | 0.60% | 172 MB | 151 MB | 81.39% | 0 | 0 B | 1.139072848 | 176128 | 154624 |
| longmen_static_method_record | 1.33 GB | 2.52% | 715 MB | 643 MB | 0.44% | 938746 | 718 B | 1.111975117 | 732160 | 658432 |
| sre_person_rank | 72.8 MB | 0.14% | 38.2 MB | 34.6 MB | 6.43% | 157539 | 230 B | 1.104046243 | 39116.8 | 35430.4 |
| dwd_change_workitem_relation | 16.8 MB | 0.03% | 8.81 MB | 8.02 MB | 19.20% | 38512 | 218 B | 1.098503741 | 9021.44 | 8212.48 |
| sre_sub_score_detail | 316 MB | 0.59% | 163 MB | 153 MB | 1.25% | 818064 | 195 B | 1.065359477 | 166912 | 156672 |


## 空间分析-原始数据
[表空间.xlsx](https://yuque.antfin.com/attachments/lark/0/2024/xlsx/137756471/1720532798013-56aa6a7b-4b89-4038-b714-2139012e1e4c.xlsx)

加上索引数据比的表格
[表空间.xlsx](https://yuque.antfin.com/attachments/lark/0/2024/xlsx/137756471/1720753977173-6afc8739-8776-4f85-afe3-d7456a1d2fe1.xlsx)


