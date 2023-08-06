#!/usr/bin/python3
# -*- coding:utf-8 -*-

desc_dict={
    "股票列表": {
        "api":"stock_basic",
        "desc": """接口：stock_basic
描述：获取基础信息数据，包括股票代码、名称、上市日期、退市日期等

输入参数
名称\t\t类型\t必选\t描述
is_hs\t\tstr\tN\t是否沪深港通标的，N否 H沪股通 S深股通
list_status\t\tstr\tN\t上市状态 L上市 D退市 P暂停上市，默认是L
exchange\t\tstr\tN\t交易所 SSE上交所 SZSE深交所
ts_code\t\tstr\tN\tTS股票代码
market\t\tstr\tN\t市场类别
limit\t\tint\tN\t取多少条数据
offset\t\tint\tN\t从第几条开始取
name\t\tstr\tN\t名称

输出参数
名称\t\t类型\t默认显示\t描述
ts_code\t\tstr\tY\tTS代码
symbol\t\tstr\tY\t股票代码
name\t\tstr\tY\t股票名称
area\t\tstr\tY\t地域
industry\t\tstr\tY\t所属行业
fullname\t\tstr\tN\t股票全称
enname\t\tstr\tN\t英文全称
cnspell\t\tstr\tN\t拼音缩写
market\t\tstr\tY\t市场类型（主板/创业板/科创板/CDR）
exchange\t\tstr\tN\t交易所代码
curr_type\t\tstr\tN\t交易货币
list_status\t\tstr\tN\t上市状态 L上市 D退市 P暂停上市
list_date\t\tstr\tY\t上市日期
delist_date\t\tstr\tN\t退市日期
is_hs\t\tstr\tN\t是否沪深港通标的，N否 H沪股通 S深股通
"""},
    "交易日历": {
        "api":"trade_cal",
        "desc":"""接口：trade_cal
描述：获取各大交易所交易日历数据,默认提取的是上交所

输入参数
名称\t\t类型\t必选\t描述
exchange\t\tstr\tN\t交易所 SSE上交所,SZSE深交所,CFFEX 中金所,SHFE 上期所,CZCE 郑商所,DCE 大商所,INE 上能源,IB 银行间,XHKG 港交所
start_date\t\tstr\tN\t开始日期 （格式：YYYYMMDD 下同）
end_date\t\tstr\tN\t结束日期
is_open\t\tstr\tN\t是否交易 '0'休市 '1'交易

输出参数
名称\t\t类型\t默认显示\t描述
exchange\t\tstr\tY\t交易所 SSE上交所 SZSE深交所
cal_date\t\tstr\tY\t日历日期
is_open\t\tstr\tY\t是否交易 0休市 1交易
pretrade_date\t\tstr\tN\t上一个交易日
        """
    },
    "股票曾用名": {
        "api":"namechange",
        "desc":"""接口：namechange
描述：历史名称变更记录

输入参数
名称\t\t类型\t必选\t描述
ts_code\t\tstr\tN\tTS代码
start_date\t\tstr\tN\t公告开始日期
end_date\t\tstr\tN\t公告结束日期

输出参数
名称\t\t类型\t默认输出\t描述
ts_code\t\tstr\tY\tTS代码
name\t\tstr\tY\t证券名称
start_date\t\tstr\tY\t开始日期
end_date\t\tstr\tY 	结束日期
ann_date\t\tstr\tY\t公告日期
change_reason\t\tstr\tY\t变更原因
        """
    },
    "沪深股通成分股": {
        "api":"hs_const",
        "desc":"""接口：hs_const
描述：获取沪股通、深股通成分数据

输入参数
名称\t\t类型\t必选\t描述
hs_type\t\tstr\tY\t类型SH沪股通SZ深股通
is_new\t\tstr\tN\t是否最新 1 是 0 否 (默认1)


输出参数
名称\t\t类型\t默认显示\t描述
ts_code\t\tstr\tY\tTS代码
hs_type\t\tstr\tY\t沪深港通类型SH沪SZ深
in_date\t\tstr\tY\t纳入日期
out_date\t\tstr\tY\t剔除日期
is_new\t\tstr\tY\t是否最新 1是 0否
        """
    },
    "上市公司基本信息": {
        "api":"stock_company",
        "desc":"""接口：stock_company
描述：获取上市公司基础信息，单次提取4500条，可以根据交易所分批提取
积分：用户需要至少120积分才可以调取，具体请参阅积分获取办法

输入参数
名称\t\t类型\t必须\t描述
ts_code\t\tstr\tN\t股票代码
exchange\t\tstr\tN\t交易所代码 ，SSE上交所 SZSE深交所

输出参数
名称\t\t类型\t默认显示\t描述
ts_code\t\tstr\tY\t股票代码
exchange\t\tstr\tY\t交易所代码 ，SSE上交所 SZSE深交所
chairman\t\tstr\tY\t法人代表
manager\t\tstr\tY\t总经理
secretary\t\tstr\tY\t董秘
reg_capital\t\tfloat\tY\t注册资本
setup_date\t\tstr\tY\t注册日期
province\t\tstr\tY\t所在省份
city\t\tstr\tY\t所在城市
introduction\t\tstr\tN\t公司介绍
website\t\tstr\tY\t公司主页
email\t\tstr\tY\t电子邮件
office\t\tstr\tN\t办公室
employees\t\tint\tY\t员工人数
main_business\t\tstr\tN\t主要业务及产品
business_scope\t\tstr\tN\t经营范围
        """
    },
    "上市公司管理层": {
        "api":"stk_managers",
        "desc":"""接口：stk_managers
描述：获取上市公司管理层
积分：用户需要2000积分才可以调取，5000积分以上频次相对较高，具体请参阅积分获取办法

输入参数
名称\t\t类型\t必选\t描述
ts_code\t\tstr\tN\t股票代码，支持单个或多个股票输入
ann_date\t\tstr\tN\t公告日期（YYYYMMDD格式，下同）
start_date\t\tstr\tN\t公告开始日期
end_date\t\tstr\tN\t公告结束日期

输出参数
名称\t\t类型\t默认显示\t描述
ts_code\t\tstr\tY\tTS股票代码
ann_date\t\tstr\tY\t公告日期
name\t\tstr\tY\t姓名
gender\t\tstr\tY\t性别
lev\t\tstr\tY\t岗位类别
title\t\tstr\tY\t岗位
edu\t\tstr\tY\t学历
national\t\tstr\tY\t国籍
birthday\t\tstr\tY\t出生年月
begin_date\t\tstr\tY\t上任日期
end_date\t\tstr\tY\t离任日期
resume\t\tstr\tN\t个人简历
        """
    },
    "管理层薪酬和持股": {
        "api":"stk_rewards",
        "desc":"""接口：stk_rewards
描述：获取上市公司管理层薪酬和持股
积分：用户需要2000积分才可以调取，5000积分以上频次相对较高，具体请参阅积分获取办法

输入参数
名称\t\t类型\t必选\t描述
ts_code\t\tstr\tY\tTS股票代码，支持单个或多个代码输入
end_date\t\tstr\tN\t报告期

输出参数
名称\t\t类型\t默认显示\t描述
ts_code\t\tstr\tY\tTS股票代码
ann_date\t\tstr\tY\t公告日期
end_date\t\tstr\tY\t截止日期
name\t\tstr\tY\t姓名
title\t\tstr\tY\t职务
reward\t\tfloat\tY\t报酬
hold_vol\t\tfloat\tY\t持股数
        """
    },
    "IPO新股上市": {
        "api":"new_share",
        "desc":"""接口：new_share
描述：获取新股上市列表数据
限量：单次最大2000条，总量不限制
积分：用户需要至少120积分才可以调取，具体请参阅积分获取办法

输入参数
名称\t\t类型\t必选\t描述
start_date\t\tstr\tN\t上网发行开始日期
end_date\t\tstr\tN\t上网发行结束日期

输出参数
名称\t\t类型\t默认显示\t描述
ts_code\t\tstr\tY\tTS股票代码
sub_code\t\tstr\tY\t申购代码
name\t\tstr\tY\t名称
ipo_date\t\tstr\tY\t上网发行日期
issue_date\t\tstr\tY\t上市日期
amount\t\tfloat\tY\t发行总量（万股）
market_amount\t\tfloat\tY\t上网发行总量（万股）
price\t\tfloat\tY\t发行价格
pe\t\tfloat\tY\t市盈率
limit_amount\t\tfloat\tY\t个人申购上限（万股）
funds\t\tfloat\tY\t募集资金（亿元）
ballot\t\tfloat\tY\t中签率
        """
    },
    "备用列表": {
        "api":"bak_basic",
        "desc":"""接口：bak_basic
描述：获取备用基础列表
限量：单次最大5000，可以根据日期参数循环获取历史

输入参数
名称\t\t类型\t必选\t描述
trade_date\t\tstr\tN\t交易日期
ts_code\t\tstr\tN\t股票代码

输出参数
名称\t\t类型\t默认显示\t描述
trade_date\t\tstr\tY\t交易日期
ts_code\t\tstr\tY\tTS股票代码
name\t\tstr\tY\t股票名称
industry\t\tstr\tY\t行业
area\t\tstr\tY\t地域
pe\t\tfloat\tY\t市盈率（动）
float_share\t\tfloat\tY\t流通股本（万）
total_share\t\tfloat\tY\t总股本（万）
total_assets\t\tfloat\tY\t总资产（万）
liquid_assets\t\tfloat\tY\t流动资产（万）
fixed_assets\t\tfloat\tY\t固定资产（万）
reserved\t\tfloat\tY\t公积金
reserved_pershare\t\tfloat\tY\t每股公积金
eps\t\tfloat\tY\t每股收益
bvps\t\tfloat\tY\t每股净资产
pb\t\tfloat\tY\t市净率
list_date\t\tstr\tY\t上市日期
undp\t\tfloat\tY\t未分配利润
per_undp\t\tfloat\tY\t每股未分配利润
rev_yoy\t\tfloat\tY\t收入同比（%）
profit_yoy\t\tfloat\tY\t利润同比（%）
gpr\t\tfloat\tY\t毛利率（%）
npr\t\tfloat\tY\t净利润率（%）
holder_num\t\tint\tY\t股东人数
        """
    },
    "日线行情": {
        "api":"daily",
        "desc":"""接口：daily
数据说明：交易日每天15点～16点之间。本接口是未复权行情，停牌期间不提供数据。
调取说明：基础积分每分钟内最多调取500次，每次5000条数据，相当于23年历史，用户获得超过5000积分正常调取无频次限制。
描述：获取股票行情数据，或通过通用行情接口获取数据，包含了前后复权数据。

输入参数
名称 	类型 	必选 	描述
ts_code 	str 	N 	股票代码（支持多个股票同时提取，逗号分隔）
trade_date 	str 	N 	交易日期（YYYYMMDD）
start_date 	str 	N 	开始日期(YYYYMMDD)
end_date 	str 	N 	结束日期(YYYYMMDD)

注：日期都填YYYYMMDD格式，比如20181010

输出参数
名称 	类型 	描述
ts_code 	str 	股票代码
trade_date 	str 	交易日期
open 	float 	开盘价
high 	float 	最高价
low 	float 	最低价
close 	float 	收盘价
pre_close 	float 	昨收价
change 	float 	涨跌额
pct_chg 	float 	涨跌幅 （未复权，如果是复权请用 通用行情接口 ）
vol 	float 	成交量 （手）
amount 	float 	成交额 （千元）
        """
    },
    "周线行情": {
        "api":"weekly",
        "desc":"""接口：weekly
描述：获取A股周线行情
限量：单次最大4500行，总量不限制
积分：用户需要至少300积分才可以调取，具体请参阅积分获取办法


输入参数
名称 	类型 	必选 	描述
ts_code 	str 	N 	TS代码 （ts_code,trade_date两个参数任选一）
trade_date 	str 	N 	交易日期 （每周最后一个交易日期，YYYYMMDD格式）
start_date 	str 	N 	开始日期
end_date 	str 	N 	结束日期


输出参数
名称 	类型 	默认显示 	描述
ts_code 	str 	Y 	股票代码
trade_date 	str 	Y 	交易日期
close 	float 	Y 	周收盘价
open 	float 	Y 	周开盘价
high 	float 	Y 	周最高价
low 	float 	Y 	周最低价
pre_close 	float 	Y 	上一周收盘价
change 	float 	Y 	周涨跌额
pct_chg 	float 	Y 	周涨跌幅 （未复权，如果是复权请用 通用行情接口 ）
vol 	float 	Y 	周成交量
amount 	float 	Y 	周成交额
        """
    },
    "月线行情": {
        "api":"monthly",
        "desc":"""接口：monthly
描述：获取A股月线数据
限量：单次最大4500行，总量不限制
积分：用户需要至少300积分才可以调取，具体请参阅积分获取办法

输入参数
名称 	类型 	必选 	描述
ts_code 	str 	N 	TS代码 （ts_code,trade_date两个参数任选一）
trade_date 	str 	N 	交易日期 （每月最后一个交易日日期，YYYYMMDD格式）
start_date 	str 	N 	开始日期
end_date 	str 	N 	结束日期

输出参数
名称 	类型 	默认显示 	描述
ts_code 	str 	Y 	股票代码
trade_date 	str 	Y 	交易日期
close 	float 	Y 	月收盘价
open 	float 	Y 	月开盘价
high 	float 	Y 	月最高价
low 	float 	Y 	月最低价
pre_close 	float 	Y 	上月收盘价
change 	float 	Y 	月涨跌额
pct_chg 	float 	Y 	月涨跌幅 （未复权，如果是复权请用 通用行情接口 ）
vol 	float 	Y 	月成交量
amount 	float 	Y 	月成交额
        """
    },
    "复权行情": {
        "api":"pro_bar",
        "desc":"""接口名称 ：pro_bar
接口说明 ：复权行情通过通用行情接口实现，利用Tushare Pro提供的复权因子进行计算，目前暂时只在SDK中提供支持，http方式无法调取。
Python SDK版本要求： >= 1.2.26


复权说明
类型 	算法 	参数标识
不复权 	无 	空或None
前复权 	当日收盘价 × 当日复权因子 / 最新复权因子 	qfq
后复权 	当日收盘价 × 当日复权因子 	hfq

注：目前支持A股的日线/周线/月线复权，分钟复权稍后支持


接口参数
名称 	类型 	必选 	描述
ts_code 	str 	Y 	证券代码
start_date 	str 	N 	开始日期 (格式：YYYYMMDD)
end_date 	str 	N 	结束日期 (格式：YYYYMMDD)
asset 	str 	Y 	资产类别：E股票 I沪深指数 C数字货币 FT期货 FD基金 O期权，默认E
adj 	str 	N 	复权类型(只针对股票)：None未复权 qfq前复权 hfq后复权 , 默认None
freq 	str 	Y 	数据频度 ：1MIN表示1分钟（1/5/15/30/60分钟） D日线 ，默认D
ma 	list 	N 	均线，支持任意周期的均价和均量，输入任意合理int数值
        """
    },
    "股票复权因子": {
        "api":"adj_factor",
        "desc":"""接口：adj_factor
更新时间：早上9点30分
描述：获取股票复权因子，可提取单只股票全部历史复权因子，也可以提取单日全部股票的复权因子。

输入参数
名称 	类型 	必选 	描述
ts_code 	str 	Y 	股票代码
trade_date 	str 	N 	交易日期(YYYYMMDD，下同)
start_date 	str 	N 	开始日期
end_date 	str 	N 	结束日期

注：日期都填YYYYMMDD格式，比如20181010

输出参数
名称 	类型 	描述
ts_code 	str 	股票代码
trade_date 	str 	交易日期
adj_factor 	float 	复权因子
        """
    },
    "停复牌信息(停)": {
        "api":"suspend",
        "desc":"""接口：suspend
更新时间：不定期
描述：获取股票每日停复牌信息

输入参数
名称 	类型 	必选 	描述
ts_code 	str 	N 	股票代码(三选一)
suspend_date 	str 	N 	停牌日期(三选一)
resume_date 	str 	N 	复牌日期(三选一)

输出参数
名称 	类型 	描述
ts_code 	str 	股票代码
suspend_date 	str 	停牌日期
resume_date 	str 	复牌日期
ann_date 	str 	公告日期
suspend_reason 	str 	停牌原因
reason_type 	str 	停牌原因类别
        """
    },
    "每日停复牌信息": {
        "api":"suspend_d",
        "desc":"""接口：suspend_d
更新时间：不定期
描述：按日期方式获取股票每日停复牌信息

输入参数
名称 	类型 	必选 	描述
ts_code 	str 	N 	股票代码(可输入多值)
trade_date 	str 	N 	交易日日期
start_date 	str 	N 	停复牌查询开始日期
end_date 	str 	N 	停复牌查询结束日期
suspend_type 	str 	N 	停复牌类型：S-停牌,R-复牌

输出参数
名称 	类型 	默认显示 	描述
ts_code 	str 	Y 	TS代码
trade_date 	str 	Y 	停复牌日期
suspend_timing 	str 	Y 	日内停牌时间段
suspend_type 	str 	Y 	停复牌类型：S-停牌，R-复牌
        """
    },
    "每日指标": {
        "api":"daily_basic",
        "desc":"""接口：daily_basic
更新时间：交易日每日15点～17点之间
描述：获取全部股票每日重要的基本面指标，可用于选股分析、报表展示等。
积分：用户需要至少600积分才可以调取，具体请参阅积分获取办法

输入参数
名称 	类型 	必选 	描述
ts_code 	str 	Y 	股票代码（二选一）
trade_date 	str 	N 	交易日期 （二选一）
start_date 	str 	N 	开始日期(YYYYMMDD)
end_date 	str 	N 	结束日期(YYYYMMDD)

注：日期都填YYYYMMDD格式，比如20181010

输出参数
名称 	类型 	描述
ts_code 	str 	TS股票代码
trade_date 	str 	交易日期
close 	float 	当日收盘价
turnover_rate 	float 	换手率（%）
turnover_rate_f 	float 	换手率（自由流通股）
volume_ratio 	float 	量比
pe 	float 	市盈率（总市值/净利润， 亏损的PE为空）
pe_ttm 	float 	市盈率（TTM，亏损的PE为空）
pb 	float 	市净率（总市值/净资产）
ps 	float 	市销率
ps_ttm 	float 	市销率（TTM）
dv_ratio 	float 	股息率 （%）
dv_ttm 	float 	股息率（TTM）（%）
total_share 	float 	总股本 （万股）
float_share 	float 	流通股本 （万股）
free_share 	float 	自由流通股本 （万）
total_mv 	float 	总市值 （万元）
circ_mv 	float 	流通市值（万元）
        """
    },
    "通用行情接口": {
        "api":"pro_bar",
        "desc":"""接口名称：pro_bar
更新时间：股票和指数通常在15点～17点之间，数字货币实时更新，具体请参考各接口文档明细。
描述：目前整合了股票（未复权、前复权、后复权）、指数、数字货币、ETF基金、期货、期权的行情数据，未来还将整合包括外汇在内的所有交易行情数据，同时提供分钟数据。不同数据对应不同的积分要求，具体请参阅每类数据的文档说明。
其它：由于本接口是集成接口，在SDK层做了一些逻辑处理，目前暂时没法用http的方式调取通用行情接口。用户可以访问Tushare的Github，查看源代码完成类似功能。

输入参数
名称 	类型 	必选 	描述
ts_code 	str 	Y 	证券代码，不支持多值输入，多值输入获取结果会有重复记录
api 	str 	N 	pro版api对象，如果初始化了set_token，此参数可以不需要
start_date 	str 	N 	开始日期 (格式：YYYYMMDD，提取分钟数据请用2019-09-01 09:00:00这种格式)
end_date 	str 	N 	结束日期 (格式：YYYYMMDD)
asset 	str 	Y 	资产类别：E股票 I沪深指数 C数字货币 FT期货 FD基金 O期权 CB可转债（v1.2.39），默认E
adj 	str 	N 	复权类型(只针对股票)：None未复权 qfq前复权 hfq后复权 , 默认None，目前只支持日线复权。
freq 	str 	Y 	数据频度 ：支持分钟(min)/日(D)/周(W)/月(M)K线，其中1min表示1分钟（类推1/5/15/30/60分钟） ，默认D。对于分钟数据有600积分用户可以试用（请求2次），正式权限请在QQ群私信群主或积分管理员。
ma 	list 	N 	均线，支持任意合理int数值。注：均线是动态计算，要设置一定时间范围才能获得相应的均线，比如5日均线，开始和结束日期参数跨度必须要超过5日。目前只支持单一个股票提取均线，即需要输入ts_code参数。
factors 	list 	N 	股票因子（asset='E'有效）支持 tor换手率 vr量比
adjfactor 	str 	N 	复权因子，在复权数据时，如果此参数为True，返回的数据中则带复权因子，默认为False。 该功能从1.2.33版本开始生效

输出指标

具体输出的数据指标可参考基础数据接口中的各行情指标
        """
    },
    "个股资金流向": {
        "api":"moneyflow",
        "desc":"""接口：moneyflow
描述：获取沪深A股票资金流向数据，分析大单小单成交情况，用于判别资金动向
限量：单次最大提取4500行记录，总量不限制
积分：用户需要至少2000积分才可以调取，基础积分有流量控制，积分越多权限越大，请自行提高积分，具体请参阅积分获取办法


输入参数
名称 	类型 	必选 	描述
ts_code 	str 	N 	股票代码 （股票和时间参数至少输入一个）
trade_date 	str 	N 	交易日期
start_date 	str 	N 	开始日期
end_date 	str 	N 	结束日期


输出参数
名称 	类型 	默认显示 	描述
ts_code 	str 	Y 	TS代码
trade_date 	str 	Y 	交易日期
buy_sm_vol 	int 	Y 	小单买入量（手）
buy_sm_amount 	float 	Y 	小单买入金额（万元）
sell_sm_vol 	int 	Y 	小单卖出量（手）
sell_sm_amount 	float 	Y 	小单卖出金额（万元）
buy_md_vol 	int 	Y 	中单买入量（手）
buy_md_amount 	float 	Y 	中单买入金额（万元）
sell_md_vol 	int 	Y 	中单卖出量（手）
sell_md_amount 	float 	Y 	中单卖出金额（万元）
buy_lg_vol 	int 	Y 	大单买入量（手）
buy_lg_amount 	float 	Y 	大单买入金额（万元）
sell_lg_vol 	int 	Y 	大单卖出量（手）
sell_lg_amount 	float 	Y 	大单卖出金额（万元）
buy_elg_vol 	int 	Y 	特大单买入量（手）
buy_elg_amount 	float 	Y 	特大单买入金额（万元）
sell_elg_vol 	int 	Y 	特大单卖出量（手）
sell_elg_amount 	float 	Y 	特大单卖出金额（万元）
net_mf_vol 	int 	Y 	净流入量（手）
net_mf_amount 	float 	Y 	净流入额（万元）

各类别统计规则如下：
小单：5万以下 中单：5万～20万 大单：20万～100万 特大单：成交额>=100万 
        """
    },
    "每日涨跌停价格": {
        "api":"stk_limit",
        "desc":"""接口：stk_limit
描述：获取全市场（包含A/B股和基金）每日涨跌停价格，包括涨停价格，跌停价格等，每个交易日8点40左右更新当日股票涨跌停价格。
限量：单次最多提取4800条记录，可循环调取，总量不限制
积分：用户积600积分可调取，单位分钟有流控，积分越高流量越大，请自行提高积分，具体请参阅积分获取办法


输入参数
名称 	类型 	必选 	描述
ts_code 	str 	N 	股票代码
trade_date 	str 	N 	交易日期
start_date 	str 	N 	开始日期
end_date 	str 	N 	结束日期


输出参数
名称 	类型 	默认显示 	描述
trade_date 	str 	Y 	交易日期
ts_code 	str 	Y 	TS股票代码
pre_close 	float 	N 	昨日收盘价
up_limit 	float 	Y 	涨停价
down_limit 	float 	Y 	跌停价
        """
    },
    "每日涨跌停统计": {
        "api":"limit_list",
        "desc":"""接口：limit_list
描述：获取每日涨跌停股票统计，包括封闭时间和打开次数等数据，帮助用户快速定位近期强（弱）势股，以及研究超短线策略。
限量：单次最大1000，总量不限制
积分：用户积2000积分可调取，5000积分以上可高频使用，具体请参阅积分获取办法


输入参数
名称 	类型 	必选 	描述
trade_date 	str 	N 	交易日期 YYYYMMDD格式，支持单个或多日期输入
ts_code 	str 	N 	股票代码 （支持单个或多个股票输入）
limit_type 	str 	N 	涨跌停类型：U涨停D跌停
start_date 	str 	N 	开始日期 YYYYMMDD格式
end_date 	str 	N 	结束日期 YYYYMMDD格式


输出参数
名称 	类型 	默认显示 	描述
trade_date 	str 	Y 	交易日期
ts_code 	str 	Y 	股票代码
name 	str 	Y 	股票名称
close 	float 	Y 	收盘价
pct_chg 	float 	Y 	涨跌幅
amp 	float 	Y 	振幅
fc_ratio 	float 	Y 	封单金额/日成交金额
fl_ratio 	float 	Y 	封单手数/流通股本
fd_amount 	float 	Y 	封单金额
first_time 	str 	Y 	首次涨停时间
last_time 	str 	Y 	最后封板时间
open_times 	int 	Y 	打开次数
strth 	float 	Y 	涨跌停强度
limit 	str 	Y 	D跌停U涨停
        """
    },
    "沪深港通资金流向": {
        "api":"moneyflow_hsgt",
        "desc":"""接口：moneyflow_hsgt
描述：获取沪股通、深股通、港股通每日资金流向数据，每次最多返回300条记录，总量不限制。

输入参数
名称 	类型 	必选 	描述
trade_date 	str 	N 	交易日期 (二选一)
start_date 	str 	N 	开始日期 (二选一)
end_date 	str 	N 	结束日期

输出参数
名称 	类型 	描述
trade_date 	str 	交易日期
ggt_ss 	float 	港股通（上海）
ggt_sz 	float 	港股通（深圳）
hgt 	float 	沪股通（百万元）
sgt 	float 	深股通（百万元）
north_money 	float 	北向资金（百万元）
south_money 	float 	南向资金（百万元）
        """
    },
    "沪深股通十大成交股": {
        "api":"hsgt_top10",
        "desc":"""接口：hsgt_top10
描述：获取沪股通、深股通每日前十大成交详细数据

输入参数
名称 	类型 	必选 	描述
ts_code 	str 	N 	股票代码（二选一）
trade_date 	str 	N 	交易日期（二选一）
start_date 	str 	N 	开始日期
end_date 	str 	N 	结束日期
market_type 	str 	N 	市场类型（1：沪市 3：深市）

输出参数
名称 	类型 	描述
trade_date 	str 	交易日期
ts_code 	str 	股票代码
name 	str 	股票名称
close 	float 	收盘价
change 	float 	涨跌额
rank 	int 	资金排名
market_type 	str 	市场类型（1：沪市 3：深市）
amount 	float 	成交金额（元）
net_amount 	float 	净成交金额（元）
buy 	float 	买入金额（元）
sell 	float 	卖出金额（元）
        """
    },
    "沪深股通持股明细": {
        "api":"hk_hold",
        "desc":"""接口：hk_hold
描述：获取沪深港股通持股明细，数据来源港交所。
限量：单次最多提取3800条记录，可循环调取，总量不限制
积分：用户积120积分可调取试用，2000积分可正常使用，单位分钟有流控，积分越高流量越大，请自行提高积分，具体请参阅积分获取办法


输入参数
名称 	类型 	必选 	描述
code 	str 	N 	交易所代码
ts_code 	str 	N 	TS股票代码
trade_date 	str 	N 	交易日期
start_date 	str 	N 	开始日期
end_date 	str 	N 	结束日期
exchange 	str 	N 	类型：SH沪股通（北向）SZ深股通（北向）HK港股通（南向持股）


输出参数
名称 	类型 	默认显示 	描述
code 	str 	Y 	原始代码
trade_date 	str 	Y 	交易日期
ts_code 	str 	Y 	TS代码
name 	str 	Y 	股票名称
vol 	int 	Y 	持股数量(股)
ratio 	float 	Y 	持股占比（%），占已发行股份百分比
exchange 	str 	Y 	类型：SH沪股通SZ深股通HK港股通
        """
    },
    "港股通每日成交统计": {
        "api":"ggt_daily",
        "desc":"""接口：ggt_daily
描述：获取港股通每日成交信息，数据从2014年开始
限量：单次最大1000，总量数据不限制
积分：用户积2000积分可调取，5000积分以上频次相对较高，请自行提高积分，具体请参阅积分获取办法


输入参数
名称 	类型 	必选 	描述
trade_date 	str 	N 	交易日期 （格式YYYYMMDD，下同。支持单日和多日输入）
start_date 	str 	N 	开始日期
end_date 	str 	N 	结束日期


输出参数
名称 	类型 	默认显示 	描述
trade_date 	str 	Y 	交易日期
buy_amount 	float 	Y 	买入成交金额（亿元）
buy_volume 	float 	Y 	买入成交笔数（万笔）
sell_amount 	float 	Y 	卖出成交金额（亿元）
sell_volume 	float 	Y 	卖出成交笔数（万笔）
        """
    },
    "港股通每月成交统计": {
        "api":"ggt_monthly",
        "desc":"""接口：ggt_monthly
描述：港股通每月成交信息，数据从2014年开始
限量：单次最大1000
积分：用户积5000积分可调取，请自行提高积分，具体请参阅积分获取办法


输入参数
名称 	类型 	必选 	描述
month 	str 	N 	月度（格式YYYYMM，下同，支持多个输入）
start_month 	str 	N 	开始月度
end_month 	str 	N 	结束月度


输出参数
名称 	类型 	默认显示 	描述
month 	str 	Y 	交易日期
day_buy_amt 	float 	Y 	当月日均买入成交金额（亿元）
day_buy_vol 	float 	Y 	当月日均买入成交笔数（万笔）
day_sell_amt 	float 	Y 	当月日均卖出成交金额（亿元）
day_sell_vol 	float 	Y 	当月日均卖出成交笔数（万笔）
total_buy_amt 	float 	Y 	总买入成交金额（亿元）
total_buy_vol 	float 	Y 	总买入成交笔数（万笔）
total_sell_amt 	float 	Y 	总卖出成交金额（亿元）
total_sell_vol 	float 	Y 	总卖出成交笔数（万笔）
        """
    },
    "备用行情": {
        "api":"bak_daily",
        "desc":"""接口：bak_daily
描述：获取备用行情，包括特定的行情指标
限量：单次最大5000行数据，可以根据日期参数循环获取

输入参数
名称 	类型 	必选 	描述
ts_code 	str 	N 	股票代码
trade_date 	str 	N 	交易日期
start_date 	str 	N 	开始日期
end_date 	str 	N 	结束日期
offset 	str 	N 	开始行数
limit 	str 	N 	最大行数

输出参数
名称 	类型 	默认显示 	描述
ts_code 	str 	Y 	股票代码
trade_date 	str 	Y 	交易日期
name 	str 	Y 	股票名称
pct_change 	float 	Y 	涨跌幅
close 	float 	Y 	收盘价
change 	float 	Y 	涨跌额
open 	float 	Y 	开盘价
high 	float 	Y 	最高价
low 	float 	Y 	最低价
pre_close 	float 	Y 	昨收价
vol_ratio 	float 	Y 	量比
turn_over 	float 	Y 	换手率
swing 	float 	Y 	振幅
vol 	float 	Y 	成交量
amount 	float 	Y 	成交额
selling 	float 	Y 	内盘（主动卖，手）
buying 	float 	Y 	外盘（主动买， 手）
total_share 	float 	Y 	总股本(万)
float_share 	float 	Y 	流通股本(万)
pe 	float 	Y 	市盈(动)
industry 	str 	Y 	所属行业
area 	str 	Y 	所属地域
float_mv 	float 	Y 	流通市值
total_mv 	float 	Y 	总市值
avg_price 	float 	Y 	平均价
strength 	float 	Y 	强弱度(%)
activity 	float 	Y 	活跃度(%)
avg_turnover 	float 	Y 	笔换手
attack 	float 	Y 	攻击波(%)
interval_3 	float 	Y 	近3月涨幅
interval_6 	float 	Y 	近6月涨幅
        """
    },
    "利润表": {
        "api":"income",
        "desc":"""接口：income
描述：获取上市公司财务利润表数据
积分：用户需要至少800积分才可以调取，具体请参阅积分获取办法

提示：当前接口只能按单只股票获取其历史数据，如果需要获取某一季度全部上市公司数据，请使用income_vip接口（参数一致），需积攒5000积分。

输入参数
名称 	类型 	必选 	描述
ts_code 	str 	Y 	股票代码
ann_date 	str 	N 	公告日期
start_date 	str 	N 	公告开始日期
end_date 	str 	N 	公告结束日期
period 	str 	N 	报告期(每个季度最后一天的日期，比如20171231表示年报)
report_type 	str 	N 	报告类型： 参考下表说明
comp_type 	str 	N 	公司类型：1一般工商业 2银行 3保险 4证券

输出参数
名称 	类型 	默认显示 	描述
ts_code 	str 	Y 	TS代码
ann_date 	str 	Y 	公告日期
f_ann_date 	str 	Y 	实际公告日期
end_date 	str 	Y 	报告期
report_type 	str 	Y 	报告类型 1合并报表 2单季合并 3调整单季合并表 4调整合并报表 5调整前合并报表 6母公司报表 7母公司单季表 8 母公司调整单季表 9母公司调整表 10母公司调整前报表 11调整前合并报表 12母公司调整前报表
comp_type 	str 	Y 	公司类型(1一般工商业2银行3保险4证券)
basic_eps 	float 	Y 	基本每股收益
diluted_eps 	float 	Y 	稀释每股收益
total_revenue 	float 	Y 	营业总收入
revenue 	float 	Y 	营业收入
int_income 	float 	Y 	利息收入
prem_earned 	float 	Y 	已赚保费
comm_income 	float 	Y 	手续费及佣金收入
n_commis_income 	float 	Y 	手续费及佣金净收入
n_oth_income 	float 	Y 	其他经营净收益
n_oth_b_income 	float 	Y 	加:其他业务净收益
prem_income 	float 	Y 	保险业务收入
out_prem 	float 	Y 	减:分出保费
une_prem_reser 	float 	Y 	提取未到期责任准备金
reins_income 	float 	Y 	其中:分保费收入
n_sec_tb_income 	float 	Y 	代理买卖证券业务净收入
n_sec_uw_income 	float 	Y 	证券承销业务净收入
n_asset_mg_income 	float 	Y 	受托客户资产管理业务净收入
oth_b_income 	float 	Y 	其他业务收入
fv_value_chg_gain 	float 	Y 	加:公允价值变动净收益
invest_income 	float 	Y 	加:投资净收益
ass_invest_income 	float 	Y 	其中:对联营企业和合营企业的投资收益
forex_gain 	float 	Y 	加:汇兑净收益
total_cogs 	float 	Y 	营业总成本
oper_cost 	float 	Y 	减:营业成本
int_exp 	float 	Y 	减:利息支出
comm_exp 	float 	Y 	减:手续费及佣金支出
biz_tax_surchg 	float 	Y 	减:营业税金及附加
sell_exp 	float 	Y 	减:销售费用
admin_exp 	float 	Y 	减:管理费用
fin_exp 	float 	Y 	减:财务费用
assets_impair_loss 	float 	Y 	减:资产减值损失
prem_refund 	float 	Y 	退保金
compens_payout 	float 	Y 	赔付总支出
reser_insur_liab 	float 	Y 	提取保险责任准备金
div_payt 	float 	Y 	保户红利支出
reins_exp 	float 	Y 	分保费用
oper_exp 	float 	Y 	营业支出
compens_payout_refu 	float 	Y 	减:摊回赔付支出
insur_reser_refu 	float 	Y 	减:摊回保险责任准备金
reins_cost_refund 	float 	Y 	减:摊回分保费用
other_bus_cost 	float 	Y 	其他业务成本
operate_profit 	float 	Y 	营业利润
non_oper_income 	float 	Y 	加:营业外收入
non_oper_exp 	float 	Y 	减:营业外支出
nca_disploss 	float 	Y 	其中:减:非流动资产处置净损失
total_profit 	float 	Y 	利润总额
income_tax 	float 	Y 	所得税费用
n_income 	float 	Y 	净利润(含少数股东损益)
n_income_attr_p 	float 	Y 	净利润(不含少数股东损益)
minority_gain 	float 	Y 	少数股东损益
oth_compr_income 	float 	Y 	其他综合收益
t_compr_income 	float 	Y 	综合收益总额
compr_inc_attr_p 	float 	Y 	归属于母公司(或股东)的综合收益总额
compr_inc_attr_m_s 	float 	Y 	归属于少数股东的综合收益总额
ebit 	float 	Y 	息税前利润
ebitda 	float 	Y 	息税折旧摊销前利润
insurance_exp 	float 	Y 	保险业务支出
undist_profit 	float 	Y 	年初未分配利润
distable_profit 	float 	Y 	可分配利润
update_flag 	str 	N 	更新标识，0未修改1更正过

主要报表类型说明
代码 	类型 	说明
1 	合并报表 	上市公司最新报表（默认）
2 	单季合并 	单一季度的合并报表
3 	调整单季合并表 	调整后的单季合并报表（如果有）
4 	调整合并报表 	本年度公布上年同期的财务报表数据，报告期为上年度
5 	调整前合并报表 	数据发生变更，将原数据进行保留，即调整前的原数据
6 	母公司报表 	该公司母公司的财务报表数据
7 	母公司单季表 	母公司的单季度表
8 	母公司调整单季表 	母公司调整后的单季表
9 	母公司调整表 	该公司母公司的本年度公布上年同期的财务报表数据
10 	母公司调整前报表 	母公司调整之前的原始财务报表数据
11 	调整前合并报表 	调整之前合并报表原数据
12 	母公司调整前报表 	母公司报表发生变更前保留的原数据
        """
    },
    "资产负债表": {
        "api":"balancesheet",
        "desc":"""接口：balancesheet
描述：获取上市公司资产负债表
积分：用户需要至少800积分才可以调取，具体请参阅积分获取办法

提示：当前接口只能按单只股票获取其历史数据，如果需要获取某一季度全部上市公司数据，请使用balancesheet_vip接口（参数一致），需积攒5000积分。

输入参数
名称 	类型 	必选 	描述
ts_code 	str 	Y 	股票代码
ann_date 	str 	N 	公告日期
start_date 	str 	N 	公告开始日期
end_date 	str 	N 	公告结束日期
period 	str 	N 	报告期(每个季度最后一天的日期，比如20171231表示年报)
report_type 	str 	N 	报告类型：见下方详细说明
comp_type 	str 	N 	公司类型：1一般工商业 2银行 3保险 4证券

输出参数
名称 	类型 	默认显示 	描述
ts_code 	str 	Y 	TS股票代码
ann_date 	str 	Y 	公告日期
f_ann_date 	str 	Y 	实际公告日期
end_date 	str 	Y 	报告期
report_type 	str 	Y 	报表类型
comp_type 	str 	Y 	公司类型
total_share 	float 	Y 	期末总股本
cap_rese 	float 	Y 	资本公积金
undistr_porfit 	float 	Y 	未分配利润
surplus_rese 	float 	Y 	盈余公积金
special_rese 	float 	Y 	专项储备
money_cap 	float 	Y 	货币资金
trad_asset 	float 	Y 	交易性金融资产
notes_receiv 	float 	Y 	应收票据
accounts_receiv 	float 	Y 	应收账款
oth_receiv 	float 	Y 	其他应收款
prepayment 	float 	Y 	预付款项
div_receiv 	float 	Y 	应收股利
int_receiv 	float 	Y 	应收利息
inventories 	float 	Y 	存货
amor_exp 	float 	Y 	待摊费用
nca_within_1y 	float 	Y 	一年内到期的非流动资产
sett_rsrv 	float 	Y 	结算备付金
loanto_oth_bank_fi 	float 	Y 	拆出资金
premium_receiv 	float 	Y 	应收保费
reinsur_receiv 	float 	Y 	应收分保账款
reinsur_res_receiv 	float 	Y 	应收分保合同准备金
pur_resale_fa 	float 	Y 	买入返售金融资产
oth_cur_assets 	float 	Y 	其他流动资产
total_cur_assets 	float 	Y 	流动资产合计
fa_avail_for_sale 	float 	Y 	可供出售金融资产
htm_invest 	float 	Y 	持有至到期投资
lt_eqt_invest 	float 	Y 	长期股权投资
invest_real_estate 	float 	Y 	投资性房地产
time_deposits 	float 	Y 	定期存款
oth_assets 	float 	Y 	其他资产
lt_rec 	float 	Y 	长期应收款
fix_assets 	float 	Y 	固定资产
cip 	float 	Y 	在建工程
const_materials 	float 	Y 	工程物资
fixed_assets_disp 	float 	Y 	固定资产清理
produc_bio_assets 	float 	Y 	生产性生物资产
oil_and_gas_assets 	float 	Y 	油气资产
intan_assets 	float 	Y 	无形资产
r_and_d 	float 	Y 	研发支出
goodwill 	float 	Y 	商誉
lt_amor_exp 	float 	Y 	长期待摊费用
defer_tax_assets 	float 	Y 	递延所得税资产
decr_in_disbur 	float 	Y 	发放贷款及垫款
oth_nca 	float 	Y 	其他非流动资产
total_nca 	float 	Y 	非流动资产合计
cash_reser_cb 	float 	Y 	现金及存放中央银行款项
depos_in_oth_bfi 	float 	Y 	存放同业和其它金融机构款项
prec_metals 	float 	Y 	贵金属
deriv_assets 	float 	Y 	衍生金融资产
rr_reins_une_prem 	float 	Y 	应收分保未到期责任准备金
rr_reins_outstd_cla 	float 	Y 	应收分保未决赔款准备金
rr_reins_lins_liab 	float 	Y 	应收分保寿险责任准备金
rr_reins_lthins_liab 	float 	Y 	应收分保长期健康险责任准备金
refund_depos 	float 	Y 	存出保证金
ph_pledge_loans 	float 	Y 	保户质押贷款
refund_cap_depos 	float 	Y 	存出资本保证金
indep_acct_assets 	float 	Y 	独立账户资产
client_depos 	float 	Y 	其中：客户资金存款
client_prov 	float 	Y 	其中：客户备付金
transac_seat_fee 	float 	Y 	其中:交易席位费
invest_as_receiv 	float 	Y 	应收款项类投资
total_assets 	float 	Y 	资产总计
lt_borr 	float 	Y 	长期借款
st_borr 	float 	Y 	短期借款
cb_borr 	float 	Y 	向中央银行借款
depos_ib_deposits 	float 	Y 	吸收存款及同业存放
loan_oth_bank 	float 	Y 	拆入资金
trading_fl 	float 	Y 	交易性金融负债
notes_payable 	float 	Y 	应付票据
acct_payable 	float 	Y 	应付账款
adv_receipts 	float 	Y 	预收款项
sold_for_repur_fa 	float 	Y 	卖出回购金融资产款
comm_payable 	float 	Y 	应付手续费及佣金
payroll_payable 	float 	Y 	应付职工薪酬
taxes_payable 	float 	Y 	应交税费
int_payable 	float 	Y 	应付利息
div_payable 	float 	Y 	应付股利
oth_payable 	float 	Y 	其他应付款
acc_exp 	float 	Y 	预提费用
deferred_inc 	float 	Y 	递延收益
st_bonds_payable 	float 	Y 	应付短期债券
payable_to_reinsurer 	float 	Y 	应付分保账款
rsrv_insur_cont 	float 	Y 	保险合同准备金
acting_trading_sec 	float 	Y 	代理买卖证券款
acting_uw_sec 	float 	Y 	代理承销证券款
non_cur_liab_due_1y 	float 	Y 	一年内到期的非流动负债
oth_cur_liab 	float 	Y 	其他流动负债
total_cur_liab 	float 	Y 	流动负债合计
bond_payable 	float 	Y 	应付债券
lt_payable 	float 	Y 	长期应付款
specific_payables 	float 	Y 	专项应付款
estimated_liab 	float 	Y 	预计负债
defer_tax_liab 	float 	Y 	递延所得税负债
defer_inc_non_cur_liab 	float 	Y 	递延收益-非流动负债
oth_ncl 	float 	Y 	其他非流动负债
total_ncl 	float 	Y 	非流动负债合计
depos_oth_bfi 	float 	Y 	同业和其它金融机构存放款项
deriv_liab 	float 	Y 	衍生金融负债
depos 	float 	Y 	吸收存款
agency_bus_liab 	float 	Y 	代理业务负债
oth_liab 	float 	Y 	其他负债
prem_receiv_adva 	float 	Y 	预收保费
depos_received 	float 	Y 	存入保证金
ph_invest 	float 	Y 	保户储金及投资款
reser_une_prem 	float 	Y 	未到期责任准备金
reser_outstd_claims 	float 	Y 	未决赔款准备金
reser_lins_liab 	float 	Y 	寿险责任准备金
reser_lthins_liab 	float 	Y 	长期健康险责任准备金
indept_acc_liab 	float 	Y 	独立账户负债
pledge_borr 	float 	Y 	其中:质押借款
indem_payable 	float 	Y 	应付赔付款
policy_div_payable 	float 	Y 	应付保单红利
total_liab 	float 	Y 	负债合计
treasury_share 	float 	Y 	减:库存股
ordin_risk_reser 	float 	Y 	一般风险准备
forex_differ 	float 	Y 	外币报表折算差额
invest_loss_unconf 	float 	Y 	未确认的投资损失
minority_int 	float 	Y 	少数股东权益
total_hldr_eqy_exc_min_int 	float 	Y 	股东权益合计(不含少数股东权益)
total_hldr_eqy_inc_min_int 	float 	Y 	股东权益合计(含少数股东权益)
total_liab_hldr_eqy 	float 	Y 	负债及股东权益总计
lt_payroll_payable 	float 	Y 	长期应付职工薪酬
oth_comp_income 	float 	Y 	其他综合收益
oth_eqt_tools 	float 	Y 	其他权益工具
oth_eqt_tools_p_shr 	float 	Y 	其他权益工具(优先股)
lending_funds 	float 	Y 	融出资金
acc_receivable 	float 	Y 	应收款项
st_fin_payable 	float 	Y 	应付短期融资款
payables 	float 	Y 	应付款项
hfs_assets 	float 	Y 	持有待售的资产
hfs_sales 	float 	Y 	持有待售的负债
update_flag 	str 	N 	更新标识

主要报表类型说明
代码 	类型 	说明
1 	合并报表 	上市公司最新报表（默认）
2 	单季合并 	单一季度的合并报表
3 	调整单季合并表 	调整后的单季合并报表（如果有）
4 	调整合并报表 	本年度公布上年同期的财务报表数据，报告期为上年度
5 	调整前合并报表 	数据发生变更，将原数据进行保留，即调整前的原数据
6 	母公司报表 	该公司母公司的财务报表数据
7 	母公司单季表 	母公司的单季度表
8 	母公司调整单季表 	母公司调整后的单季表
9 	母公司调整表 	该公司母公司的本年度公布上年同期的财务报表数据
10 	母公司调整前报表 	母公司调整之前的原始财务报表数据
11 	调整前合并报表 	调整之前合并报表原数据
12 	母公司调整前报表 	母公司报表发生变更前保留的原数据
        """
    },
    "现金流量表": {
        "api":"cashflow",
        "desc":"""接口：cashflow
描述：获取上市公司现金流量表
积分：用户需要至少800积分才可以调取，具体请参阅积分获取办法

提示：当前接口只能按单只股票获取其历史数据，如果需要获取某一季度全部上市公司数据，请使用cashflow_vip接口（参数一致），需积攒5000积分。

输入参数
名称 	类型 	必选 	描述
ts_code 	str 	Y 	股票代码
ann_date 	str 	N 	公告日期
start_date 	str 	N 	公告开始日期
end_date 	str 	N 	公告结束日期
period 	str 	N 	报告期(每个季度最后一天的日期，比如20171231表示年报)
report_type 	str 	N 	报告类型：见下方详细说明
comp_type 	str 	N 	公司类型：1一般工商业 2银行 3保险 4证券

输出参数
名称 	类型 	默认显示 	描述
ts_code 	str 	Y 	TS股票代码
ann_date 	str 	Y 	公告日期
f_ann_date 	str 	Y 	实际公告日期
end_date 	str 	Y 	报告期
comp_type 	str 	Y 	公司类型
report_type 	str 	Y 	报表类型
net_profit 	float 	Y 	净利润
finan_exp 	float 	Y 	财务费用
c_fr_sale_sg 	float 	Y 	销售商品、提供劳务收到的现金
recp_tax_rends 	float 	Y 	收到的税费返还
n_depos_incr_fi 	float 	Y 	客户存款和同业存放款项净增加额
n_incr_loans_cb 	float 	Y 	向中央银行借款净增加额
n_inc_borr_oth_fi 	float 	Y 	向其他金融机构拆入资金净增加额
prem_fr_orig_contr 	float 	Y 	收到原保险合同保费取得的现金
n_incr_insured_dep 	float 	Y 	保户储金净增加额
n_reinsur_prem 	float 	Y 	收到再保业务现金净额
n_incr_disp_tfa 	float 	Y 	处置交易性金融资产净增加额
ifc_cash_incr 	float 	Y 	收取利息和手续费净增加额
n_incr_disp_faas 	float 	Y 	处置可供出售金融资产净增加额
n_incr_loans_oth_bank 	float 	Y 	拆入资金净增加额
n_cap_incr_repur 	float 	Y 	回购业务资金净增加额
c_fr_oth_operate_a 	float 	Y 	收到其他与经营活动有关的现金
c_inf_fr_operate_a 	float 	Y 	经营活动现金流入小计
c_paid_goods_s 	float 	Y 	购买商品、接受劳务支付的现金
c_paid_to_for_empl 	float 	Y 	支付给职工以及为职工支付的现金
c_paid_for_taxes 	float 	Y 	支付的各项税费
n_incr_clt_loan_adv 	float 	Y 	客户贷款及垫款净增加额
n_incr_dep_cbob 	float 	Y 	存放央行和同业款项净增加额
c_pay_claims_orig_inco 	float 	Y 	支付原保险合同赔付款项的现金
pay_handling_chrg 	float 	Y 	支付手续费的现金
pay_comm_insur_plcy 	float 	Y 	支付保单红利的现金
oth_cash_pay_oper_act 	float 	Y 	支付其他与经营活动有关的现金
st_cash_out_act 	float 	Y 	经营活动现金流出小计
n_cashflow_act 	float 	Y 	经营活动产生的现金流量净额
oth_recp_ral_inv_act 	float 	Y 	收到其他与投资活动有关的现金
c_disp_withdrwl_invest 	float 	Y 	收回投资收到的现金
c_recp_return_invest 	float 	Y 	取得投资收益收到的现金
n_recp_disp_fiolta 	float 	Y 	处置固定资产、无形资产和其他长期资产收回的现金净额
n_recp_disp_sobu 	float 	Y 	处置子公司及其他营业单位收到的现金净额
stot_inflows_inv_act 	float 	Y 	投资活动现金流入小计
c_pay_acq_const_fiolta 	float 	Y 	购建固定资产、无形资产和其他长期资产支付的现金
c_paid_invest 	float 	Y 	投资支付的现金
n_disp_subs_oth_biz 	float 	Y 	取得子公司及其他营业单位支付的现金净额
oth_pay_ral_inv_act 	float 	Y 	支付其他与投资活动有关的现金
n_incr_pledge_loan 	float 	Y 	质押贷款净增加额
stot_out_inv_act 	float 	Y 	投资活动现金流出小计
n_cashflow_inv_act 	float 	Y 	投资活动产生的现金流量净额
c_recp_borrow 	float 	Y 	取得借款收到的现金
proc_issue_bonds 	float 	Y 	发行债券收到的现金
oth_cash_recp_ral_fnc_act 	float 	Y 	收到其他与筹资活动有关的现金
stot_cash_in_fnc_act 	float 	Y 	筹资活动现金流入小计
free_cashflow 	float 	Y 	企业自由现金流量
c_prepay_amt_borr 	float 	Y 	偿还债务支付的现金
c_pay_dist_dpcp_int_exp 	float 	Y 	分配股利、利润或偿付利息支付的现金
incl_dvd_profit_paid_sc_ms 	float 	Y 	其中:子公司支付给少数股东的股利、利润
oth_cashpay_ral_fnc_act 	float 	Y 	支付其他与筹资活动有关的现金
stot_cashout_fnc_act 	float 	Y 	筹资活动现金流出小计
n_cash_flows_fnc_act 	float 	Y 	筹资活动产生的现金流量净额
eff_fx_flu_cash 	float 	Y 	汇率变动对现金的影响
n_incr_cash_cash_equ 	float 	Y 	现金及现金等价物净增加额
c_cash_equ_beg_period 	float 	Y 	期初现金及现金等价物余额
c_cash_equ_end_period 	float 	Y 	期末现金及现金等价物余额
c_recp_cap_contrib 	float 	Y 	吸收投资收到的现金
incl_cash_rec_saims 	float 	Y 	其中:子公司吸收少数股东投资收到的现金
uncon_invest_loss 	float 	Y 	未确认投资损失
prov_depr_assets 	float 	Y 	加:资产减值准备
depr_fa_coga_dpba 	float 	Y 	固定资产折旧、油气资产折耗、生产性生物资产折旧
amort_intang_assets 	float 	Y 	无形资产摊销
lt_amort_deferred_exp 	float 	Y 	长期待摊费用摊销
decr_deferred_exp 	float 	Y 	待摊费用减少
incr_acc_exp 	float 	Y 	预提费用增加
loss_disp_fiolta 	float 	Y 	处置固定、无形资产和其他长期资产的损失
loss_scr_fa 	float 	Y 	固定资产报废损失
loss_fv_chg 	float 	Y 	公允价值变动损失
invest_loss 	float 	Y 	投资损失
decr_def_inc_tax_assets 	float 	Y 	递延所得税资产减少
incr_def_inc_tax_liab 	float 	Y 	递延所得税负债增加
decr_inventories 	float 	Y 	存货的减少
decr_oper_payable 	float 	Y 	经营性应收项目的减少
incr_oper_payable 	float 	Y 	经营性应付项目的增加
others 	float 	Y 	其他
im_net_cashflow_oper_act 	float 	Y 	经营活动产生的现金流量净额(间接法)
conv_debt_into_cap 	float 	Y 	债务转为资本
conv_copbonds_due_within_1y 	float 	Y 	一年内到期的可转换公司债券
fa_fnc_leases 	float 	Y 	融资租入固定资产
end_bal_cash 	float 	Y 	现金的期末余额
beg_bal_cash 	float 	Y 	减:现金的期初余额
end_bal_cash_equ 	float 	Y 	加:现金等价物的期末余额
beg_bal_cash_equ 	float 	Y 	减:现金等价物的期初余额
im_n_incr_cash_equ 	float 	Y 	现金及现金等价物净增加额(间接法)
update_flag 	str 	N 	更新标识

主要报表类型说明
代码 	类型 	说明
1 	合并报表 	上市公司最新报表（默认）
2 	单季合并 	单一季度的合并报表
3 	调整单季合并表 	调整后的单季合并报表（如果有）
4 	调整合并报表 	本年度公布上年同期的财务报表数据，报告期为上年度
5 	调整前合并报表 	数据发生变更，将原数据进行保留，即调整前的原数据
6 	母公司报表 	该公司母公司的财务报表数据
7 	母公司单季表 	母公司的单季度表
8 	母公司调整单季表 	母公司调整后的单季表
9 	母公司调整表 	该公司母公司的本年度公布上年同期的财务报表数据
10 	母公司调整前报表 	母公司调整之前的原始财务报表数据
11 	调整前合并报表 	调整之前合并报表原数据
12 	母公司调整前报表 	母公司报表发生变更前保留的原数据
        """
    },
    "业绩预告": {
        "api":"forecast",
        "desc":"""接口：forecast
描述：获取业绩预告数据
权限：用户需要至少800积分才可以调取，具体请参阅积分获取办法

提示：当前接口只能按单只股票获取其历史数据，如果需要获取某一季度全部上市公司数据，请使用forecast_vip接口（参数一致），需积攒5000积分。

输入参数
名称 	类型 	必选 	描述
ts_code 	str 	N 	股票代码(二选一)
ann_date 	str 	N 	公告日期 (二选一)
start_date 	str 	N 	公告开始日期
end_date 	str 	N 	公告结束日期
period 	str 	N 	报告期(每个季度最后一天的日期，比如20171231表示年报)
type 	str 	N 	预告类型(预增/预减/扭亏/首亏/续亏/续盈/略增/略减)

输出参数
名称 	类型 	描述
ts_code 	str 	TS股票代码
ann_date 	str 	公告日期
end_date 	str 	报告期
type 	str 	业绩预告类型(预增/预减/扭亏/首亏/续亏/续盈/略增/略减)
p_change_min 	float 	预告净利润变动幅度下限（%）
p_change_max 	float 	预告净利润变动幅度上限（%）
net_profit_min 	float 	预告净利润下限（万元）
net_profit_max 	float 	预告净利润上限（万元）
last_parent_net 	float 	上年同期归属母公司净利润
first_ann_date 	str 	首次公告日
summary 	str 	业绩预告摘要
change_reason 	str 	业绩变动原因
        """
    },
    "业绩快报": {
        "api":"express",
        "desc":"""接口：express
描述：获取上市公司业绩快报
权限：用户需要至少800积分才可以调取，具体请参阅积分获取办法

提示：当前接口只能按单只股票获取其历史数据，如果需要获取某一季度全部上市公司数据，请使用express_vip接口（参数一致），需积攒5000积分。

输入参数
名称 	类型 	必选 	描述
ts_code 	str 	Y 	股票代码
ann_date 	str 	N 	公告日期
start_date 	str 	N 	公告开始日期
end_date 	str 	N 	公告结束日期
period 	str 	N 	报告期(每个季度最后一天的日期,比如20171231表示年报)

输出参数
名称 	类型 	描述
ts_code 	str 	TS股票代码
ann_date 	str 	公告日期
end_date 	str 	报告期
revenue 	float 	营业收入(元)
operate_profit 	float 	营业利润(元)
total_profit 	float 	利润总额(元)
n_income 	float 	净利润(元)
total_assets 	float 	总资产(元)
total_hldr_eqy_exc_min_int 	float 	股东权益合计(不含少数股东权益)(元)
diluted_eps 	float 	每股收益(摊薄)(元)
diluted_roe 	float 	净资产收益率(摊薄)(%)
yoy_net_profit 	float 	去年同期修正后净利润
bps 	float 	每股净资产
yoy_sales 	float 	同比增长率:营业收入
yoy_op 	float 	同比增长率:营业利润
yoy_tp 	float 	同比增长率:利润总额
yoy_dedu_np 	float 	同比增长率:归属母公司股东的净利润
yoy_eps 	float 	同比增长率:基本每股收益
yoy_roe 	float 	同比增减:加权平均净资产收益率
growth_assets 	float 	比年初增长率:总资产
yoy_equity 	float 	比年初增长率:归属母公司的股东权益
growth_bps 	float 	比年初增长率:归属于母公司股东的每股净资产
or_last_year 	float 	去年同期营业收入
op_last_year 	float 	去年同期营业利润
tp_last_year 	float 	去年同期利润总额
np_last_year 	float 	去年同期净利润
eps_last_year 	float 	去年同期每股收益
open_net_assets 	float 	期初净资产
open_bps 	float 	期初每股净资产
perf_summary 	str 	业绩简要说明
is_audit 	int 	是否审计： 1是 0否
remark 	str 	备注
        """
    },
    "分红送股数据": {
        "api":"dividend",
        "desc":"""接口：dividend
描述：分红送股数据
权限：用户需要至少900积分才可以调取，具体请参阅积分获取办法

输入参数
名称 	类型 	必选 	描述
ts_code 	str 	N 	TS代码
ann_date 	str 	N 	公告日
record_date 	str 	N 	股权登记日期
ex_date 	str 	N 	除权除息日
imp_ann_date 	str 	N 	实施公告日

以上参数至少有一个不能为空


输出参数
名称 	类型 	默认显示 	描述
ts_code 	str 	Y 	TS代码
end_date 	str 	Y 	分红年度
ann_date 	str 	Y 	预案公告日
div_proc 	str 	Y 	实施进度
stk_div 	float 	Y 	每股送转
stk_bo_rate 	float 	Y 	每股送股比例
stk_co_rate 	float 	Y 	每股转增比例
cash_div 	float 	Y 	每股分红（税后）
cash_div_tax 	float 	Y 	每股分红（税前）
record_date 	str 	Y 	股权登记日
ex_date 	str 	Y 	除权除息日
pay_date 	str 	Y 	派息日
div_listdate 	str 	Y 	红股上市日
imp_ann_date 	str 	Y 	实施公告日
base_date 	str 	N 	基准日
base_share 	float 	N 	基准股本（万）
        """
    },
    "财务指标数据": {
        "api":"fina_indicator",
        "desc":"""接口：fina_indicator
描述：获取上市公司财务指标数据，为避免服务器压力，现阶段每次请求最多返回60条记录，可通过设置日期多次请求获取更多数据。
权限：用户需要至少800积分才可以调取，具体请参阅积分获取办法

提示：当前接口只能按单只股票获取其历史数据，如果需要获取某一季度全部上市公司数据，请使用fina_indicator_vip接口（参数一致），需积攒5000积分。

输入参数
名称 	类型 	必选 	描述
ts_code 	str 	Y 	TS股票代码,e.g. 600001.SH/000001.SZ
ann_date 	str 	N 	公告日期
start_date 	str 	N 	报告期开始日期
end_date 	str 	N 	报告期结束日期
period 	str 	N 	报告期(每个季度最后一天的日期,比如20171231表示年报)

输出参数
名称 	类型 	默认显示 	描述
ts_code 	str 	Y 	TS代码
ann_date 	str 	Y 	公告日期
end_date 	str 	Y 	报告期
eps 	float 	Y 	基本每股收益
dt_eps 	float 	Y 	稀释每股收益
total_revenue_ps 	float 	Y 	每股营业总收入
revenue_ps 	float 	Y 	每股营业收入
capital_rese_ps 	float 	Y 	每股资本公积
surplus_rese_ps 	float 	Y 	每股盈余公积
undist_profit_ps 	float 	Y 	每股未分配利润
extra_item 	float 	Y 	非经常性损益
profit_dedt 	float 	Y 	扣除非经常性损益后的净利润
gross_margin 	float 	Y 	毛利
current_ratio 	float 	Y 	流动比率
quick_ratio 	float 	Y 	速动比率
cash_ratio 	float 	Y 	保守速动比率
invturn_days 	float 	N 	存货周转天数
arturn_days 	float 	N 	应收账款周转天数
inv_turn 	float 	N 	存货周转率
ar_turn 	float 	Y 	应收账款周转率
ca_turn 	float 	Y 	流动资产周转率
fa_turn 	float 	Y 	固定资产周转率
assets_turn 	float 	Y 	总资产周转率
op_income 	float 	Y 	经营活动净收益
valuechange_income 	float 	N 	价值变动净收益
interst_income 	float 	N 	利息费用
daa 	float 	N 	折旧与摊销
ebit 	float 	Y 	息税前利润
ebitda 	float 	Y 	息税折旧摊销前利润
fcff 	float 	Y 	企业自由现金流量
fcfe 	float 	Y 	股权自由现金流量
current_exint 	float 	Y 	无息流动负债
noncurrent_exint 	float 	Y 	无息非流动负债
interestdebt 	float 	Y 	带息债务
netdebt 	float 	Y 	净债务
tangible_asset 	float 	Y 	有形资产
working_capital 	float 	Y 	营运资金
networking_capital 	float 	Y 	营运流动资本
invest_capital 	float 	Y 	全部投入资本
retained_earnings 	float 	Y 	留存收益
diluted2_eps 	float 	Y 	期末摊薄每股收益
bps 	float 	Y 	每股净资产
ocfps 	float 	Y 	每股经营活动产生的现金流量净额
retainedps 	float 	Y 	每股留存收益
cfps 	float 	Y 	每股现金流量净额
ebit_ps 	float 	Y 	每股息税前利润
fcff_ps 	float 	Y 	每股企业自由现金流量
fcfe_ps 	float 	Y 	每股股东自由现金流量
netprofit_margin 	float 	Y 	销售净利率
grossprofit_margin 	float 	Y 	销售毛利率
cogs_of_sales 	float 	Y 	销售成本率
expense_of_sales 	float 	Y 	销售期间费用率
profit_to_gr 	float 	Y 	净利润/营业总收入
saleexp_to_gr 	float 	Y 	销售费用/营业总收入
adminexp_of_gr 	float 	Y 	管理费用/营业总收入
finaexp_of_gr 	float 	Y 	财务费用/营业总收入
impai_ttm 	float 	Y 	资产减值损失/营业总收入
gc_of_gr 	float 	Y 	营业总成本/营业总收入
op_of_gr 	float 	Y 	营业利润/营业总收入
ebit_of_gr 	float 	Y 	息税前利润/营业总收入
roe 	float 	Y 	净资产收益率
roe_waa 	float 	Y 	加权平均净资产收益率
roe_dt 	float 	Y 	净资产收益率(扣除非经常损益)
roa 	float 	Y 	总资产报酬率
npta 	float 	Y 	总资产净利润
roic 	float 	Y 	投入资本回报率
roe_yearly 	float 	Y 	年化净资产收益率
roa2_yearly 	float 	Y 	年化总资产报酬率
roe_avg 	float 	N 	平均净资产收益率(增发条件)
opincome_of_ebt 	float 	N 	经营活动净收益/利润总额
investincome_of_ebt 	float 	N 	价值变动净收益/利润总额
n_op_profit_of_ebt 	float 	N 	营业外收支净额/利润总额
tax_to_ebt 	float 	N 	所得税/利润总额
dtprofit_to_profit 	float 	N 	扣除非经常损益后的净利润/净利润
salescash_to_or 	float 	N 	销售商品提供劳务收到的现金/营业收入
ocf_to_or 	float 	N 	经营活动产生的现金流量净额/营业收入
ocf_to_opincome 	float 	N 	经营活动产生的现金流量净额/经营活动净收益
capitalized_to_da 	float 	N 	资本支出/折旧和摊销
debt_to_assets 	float 	Y 	资产负债率
assets_to_eqt 	float 	Y 	权益乘数
dp_assets_to_eqt 	float 	Y 	权益乘数(杜邦分析)
ca_to_assets 	float 	Y 	流动资产/总资产
nca_to_assets 	float 	Y 	非流动资产/总资产
tbassets_to_totalassets 	float 	Y 	有形资产/总资产
int_to_talcap 	float 	Y 	带息债务/全部投入资本
eqt_to_talcapital 	float 	Y 	归属于母公司的股东权益/全部投入资本
currentdebt_to_debt 	float 	Y 	流动负债/负债合计
longdeb_to_debt 	float 	Y 	非流动负债/负债合计
ocf_to_shortdebt 	float 	Y 	经营活动产生的现金流量净额/流动负债
debt_to_eqt 	float 	Y 	产权比率
eqt_to_debt 	float 	Y 	归属于母公司的股东权益/负债合计
eqt_to_interestdebt 	float 	Y 	归属于母公司的股东权益/带息债务
tangibleasset_to_debt 	float 	Y 	有形资产/负债合计
tangasset_to_intdebt 	float 	Y 	有形资产/带息债务
tangibleasset_to_netdebt 	float 	Y 	有形资产/净债务
ocf_to_debt 	float 	Y 	经营活动产生的现金流量净额/负债合计
ocf_to_interestdebt 	float 	N 	经营活动产生的现金流量净额/带息债务
ocf_to_netdebt 	float 	N 	经营活动产生的现金流量净额/净债务
ebit_to_interest 	float 	N 	已获利息倍数(EBIT/利息费用)
longdebt_to_workingcapital 	float 	N 	长期债务与营运资金比率
ebitda_to_debt 	float 	N 	息税折旧摊销前利润/负债合计
turn_days 	float 	Y 	营业周期
roa_yearly 	float 	Y 	年化总资产净利率
roa_dp 	float 	Y 	总资产净利率(杜邦分析)
fixed_assets 	float 	Y 	固定资产合计
profit_prefin_exp 	float 	N 	扣除财务费用前营业利润
non_op_profit 	float 	N 	非营业利润
op_to_ebt 	float 	N 	营业利润／利润总额
nop_to_ebt 	float 	N 	非营业利润／利润总额
ocf_to_profit 	float 	N 	经营活动产生的现金流量净额／营业利润
cash_to_liqdebt 	float 	N 	货币资金／流动负债
cash_to_liqdebt_withinterest 	float 	N 	货币资金／带息流动负债
op_to_liqdebt 	float 	N 	营业利润／流动负债
op_to_debt 	float 	N 	营业利润／负债合计
roic_yearly 	float 	N 	年化投入资本回报率
total_fa_trun 	float 	N 	固定资产合计周转率
profit_to_op 	float 	Y 	利润总额／营业收入
q_opincome 	float 	N 	经营活动单季度净收益
q_investincome 	float 	N 	价值变动单季度净收益
q_dtprofit 	float 	N 	扣除非经常损益后的单季度净利润
q_eps 	float 	N 	每股收益(单季度)
q_netprofit_margin 	float 	N 	销售净利率(单季度)
q_gsprofit_margin 	float 	N 	销售毛利率(单季度)
q_exp_to_sales 	float 	N 	销售期间费用率(单季度)
q_profit_to_gr 	float 	N 	净利润／营业总收入(单季度)
q_saleexp_to_gr 	float 	Y 	销售费用／营业总收入 (单季度)
q_adminexp_to_gr 	float 	N 	管理费用／营业总收入 (单季度)
q_finaexp_to_gr 	float 	N 	财务费用／营业总收入 (单季度)
q_impair_to_gr_ttm 	float 	N 	资产减值损失／营业总收入(单季度)
q_gc_to_gr 	float 	Y 	营业总成本／营业总收入 (单季度)
q_op_to_gr 	float 	N 	营业利润／营业总收入(单季度)
q_roe 	float 	Y 	净资产收益率(单季度)
q_dt_roe 	float 	Y 	净资产单季度收益率(扣除非经常损益)
q_npta 	float 	Y 	总资产净利润(单季度)
q_opincome_to_ebt 	float 	N 	经营活动净收益／利润总额(单季度)
q_investincome_to_ebt 	float 	N 	价值变动净收益／利润总额(单季度)
q_dtprofit_to_profit 	float 	N 	扣除非经常损益后的净利润／净利润(单季度)
q_salescash_to_or 	float 	N 	销售商品提供劳务收到的现金／营业收入(单季度)
q_ocf_to_sales 	float 	Y 	经营活动产生的现金流量净额／营业收入(单季度)
q_ocf_to_or 	float 	N 	经营活动产生的现金流量净额／经营活动净收益(单季度)
basic_eps_yoy 	float 	Y 	基本每股收益同比增长率(%)
dt_eps_yoy 	float 	Y 	稀释每股收益同比增长率(%)
cfps_yoy 	float 	Y 	每股经营活动产生的现金流量净额同比增长率(%)
op_yoy 	float 	Y 	营业利润同比增长率(%)
ebt_yoy 	float 	Y 	利润总额同比增长率(%)
netprofit_yoy 	float 	Y 	归属母公司股东的净利润同比增长率(%)
dt_netprofit_yoy 	float 	Y 	归属母公司股东的净利润-扣除非经常损益同比增长率(%)
ocf_yoy 	float 	Y 	经营活动产生的现金流量净额同比增长率(%)
roe_yoy 	float 	Y 	净资产收益率(摊薄)同比增长率(%)
bps_yoy 	float 	Y 	每股净资产相对年初增长率(%)
assets_yoy 	float 	Y 	资产总计相对年初增长率(%)
eqt_yoy 	float 	Y 	归属母公司的股东权益相对年初增长率(%)
tr_yoy 	float 	Y 	营业总收入同比增长率(%)
or_yoy 	float 	Y 	营业收入同比增长率(%)
q_gr_yoy 	float 	N 	营业总收入同比增长率(%)(单季度)
q_gr_qoq 	float 	N 	营业总收入环比增长率(%)(单季度)
q_sales_yoy 	float 	Y 	营业收入同比增长率(%)(单季度)
q_sales_qoq 	float 	N 	营业收入环比增长率(%)(单季度)
q_op_yoy 	float 	N 	营业利润同比增长率(%)(单季度)
q_op_qoq 	float 	Y 	营业利润环比增长率(%)(单季度)
q_profit_yoy 	float 	N 	净利润同比增长率(%)(单季度)
q_profit_qoq 	float 	N 	净利润环比增长率(%)(单季度)
q_netprofit_yoy 	float 	N 	归属母公司股东的净利润同比增长率(%)(单季度)
q_netprofit_qoq 	float 	N 	归属母公司股东的净利润环比增长率(%)(单季度)
equity_yoy 	float 	Y 	净资产同比增长率
rd_exp 	float 	N 	研发费用
update_flag 	str 	N 	更新标识
        """
    },
    "财务审计意见": {
        "api":"fina_audit",
        "desc":"""接口：fina_audit
描述：获取上市公司定期财务审计意见数据
权限：用户需要至少500积分才可以调取，具体请参阅积分获取办法

输入参数
名称 	类型 	必选 	描述
ts_code 	str 	Y 	股票代码
ann_date 	str 	N 	公告日期
start_date 	str 	N 	公告开始日期
end_date 	str 	N 	公告结束日期
period 	str 	N 	报告期(每个季度最后一天的日期,比如20171231表示年报)

输出参数
名称 	类型 	描述
ts_code 	str 	TS股票代码
ann_date 	str 	公告日期
end_date 	str 	报告期
audit_result 	str 	审计结果
audit_fees 	float 	审计总费用（元）
audit_agency 	str 	会计事务所
audit_sign 	str 	签字会计师
        """
    },
    "主营业务构成": {
        "api":"fina_mainbz",
        "desc":"""接口：fina_mainbz
描述：获得上市公司主营业务构成，分地区和产品两种方式
权限：用户需要至少900积分才可以调取，具体请参阅积分获取办法 ，单次最大提取100行，总量不限制，可循环获取。

提示：当前接口只能按单只股票获取其历史数据，如果需要获取某一季度全部上市公司数据，请使用fina_mainbz_vip接口（参数一致），需积攒5000积分。

输入参数
名称 	类型 	必选 	描述
ts_code 	str 	Y 	股票代码
period 	str 	N 	报告期(每个季度最后一天的日期,比如20171231表示年报)
type 	str 	N 	类型：P按产品 D按地区（请输入大写字母P或者D）
start_date 	str 	N 	报告期开始日期
end_date 	str 	N 	报告期结束日期

输出参数
名称 	类型 	描述
ts_code 	str 	TS代码
end_date 	str 	报告期
bz_item 	str 	主营业务来源
bz_sales 	float 	主营业务收入(元)
bz_profit 	float 	主营业务利润(元)
bz_cost 	float 	主营业务成本(元)
curr_type 	str 	货币代码
update_flag 	str 	是否更新
        """
    },
    "财报披露日期表": {
        "api":"disclosure_date",
        "desc":"""接口：disclosure_date
描述：获取财报披露计划日期
限量：单次最大3000，总量不限制
积分：用户需要至少500积分才可以调取，积分越多权限越大，具体请参阅积分获取办法

输入参数
名称 	类型 	必选 	描述
ts_code 	str 	N 	TS股票代码
end_date 	str 	N 	财报周期（比如20181231表示2018年年报，20180630表示中报)
pre_date 	str 	N 	计划披露日期
actual_date 	str 	N 	实际披露日期

输出参数
名称 	类型 	默认显示 	描述
ts_code 	str 	Y 	TS代码
ann_date 	str 	Y 	最新披露公告日
end_date 	str 	Y 	报告期
pre_date 	str 	Y 	预计披露日期
actual_date 	str 	Y 	实际披露日期
modify_date 	str 	N 	披露日期修正记录
        """
    },
    "港股通十大成交股": {
        "api":"ggt_top10",
        "desc":"""接口：ggt_top10
描述：获取港股通每日成交数据，其中包括沪市、深市详细数据

输入参数
名称 	类型 	必选 	描述
ts_code 	str 	N 	股票代码（二选一）
trade_date 	str 	N 	交易日期（二选一）
start_date 	str 	N 	开始日期
end_date 	str 	N 	结束日期
market_type 	str 	N 	市场类型 2：港股通（沪） 4：港股通（深）

输出参数
名称 	类型 	描述
trade_date 	str 	交易日期
ts_code 	str 	股票代码
name 	str 	股票名称
close 	float 	收盘价
p_change 	float 	涨跌幅
rank 	str 	资金排名
market_type 	str 	市场类型 2：港股通（沪） 4：港股通（深）
amount 	float 	累计成交金额（元）
net_amount 	float 	净买入金额（元）
sh_amount 	float 	沪市成交金额（元）
sh_net_amount 	float 	沪市净买入金额（元）
sh_buy 	float 	沪市买入金额（元）
sh_sell 	float 	沪市卖出金额
sz_amount 	float 	深市成交金额（元）
sz_net_amount 	float 	深市净买入金额（元）
sz_buy 	float 	深市买入金额（元）
sz_sell 	float 	深市卖出金额（元）
        """
    },
    "融资融券交易汇总": {
        "api":"margin",
        "desc":"""接口：margin
描述：获取融资融券每日交易汇总数据

输入参数
名称 	类型 	必选 	描述
trade_date 	str 	N 	交易日期
exchange_id 	str 	N 	交易所代码
start_date 	str 	N 	开始日期
end_date 	str 	N 	结束日期

输出参数
名称 	类型 	描述
trade_date 	str 	交易日期
exchange_id 	str 	交易所代码（SSE上交所SZSE深交所）
rzye 	float 	融资余额(元)
rzmre 	float 	融资买入额(元)
rzche 	float 	融资偿还额(元)
rqye 	float 	融券余额(元)
rqmcl 	float 	融券卖出量(股,份,手)
rzrqye 	float 	融资融券余额(元)
rqyl 	float 	融券余量(股,份,手)
        """
    },
    "融资融券交易明细": {
        "api":"margin_detail",
        "desc":"""接口：margin_detail
描述：获取沪深两市每日融资融券明细

输入参数
名称 	类型 	必选 	描述
trade_date 	str 	N 	交易日期
ts_code 	str 	N 	TS代码
start_date 	str 	N 	开始日期
end_date 	str 	N 	结束日期

输出参数
名称 	类型 	描述
trade_date 	str 	交易日期
ts_code 	str 	TS股票代码
name 	str 	股票名称 （20190910后有数据）
rzye 	float 	融资余额(元)
rqye 	float 	融券余额(元)
rzmre 	float 	融资买入额(元)
rqyl 	float 	融券余量（手）
rzche 	float 	融资偿还额(元)
rqchl 	float 	融券偿还量(手)
rqmcl 	float 	融券卖出量(股,份,手)
rzrqye 	float 	融资融券余额(元)
        """
    },
    "前十大股东": {
        "api":"top10_holders",
        "desc":"""接口：top10_holders
描述：获取上市公司前十大股东数据，包括持有数量和比例等信息。

输入参数
名称 	类型 	必选 	描述
ts_code 	str 	Y 	TS代码
period 	str 	N 	报告期
ann_date 	str 	N 	公告日期
start_date 	str 	N 	报告期开始日期
end_date 	str 	N 	报告期结束日期

注：一次取100行记录

输出参数
名称 	类型 	描述
ts_code 	str 	TS股票代码
ann_date 	str 	公告日期
end_date 	str 	报告期
holder_name 	str 	股东名称
hold_amount 	float 	持有数量（股）
hold_ratio 	float 	持有比例
        """
    },
    "前十大流通股东": {
        "api":"top10_floatholders",
        "desc":"""接口：top10_floatholders
描述：获取上市公司前十大流通股东数据。

输入参数
名称 	类型 	必选 	描述
ts_code 	str 	Y 	TS代码
period 	str 	N 	报告期
ann_date 	str 	N 	公告日期
start_date 	str 	N 	报告期开始日期
end_date 	str 	N 	报告期结束日期

注：一次取100行记录

输出参数
名称 	类型 	描述
ts_code 	str 	TS股票代码
ann_date 	str 	公告日期
end_date 	str 	报告期
holder_name 	str 	股东名称
hold_amount 	float 	持有数量（股）
        """
    },
    "龙虎榜每日明细": {
        "api":"top_list",
        "desc":"""接口：top_list
描述：龙虎榜每日交易明细
数据历史： 2005年至今
限量：单次最大10000
积分：用户需要至少300积分才可以调取，具体请参阅积分获取办法

输入参数
名称 	类型 	必选 	描述
trade_date 	str 	Y 	交易日期
ts_code 	str 	N 	股票代码

输出参数
名称 	类型 	默认显示 	描述
trade_date 	str 	Y 	交易日期
ts_code 	str 	Y 	TS代码
name 	str 	Y 	名称
close 	float 	Y 	收盘价
pct_change 	float 	Y 	涨跌幅
turnover_rate 	float 	Y 	换手率
amount 	float 	Y 	总成交额
l_sell 	float 	Y 	龙虎榜卖出额
l_buy 	float 	Y 	龙虎榜买入额
l_amount 	float 	Y 	龙虎榜成交额
net_amount 	float 	Y 	龙虎榜净买入额
net_rate 	float 	Y 	龙虎榜净买额占比
amount_rate 	float 	Y 	龙虎榜成交额占比
float_values 	float 	Y 	当日流通市值
reason 	str 	Y 	上榜理由
        """
    },
    "龙虎榜机构交易明细": {
        "api":"top_inst",
        "desc":"""接口：top_inst
描述：龙虎榜机构成交明细
限量：单次最大10000
积分：用户需要至少300积分才可以调取，具体请参阅积分获取办法

输入参数
名称 	类型 	必选 	描述
trade_date 	str 	Y 	交易日期
ts_code 	str 	N 	TS代码

输出参数
名称 	类型 	默认显示 	描述
trade_date 	str 	Y 	交易日期
ts_code 	str 	Y 	TS代码
exalter 	str 	Y 	营业部名称
side 	str 	Y 	买卖类型0：买入金额最大的前5名， 1：卖出金额最大的前5名
buy 	float 	Y 	买入额（元）
buy_rate 	float 	Y 	买入占总成交比例
sell 	float 	Y 	卖出额（元）
sell_rate 	float 	Y 	卖出占总成交比例
net_buy 	float 	Y 	净成交额（元）
reason 	str 	Y 	上榜理由
        """
    },
    "股权质押统计数据": {
        "api":"pledge_stat",
        "desc":"""接口：pledge_stat
描述：获取股票质押统计数据
限量：单次最大1000
积分：用户需要至少500积分才可以调取，具体请参阅积分获取办法

输入参数
名称 	类型 	必选 	描述
ts_code 	str 	N 	股票代码
end_date 	str 	N 	截止日期

输出参数
名称 	类型 	默认显示 	描述
ts_code 	str 	Y 	TS代码
end_date 	str 	Y 	截止日期
pledge_count 	int 	Y 	质押次数
unrest_pledge 	float 	Y 	无限售股质押数量（万）
rest_pledge 	float 	Y 	限售股份质押数量（万）
total_share 	float 	Y 	总股本
pledge_ratio 	float 	Y 	质押比例
        """
    },
    "股权质押明细数据": {
        "api":"pledge_detail",
        "desc":"""接口：pledge_detail
描述：获取股票质押明细数据
限量：单次最大1000
积分：用户需要至少500积分才可以调取，具体请参阅积分获取办法

输入参数
名称 	类型 	必选 	描述
ts_code 	str 	Y 	股票代码

输出参数
名称 	类型 	默认显示 	描述
ts_code 	str 	Y 	TS股票代码
ann_date 	str 	Y 	公告日期
holder_name 	str 	Y 	股东名称
pledge_amount 	float 	Y 	质押数量（万股）
start_date 	str 	Y 	质押开始日期
end_date 	str 	Y 	质押结束日期
is_release 	str 	Y 	是否已解押
release_date 	str 	Y 	解押日期
pledgor 	str 	Y 	质押方
holding_amount 	float 	Y 	持股总数（万股）
pledged_amount 	float 	Y 	质押总数（万股）
p_total_ratio 	float 	Y 	本次质押占总股本比例
h_total_ratio 	float 	Y 	持股总数占总股本比例
is_buyback 	str 	Y 	是否回购
        """
    },
    "股票回购": {
        "api":"repurchase",
        "desc":"""接口：repurchase
描述：获取上市公司回购股票数据
积分：用户需要至少600积分才可以调取，具体请参阅积分获取办法

输入参数
名称 	类型 	必选 	描述
ann_date 	str 	N 	公告日期（任意填参数，如果都不填，单次默认返回2000条）
start_date 	str 	N 	公告开始日期
end_date 	str 	N 	公告结束日期

以上日期格式为：YYYYMMDD，比如20181010

输出参数
名称 	类型 	默认显示 	描述
ts_code 	str 	Y 	TS代码
ann_date 	str 	Y 	公告日期
end_date 	str 	Y 	截止日期
proc 	str 	Y 	进度
exp_date 	str 	Y 	过期日期
vol 	float 	Y 	回购数量
amount 	float 	Y 	回购金额
high_limit 	float 	Y 	回购最高价
low_limit 	float 	Y 	回购最低价
        """
    },
    "概念股分类表": {
        "api":"concept",
        "desc":"""接口：concept
描述：获取概念股分类，目前只有ts一个来源，未来将逐步增加来源
积分：用户需要至少300积分才可以调取，具体请参阅积分获取办法

输入参数
名称 	类型 	必选 	描述
src 	str 	N 	来源，默认为ts

输出参数
名称 	类型 	默认显示 	描述
code 	str 	Y 	概念分类ID
name 	str 	Y 	概念分类名称
src 	str 	Y 	来源
        """
    },
    "概念股明细列表": {
        "api":"concept_detail",
        "desc":"""接口：concept_detail
描述：获取概念股分类明细数据
积分：用户需要至少300积分才可以调取，具体请参阅积分获取办法

输入参数
名称 	类型 	必选 	描述
id 	str 	N 	概念分类ID （id来自概念股分类接口）
ts_code 	str 	N 	股票代码 （以上参数二选一）

输出参数
名称 	类型 	默认显示 	描述
id 	str 	Y 	概念代码
concept_name 	str 	Y 	概念名称
ts_code 	str 	Y 	股票代码
name 	str 	Y 	股票名称
in_date 	str 	N 	纳入日期
out_date 	str 	N 	剔除日期
        """
    },
    "限售股解禁": {
        "api":"share_float",
        "desc":"""接口：share_float
描述：获取限售股解禁
限量：单次最大5000条，总量不限制
积分：120分可调取，每分钟内限制次数，超过5000积分频次相对较高，具体请参阅积分获取办法


输入参数
名称 	类型 	必选 	描述
ts_code 	str 	N 	TS股票代码（至少输入一个参数）
ann_date 	str 	N 	公告日期（日期格式：YYYYMMDD，下同）
float_date 	str 	N 	解禁日期
start_date 	str 	N 	解禁开始日期
end_date 	str 	N 	解禁结束日期


输出参数
名称 	类型 	默认显示 	描述
ts_code 	str 	Y 	TS代码
ann_date 	str 	Y 	公告日期
float_date 	str 	Y 	解禁日期
float_share 	float 	Y 	流通股份
float_ratio 	float 	Y 	流通股份占总股本比率
holder_name 	str 	Y 	股东名称
share_type 	str 	Y 	股份类型
        """
    },
    "大宗交易": {
        "api":"block_trade",
        "desc":"""接口：block_trade
描述：大宗交易
限量：单次最大1000条，总量不限制
积分：300积分可调取，每分钟内限制次数，超过5000积分频次相对较高，具体请参阅积分获取办法


输入参数
名称 	类型 	必选 	描述
ts_code 	str 	N 	TS代码（股票代码和日期至少输入一个参数）
trade_date 	str 	N 	交易日期（格式：YYYYMMDD，下同）
start_date 	str 	N 	开始日期
end_date 	str 	N 	结束日期


输出参数
名称 	类型 	默认显示 	描述
ts_code 	str 	Y 	TS代码
trade_date 	str 	Y 	交易日历
price 	float 	Y 	成交价
vol 	float 	Y 	成交量（万股）
amount 	float 	Y 	成交金额
buyer 	str 	Y 	买方营业部
seller 	str 	Y 	卖方营业部
        """
    },
    "股票开户数据（停）": {
        "api":"stk_account",
        "desc":"""接口：stk_account
描述：获取股票账户开户数据，统计周期为一周
积分：600积分可调取，具体请参阅积分获取办法

注：此数据官方已经停止更新。


输入参数
名称 	类型 	必选 	描述
date 	str 	N 	日期
start_date 	str 	N 	开始日期
end_date 	str 	N 	结束日期


输出参数
名称 	类型 	默认显示 	描述
date 	str 	Y 	统计周期
weekly_new 	float 	Y 	本周新增（万）
total 	float 	Y 	期末总账户数（万）
weekly_hold 	float 	Y 	本周持仓账户数（万）
weekly_trade 	float 	Y 	本周参与交易账户数（万）
        """
    },
    "股票开户数据（旧）": {
        "api":"stk_account_old",
        "desc":"""接口：stk_account_old
描述：获取股票账户开户数据旧版格式数据，数据从2008年1月开始，到2015年5月29，新数据请通过股票开户数据获取。
积分：600积分可调取，具体请参阅积分获取办法


输入参数
名称 	类型 	必选 	描述
start_date 	str 	N 	开始日期
end_date 	str 	N 	结束日期


输出参数
名称 	类型 	默认显示 	描述
date 	str 	Y 	统计周期
new_sh 	int 	Y 	本周新增（上海，户）
new_sz 	int 	Y 	本周新增（深圳，户）
active_sh 	float 	Y 	期末有效账户（上海，万户）
active_sz 	float 	Y 	期末有效账户（深圳，万户）
total_sh 	float 	Y 	期末账户数（上海，万户）
total_sz 	float 	Y 	期末账户数（深圳，万户）
trade_sh 	float 	Y 	参与交易账户数（上海，万户）
trade_sz 	float 	Y 	参与交易账户数（深圳，万户）
        """
    },
    "股东人数": {
        "api":"stk_holdernumber",
        "desc":"""接口：stk_holdernumber
描述：获取上市公司股东户数数据，数据不定期公布
限量：单次最大3000,总量不限制
积分：600积分可调取，基础积分每分钟调取100次，5000积分以上频次相对较高。具体请参阅积分获取办法


输入参数
名称 	类型 	必选 	描述
ts_code 	str 	N 	TS股票代码
enddate 	str 	N 	截止日期
start_date 	str 	N 	公告开始日期
end_date 	str 	N 	公告结束日期


输出参数
名称 	类型 	默认显示 	描述
ts_code 	str 	Y 	TS股票代码
ann_date 	str 	Y 	公告日期
end_date 	str 	Y 	截止日期
holder_num 	int 	Y 	股东户数
        """
    },
    "股东增减持": {
        "api":"stk_holdertrade",
        "desc":"""接口：stk_holdertrade
描述：获取上市公司增减持数据，了解重要股东近期及历史上的股份增减变化
限量：单次最大提取3000行记录，总量不限制
积分：用户需要至少2000积分才可以调取。基础积分有流量控制，积分越多权限越大，5000积分以上无明显限制，请自行提高积分，具体请参阅积分获取办法


输入参数
名称 	类型 	必选 	描述
ts_code 	str 	N 	TS股票代码
ann_date 	str 	N 	公告日期
start_date 	str 	N 	公告开始日期
end_date 	str 	N 	公告结束日期
trade_type 	str 	N 	交易类型IN增持DE减持
holder_type 	str 	N 	股东类型C公司P个人G高管


输出参数
名称 	类型 	默认显示 	描述
ts_code 	str 	Y 	TS代码
ann_date 	str 	Y 	公告日期
holder_name 	str 	Y 	股东名称
holder_type 	str 	Y 	股东类型G高管P个人C公司
in_de 	str 	Y 	类型IN增持DE减持
change_vol 	float 	Y 	变动数量
change_ratio 	float 	Y 	占流通比例（%）
after_share 	float 	Y 	变动后持股
after_ratio 	float 	Y 	变动后占流通比例（%）
avg_price 	float 	Y 	平均价格
total_share 	float 	Y 	持股总数
begin_date 	str 	N 	增减持开始日期
close_date 	str 	N 	增减持结束日期
        """
    },
    "券商月度金股": {
        "api":"broker_recommend",
        "desc":"""接口：broker_recommend
描述：每月初获取券商月度金股
限量：单次最大1000，积分达到600即可调用，具体请参阅积分获取办法

输入参数
名称 	类型 	必选 	描述
month 	str 	Y 	月度（YYYYMM）

输出参数
名称 	类型 	默认显示 	描述
month 	str 	Y 	月度
broker 	str 	Y 	券商
ts_code 	str 	Y 	股票代码
name 	str 	Y 	股票简称
        """
    },
    "指数基本信息": {
        "api":"index_basic",
        "desc":"""接口：index_basic
描述：获取指数基础信息。

输入参数
名称 	类型 	必选 	描述
ts_code 	str 	N 	指数代码
name 	str 	N 	指数简称
market 	str 	N 	交易所或服务商(默认SSE)
publisher 	str 	N 	发布商
category 	str 	N 	指数类别

输出参数
名称 	类型 	描述
ts_code 	str 	TS代码
name 	str 	简称
fullname 	str 	指数全称
market 	str 	市场
publisher 	str 	发布方
index_type 	str 	指数风格
category 	str 	指数类别
base_date 	str 	基期
base_point 	float 	基点
list_date 	str 	发布日期
weight_rule 	str 	加权方式
desc 	str 	描述
exp_date 	str 	终止日期

市场说明(market)
市场代码 	说明
MSCI 	MSCI指数
CSI 	中证指数
SSE 	上交所指数
SZSE 	深交所指数
CICC 	中金指数
SW 	申万指数
OTH 	其他指数

指数列表

    主题指数
    规模指数
    策略指数
    风格指数
    综合指数
    成长指数
    价值指数
    有色指数
    化工指数
    能源指数
    其他指数
    外汇指数
    基金指数
    商品指数
    债券指数
    行业指数
    贵金属指数
    农副产品指数
    软商品指数
    油脂油料指数
    非金属建材指数
    煤焦钢矿指数
    谷物指数

        """
    },
    "指数日线行情": {
        "api":"index_daily",
        "desc":"""接口：index_daily
描述：获取指数每日行情，还可以通过bar接口获取。由于服务器压力，目前规则是单次调取最多取8000行记录，可以设置start和end日期补全。指数行情也可以通过通用行情接口获取数据．
权限：常规指数需累积200积分可低频调取，5000积分以上频次相对较高。本接口不包括申万行情数据，申万等行业指数行情请在QQ群联系群主，具体请参阅积分获取办法

输入参数
名称 	类型 	必选 	描述
ts_code 	str 	Y 	指数代码
trade_date 	str 	N 	交易日期 （日期格式：YYYYMMDD，下同）
start_date 	str 	N 	开始日期
end_date 	str 	N 	结束日期

输出参数
名称 	类型 	描述
ts_code 	str 	TS指数代码
trade_date 	str 	交易日
close 	float 	收盘点位
open 	float 	开盘点位
high 	float 	最高点位
low 	float 	最低点位
pre_close 	float 	昨日收盘点
change 	float 	涨跌点
pct_chg 	float 	涨跌幅（%）
vol 	float 	成交量（手）
amount 	float 	成交额（千元）
        """
    },
    "指数周线行情": {
        "api":"index_weekly",
        "desc":"""接口：index_weekly
描述：获取指数周线行情
限量：单次最大1000行记录，可分批获取，总量不限制
积分：用户需要至少600积分才可以调取，积分越多频次越高，具体请参阅积分获取办法

输入参数
名称 	类型 	必选 	描述
ts_code 	str 	N 	TS代码
trade_date 	str 	N 	交易日期
start_date 	str 	N 	开始日期
end_date 	str 	N 	结束日期

输出参数
名称 	类型 	默认显示 	描述
ts_code 	str 	Y 	TS指数代码
trade_date 	str 	Y 	交易日
close 	float 	Y 	收盘点位
open 	float 	Y 	开盘点位
high 	float 	Y 	最高点位
low 	float 	Y 	最低点位
pre_close 	float 	Y 	昨日收盘点
change 	float 	Y 	涨跌点位
pct_chg 	float 	Y 	涨跌幅
vol 	float 	Y 	成交量
amount 	float 	Y 	成交额
        """
    },
    "指数月线行情": {
        "api":"index_monthly",
        "desc":"""接口：index_monthly
描述：获取指数月线行情,每月更新一次
限量：单次最大1000行记录,可多次获取,总量不限制
积分：用户需要至少600积分才可以调取，积分越多频次越高，具体请参阅积分获取办法


输入参数
名称 	类型 	必选 	描述
ts_code 	str 	N 	TS代码
trade_date 	str 	N 	交易日期
start_date 	str 	N 	开始日期
end_date 	str 	N 	结束日期


输出参数
名称 	类型 	默认显示 	描述
ts_code 	str 	Y 	TS指数代码
trade_date 	str 	Y 	交易日
close 	float 	Y 	收盘点位
open 	float 	Y 	开盘点位
high 	float 	Y 	最高点位
low 	float 	Y 	最低点位
pre_close 	float 	Y 	昨日收盘点
change 	float 	Y 	涨跌点位
pct_chg 	float 	Y 	涨跌幅
vol 	float 	Y 	成交量
amount 	float 	Y 	成交额
        """
    },
    "指数成分和权重": {
        "api":"index_weight",
        "desc":"""接口：index_weight
描述：获取各类指数成分和权重，月度数据 。
来源：指数公司网站公开数据
积分：用户需要至少400积分才可以调取，具体请参阅积分获取办法

输入参数
名称 	类型 	必选 	描述
index_code 	str 	Y 	指数代码 (二选一)
trade_date 	str 	Y 	交易日期 （二选一）
start_date 	str 	N 	开始日期
end_date 	None 	N 	结束日期

输出参数
名称 	类型 	描述
index_code 	str 	指数代码
con_code 	str 	成分代码
trade_date 	str 	交易日期
weight 	float 	权重
        """
    },
    "大盘指数每日指标": {
        "api":"index_dailybasic",
        "desc":"""接口：index_dailybasic
描述：目前只提供上证综指，深证成指，上证50，中证500，中小板指，创业板指的每日指标数据
数据来源：Tushare社区统计计算
数据历史：从2004年1月开始提供
数据权限：用户需要至少400积分才可以调取，具体请参阅积分获取办法

输入参数
名称 	类型 	必选 	描述
trade_date 	str 	N 	交易日期 （格式：YYYYMMDD，比如20181018，下同）
ts_code 	str 	N 	TS代码
start_date 	str 	N 	开始日期
end_date 	str 	N 	结束日期

注：trade_date，ts_code 至少要输入一个参数，单次限量3000条（即，单一指数单次可提取超过12年历史），总量不限制。

输出参数
名称 	类型 	默认显示 	描述
ts_code 	str 	Y 	TS代码
trade_date 	str 	Y 	交易日期
total_mv 	float 	Y 	当日总市值（元）
float_mv 	float 	Y 	当日流通市值（元）
total_share 	float 	Y 	当日总股本（股）
float_share 	float 	Y 	当日流通股本（股）
free_share 	float 	Y 	当日自由流通股本（股）
turnover_rate 	float 	Y 	换手率
turnover_rate_f 	float 	Y 	换手率(基于自由流通股本)
pe 	float 	Y 	市盈率
pe_ttm 	float 	Y 	市盈率TTM
pb 	float 	Y 	市净率
        """
    },
    "申万行业分类": {
        "api":"index_classify",
        "desc":"""接口：index_classify
描述：获取申万行业分类，包括申万28个一级分类，104个二级分类，227个三级分类的列表信息
权限：用户需2000积分可以调取，具体请参阅积分获取办法


输入参数
名称 	类型 	必选 	描述
index_code 	str 	N 	指数代码
level 	str 	N 	行业分级（L1/L2/L3）
src 	str 	N 	指数来源（SW申万）


输出参数
名称 	类型 	默认显示 	描述
index_code 	str 	Y 	指数代码
industry_name 	str 	Y 	行业名称
level 	str 	Y 	行业名称
industry_code 	str 	N 	行业代码
src 	str 	N 	行业分类（SW申万）
        """
    },
    "申万行业成分": {
        "api":"index_member",
        "desc":"""接口：index_member
描述：申万行业成分
限量：单次最大2000行，总量不限制
权限：用户需2000积分可调取，积分获取方法请参阅积分获取办法


输入参数
名称 	类型 	必选 	描述
index_code 	str 	N 	指数代码
ts_code 	str 	N 	股票代码
is_new 	str 	N 	是否最新（默认为“Y是”）


输出参数
名称 	类型 	默认显示 	描述
index_code 	str 	Y 	指数代码
index_name 	str 	N 	指数名称
con_code 	str 	Y 	成分股票代码
con_name 	str 	Y 	成分股票名称
in_date 	str 	Y 	纳入日期
out_date 	str 	Y 	剔除日期
is_new 	str 	N 	是否最新Y是N否
        """
    },
    "市场每日交易统计": {
        "api":"daily_info",
        "desc":"""接口：daily_info
描述：获取交易所股票交易统计，包括各板块明细
限量：单次最大4000，可循环获取，总量不限制
权限：用户积600积分可调取， 频次有限制，积分越高每分钟调取频次越高，5000积分以上频次相对较高，积分获取方法请参阅积分获取办法


输入参数
名称 	类型 	必选 	描述
trade_date 	str 	N 	交易日期（YYYYMMDD格式，下同）
ts_code 	str 	N 	板块代码（请参阅下方列表）
exchange 	str 	N 	股票市场（SH上交所 SZ深交所）
start_date 	str 	N 	开始日期
end_date 	str 	N 	结束日期
fields 	str 	N 	指定提取字段


板块代码（TS_CODE） 	板块名称（TS_NAME） 	数据开始日期
SZ_MARKET 	深圳市场 	20041231
SZ_MAIN 	深圳主板 	20081231
SZ_A 	深圳A股 	20080103
SZ_B 	深圳B股 	20080103
SZ_GEM 	创业板 	20091030
SZ_SME 	中小企业板 	20040602
SZ_FUND 	深圳基金市场 	20080103
SZ_FUND_ETF 	深圳基金ETF 	20080103
SZ_FUND_LOF 	深圳基金LOF 	20080103
SZ_FUND_CEF 	深圳封闭基金 	20080103
SZ_FUND_SF 	深圳分级基金 	20080103
SZ_BOND 	深圳债券 	20080103
SZ_BOND_CN 	深圳债券现券 	20080103
SZ_BOND_REP 	深圳债券回购 	20080103
SZ_BOND_ABS 	深圳债券ABS 	20080103
SZ_BOND_GOV 	深圳国债 	20080103
SZ_BOND_ENT 	深圳企业债 	20080103
SZ_BOND_COR 	深圳公司债 	20080103
SZ_BOND_CB 	深圳可转债 	20080103
SZ_WR 	深圳权证 	20080103
---- 	---- 	---
SH_MARKET 	上海市场 	20190102
SH_A 	上海A股 	19910102
SH_B 	上海B股 	19920221
SH_STAR 	科创板 	20190722
SH_REP 	股票回购 	20190102
SH_FUND 	上海基金市场 	19901219
SH_FUND_ETF 	上海基金ETF 	19901219
SH_FUND_LOF 	上海基金LOF 	19901219
SH_FUND_REP 	上海基金回购 	19901219
SH_FUND_CEF 	上海封闭式基金 	19901219
SH_FUND_METF 	上海交易型货币基金 	19901219


输出参数
名称 	类型 	默认显示 	描述
trade_date 	str 	Y 	交易日期
ts_code 	str 	Y 	市场代码
ts_name 	str 	Y 	市场名称
com_count 	int 	Y 	挂牌数
total_share 	float 	Y 	总股本（亿股）
float_share 	float 	Y 	流通股本（亿股）
total_mv 	float 	Y 	总市值（亿元）
float_mv 	float 	Y 	流通市值（亿元）
amount 	float 	Y 	交易金额（亿元）
vol 	float 	Y 	成交量（亿股）
trans_count 	int 	Y 	成交笔数（万笔）
pe 	float 	Y 	平均市盈率
tr 	float 	Y 	换手率（％），注：深交所暂无此列
exchange 	str 	Y 	交易所（SH上交所 SZ深交所）
        """
    },
    "同花顺概念和行业列表": {
        "api":"ths_index",
        "desc":"""接口：ths_index
描述：获取同花顺板块指数。注：数据版权归属同花顺，如做商业用途，请主动联系同花顺，如需帮助请联系微信migedata 。
限量：本接口需获得600积分，单次最大5000，一次可提取全部数据，请勿循环提取。


输入参数
名称 	类型 	必选 	描述
ts_code 	str 	N 	指数代码
exchange 	str 	N 	市场类型A-a股 HK-港股 US-美股
type 	str 	N 	指数类型 N-板块指数 I-行业指数 S-同花顺特色指数


输出参数
名称 	类型 	默认显示 	描述
ts_code 	str 	Y 	代码
name 	str 	Y 	名称
count 	int 	Y 	成分个数
exchange 	str 	Y 	交易所
list_date 	str 	Y 	上市日期
type 	str 	Y 	N概念指数S特色指数
        """
    },
    "同花顺概念和行业指数行情": {
        "api":"ths_daily",
        "desc":"""接口：ths_daily
描述：获取同花顺板块指数行情。注：数据版权归属同花顺，如做商业用途，请主动联系同花顺，如需帮助请联系微信migedata 。
限量：单次最大3000行数据，可根据指数代码、日期参数循环提取。


输入参数
名称 	类型 	必选 	描述
ts_code 	str 	N 	指数代码
trade_date 	str 	N 	交易日期（YYYYMMDD格式，下同）
start_date 	str 	N 	开始日期
end_date 	str 	N 	结束日期


输出参数
名称 	类型 	默认显示 	描述
ts_code 	str 	Y 	TS指数代码
trade_date 	str 	Y 	交易日
close 	float 	Y 	收盘点位
open 	float 	Y 	开盘点位
high 	float 	Y 	最高点位
low 	float 	Y 	最低点位
pre_close 	float 	Y 	昨日收盘点
avg_price 	float 	Y 	平均价
change 	float 	Y 	涨跌点位
pct_change 	float 	Y 	涨跌幅
vol 	float 	Y 	成交量
turnover_rate 	float 	Y 	换手率
total_mv 	float 	N 	总市值
float_mv 	float 	N 	流通市值
        """
    },
    "同花顺概念和行业指数成分": {
        "api":"ths_member",
        "desc":"""接口：ths_member
描述：获取同花顺概念板块成分列表注：数据版权归属同花顺，如做商业用途，请主动联系同花顺。
限量：用户积累5000积分可调取，可按概念板块代码循环提取所有成分


输入参数
名称 	类型 	必选 	描述
ts_code 	str 	N 	板块指数代码


输出参数
名称 	类型 	默认显示 	描述
ts_code 	str 	Y 	指数代码
code 	str 	Y 	股票代码
name 	str 	Y 	股票名称
weight 	float 	N 	权重
in_date 	str 	N 	纳入日期
out_date 	str 	N 	剔除日期
is_new 	str 	N 	是否最新Y是N否
        """
    },
    "国际主要指数": {
        "api":"index_global",
        "desc":"""接口：index_global
描述：获取国际主要指数日线行情
限量：单次最大提取4000行情数据，可循环获取，总量不限制
积分：用户积6000积分可调取，积分越高频次越高，请自行提高积分，具体请参阅积分获取办法


输入参数
名称 	类型 	必选 	描述
ts_code 	str 	N 	TS指数代码，见下表
trade_date 	str 	N 	交易日期，YYYYMMDD格式，下同
start_date 	str 	N 	开始日期
end_date 	str 	N 	结束日期


TS指数代码 	指数名称
XIN9 	富时中国A50指数 (富时A50)
HSI 	恒生指数
DJI 	道琼斯工业指数
SPX 	标普500指数
IXIC 	纳斯达克指数
FTSE 	富时100指数
FCHI 	法国CAC40指数
GDAXI 	德国DAX指数
N225 	日经225指数
KS11 	韩国综合指数
AS51 	澳大利亚标普200指数
SENSEX 	印度孟买SENSEX指数
IBOVESPA 	巴西IBOVESPA指数
RTS 	俄罗斯RTS指数
TWII 	台湾加权指数
CKLSE 	马来西亚指数
SPTSX 	加拿大S&P/TSX指数
CSX5P 	STOXX欧洲50指数
RUT 	罗素2000指数


输出参数
名称 	类型 	默认显示 	描述
ts_code 	str 	Y 	TS指数代码
trade_date 	str 	Y 	交易日
open 	float 	Y 	开盘点位
close 	float 	Y 	收盘点位
high 	float 	Y 	最高点位
low 	float 	Y 	最低点位
pre_close 	float 	Y 	昨日收盘点
change 	float 	Y 	涨跌点位
pct_chg 	float 	Y 	涨跌幅
swing 	float 	Y 	振幅
vol 	float 	Y 	成交量 （大部分无此项数据）
amount 	float 	N 	成交额 （大部分无此项数据）
        """
    },
    "基金列表": {
        "api":"fund_basic",
        "desc":"""接口：fund_basic
描述：获取公募基金数据列表，包括场内和场外基金
积分：用户需要1500积分才可以调取，具体请参阅积分获取办法

输入参数
名称 	类型 	必选 	描述
market 	str 	N 	交易市场: E场内 O场外（默认E）
status 	str 	N 	存续状态 D摘牌 I发行 L上市中

输出参数
名称 	类型 	默认显示 	描述
ts_code 	str 	Y 	基金代码
name 	str 	Y 	简称
management 	str 	Y 	管理人
custodian 	str 	Y 	托管人
fund_type 	str 	Y 	投资类型
found_date 	str 	Y 	成立日期
due_date 	str 	Y 	到期日期
list_date 	str 	Y 	上市时间
issue_date 	str 	Y 	发行日期
delist_date 	str 	Y 	退市日期
issue_amount 	float 	Y 	发行份额(亿)
m_fee 	float 	Y 	管理费
c_fee 	float 	Y 	托管费
duration_year 	float 	Y 	存续期
p_value 	float 	Y 	面值
min_amount 	float 	Y 	起点金额(万元)
exp_return 	float 	Y 	预期收益率
benchmark 	str 	Y 	业绩比较基准
status 	str 	Y 	存续状态D摘牌 I发行 L已上市
invest_type 	str 	Y 	投资风格
type 	str 	Y 	基金类型
trustee 	str 	Y 	受托人
purc_startdate 	str 	Y 	日常申购起始日
redm_startdate 	str 	Y 	日常赎回起始日
market 	str 	Y 	E场内O场外
        """
    },
    "基金管理人": {
        "api":"fund_company",
        "desc":"""接口：fund_company
描述：获取公募基金管理人列表
积分：用户需要1500积分才可以调取，一次可以提取全部数据。具体请参阅积分获取办法

输入参数

无，可提取全部

输出参数
名称 	类型 	默认显示 	描述
name 	str 	Y 	基金公司名称
shortname 	str 	Y 	简称
short_enname 	str 	N 	英文缩写
province 	str 	Y 	省份
city 	str 	Y 	城市
address 	str 	Y 	注册地址
phone 	str 	Y 	电话
office 	str 	Y 	办公地址
website 	str 	Y 	公司网址
chairman 	str 	Y 	法人代表
manager 	str 	Y 	总经理
reg_capital 	float 	Y 	注册资本
setup_date 	str 	Y 	成立日期
end_date 	str 	Y 	公司终止日期
employees 	float 	Y 	员工总数
main_business 	str 	Y 	主要产品及业务
org_code 	str 	Y 	组织机构代码
credit_code 	str 	Y 	统一社会信用代码
        """
    },
    "基金经理": {
        "api":"fund_manager",
        "desc":"""接口：fund_manager
描述：获取公募基金经理数据，包括基金经理简历等数据
限量：单次最大5000，支持分页提取数据
积分：用户有500积分可获取数据，2000积分以上可以提高访问频次


输入参数
名称 	类型 	必选 	描述
ts_code 	str 	N 	基金代码，支持多只基金，逗号分隔
ann_date 	str 	N 	公告日期，格式：YYYYMMDD
name 	str 	N 	基金经理姓名
offset 	intint 	N 	开始行数
limit 	int 	N 	每页行数


输出参数
名称 	类型 	默认显示 	描述
ts_code 	str 	Y 	基金代码
ann_date 	str 	Y 	公告日期
name 	str 	Y 	基金经理姓名
gender 	str 	Y 	性别
birth_year 	str 	Y 	出生年份
edu 	str 	Y 	学历
nationality 	str 	Y 	国籍
begin_date 	str 	Y 	任职日期
end_date 	str 	Y 	离任日期
resume 	str 	Y 	简历
        """
    },
    "基金规模": {
        "api":"fund_share",
        "desc":"""接口：fund_share
描述：获取基金规模数据，包含上海和深圳ETF基金
限量：单次最大提取2000行数据
积分：用户需要至少2000积分可以调取，5000积分以上正常调取无频次限制，具体请参阅积分获取办法


输入参数
名称 	类型 	必选 	描述
ts_code 	str 	N 	TS基金代码
trade_date 	str 	N 	交易日期
start_date 	str 	N 	开始日期
end_date 	str 	N 	结束日期
fund_type 	str 	N 	基金类型，见下表
market 	str 	N 	市场：SH/SZ


fund_type标识说明：
标识 	含义
ETF 	ETF基金
LOF 	LOF基金
SF 	分级基金
CEF 	封闭基金


输出参数
名称 	类型 	默认显示 	描述
ts_code 	str 	Y 	基金代码，支持多只基金同时提取，用逗号分隔
trade_date 	str 	Y 	交易（变动）日期，格式YYYYMMDD
fd_share 	float 	Y 	基金份额（万）
        """
    },
    "基金净值": {
        "api":"fund_nav",
        "desc":"""接口：fund_nav
描述：获取公募基金净值数据
积分：用户需要至少2000积分才可以调取，具体请参阅积分获取办法

输入参数
名称 	类型 	必选 	描述
ts_code 	str 	N 	TS基金代码 （二选一）
end_date 	str 	N 	净值日期 （二选一）
market 	str 	N 	E场内 O场外

输出参数
名称 	类型 	默认显示 	描述
ts_code 	str 	Y 	TS代码
ann_date 	str 	Y 	公告日期
end_date 	str 	Y 	截止日期
unit_nav 	float 	Y 	单位净值
accum_nav 	float 	Y 	累计净值
accum_div 	float 	Y 	累计分红
net_asset 	float 	Y 	资产净值
total_netasset 	float 	Y 	合计资产净值
adj_nav 	float 	Y 	复权单位净值
        """
    },
    "基金分红": {
        "api":"fund_div",
        "desc":"""接口：fund_div
描述：获取公募基金分红数据
积分：用户需要至少400积分才可以调取，具体请参阅积分获取办法

输入参数
名称 	类型 	必选 	描述
ann_date 	str 	N 	公告日（以下参数四选一）
ex_date 	str 	N 	除息日
pay_date 	str 	N 	派息日
ts_code 	str 	N 	基金代码

输出参数
名称 	类型 	默认显示 	描述
ts_code 	str 	Y 	TS代码
ann_date 	str 	Y 	公告日期
imp_anndate 	str 	Y 	分红实施公告日
base_date 	str 	Y 	分配收益基准日
div_proc 	str 	Y 	方案进度
record_date 	str 	Y 	权益登记日
ex_date 	str 	Y 	除息日
pay_date 	str 	Y 	派息日
earpay_date 	str 	Y 	收益支付日
net_ex_date 	str 	Y 	净值除权日
div_cash 	float 	Y 	每股派息(元)
base_unit 	float 	Y 	基准基金份额(万份)
ear_distr 	float 	Y 	可分配收益(元)
ear_amount 	float 	Y 	收益分配金额(元)
account_date 	str 	Y 	红利再投资到账日
base_year 	str 	Y 	份额基准年度
        """
    },
    "基金持仓": {
        "api":"fund_portfolio",
        "desc":"""接口：fund_portfolio
描述：获取公募基金持仓数据，季度更新
积分：用户需要至少2000积分才可以调取，5000积分以上频次会比较高，具体请参阅积分获取办法

输入参数
名称 	类型 	必选 	描述
ts_code 	str 	Y 	基金代码
ann_date 	str 	N 	公告日期（YYYYMMDD格式）
start_date 	str 	N 	报告期开始日期（YYYYMMDD格式）
end_date 	str 	N 	报告期结束日期（YYYYMMDD格式）

输出参数
名称 	类型 	默认显示 	描述
ts_code 	str 	Y 	TS基金代码
ann_date 	str 	Y 	公告日期
end_date 	str 	Y 	截止日期
symbol 	str 	Y 	股票代码
mkv 	float 	Y 	持有股票市值(元)
amount 	float 	Y 	持有股票数量（股）
stk_mkv_ratio 	float 	Y 	占股票市值比
stk_float_ratio 	float 	Y 	占流通股本比例
        """
    },
    "基金行情": {
        "api":"fund_daily",
        "desc":"""接口：fund_daily
描述：获取场内基金日线行情，类似股票日行情
更新：每日收盘后2小时内
限量：单次最大800行记录，总量不限制
积分：用户需要至少500积分才可以调取，具体请参阅积分获取办法

复权行情实现参考：

后复权 = 当日最新价 × 当日复权因子
前复权 = 当日复权价 ÷ 最新复权因子

输入参数
名称 	类型 	必选 	描述
ts_code 	str 	N 	基金代码（二选一）
trade_date 	str 	N 	交易日期（二选一）
start_date 	str 	N 	开始日期
end_date 	str 	N 	结束日期

输出参数
名称 	类型 	默认显示 	描述
ts_code 	str 	Y 	TS代码
trade_date 	str 	Y 	交易日期
open 	float 	Y 	开盘价(元)
high 	float 	Y 	最高价(元)
low 	float 	Y 	最低价(元)
close 	float 	Y 	收盘价(元)
pre_close 	float 	Y 	昨收盘价(元)
change 	float 	Y 	涨跌额(元)
pct_chg 	float 	Y 	涨跌幅(%)
vol 	float 	Y 	成交量(手)
amount 	float 	Y 	成交额(千元)
        """
    },
    "基金复权因子": {
        "api":"fund_adj",
        "desc":"""接口：fund_adj
描述：获取基金复权因子，用于计算基金复权行情
限量：单次最大提取2000行记录，可循环提取，数据总量不限制
积分：用户积600积分可调取，超过5000积分以上频次相对较高。具体请参阅积分获取办法


复权行情实现参考：

后复权 = 当日最新价 × 当日复权因子
前复权 = 当日复权价 ÷ 最新复权因子


输入参数
名称 	类型 	必选 	描述
ts_code 	str 	N 	TS基金代码（支持多只基金输入）
trade_date 	str 	N 	交易日期（格式：yyyymmdd，下同）
start_date 	str 	N 	开始日期
end_date 	str 	N 	结束日期
offset 	str 	N 	开始行数
limit 	str 	N 	最大行数


输出参数
名称 	类型 	默认显示 	描述
ts_code 	str 	Y 	ts基金代码
trade_date 	str 	Y 	交易日期
adj_factor 	float 	Y 	复权因子
        """
    },
    "期货合约信息": {
        "api":"fut_basic",
        "desc":"""接口：fut_basic
描述：获取期货合约列表数据
限量：单次最大10000
积分：用户需要至少200积分才可以调取，具体请参阅积分获取办法

输入参数
名称 	类型 	必选 	描述
exchange 	str 	Y 	交易所代码 CFFEX-中金所 DCE-大商所 CZCE-郑商所 SHFE-上期所 INE-上海国际能源交易中心
fut_type 	str 	N 	合约类型 (1 普通合约 2主力与连续合约 默认取全部)

输出参数
名称 	类型 	默认显示 	描述
ts_code 	str 	Y 	合约代码
symbol 	str 	Y 	交易标识
exchange 	str 	Y 	交易市场
name 	str 	Y 	中文简称
fut_code 	str 	Y 	合约产品代码
multiplier 	float 	Y 	合约乘数
trade_unit 	str 	Y 	交易计量单位
per_unit 	float 	Y 	交易单位(每手)
quote_unit 	str 	Y 	报价单位
quote_unit_desc 	str 	Y 	最小报价单位说明
d_mode_desc 	str 	Y 	交割方式说明
list_date 	str 	Y 	上市日期
delist_date 	str 	Y 	最后交易日期
d_month 	str 	Y 	交割月份
last_ddate 	str 	Y 	最后交割日
trade_time_desc 	str 	N 	交易时间说明
        """
    },
    "期货交易日历": {
        "api":"trade_cal",
        "desc":"""接口：trade_cal
描述：获取各大期货交易所交易日历数据
积分：注册用户即可获取，无积分要求

输入参数
名称 	类型 	必选 	描述
exchange 	str 	N 	交易所 SHFE 上期所 DCE 大商所 CFFEX中金所 CZCE郑商所 INE上海国际能源交易所
start_date 	str 	N 	开始日期
end_date 	str 	N 	结束日期
is_open 	int 	N 	是否交易 0休市 1交易

输出参数
名称 	类型 	默认显示 	描述
exchange 	str 	Y 	交易所 同参数部分描述
cal_date 	str 	Y 	日历日期
is_open 	int 	Y 	是否交易 0休市 1交易
pretrade_date 	str 	N 	上一个交易日
        """
    },
    "期货日线行情": {
        "api":"fut_daily",
        "desc":"""接口：fut_daily
描述：期货日线行情数据
限量：单次最大2000条，总量不限制
积分：用户需要至少2000积分才可以调取，未来可能调整积分，请尽量多的积累积分。具体请参阅积分获取办法

输入参数
名称 	类型 	必选 	描述
trade_date 	str 	N 	交易日期
ts_code 	str 	N 	合约代码
exchange 	str 	N 	交易所代码
start_date 	str 	N 	开始日期
end_date 	str 	N 	结束日期

输出参数
名称 	类型 	默认显示 	描述
ts_code 	str 	Y 	TS合约代码
trade_date 	str 	Y 	交易日期
pre_close 	float 	Y 	昨收盘价
pre_settle 	float 	Y 	昨结算价
open 	float 	Y 	开盘价
high 	float 	Y 	最高价
low 	float 	Y 	最低价
close 	float 	Y 	收盘价
settle 	float 	Y 	结算价
change1 	float 	Y 	涨跌1 收盘价-昨结算价
change2 	float 	Y 	涨跌2 结算价-昨结算价
vol 	float 	Y 	成交量(手)
amount 	float 	Y 	成交金额(万元)
oi 	float 	Y 	持仓量(手)
oi_chg 	float 	Y 	持仓量变化
delv_settle 	float 	N 	交割结算价
        """
    },
    "每日持仓排名": {
        "api":"fut_holding",
        "desc":"""接口：fut_holding
描述：获取每日成交持仓排名数据
限量：单次最大2000，总量不限制
积分：用户需要至少600积分才可以调取，具体请参阅积分获取办法

输入参数
名称 	类型 	必选 	描述
trade_date 	str 	N 	交易日期 （trade_date/symbol至少输入一个参数）
symbol 	str 	N 	合约或产品代码
start_date 	str 	N 	开始日期
end_date 	str 	N 	结束日期
exchange 	str 	N 	交易所代码

输出参数
名称 	类型 	默认显示 	描述
trade_date 	str 	Y 	交易日期
symbol 	str 	Y 	合约代码或类型
broker 	str 	Y 	期货公司会员简称
vol 	int 	Y 	成交量
vol_chg 	int 	Y 	成交量变化
long_hld 	int 	Y 	持买仓量
long_chg 	int 	Y 	持买仓量变化
short_hld 	int 	Y 	持卖仓量
short_chg 	int 	Y 	持卖仓量变化
exchange 	str 	N 	交易所
        """
    },
    "仓单日报": {
        "api":"fut_wsr",
        "desc":"""接口：fut_wsr
描述：获取仓单日报数据，了解各仓库/厂库的仓单变化
限量：单次最大1000，总量不限制
积分：用户需要至少600积分才可以调取，具体请参阅积分获取办法

输入参数
名称 	类型 	必选 	描述
trade_date 	str 	N 	交易日期
symbol 	str 	N 	产品代码
start_date 	str 	N 	开始日期
end_date 	str 	N 	结束日期
exchange 	str 	N 	交易所代码

输出参数
名称 	类型 	默认显示 	描述
trade_date 	str 	Y 	交易日期
symbol 	str 	Y 	产品代码
fut_name 	str 	Y 	产品名称
warehouse 	str 	Y 	仓库名称
wh_id 	str 	N 	仓库编号
pre_vol 	int 	Y 	昨日仓单量
vol 	int 	Y 	今日仓单量
vol_chg 	int 	Y 	增减量
area 	str 	N 	地区
year 	str 	N 	年度
grade 	str 	N 	等级
brand 	str 	N 	品牌
place 	str 	N 	产地
pd 	int 	N 	升贴水
is_ct 	str 	N 	是否折算仓单
unit 	str 	Y 	单位
exchange 	str 	N 	交易所
        """
    },
    "每日结算参数": {
        "api":"fut_settle",
        "desc":"""接口：fut_settle
描述：获取每日结算参数数据，包括交易和交割费率等
限量：单次最大1000，总量不限制
积分：用户需要至少600积分才可以调取，具体请参阅积分获取办法

输入参数
名称 	类型 	必选 	描述
trade_date 	str 	N 	交易日期 （trade_date/ts_code至少需要输入一个参数）
ts_code 	str 	N 	合约代码
start_date 	str 	N 	开始日期
end_date 	str 	N 	结束日期
exchange 	str 	N 	交易所代码

输出参数
名称 	类型 	默认显示 	描述
ts_code 	str 	Y 	合约代码
trade_date 	str 	Y 	交易日期
settle 	float 	Y 	结算价
trading_fee_rate 	float 	Y 	交易手续费率
trading_fee 	float 	Y 	交易手续费
delivery_fee 	float 	Y 	交割手续费
b_hedging_margin_rate 	float 	Y 	买套保交易保证金率
s_hedging_margin_rate 	float 	Y 	卖套保交易保证金率
long_margin_rate 	float 	Y 	买投机交易保证金率
short_margin_rate 	float 	Y 	卖投机交易保证金率
offset_today_fee 	float 	N 	平今仓手续率
exchange 	str 	N 	交易所
        """
    },
    "南华期货指数行情": {
        "api":"index_daily",
        "desc":"""接口：index_daily
描述：获取南华指数每日行情，指数行情也可以通过通用行情接口获取数据．
权限：用户需要累积200积分才可以调取，具体请参阅积分获取办法


输入参数
名称 	类型 	必选 	描述
ts_code 	str 	N 	指数代码（南华期货指数以 .NH 结尾，具体请参考本文最下方）
trade_date 	str 	N 	交易日期 （日期格式：YYYYMMDD，下同）
start_date 	str 	N 	开始日期
end_date 	None 	N 	结束日期


输出参数
名称 	类型 	描述
ts_code 	str 	TS指数代码
trade_date 	str 	交易日
close 	float 	收盘点位
open 	float 	开盘点位
high 	float 	最高点位
low 	float 	最低点位
pre_close 	float 	昨日收盘点
change 	float 	涨跌点
pct_chg 	float 	涨跌幅
vol 	float 	成交量（手）
amount 	float 	成交额（千元）
        """
    },
    "期货主力与连续合约": {
        "api":"fut_mapping",
        "desc":"""接口：fut_mapping
描述：获取期货主力（或连续）合约与月合约映射数据
限量：单次最大2000条，总量不限制
积分：用户需要至少600积分才可以调取，未来可能调整积分，请尽可能多积累积分。具体请参阅积分获取办法


输入参数
名称 	类型 	必选 	描述
ts_code 	str 	N 	合约代码
trade_date 	str 	N 	交易日期
start_date 	str 	N 	开始日期
end_date 	str 	N 	结束日期


输出参数
名称 	类型 	默认显示 	描述
ts_code 	str 	Y 	连续合约代码
trade_date 	str 	Y 	起始日期
mapping_ts_code 	str 	Y 	期货合约代码
        """
    },
    "期货主要品种交易周报": {
        "api":"fut_weekly_detail",
        "desc":"""接口：fut_weekly_detail
描述：获取期货交易所主要品种每周交易统计信息，数据从2010年3月开始
权限：600积分可调取，单次最大获取4000行数据，积分越高频次越高，5000积分以上正常调取不受限制
数据来源：中国证监会，本数据由Tushare社区成员CE完成规划和采集


输入参数
名称 	类型 	必选 	描述
week 	str 	N 	周期（每年第几周，e.g. 202001 表示2020第1周）
prd 	str 	N 	期货品种（支持多品种输入，逗号分隔）
start_week 	str 	N 	开始周期
end_week 	str 	N 	结束周期
exchange 	str 	N 	交易所（请参考交易所说明）
fields 	str 	N 	提取的字段，e.g. fields='prd,name,vol'


输出参数
名称 	类型 	默认显示 	描述
exchange 	str 	Y 	交易所代码
prd 	str 	Y 	期货品种代码
name 	str 	Y 	品种名称
vol 	int 	Y 	成交量（手）
vol_yoy 	float 	Y 	同比增减（%）
amount 	float 	Y 	成交金额（亿元）
amout_yoy 	float 	Y 	同比增减（%）
cumvol 	int 	Y 	年累计成交总量（手）
cumvol_yoy 	float 	Y 	同比增减（%）
cumamt 	float 	Y 	年累计成交金额（亿元）
cumamt_yoy 	float 	Y 	同比增减（%）
open_interest 	int 	Y 	持仓量（手）
interest_wow 	float 	Y 	环比增减（%）
mc_close 	float 	Y 	本周主力合约收盘价
close_wow 	float 	Y 	环比涨跌（%）
week 	str 	Y 	周期
week_date 	str 	Y 	周日期
        """
    },
    "期权合约信息": {
        "api":"opt_basic",
        "desc":"""接口：opt_basic
描述：获取期权合约信息
积分：用户需要至少600积分才可以调取，但有流量控制，请自行提高积分，积分越多权限越大，具体请参阅积分获取办法


输入参数
名称 	类型 	必选 	描述
ts_code 	str 	N 	TS期权代码
exchange 	str 	N 	交易所代码 （包括上交所SSE等交易所）
call_put 	str 	N 	期权类型


输出参数
名称 	类型 	默认显示 	描述
ts_code 	str 	Y 	TS代码
exchange 	str 	Y 	交易市场
name 	str 	Y 	合约名称
per_unit 	str 	Y 	合约单位
opt_code 	str 	Y 	标准合约代码
opt_type 	str 	Y 	合约类型
call_put 	str 	Y 	期权类型
exercise_type 	str 	Y 	行权方式
exercise_price 	float 	Y 	行权价格
s_month 	str 	Y 	结算月
maturity_date 	str 	Y 	到期日
list_price 	float 	Y 	挂牌基准价
list_date 	str 	Y 	开始交易日期
delist_date 	str 	Y 	最后交易日期
last_edate 	str 	Y 	最后行权日期
last_ddate 	str 	Y 	最后交割日期
quote_unit 	str 	Y 	报价单位
min_price_chg 	str 	Y 	最小价格波幅
        """
    },
    "期权日线行情": {
        "api":"opt_daily",
        "desc":"""接口：opt_daily
描述：获取期权日线行情
限量：单次最大1000，总量不限制
积分：用户需要至少2000积分才可以调取，但有流量控制，请自行提高积分，积分越多权限越大，具体请参阅积分获取办法


输入参数
名称 	类型 	必选 	描述
ts_code 	str 	N 	TS合约代码（输入代码或时间至少任意一个参数）
trade_date 	str 	N 	交易日期
start_date 	str 	N 	开始日期
end_date 	str 	N 	结束日期
exchange 	str 	N 	交易所


输出参数
名称 	类型 	默认显示 	描述
ts_code 	str 	Y 	TS代码
trade_date 	str 	Y 	交易日期
exchange 	str 	Y 	交易市场
pre_settle 	float 	Y 	昨结算价
pre_close 	float 	Y 	前收盘价
open 	float 	Y 	开盘价
high 	float 	Y 	最高价
low 	float 	Y 	最低价
close 	float 	Y 	收盘价
settle 	float 	Y 	结算价
vol 	float 	Y 	成交量(手)
amount 	float 	Y 	成交金额(万元)
oi 	float 	Y 	持仓量(手)
        """
    },
    "TICK数据": {
        "api":"ft_tick",
        "desc":"""接口：ft_tick
描述：获取期权和期货的tick数据
限量：单次最大10000条数据，可循环获取

注：本数据归属上海中期期货有限公司，具备该公司交易账号才可以获取

输入参数
名称 	类型 	必选 	描述
symbol 	str 	Y 	期货期权代码
start_date 	datetime 	N 	开始时间
end_date 	datetime 	N 	结束时间

输出参数
名称 	类型 	默认显示 	描述
symbol 	str 	Y 	交易代码
trade_time 	str 	Y 	交易时间
trade_ms 	str 	Y 	交易毫秒数
price 	str 	Y 	当前价
vol 	str 	Y 	成交量
amount 	str 	Y 	成交金额
ask_p1 	str 	Y 	申卖价一
ask_v1 	str 	Y 	申卖量一
bid_p1 	str 	Y 	申买价一
bid_v1 	str 	Y 	申买量一
oi 	str 	Y 	持仓量
        """
    },
    "可转债基础信息": {
        "api":"cb_basic",
        "desc":"""接口：cb_basic
描述：获取可转债基本信息
限量：单次最大2000，总量不限制
权限：用户需要至少2000积分才可以调取，但有流量控制，5000积分以上频次相对较高，积分越多权限越大，具体请参阅积分获取办法


输入参数
名称 	类型 	必选 	描述
ts_code 	str 	N 	转债代码
list_date 	str 	N 	上市日期
exchange 	str 	N 	上市地点


输出参数
名称 	类型 	默认显示 	描述
ts_code 	str 	Y 	转债代码
bond_full_name 	str 	Y 	转债名称
bond_short_name 	str 	Y 	转债简称
cb_code 	str 	Y 	转股申报代码
stk_code 	str 	Y 	正股代码
stk_short_name 	str 	Y 	正股简称
maturity 	float 	Y 	发行期限（年）
par 	float 	Y 	面值
issue_price 	float 	Y 	发行价格
issue_size 	float 	Y 	发行总额（元）
remain_size 	float 	Y 	债券余额（元）
value_date 	str 	Y 	起息日期
maturity_date 	str 	Y 	到期日期
rate_type 	str 	Y 	利率类型
coupon_rate 	float 	Y 	票面利率（%）
add_rate 	float 	Y 	补偿利率（%）
pay_per_year 	int 	Y 	年付息次数
list_date 	str 	Y 	上市日期
delist_date 	str 	Y 	摘牌日
exchange 	str 	Y 	上市地点
conv_start_date 	str 	Y 	转股起始日
conv_end_date 	str 	Y 	转股截止日
first_conv_price 	float 	Y 	初始转股价
conv_price 	float 	Y 	最新转股价
rate_clause 	str 	Y 	利率说明
put_clause 	str 	N 	赎回条款
maturity_put_price 	str 	N 	到期赎回价格(含税)
call_clause 	str 	N 	回售条款
reset_clause 	str 	N 	特别向下修正条款
conv_clause 	str 	N 	转股条款
guarantor 	str 	N 	担保人
guarantee_type 	str 	N 	担保方式
issue_rating 	str 	N 	发行信用等级
newest_rating 	str 	N 	最新信用等级
rating_comp 	str 	N 	最新评级机构
        """
    },
    "可转债发行": {
        "api":"cb_issue",
        "desc":"""接口：cb_issue
描述：获取可转债发行数据
限量：单次最大2000，可多次提取，总量不限制
积分：用户需要至少2000积分才可以调取，5000积分以上频次相对较高，积分越多权限越大，具体请参阅积分获取办法


输入参数
名称 	类型 	必选 	描述
ts_code 	str 	N 	TS代码
ann_date 	str 	N 	发行公告日
start_date 	str 	N 	公告开始日期
end_date 	str 	N 	公告结束日期


输出参数
名称 	类型 	默认显示 	描述
ts_code 	str 	Y 	转债代码
ann_date 	str 	Y 	发行公告日
res_ann_date 	str 	Y 	发行结果公告日
plan_issue_size 	float 	Y 	计划发行总额（元）
issue_size 	float 	Y 	发行总额（元）
issue_price 	float 	Y 	发行价格
issue_type 	str 	Y 	发行方式
issue_cost 	float 	N 	发行费用（元）
onl_code 	str 	Y 	网上申购代码
onl_name 	str 	Y 	网上申购简称
onl_date 	str 	Y 	网上发行日期
onl_size 	float 	Y 	网上发行总额（张）
onl_pch_vol 	float 	Y 	网上发行有效申购数量（张）
onl_pch_num 	int 	Y 	网上发行有效申购户数
onl_pch_excess 	float 	Y 	网上发行超额认购倍数
onl_winning_rate 	float 	N 	网上发行中签率（%）
shd_ration_code 	str 	Y 	老股东配售代码
shd_ration_name 	str 	Y 	老股东配售简称
shd_ration_date 	str 	Y 	老股东配售日
shd_ration_record_date 	str 	Y 	老股东配售股权登记日
shd_ration_pay_date 	str 	Y 	老股东配售缴款日
shd_ration_price 	float 	Y 	老股东配售价格
shd_ration_ratio 	float 	Y 	老股东配售比例
shd_ration_size 	float 	Y 	老股东配售数量（张）
shd_ration_vol 	float 	N 	老股东配售有效申购数量（张）
shd_ration_num 	int 	N 	老股东配售有效申购户数
shd_ration_excess 	float 	N 	老股东配售超额认购倍数
offl_size 	float 	Y 	网下发行总额（张）
offl_deposit 	float 	N 	网下发行定金比例（%）
offl_pch_vol 	float 	N 	网下发行有效申购数量（张）
offl_pch_num 	int 	N 	网下发行有效申购户数
offl_pch_excess 	float 	N 	网下发行超额认购倍数
offl_winning_rate 	float 	N 	网下发行中签率
lead_underwriter 	str 	N 	主承销商
lead_underwriter_vol 	float 	N 	主承销商包销数量（张）
        """
    },
    "可转债行情": {
        "api":"cb_daily",
        "desc":"""接口：cb_daily
描述：获取可转债行情
限量：单次最大2000条，可多次提取，总量不限制
积分：用户需要至少2000积分才可以调取，5000积分以上频次相对较高，积分越多权限越大，具体请参阅积分获取办法


输入参数
名称 	类型 	必选 	描述
ts_code 	str 	N 	TS代码
trade_date 	str 	N 	交易日期(YYYYMMDD格式，下同)
start_date 	str 	N 	开始日期
end_date 	str 	N 	结束日期


输出参数
名称 	类型 	默认显示 	描述
ts_code 	str 	Y 	转债代码
trade_date 	str 	Y 	交易日期
pre_close 	float 	Y 	昨收盘价(元)
open 	float 	Y 	开盘价(元)
high 	float 	Y 	最高价(元)
low 	float 	Y 	最低价(元)
close 	float 	Y 	收盘价(元)
change 	float 	Y 	涨跌(元)
pct_chg 	float 	Y 	涨跌幅(%)
vol 	float 	Y 	成交量(手)
amount 	float 	Y 	成交金额(万元)
        """
    },
    "可转债转股价变动": {
        "api":"cb_price_chg",
        "desc":"""接口：cb_price_chg
描述：获取可转债转股价变动
限量：单次最大2000，总量不限制
权限：用户需要至少2000积分才可以调取，但有流量控制，5000积分以上频次相对较高，积分越多权限越大，具体请参阅积分获取办法

输入参数
名称 	类型 	必选 	描述
ts_code 	str 	Y 	转债代码，支持多值输入

输出参数
名称 	类型 	默认显示 	描述
ts_code 	str 	Y 	转债代码
bond_short_name 	str 	Y 	转债简称
publish_date 	str 	Y 	公告日期
change_date 	str 	Y 	变动日期
convert_price_initial 	float 	Y 	初始转股价格
convertprice_bef 	float 	Y 	修正前转股价格
convertprice_aft 	float 	Y 	修正后转股价格
        """
    },
    "可转债转股结果": {
        "api":"cb_share",
        "desc":"""接口：cb_share
描述：获取可转债转股结果
限量：单次最大2000，总量不限制
权限：用户需要至少2000积分才可以调取，但有流量控制，5000积分以上频次相对较高，积分越多权限越大，具体请参阅积分获取办法

输入参数
名称 	类型 	必选 	描述
ts_code 	str 	Y 	转债代码，支持多值输入

输出参数
名称 	类型 	默认显示 	描述
ts_code 	str 	Y 	债券代码
bond_short_name 	str 	Y 	债券简称
publish_date 	str 	Y 	公告日期
end_date 	str 	Y 	统计截止日期
issue_size 	float 	Y 	可转债发行总额
convert_price_initial 	float 	Y 	初始转换价格
convert_price 	float 	Y 	本次转换价格
convert_val 	float 	Y 	本次转股金额
convert_vol 	float 	Y 	本次转股数量
convert_ratio 	float 	Y 	本次转股比例
acc_convert_val 	float 	Y 	累计转股金额
acc_convert_vol 	float 	Y 	累计转股数量
acc_convert_ratio 	float 	Y 	累计转股比例
remain_size 	float 	Y 	可转债剩余金额
total_shares 	float 	Y 	转股后总股本
        """
    },
    "债券回购日行情": {
        "api":"repo_daily",
        "desc":"""接口：repo_daily
描述：债券回购日行情
限量：单次最大2000条，可多次提取，总量不限制
权限：用户需要累积2000积分才可以调取，具体请参阅积分获取办法

输入参数
名称 	类型 	必选 	描述
ts_code 	str 	N 	TS代码
trade_date 	str 	N 	交易日期(YYYYMMDD格式，下同)
start_date 	str 	N 	开始日期
end_date 	str 	N 	结束日期

输出参数
名称 	类型 	默认显示 	描述
ts_code 	str 	Y 	TS代码
trade_date 	str 	Y 	交易日期
repo_maturity 	str 	Y 	期限品种
pre_close 	float 	Y 	前收盘(%)
open 	float 	Y 	开盘价(%)
high 	float 	Y 	最高价(%)
low 	float 	Y 	最低价(%)
close 	float 	Y 	收盘价(%)
weight 	float 	Y 	加权价(%)
weight_r 	float 	Y 	加权价(利率债)(%)
amount 	float 	Y 	成交金额(万元)
num 	int 	Y 	成交笔数(笔)
        """
    },
    "全球财经事件": {
        "api":"eco_cal",
        "desc":"""接口：eco_cal
描述：获取全球财经日历、包括经济事件数据更新
限量：单次最大获取100行数据
积分：2000积分可调取


输入参数
名称 	类型 	必选 	描述
date 	str 	N 	日期（YYYYMMDD格式）
start_date 	str 	N 	开始日期
end_date 	str 	N 	结束日期
currency 	str 	N 	货币代码
country 	str 	N 	国家（比如：中国、美国）
event 	str 	N 	事件 （支持模糊匹配： *非农*）


输出参数
名称 	类型 	默认显示 	描述
date 	str 	Y 	日期
time 	str 	Y 	时间
currency 	str 	Y 	货币代码
country 	str 	Y 	国家
event 	str 	Y 	经济事件
value 	str 	Y 	今值
pre_value 	str 	Y 	前值
fore_value 	str 	Y 	预测值
        """
    },
    "外汇基础信息（海外）": {
        "api":"fx_obasic",
        "desc":"""接口：fx_obasic
描述：获取海外外汇基础信息，目前只有FXCM交易商的数据
数量：单次可提取全部数据
积分：用户需要至少2000积分才可以调取，具体请参阅积分获取办法


输入参数
名称 	类型 	必选 	描述
exchange 	str 	N 	交易商
classify 	str 	N 	分类
ts_code 	str 	N 	TS代码


classify分类说明
序号 	分类代码 	分类名称 	样例
1 	FX 	外汇货币对 	USDCNH（美元人民币对）
2 	INDEX 	指数 	US30（美国道琼斯工业平均指数）
3 	COMMODITY 	大宗商品 	SOYF（大豆）
4 	METAL 	金属 	XAUUSD （黄金）
5 	BUND 	国库债券 	Bund（长期欧元债券）
6 	CRYPTO 	加密数字货币 	BTCUSD (比特币)
7 	FX_BASKET 	外汇篮子 	USDOLLAR （美元指数）


输出参数
名称 	类型 	默认显示 	描述
ts_code 	str 	Y 	外汇代码
name 	str 	Y 	名称
classify 	str 	Y 	分类
exchange 	str 	Y 	交易商
min_unit 	float 	Y 	最小交易单位
max_unit 	float 	Y 	最大交易单位
pip 	float 	Y 	最大交易单位
pip_cost 	float 	Y 	点值
traget_spread 	float 	Y 	目标差价
min_stop_distance 	float 	Y 	最小止损距离（点子）
trading_hours 	str 	Y 	交易时间
break_time 	str 	Y 	休市时间
        """
    },
    "外汇日线行情": {
        "api":"fx_daily",
        "desc":"""接口：fx_daily
描述：获取外汇日线行情
限量：单次最大提取1000行记录，可多次提取，总量不限制
积分：用户需要至少2000积分才可以调取，但有流量控制，5000积分以上频次相对较高，积分越多权限越大，具体请参阅积分获取办法


输入参数
名称 	类型 	必选 	描述
ts_code 	str 	N 	TS代码
trade_date 	str 	N 	交易日期（GMT，日期是格林尼治时间，比北京时间晚一天）
start_date 	str 	N 	开始日期（GMT）
end_date 	str 	N 	结束日期（GMT）
exchange 	str 	N 	交易商，目前只有FXCM


输出参数
名称 	类型 	默认显示 	描述
ts_code 	str 	Y 	外汇代码
trade_date 	str 	Y 	交易日期
bid_open 	float 	Y 	买入开盘价
bid_close 	float 	Y 	买入收盘价
bid_high 	float 	Y 	买入最高价
bid_low 	float 	Y 	买入最低价
ask_open 	float 	Y 	卖出开盘价
ask_close 	float 	Y 	卖出收盘价
ask_high 	float 	Y 	卖出最高价
ask_low 	float 	Y 	卖出最低价
tick_qty 	int 	Y 	报价笔数
exchange 	str 	N 	交易商
        """
    },
    "港股列表": {
        "api":"hk_basic",
        "desc":"""接口：hk_basic
描述：获取港股列表信息
数量：单次可提取全部在交易的港股列表数据
积分：用户需要至少2000积分才可以调取，具体请参阅积分获取办法


输入参数
名称 	类型 	必选 	描述
ts_code 	str 	N 	TS代码
list_status 	str 	N 	上市状态 L上市 D退市 P暂停上市 ，默认L


输出参数
名称 	类型 	默认显示 	描述
ts_code 	str 	Y 	
name 	str 	Y 	股票简称
fullname 	str 	Y 	公司全称
enname 	str 	Y 	英文名称
cn_spell 	str 	Y 	拼音
market 	str 	Y 	市场类别
list_status 	str 	Y 	上市状态
list_date 	str 	Y 	上市日期
delist_date 	str 	Y 	退市日期
trade_unit 	float 	Y 	交易单位
isin 	str 	Y 	ISIN代码
curr_type 	str 	Y 	货币代码
        """
    },
    "港股交易日历": {
        "api":"hk_tradecal",
        "desc":"""接口：hk_tradecal
描述：获取交易日历
限量：单次最大2000
权限：用户积累2000积分才可调取


输入参数
名称 	类型 	必选 	描述
start_date 	str 	N 	开始日期
end_date 	str 	N 	结束日期
is_open 	str 	N 	是否交易 '0'休市 '1'交易


输出参数
名称 	类型 	默认显示 	描述
cal_date 	str 	Y 	日历日期
is_open 	int 	Y 	是否交易 '0'休市 '1'交易
pretrade_date 	str 	Y 	上一个交易日
        """
    },
    "港股日线行情": {
        "api":"hk_daily",
        "desc":"""接口：hk_daily
描述：获取港股每日增量和历史行情
限量：单次最大提取3000行记录，可多次提取，总量不限制
积分：用户需要至少2000积分才可以调取，但有流量控制，5000积分频次相对较高，积分越多权限越大，具体请参阅积分获取办法


输入参数
名称 	类型 	必选 	描述
ts_code 	str 	N 	股票代码
trade_date 	str 	N 	交易日期
start_date 	str 	N 	开始日期
end_date 	str 	N 	结束日期


输出参数
名称 	类型 	默认显示 	描述
ts_code 	str 	Y 	股票代码
trade_date 	str 	Y 	交易日期
open 	float 	Y 	开盘价
high 	float 	Y 	最高价
low 	float 	Y 	最低价
close 	float 	Y 	收盘价
pre_close 	float 	Y 	昨收价
change 	float 	Y 	涨跌额
pct_chg 	float 	Y 	涨跌幅(%)
vol 	float 	Y 	成交量(股)
amount 	float 	Y 	成交额(元)
        """
    },
    "美股列表": {
        "api":"us_basic",
        "desc":"""接口：us_basic
描述：获取美股列表信息
限量：单次最大6000，可分页提取
积分：120积分可以试用，5000积分有正式权限


输入参数
名称 	类型 	必选 	描述 	示例
ts_code 	str 	N 	股票代码 	AAPL（苹果）
classify 	str 	N 	股票分类 	ADR/GDR/EQ
offset 	str 	N 	开始行数 	1：第一行
limit 	str 	N 	每页最大行数 	500：每页500行


输出参数
名称 	类型 	默认显示 	描述
ts_code 	str 	Y 	美股代码
name 	str 	Y 	中文名称
enname 	str 	N 	英文名称
classify 	str 	Y 	分类ADR/GDR/EQ
list_date 	str 	Y 	上市日期
delist_date 	str 	Y 	退市日期
        """
    },
    "美股交易日历": {
        "api":"us_tradecal",
        "desc":"""接口：us_tradecal
描述：获取美股交易日历信息
限量：单次最大6000，可根据日期阶段获取


输入参数
名称 	类型 	必选 	描述 	示例
start_date 	str 	N 	开始日期 	20200101
end_date 	str 	N 	结束日期 	20200701
is_open 	str 	N 	是否交易 	0：休市 、1：交易


输出参数
名称 	类型 	默认显示 	描述
cal_date 	str 	Y 	日历日期
is_open 	int 	Y 	是否交易 '0'休市 '1'交易
pretrade_date 	str 	Y 	上一个交易日
        """
    },
    "美股日线行情": {
        "api":"us_daily",
        "desc":"""接口：us_daily
描述：获取美股行情（未复权），包括全部股票全历史行情，以及重要的市场和估值指标
限量：单次最大6000行数据，可根据日期参数循环提取，开通正式权限后也可支持分页提取全部历史
要求：120积分可以试用查看数据，开通正式权限请在QQ群联系群主或积分管理员。


输入参数
名称 	类型 	必选 	描述
ts_code 	str 	N 	股票代码（e.g. AAPL）
trade_date 	str 	N 	交易日期（YYYYMMDD）
start_date 	str 	N 	开始日期（YYYYMMDD）
end_date 	str 	N 	结束日期（YYYYMMDD）


输出参数
名称 	类型 	默认显示 	描述
ts_code 	str 	Y 	股票代码
trade_date 	str 	Y 	交易日期
close 	float 	Y 	收盘价
open 	float 	Y 	开盘价
high 	float 	Y 	最高价
low 	float 	Y 	最低价
pre_close 	float 	Y 	昨收价
change 	float 	N 	涨跌额
pct_change 	float 	Y 	涨跌幅
vol 	float 	Y 	成交量
amount 	float 	Y 	成交额
vwap 	float 	Y 	平均价
turnover_ratio 	float 	N 	换手率
total_mv 	float 	N 	总市值
pe 	float 	N 	PE
pb 	float 	N 	PB
        """
    },
    "台湾电子产业月营收": {
        "api":"tmt_twincome",
        "desc":"""接口：tmt_twincome
描述：获取台湾TMT电子产业领域各类产品月度营收数据。

输入参数
名称 	类型 	必选 	描述
date 	str 	N 	报告期
item 	str 	Y 	产品代码
start_date 	str 	N 	报告期开始日期
end_date 	str 	N 	报告期结束日期

输出参数
名称 	类型 	描述
date 	str 	报告期
item 	str 	产品代码
op_income 	str 	月度收入

由于服务器压力，单次最多获取30个月数据，后续再逐步全部开放，目前可根据日期范围多次获取数据。
        """
    },
    "台湾电子产业月营收明细": {
        "api":"tmt_twincomedetail",
        "desc":"""接口：tmt_twincomedetail
描述：获取台湾TMT行业上市公司各类产品月度营收情况。

输入参数
名称 	类型 	必选 	描述
date 	str 	N 	报告期
item 	str 	N 	产品代码
symbol 	str 	N 	公司代码
start_date 	str 	N 	报告期开始日期
end_date 	str 	N 	报告期结束日期
source 	str 	N 	None

输出参数
名称 	类型 	描述
date 	str 	报告期
item 	str 	产品代码
symbol 	str 	公司代码
op_income 	str 	月度营收
consop_income 	str 	合并月度营收（默认不展示）
        """
    },
    "电影月度票房": {
        "api":"bo_monthly",
        "desc":"""接口：bo_monthly
描述：获取电影月度票房数据
数据更新：本月更新上一月数据
数据历史： 数据从2008年1月1日开始，超过10年历史数据。
数据权限：用户需要至少500积分才可以调取，具体请参阅积分获取办法

输入参数
名称 	类型 	必选 	描述
date 	str 	Y 	日期（每月1号，格式YYYYMMDD）

输出参数
名称 	类型 	默认显示 	描述
date 	str 	Y 	日期
name 	str 	Y 	影片名称
list_date 	str 	Y 	上映日期
avg_price 	float 	Y 	平均票价
month_amount 	float 	Y 	当月票房（万）
list_day 	int 	Y 	月内天数
p_pc 	int 	Y 	场均人次
wom_index 	float 	Y 	口碑指数
m_ratio 	float 	Y 	月度占比（%）
rank 	int 	Y 	排名
        """
    },
    "电影周度票房": {
        "api":"bo_weekly",
        "desc":"""接口：bo_weekly
描述：获取周度票房数据
数据更新：本周更新上一周数据
数据历史： 数据从2008年第一周开始，超过10年历史数据。
数据权限：用户需要至少500积分才可以调取，具体请参阅积分获取办法

输入参数
名称 	类型 	必选 	描述
date 	str 	Y 	日期（每周一日期，格式YYYYMMDD）

输出参数
名称 	类型 	默认显示 	描述
date 	str 	Y 	日期
name 	str 	Y 	影片名称
avg_price 	float 	Y 	平均票价
week_amount 	float 	Y 	当周票房（万）
total 	float 	Y 	累计票房（万）
list_day 	int 	Y 	上映天数
p_pc 	int 	Y 	场均人次
wom_index 	float 	Y 	口碑指数
up_ratio 	float 	Y 	环比变化 （%）
rank 	int 	Y 	排名
        """
    },
    "电影日度票房": {
        "api":"bo_daily",
        "desc":"""接口：bo_daily
描述：获取电影日度票房
数据更新：当日更新上一日数据
数据历史： 数据从2018年9月开始，更多历史数据正在补充
数据权限：用户需要至少500积分才可以调取，具体请参阅积分获取办法

输入参数
名称 	类型 	必选 	描述
date 	str 	Y 	日期 （格式YYYYMMDD）

输出参数
名称 	类型 	默认显示 	描述
date 	str 	Y 	日期
name 	str 	Y 	影片名称
avg_price 	float 	Y 	平均票价
day_amount 	float 	Y 	当日票房（万）
total 	float 	Y 	累计票房（万）
list_day 	int 	Y 	上映天数
p_pc 	int 	Y 	场均人次
wom_index 	float 	Y 	口碑指数
up_ratio 	float 	Y 	环比变化 （%）
rank 	int 	Y 	排名
        """
    },
    "影院日度票房": {
        "api":"bo_cinema",
        "desc":"""接口：bo_cinema
描述：获取每日各影院的票房数据
数据历史： 数据从2018年9月开始，更多历史数据正在补充
数据权限：用户需要至少500积分才可以调取，具体请参阅积分获取办法

输入参数
名称 	类型 	必选 	描述
date 	str 	Y 	日期(格式:YYYYMMDD)

输出参数
名称 	类型 	默认显示 	描述
date 	str 	Y 	日期
c_name 	str 	Y 	影院名称
aud_count 	int 	Y 	观众人数
att_ratio 	float 	Y 	上座率
day_amount 	float 	Y 	当日票房
day_showcount 	float 	Y 	当日场次
avg_price 	float 	Y 	场均票价（元）
p_pc 	float 	Y 	场均人次
rank 	int 	Y 	排名
        """
    },
    "全国电影剧本备案数据": {
        "api":"film_record",
        "desc":"""接口：film_record
描述：获取全国电影剧本备案的公示数据
限量：单次最大500，总量不限制
数据权限：用户需要至少120积分才可以调取，积分越多调取频次越高，具体请参阅积分获取办法


输入参数
名称 	类型 	必选 	描述
ann_date 	str 	N 	公布日期 （至少输入一个参数，格式：YYYYMMDD，日期不连续，定期公布）
start_date 	str 	N 	开始日期
end_date 	str 	N 	结束日期


输出参数
名称 	类型 	默认显示 	描述
rec_no 	str 	Y 	备案号
film_name 	str 	Y 	影片名称
rec_org 	str 	Y 	备案单位
script_writer 	str 	Y 	编剧
rec_result 	str 	Y 	备案结果
rec_area 	str 	Y 	备案地（备案时间）
classified 	str 	Y 	影片分类
date_range 	str 	Y 	备案日期区间
ann_date 	str 	Y 	备案结果发布时间
        """
    },
    "全国电视剧备案公示数据": {
        "api":"teleplay_record",
        "desc":"""接口：teleplay_record
描述：获取2009年以来全国拍摄制作电视剧备案公示数据
限量：单次最大1000，总量不限制
数据权限：用户需要至少积分600才可以调取，积分越多调取频次越高，具体请参阅积分获取办法

输入参数
名称 	类型 	必选 	描述
report_date 	str 	N 	备案月份（YYYYMM）
start_date 	str 	N 	备案开始月份（YYYYMM）
end_date 	str 	N 	备案结束月份（YYYYMM）
org 	str 	N 	备案机构
name 	str 	N 	电视剧名称

输出参数
名称 	类型 	默认显示 	描述
name 	str 	Y 	电视剧名称
classify 	str 	Y 	题材
types 	str 	Y 	体裁
org 	str 	Y 	报备机构
report_date 	str 	Y 	报备时间
license_key 	str 	Y 	许可证号
episodes 	str 	Y 	集数
shooting_date 	str 	Y 	拍摄时间
prod_cycle 	str 	Y 	制作周期
content 	str 	Y 	内容提要
pro_opi 	str 	Y 	省级管理部门备案意见
dept_opi 	str 	Y 	相关部门意见
remarks 	str 	Y 	备注
        """
    },
    "Shibor利率": {
        "api":"shibor",
        "desc":"""接口：shibor
描述：shibor利率
限量：单次最大2000，总量不限制，可通过设置开始和结束日期分段获取
积分：用户积累120积分可以调取，具体请参阅积分获取办法

Shibor利率介绍

    上海银行间同业拆放利率（Shanghai Interbank Offered Rate，简称Shibor），以位于上海的全国银行间同业拆借中心为技术平台计算、发布并命名，是由信用等级较高的银行组成报价团自主报出的人民币同业拆出利率计算确定的算术平均利率，是单利、无担保、批发性利率。目前，对社会公布的Shibor品种包括隔夜、1周、2周、1个月、3个月、6个月、9个月及1年。

    Shibor报价银行团现由18家商业银行组成。报价银行是公开市场一级交易商或外汇市场做市商，在中国货币市场上人民币交易相对活跃、信息披露比较充分的银行。中国人民银行成立Shibor工作小组，依据《上海银行间同业拆放利率（Shibor）实施准则》确定和调整报价银行团成员、监督和管理Shibor运行、规范报价行与指定发布人行为。

    全国银行间同业拆借中心受权Shibor的报价计算和信息发布。每个交易日根据各报价行的报价，剔除最高、最低各4家报价，对其余报价进行算术平均计算后，得出每一期限品种的Shibor，并于11:00对外发布。



输入参数
名称 	类型 	必选 	描述
date 	str 	N 	日期 (日期输入格式：YYYYMMDD，下同)
start_date 	str 	N 	开始日期
end_date 	str 	N 	结束日期


输出参数
名称 	类型 	默认显示 	描述
date 	str 	Y 	日期
on 	float 	Y 	隔夜
1w 	float 	Y 	1周
2w 	float 	Y 	2周
1m 	float 	Y 	1个月
3m 	float 	Y 	3个月
6m 	float 	Y 	6个月
9m 	float 	Y 	9个月
1y 	float 	Y 	1年
        """
    },
    "Shibor报价数据": {
        "api":"shibor_quote",
        "desc":"""接口：shibor_quote
描述：Shibor报价数据
限量：单次最大4000行数据，总量不限制，可通过设置开始和结束日期分段获取
积分：用户积累120积分可以调取，具体请参阅积分获取办法


输入参数
名称 	类型 	必选 	描述
date 	str 	N 	日期 (日期输入格式：YYYYMMDD，下同)
start_date 	str 	N 	开始日期
end_date 	str 	N 	结束日期
bank 	str 	N 	银行名称 （中文名称，例如 农业银行）

输出参数
名称 	类型 	默认显示 	描述
date 	str 	Y 	日期
bank 	str 	Y 	报价银行
on_b 	float 	Y 	隔夜_Bid
on_a 	float 	Y 	隔夜_Ask
1w_b 	float 	Y 	1周_Bid
1w_a 	float 	Y 	1周_Ask
2w_b 	float 	Y 	2周_Bid
2w_a 	float 	Y 	2周_Ask
1m_b 	float 	Y 	1月_Bid
1m_a 	float 	Y 	1月_Ask
3m_b 	float 	Y 	3月_Bid
3m_a 	float 	Y 	3月_Ask
6m_b 	float 	Y 	6月_Bid
6m_a 	float 	Y 	6月_Ask
9m_b 	float 	Y 	9月_Bid
9m_a 	float 	Y 	9月_Ask
1y_b 	float 	Y 	1年_Bid
1y_a 	float 	Y 	1年_Ask
        """
    },
    "LPR贷款基础利率": {
        "api":"shibor_lpr",
        "desc":"""接口：shibor_lpr
描述：LPR贷款基础利率
限量：单次最大4000(相当于单次可提取18年历史)，总量不限制，可通过设置开始和结束日期分段获取
积分：用户积累120积分可以调取，具体请参阅积分获取办法

LPR介绍

    贷款基础利率（Loan Prime Rate，简称LPR），是基于报价行自主报出的最优贷款利率计算并发布的贷款市场参考利率。目前，对社会公布1年期贷款基础利率。

    LPR报价银行团现由10家商业银行组成。报价银行应符合财务硬约束条件和宏观审慎政策框架要求，系统重要性程度高、市场影响力大、综合实力强，已建立内部收益率曲线和内部转移定价机制，具有较强的自主定价能力，已制定本行贷款基础利率管理办法，以及有利于开展报价工作的其他条件。市场利率定价自律机制依据《贷款基础利率集中报价和发布规则》确定和调整报价行成员，监督和管理贷款基础利率运行，规范报价行与指定发布人行为。

    全国银行间同业拆借中心受权贷款基础利率的报价计算和信息发布。每个交易日根据各报价行的报价，剔除最高、最低各1家报价，对其余报价进行加权平均计算后，得出贷款基础利率报价平均利率，并于11:30对外发布。


输入参数
名称 	类型 	必选 	描述
date 	str 	N 	日期 (日期输入格式：YYYYMMDD，下同)
start_date 	str 	N 	开始日期
end_date 	str 	N 	结束日期

输出参数
名称 	类型 	默认显示 	描述
date 	str 	Y 	日期
1y 	float 	Y 	1年贷款利率
        """
    },
    "Libor利率": {
        "api":"libor",
        "desc":"""接口：libor
描述：Libor拆借利率
限量：单次最大4000行数据，总量不限制，可通过设置开始和结束日期分段获取
积分：用户积累120积分可以调取，具体请参阅积分获取办法


    Libor（London Interbank Offered Rate ），即伦敦同业拆借利率，是指伦敦的第一流银行之间短期资金借贷的利率，是国际金融市场中大多数浮动利率的基础利率。作为银行从市场上筹集资金进行转贷的融资成本，贷款协议中议定的LIBOR通常是由几家指定的参考银行，在规定的时间（一般是伦敦时间上午11：00）报价的平均利率。


输入参数
名称 	类型 	必选 	描述
date 	str 	N 	日期 (日期输入格式：YYYYMMDD，下同)
start_date 	str 	N 	开始日期
end_date 	str 	N 	结束日期
curr_type 	str 	N 	货币代码 (USD美元 EUR欧元 JPY日元 GBP英镑 CHF瑞郎，默认是USD)

输出参数
名称 	类型 	默认显示 	描述
date 	str 	Y 	日期
curr_type 	str 	Y 	货币
on 	float 	Y 	隔夜
1w 	float 	Y 	1周
1m 	float 	Y 	1个月
2m 	float 	Y 	2个月
3m 	float 	Y 	3个月
6m 	float 	Y 	6个月
12m 	float 	Y 	12个月
        """
    },
    "Hibor利率": {
        "api":"hibor",
        "desc":"""接口：hibor
描述：Hibor利率
限量：单次最大4000行数据，总量不限制，可通过设置开始和结束日期分段获取
积分：用户积累120积分可以调取，具体请参阅积分获取办法


    HIBOR (Hongkong InterBank Offered Rate)，是香港银行同行业拆借利率。指香港货币市场上，银行与银行之间的一年期以下的短期资金借贷利率，从伦敦同业拆借利率（LIBOR）变化出来的。


输入参数
名称 	类型 	必选 	描述
date 	str 	N 	日期 (日期输入格式：YYYYMMDD，下同)
start_date 	str 	N 	开始日期
end_date 	str 	N 	结束日期

输出参数
名称 	类型 	默认显示 	描述
date 	str 	Y 	日期
on 	float 	Y 	隔夜
1w 	float 	Y 	1周
2w 	float 	Y 	2周
1m 	float 	Y 	1个月
2m 	float 	Y 	2个月
3m 	float 	Y 	3个月
6m 	float 	Y 	6个月
12m 	float 	Y 	12个月
        """
    },
    "温州民间借贷利率": {
        "api":"wz_index",
        "desc":"""接口：wz_index
描述：温州民间借贷利率，即温州指数
限量：不限量，一次可取全部指标全部历史数据
积分：用户需要积攒2000积分可调取，具体请参阅积分获取办法
数据来源：温州指数网


注：
温州指数 ，即温州民间融资综合利率指数，该指数及时反映民间金融交易活跃度和交易价格。该指数样板数据主要采集于四个方面：由温州市设立的几百家企业测报点，把各自借入的民间资本利率通过各地方金融办不记名申报收集起来；对各小额贷款公司借出的利率进行加权平均；融资性担保公司如典当行在融资过程中的利率，由温州经信委和商务局负责测报；民间借贷服务中心的实时利率。这些利率进行加权平均，就得出了“温州指数”。它是温州民间融资利率的风向标。2012年12月7日，温州指数正式对外发布。

输入参数
名称 	类型 	必选 	描述
date 	str 	N 	日期
start_date 	str 	N 	开始日期
end_date 	str 	N 	结束日期


输出参数
名称 	类型 	默认显示 	描述
date 	str 	Y 	日期
comp_rate 	float 	Y 	温州民间融资综合利率指数 (%，下同)
center_rate 	float 	Y 	民间借贷服务中心利率
micro_rate 	float 	Y 	小额贷款公司放款利率
cm_rate 	float 	Y 	民间资本管理公司融资价格
sdb_rate 	float 	Y 	社会直接借贷利率
om_rate 	float 	Y 	其他市场主体利率
aa_rate 	float 	Y 	农村互助会互助金费率
m1_rate 	float 	Y 	温州地区民间借贷分期限利率（一月期）
m3_rate 	float 	Y 	温州地区民间借贷分期限利率（三月期）
m6_rate 	float 	Y 	温州地区民间借贷分期限利率（六月期）
m12_rate 	float 	Y 	温州地区民间借贷分期限利率（一年期）
long_rate 	float 	Y 	温州地区民间借贷分期限利率（长期）
        """
    },
    "广州民间借贷利率": {
        "api":"gz_index",
        "desc":"""接口：gz_index
描述：广州民间借贷利率
限量：不限量，一次可取全部指标全部历史数据
积分：用户需要积攒2000积分可调取，具体请参阅积分获取办法
数据来源：广州民间金融街


输入参数
名称 	类型 	必选 	描述
date 	str 	N 	日期
start_date 	str 	N 	开始日期
end_date 	str 	N 	结束日期


输出参数
名称 	类型 	默认显示 	描述
date 	str 	Y 	日期
d10_rate 	float 	Y 	小额贷市场平均利率（十天） （单位：%，下同）
m1_rate 	float 	Y 	小额贷市场平均利率（一月期）
m3_rate 	float 	Y 	小额贷市场平均利率（三月期）
m6_rate 	float 	Y 	小额贷市场平均利率（六月期）
m12_rate 	float 	Y 	小额贷市场平均利率（一年期）
long_rate 	float 	Y 	小额贷市场平均利率（长期）
        """
    },
    "国内生产总值（GDP）": {
        "api":"cn_gdp",
        "desc":"""接口：cn_gdp
描述：获取国民经济之GDP数据
限量：单次最大10000，一次可以提取全部数据
权限：用户积累600积分可以使用，具体请参阅积分获取办法


输入参数
名称 	类型 	必选 	描述
q 	str 	N 	季度（2019Q1表示，2019年第一季度）
start_q 	str 	N 	开始季度
end_q 	str 	N 	结束季度
fields 	str 	N 	指定输出字段（e.g. fields='quarter,gdp,gdp_yoy'）


输出参数
名称 	类型 	默认显示 	描述
quarter 	str 	Y 	季度
gdp 	float 	Y 	GDP累计值（亿元）
gdp_yoy 	float 	Y 	当季同比增速（%）
pi 	float 	Y 	第一产业累计值（亿元）
pi_yoy 	float 	Y 	第一产业同比增速（%）
si 	float 	Y 	第二产业累计值（亿元）
si_yoy 	float 	Y 	第二产业同比增速（%）
ti 	float 	Y 	第三产业累计值（亿元）
ti_yoy 	float 	Y 	第三产业同比增速（%）
        """
    },
    "居民消费价格指数（CPI）": {
        "api":"cn_cpi",
        "desc":"""接口：cn_cpi
描述：获取CPI居民消费价格数据，包括全国、城市和农村的数据
限量：单次最大5000行，一次可以提取全部数据
权限：用户积累600积分可以使用，具体请参阅积分获取办法


输入参数
名称 	类型 	必选 	描述
m 	str 	N 	月份（YYYYMM，下同），支持多个月份同时输入，逗号分隔
start_m 	str 	N 	开始月份
end_m 	str 	N 	结束月份


输出参数
名称 	类型 	默认显示 	描述
month 	str 	Y 	月份YYYYMM
nt_val 	float 	Y 	全国当月至
nt_yoy 	float 	Y 	全国同比（%）
nt_mom 	float 	Y 	全国环比（%）
nt_accu 	float 	Y 	全国累计值
town_val 	float 	Y 	城市当值月
town_yoy 	float 	Y 	城市同比（%）
town_mom 	float 	Y 	城市环比（%）
town_accu 	float 	Y 	城市累计值
cnt_val 	float 	Y 	农村当月值
cnt_yoy 	float 	Y 	农村同比（%）
cnt_mom 	float 	Y 	农村环比（%）
cnt_accu 	float 	Y 	农村累计值
        """
    },
    "工业生产者出厂价格指数（PPI）": {
        "api":"cn_ppi",
        "desc":"""接口：cn_ppi
描述：获取PPI工业生产者出厂价格指数数据
限量：单次最大5000，一次可以提取全部数据
权限：用户600积分可以使用，具体请参阅积分获取办法

输入参数
名称 	类型 	必选 	描述
m 	str 	N 	月份（YYYYMM，下同），支持多个月份同时输入，逗号分隔
start_m 	str 	N 	开始月份
end_m 	str 	N 	结束月份

输出参数
名称 	类型 	默认显示 	描述
month 	str 	Y 	月份YYYYMM
ppi_yoy 	float 	Y 	PPI：全部工业品：当月同比
ppi_mp_yoy 	float 	Y 	PPI：生产资料：当月同比
ppi_mp_qm_yoy 	float 	Y 	PPI：生产资料：采掘业：当月同比
ppi_mp_rm_yoy 	float 	Y 	PPI：生产资料：原料业：当月同比
ppi_mp_p_yoy 	float 	Y 	PPI：生产资料：加工业：当月同比
ppi_cg_yoy 	float 	Y 	PPI：生活资料：当月同比
ppi_cg_f_yoy 	float 	Y 	PPI：生活资料：食品类：当月同比
ppi_cg_c_yoy 	float 	Y 	PPI：生活资料：衣着类：当月同比
ppi_cg_adu_yoy 	float 	Y 	PPI：生活资料：一般日用品类：当月同比
ppi_cg_dcg_yoy 	float 	Y 	PPI：生活资料：耐用消费品类：当月同比
ppi_mom 	float 	Y 	PPI：全部工业品：环比
ppi_mp_mom 	float 	Y 	PPI：生产资料：环比
ppi_mp_qm_mom 	float 	Y 	PPI：生产资料：采掘业：环比
ppi_mp_rm_mom 	float 	Y 	PPI：生产资料：原料业：环比
ppi_mp_p_mom 	float 	Y 	PPI：生产资料：加工业：环比
ppi_cg_mom 	float 	Y 	PPI：生活资料：环比
ppi_cg_f_mom 	float 	Y 	PPI：生活资料：食品类：环比
ppi_cg_c_mom 	float 	Y 	PPI：生活资料：衣着类：环比
ppi_cg_adu_mom 	float 	Y 	PPI：生活资料：一般日用品类：环比
ppi_cg_dcg_mom 	float 	Y 	PPI：生活资料：耐用消费品类：环比
ppi_accu 	float 	Y 	PPI：全部工业品：累计同比
ppi_mp_accu 	float 	Y 	PPI：生产资料：累计同比
ppi_mp_qm_accu 	float 	Y 	PPI：生产资料：采掘业：累计同比
ppi_mp_rm_accu 	float 	Y 	PPI：生产资料：原料业：累计同比
ppi_mp_p_accu 	float 	Y 	PPI：生产资料：加工业：累计同比
ppi_cg_accu 	float 	Y 	PPI：生活资料：累计同比
ppi_cg_f_accu 	float 	Y 	PPI：生活资料：食品类：累计同比
ppi_cg_c_accu 	float 	Y 	PPI：生活资料：衣着类：累计同比
ppi_cg_adu_accu 	float 	Y 	PPI：生活资料：一般日用品类：累计同比
ppi_cg_dcg_accu 	float 	Y 	PPI：生活资料：耐用消费品类：累计同比
        """
    },
    "货币供应量（月）": {
        "api":"cn_m",
        "desc":"""接口：cn_m
描述：获取货币供应量之月度数据
限量：单次最大5000，一次可以提取全部数据
权限：用户积累600积分可以使用，具体请参阅积分获取办法

输入参数
名称 	类型 	必选 	描述
m 	str 	N 	月度（202001表示，2020年1月）
start_m 	str 	N 	开始月度
end_m 	str 	N 	结束月度
fields 	str 	N 	指定输出字段（e.g. fields='month,m0,m1,m2'）

输出参数
名称 	类型 	默认显示 	描述
month 	str 	Y 	月份YYYYMM
m0 	float 	Y 	M0（亿元）
m0_yoy 	float 	Y 	M0同比（%）
m0_mom 	float 	Y 	M0环比（%）
m1 	float 	Y 	M1（亿元）
m1_yoy 	float 	Y 	M1同比（%）
m1_mom 	float 	Y 	M1环比（%）
m2 	float 	Y 	M2（亿元）
m2_yoy 	float 	Y 	M2同比（%）
m2_mom 	float 	Y 	M2环比（%）
        """
    },
    "国债收益率曲线利率": {
        "api":"us_tycr",
        "desc":"""接口：us_tycr
描述：获取美国每日国债收益率曲线利率
限量：单次最大可获取2000条数据
权限：用户积累120积分可以使用，积分越高频次越高。具体请参阅积分获取办法


输入参数
名称 	类型 	必选 	描述
date 	str 	N 	日期 （YYYYMMDD格式，下同）
start_date 	str 	N 	开始日期
end_date 	str 	N 	结束日期
fields 	str 	N 	指定输出字段（e.g. fields='m1,y1'）


输出参数
名称 	类型 	默认显示 	描述
date 	str 	Y 	日期
m1 	float 	Y 	1月期
m2 	float 	Y 	2月期
m3 	float 	Y 	3月期
m6 	float 	Y 	6月期
y1 	float 	Y 	1年期
y2 	float 	Y 	2年期
y3 	float 	Y 	3年期
y5 	float 	Y 	5年期
y7 	float 	Y 	7年期
y10 	float 	Y 	10年期
y20 	float 	Y 	20年期
y30 	float 	Y 	30年期
        """
    },
    "国债实际收益率曲线利率": {
        "api":"us_trycr",
        "desc":"""接口：us_trycr
描述：国债实际收益率曲线利率
限量：单次最大可获取2000行数据，可循环获取
权限：用户积累120积分可以使用，积分越高频次越高。具体请参阅积分获取办法


输入参数
名称 	类型 	必选 	描述
date 	str 	N 	日期 （YYYYMMDD格式，下同）
start_date 	str 	N 	开始日期
end_date 	str 	N 	结束日期
fields 	str 	N 	指定输出字段


输出参数
名称 	类型 	默认显示 	描述
date 	str 	Y 	日期
y5 	float 	Y 	5年期
y7 	float 	Y 	7年期
y10 	float 	Y 	10年期
y20 	float 	Y 	20年期
y30 	float 	Y 	30年期
        """
    },
    "短期国债利率": {
        "api":"us_tbr",
        "desc":"""接口：us_tbr
描述：获取美国短期国债利率数据
限量：单次最大可获取2000行数据，可循环获取
权限：用户积累120积分可以使用，积分越高频次越高。具体请参阅积分获取办法


输入参数
名称 	类型 	必选 	描述
date 	str 	N 	日期
start_date 	str 	N 	开始日期(YYYYMMDD格式)
end_date 	str 	N 	结束日期
fields 	str 	N 	指定输出字段(e.g. fields='w4_bd,w52_ce')


输出参数
名称 	类型 	默认显示 	描述
date 	str 	Y 	日期
w4_bd 	float 	Y 	4周银行折现收益率
w4_ce 	float 	Y 	4周票面利率
w8_bd 	float 	Y 	8周银行折现收益率
w8_ce 	float 	Y 	8周票面利率
w13_bd 	float 	Y 	13周银行折现收益率
w13_ce 	float 	Y 	13周票面利率
w26_bd 	float 	Y 	26周银行折现收益率
w26_ce 	float 	Y 	26周票面利率
w52_bd 	float 	Y 	52周银行折现收益率
w52_ce 	float 	Y 	52周票面利率
        """
    },
    "国债长期利率": {
        "api":"us_tltr",
        "desc":"""接口：us_tltr
描述：国债长期利率
限量：单次最大可获取2000行数据，可循环获取
权限：用户积累120积分可以使用，积分越高频次越高。具体请参阅积分获取办法


输入参数
名称 	类型 	必选 	描述
date 	str 	N 	日期
start_date 	str 	N 	开始日期
end_date 	str 	N 	结束日期
fields 	str 	N 	指定字段


输出参数
名称 	类型 	默认显示 	描述
date 	str 	Y 	日期
ltc 	float 	Y 	收益率 LT COMPOSITE (>10 Yrs)
cmt 	float 	Y 	20年期CMT利率(TREASURY 20-Yr CMT)
e_factor 	float 	Y 	外推因子EXTRAPOLATION FACTOR
        """
    },
    "国债长期利率平均值": {
        "api":"us_trltr",
        "desc":"""接口：us_trltr
描述：国债实际长期利率平均值
限量：单次最大可获取2000行数据，可循环获取
权限：用户积累120积分可以使用，积分越高频次越高。具体请参阅积分获取办法


输入参数
名称 	类型 	必选 	描述
date 	str 	N 	日期
start_date 	str 	N 	开始日期
end_date 	str 	N 	结束日期
fields 	str 	N 	指定字段


输出参数
名称 	类型 	默认显示 	描述
date 	str 	Y 	日期
ltr_avg 	float 	Y 	实际平均利率LT Real Average (10> Yrs)
        """
    },
    "新闻快讯": {
        "api":"news",
        "desc":"""接口：news
描述：获取主流新闻网站的快讯新闻数据
限量：单次最大1000条新闻
积分：用户积累5000积分可以调取，具体请参阅积分获取办法

输入参数
名称 	类型 	必选 	描述
start_date 	datetime 	Y 	开始日期
end_date 	datetime 	Y 	结束日期
src 	str 	Y 	新闻来源 见下表

数据源
来源名称 	src标识 	描述
新浪财经 	sina 	获取新浪财经实时资讯
华尔街见闻 	wallstreetcn 	华尔街见闻快讯
同花顺 	10jqka 	同花顺财经新闻
东方财富 	eastmoney 	东方财富财经新闻
云财经 	yuncaijing 	云财经新闻


日期输入说明：

    如果是某一天的数据，可以输入日期 20181120 或者 2018-11-20，比如要想取2018年11月20日的新闻，可以设置start_date='20181120', end_date='20181121' （大于数据一天）
    如果是加时间参数，可以设置：start_date='2018-11-20 09:00:00', end_date='2018-11-20 22:05:03'



输出参数
名称 	类型 	默认显示 	描述
datetime 	str 	Y 	新闻时间
content 	str 	Y 	内容
title 	str 	Y 	标题
channels 	str 	N 	分类
        """
    },
    "新闻通讯（长篇）": {
        "api":"major_news",
        "desc":"""接口：major_news
描述：获取长篇通讯信息，覆盖主要新闻资讯网站
限量：单次最大60行记录，如果需要扩大数量请在QQ群私信群主。
积分：用户积累120积分可以调取试用，超过5000以上频次相对较高，具体请参阅积分获取办法



输入参数
名称 	类型 	必选 	描述
src 	str 	N 	新闻来源
start_date 	str 	N 	新闻发布开始时间，e.g. 2018-11-21 00:00:00
end_date 	str 	N 	新闻发布结束时间，e.g. 2018-11-22 00:00:00



输出参数
名称 	类型 	默认显示 	描述
title 	str 	Y 	标题
content 	str 	N 	内容 (默认不显示，需要在fields里指定)
pub_time 	str 	Y 	发布时间
src 	str 	Y 	来源网站
        """
    },
    "新闻联播文字稿": {
        "api":"cctv_news",
        "desc":"""为了更加深入地学习贯彻我党的重要指示精神，利用新时代的新技术弘扬社会主义新价值观，特地整理了过去十年新闻联播的文字稿供大家研究、参考学习。希望大家领悟在心，实务在行，同时也别忘了抓住投资机会。

接口：cctv_news
描述：获取新闻联播文字稿数据，数据开始于2006年6月，超过12年历史
限量：总量不限制
积分：用户积累120积分可以调取，但会做流控限制，超过5000频次相对较高，具体请参阅积分获取办法


输入参数
名称 	类型 	必选 	描述
date 	str 	Y 	日期（输入格式：YYYYMMDD 比如：20181211）


输出参数
名称 	类型 	默认显示 	描述
date 	str 	Y 	日期
title 	str 	Y 	标题
content 	str 	Y 	内容
        """
    },
    "上市公司公告原文": {
        "api":"anns",
        "desc":"""接口：anns
描述：获取上市公司公告数据及原文文本，数据从2000年开始，内容很大，请注意数据调取节奏。
提示：单次最大50行记录，可设置开始和结束时间分阶段获取数据，数据总量不限制
积分：用户需要至少5000积分才可以调取。基础积分有流量控制，积分越多权限越大，请自行提高积分，具体请参阅积分获取办法


输入参数
名称 	类型 	必选 	描述
ts_code 	str 	N 	股票代码
ann_date 	str 	N 	公告日期
start_date 	str 	N 	公告开始日期
end_date 	str 	N 	公告结束日期


输出参数
名称 	类型 	默认显示 	描述
ts_code 	str 	Y 	股票代码
ann_date 	str 	Y 	公告日期
ann_type 	str 	N 	公告类型
title 	str 	Y 	公告标题
content 	str 	N 	公告内容
pub_time 	str 	N 	公告发布时间
        """
    },
    "新冠状肺炎感染人数": {
        "api":"ncov_num",
        "desc":"""接口：ncov_num
描述：获取新冠状肺炎疫情感染人数统计数据
限量：单次最大2000


输入参数
名称 	类型 	必选 	描述
area_name 	str 	N 	地区名称
level 	str 	N 	级别：2-中国内地，3-省级，4-地区市级别
ann_date 	str 	N 	公告日期
start_date 	str 	N 	查询开始日期
end_date 	str 	N 	查询结束日期


输出参数
名称 	类型 	默认显示 	描述
ann_date 	str 	Y 	发布日期
area_name 	str 	Y 	地区名称
parent_name 	str 	Y 	上一级地区
level 	int 	Y 	级别
confirmed_num 	int 	Y 	累计确诊人数
suspected_num 	int 	Y 	累计疑似人数
confirmed_num_now 	int 	Y 	现有确诊人数
suspected_num_now 	int 	Y 	现有疑似人数
cured_num 	int 	Y 	累计治愈人数
dead_num 	int 	Y 	累计死亡人数
        """
    },
    "全球新冠疫情数据": {
        "api":"ncov_global",
        "desc":"""接口：ncov_global
描述：获取全球新冠疫情数据，包括国家和地区
限量：单次最大10000，目前数据量大概是9000多行情，可以一次提取全部
积分：120积分可以获取。（积分获取方法：注册Tushare账号可100积分，修改个人信息20积分）

注意：同一日期可能有多条数据，当日可能多次公布，可以采用update_time最新时间的数据。如果取country=‘中国'，包含了各省市的明细数据。


输入参数
名称 	类型 	必选 	描述
country 	str 	N 	国家名称
province 	str 	N 	省份简称（北京、上海）
publish_date 	datetime 	N 	公布日期
start_date 	datetime 	N 	开始日期（YYYYMMDD）
end_date 	datetime 	N 	结束日期（YYYYMMDD）


输出参数
名称 	类型 	默认显示 	描述
area_id 	str 	N 	地区代码
publish_date 	str 	Y 	发布日期
country 	str 	Y 	国家
country_enname 	str 	Y 	国家英文名
province 	str 	Y 	省份
province_short 	str 	Y 	省份简称
province_enname 	str 	Y 	省份英文名
confirmed_num 	int 	Y 	累计确诊病例
confirmed_num_now 	int 	Y 	现有确诊病例
suspected_num 	int 	Y 	疑似感染病例
cured_num 	int 	Y 	治愈人数
dead_num 	int 	Y 	死亡人数
update_time 	str 	Y 	更新时间
        """
    },
    "各渠道公募基金销售保有规模占比": {
        "api":"fund_sales_ratio",
        "desc":"""接口：fund_sales_ratio
描述：获取各渠道公募基金销售保有规模占比数据，年度更新
限量：单次最大100行数据，数据从2015年开始公布，当前数据量很小


输入参数
名称 	类型 	必选 	描述
年份 	str 	N 	年度


输出参数
名称 	类型 	默认显示 	描述
year 	int 	Y 	年度
bank 	float 	Y 	商业银行（%）
sec_comp 	float 	Y 	证券公司（%）
fund_comp 	float 	Y 	基金公司直销（%）
indep_comp 	float 	Y 	独立基金销售机构（%）
rests 	float 	Y 	其他（%）
        """
    },
    "销售机构公募基金销售保有规模": {
        "api":"fund_sales_vol",
        "desc":"""接口：fund_sales_vol
描述：获取销售机构公募基金销售保有规模数据，本数据从2021年Q1开始公布，季度更新
限量：单次最大500行数据，目前总量只有100行，未来随着数据量增加会提高上限


输入参数
名称 	类型 	必选 	描述
year 	str 	N 	年度
quarter 	str 	N 	季度
name 	str 	N 	机构名称


输出参数
名称 	类型 	默认显示 	描述
year 	int 	Y 	年度
quarter 	str 	Y 	季度
inst_name 	str 	Y 	销售机构
fund_scale 	float 	Y 	股票+混合公募基金保有规模（亿元）
scale 	float 	Y 	非货币市场公募基金保有规模（亿元）
rank 	int 	Y 	排名
        """
    }
}