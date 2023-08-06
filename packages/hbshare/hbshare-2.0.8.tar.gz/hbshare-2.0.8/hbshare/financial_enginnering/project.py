import pandas as pd
from ..financial_enginnering import functionality
from ..financial_enginnering import db_engine as dben
from ..financial_enginnering import config

class Projects:

    def __init__(self):

        self.config=config.Config()

    def prv_hld_analysis (self,prd_name,tablename):

        config=self.config

        # initial the temp database class
        Pfdb = dben.PrvFunDB()

        # write fold files to DB
        # Pfdb.write2DB(table_name='prvfund',fold_dir="E:\私募主观\主观股多估值表基地",increment=0)

        # initial the class
        Jydb = dben.HBDB()

        # extra data from the temp database
        df1 = Pfdb.extract_from_db(prd_name=prd_name, columns='*', tablename=tablename)

        # get the unique date list and stock code list
        date_list = df1['Stamp_date'].dropna().unique()
        sec_code = df1['Stock_code'].dropna().unique()

        # extra industry data from the JY database
        df2 = Jydb.extract_industry(sec_code)

        # extra financial data from the JY database
        df3 = Jydb.extract_fin_info(sec_code,date_list)

        # extra benchmark data from the JY database
        df4 = Jydb.extract_benchmark(config.Index_type, sec_code=sec_code,date_list=date_list)

        fun = functionality.Untils(df1, df2, df3, df4)

        asset_allocation_df = fun.asset_allocation_stats()

        ind_hld = fun.aggregate_by(fun.purified_stk_hld, groupby=['Stamp_date', 'FIRSTINDUSTRYNAME'], method='sum',
                                   method_on='Weight')
        indutry_allocation_df_ranked = fun.rank_filter(ind_hld, [1, 3, 5])

        stk_hld = fun.aggregate_by(fun.purified_stk_hld, groupby=['Stamp_date', 'Name'], method='sum',
                                   method_on='Weight')
        asset_allocation_df_ranked = fun.rank_filter(stk_hld, [3, 5, 10])

        fin_hld = fun.aggregate_by(fun.purified_stk_hld, groupby=['Stamp_date', 'Name'], method='sum',
                                   method_on=['PE', 'PB', 'DIVIDENDRATIO'])
        ben_hld = fun.aggregate_by(fun.bench_info, groupby=['Stamp_date', 'Index_type'], method='sum',
                                   method_on='Weight')

        # drawing the pics
        plot = functionality.Plot(fig_width=800, fig_height=600)

        # 1.资产配置时序：A股 / 港股 / 债券 / 基金 / 现金等类别时序的累计区域图；
        plot.plotly_area(asset_allocation_df[['活期存款', '债券', '基金', '权证', '其他', 'A股',
                                              '港股', '日期']], '资产配置时序')

        # 2.行业配置时序：基于申万一级行业分别规则，对持仓的行业分布做一个时序统计；
        plot.plotly_area(ind_hld, '行业配置时序')

        # 3. 行业集中度时序：持仓前一 / 三 / 五大行业的权重时序
        inputdf = indutry_allocation_df_ranked.copy()
        cols = inputdf.columns.tolist()
        cols.remove('日期')
        for col in cols:
            inputdf[col] = [x[0].sum() for x in inputdf[col]]
        plot.plotly_line(inputdf, '行业集中度时序')

        # 4.重仓明细：时序上各个时间点的持仓明细（表格）；
        for date in date_list:
            tempdf = df1[df1['Stamp_date'] == date][list(config.Columns_name_trans.values())]
            tempdf.columns = list(config.Columns_name_trans.keys())
            colwidth = [100, 150, 100, 80, 120, 120, 80, 120, 120, 120, 80, 60, 60, 70]
            plot.plotly_table(tempdf, colwidth, '持仓明细\n日期：{0}'.format(str(date)))

        # 5.持股集中度时序：持仓前三 / 五 / 十大权重和的时序折线图；
        inputdf = asset_allocation_df_ranked.copy()
        cols = inputdf.columns.tolist()
        cols.remove('日期')
        for col in cols:
            inputdf[col] = [x[0].sum() for x in inputdf[col]]
        plot.plotly_line(inputdf, '持股集中度时序')

        # 6.组合中A股持仓的平均PE / PB / 股息率的折线图；
        tempdf = pd.DataFrame()
        for item in ['PE', 'PB', 'DIVIDENDRATIO']:
            tempdf[item] = ((fin_hld.loc[:, (item, slice(None))].values) * (stk_hld.drop('日期', axis=1).values)).sum(
                axis=1) / stk_hld.drop('日期', axis=1).values.sum(axis=1)
        tempdf['日期'] = date_list
        plot.plotly_line_multi_yaxis(tempdf, '持股估值分析', ['PB', 'DIVIDENDRATIO'])

        # 7.持股分布：所持股票在各类宽基成分股中的权重时序的折线图，包括：沪深300、中证500、中证1000、1800以外。
        plot.plotly_area(ben_hld, '宽基成分股配置走势')


