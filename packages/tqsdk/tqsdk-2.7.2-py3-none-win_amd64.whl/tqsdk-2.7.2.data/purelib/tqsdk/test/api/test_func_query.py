#!/usr/bin/env python
#  -*- coding: utf-8 -*-

import os
import random
import sys
import unittest

from tqsdk.test.base_testcase import TQBaseTestcase
from tqsdk import TqApi, utils


class TestFuncQuery(TQBaseTestcase):
    """
    TqApi中功能函数的基本功能测试.

    注：
    1. 在本地运行测试用例前需设置运行环境变量(Environment variables), 保证api中dict及set等类型的数据序列在每次运行时元素顺序一致: PYTHONHASHSEED=32
    2. 若测试用例中调用了会使用uuid的功能函数时（如insert_order()会使用uuid生成order_id）,
        则：在生成script文件时及测试用例中都需设置 TqApi.RD = random.Random(x), 以保证两次生成的uuid一致, x取值范围为0-2^32
    3. 对盘中的测试用例（即非回测）：因为TqSim模拟交易 Order 的 insert_date_time 和 Trade 的 trade_date_time 不是固定值，所以改为判断范围。
        盘中时：self.assertAlmostEqual(1575292560005832000 / 1e9, order1.insert_date_time / 1e9, places=1)
        回测时：self.assertEqual(1575291600000000000, order1.insert_date_time)
    """

    def setUp(self):
        super(TestFuncQuery, self).setUp(md_url="wss://api.shinnytech.com/t/nfmd/front/mobile")

    def tearDown(self):
        super(TestFuncQuery, self).tearDown()

    def test_func_query(self):
        """
            is_changing() 测试
            注：本函数不是回测，重新生成测试用例script文件时更改为当前可交易的合约代码,在盘中生成,且_ins_url可能需修改。
        """

        # 预设服务器端响应
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.md_mock.run(os.path.join(dir_path, "log_file", "test_func_query.script.lzma"))
        md_url = f"ws://127.0.0.1:{self.md_mock.port}/"
        # 测试: 模拟账户下单
        utils.RD = random.Random(4)
        api = TqApi(auth="tianqin,tianqin", _md_url=md_url)
        ls = api.query_quotes(ins_class="FUTURE", exchange_id="SHFE", product_id="rb", expired=False)
        self.assertEqual(ls, ['SHFE.rb2203', 'SHFE.rb2201', 'SHFE.rb2205', 'SHFE.rb2110', 'SHFE.rb2202', 'SHFE.rb2207', 'SHFE.rb2112', 'SHFE.rb2109', 'SHFE.rb2111', 'SHFE.rb2108', 'SHFE.rb2206', 'SHFE.rb2204'])
        ls_cont = api.query_cont_quotes(exchange_id="DCE")
        self.assertEqual(ls_cont, ['DCE.fb2109', 'DCE.m2109', 'DCE.c2109', 'DCE.p2109', 'DCE.cs2109', 'DCE.pg2109', 'DCE.y2109', 'DCE.eb2109', 'DCE.pp2109', 'DCE.jm2109', 'DCE.j2109', 'DCE.jd2109', 'DCE.b2109', 'DCE.a2109', 'DCE.bb2201', 'DCE.rr2109', 'DCE.l2109', 'DCE.v2109', 'DCE.lh2109', 'DCE.i2109', 'DCE.eg2109'])
        in_options, at_options, out_options = api.query_all_level_options(underlying_symbol="DCE.m2109",
                                                                          underlying_price=2620, option_class="PUT")
        self.assertEqual(in_options, ['DCE.m2109-P-4150', 'DCE.m2109-P-4100', 'DCE.m2109-P-4050', 'DCE.m2109-P-4000', 'DCE.m2109-P-3950', 'DCE.m2109-P-3900', 'DCE.m2109-P-3850', 'DCE.m2109-P-3800', 'DCE.m2109-P-3750', 'DCE.m2109-P-3700', 'DCE.m2109-P-3650', 'DCE.m2109-P-3600', 'DCE.m2109-P-3550', 'DCE.m2109-P-3500', 'DCE.m2109-P-3450', 'DCE.m2109-P-3400', 'DCE.m2109-P-3350', 'DCE.m2109-P-3300', 'DCE.m2109-P-3250', 'DCE.m2109-P-3200', 'DCE.m2109-P-3150', 'DCE.m2109-P-3100', 'DCE.m2109-P-3050', 'DCE.m2109-P-3000', 'DCE.m2109-P-2950', 'DCE.m2109-P-2900', 'DCE.m2109-P-2850', 'DCE.m2109-P-2800', 'DCE.m2109-P-2750', 'DCE.m2109-P-2700', 'DCE.m2109-P-2650'])
        self.assertEqual(at_options, ['DCE.m2109-P-2600'])
        self.assertEqual(out_options, ['DCE.m2109-P-2550', 'DCE.m2109-P-2500'])
        in_options, at_options, out_options = api.query_all_level_finance_options(underlying_symbol="SSE.510300",
                                                                                  underlying_price=4.87,
                                                                                  option_class="CALL",
                                                                                  nearbys=[0, 1])
        self.assertEqual(in_options, ['SSE.10003521', 'SSE.10003525', 'SSE.10003522', 'SSE.10003323', 'SSE.10003499', 'SSE.10003313', 'SSE.10003479', 'SSE.10003249', 'SSE.10003480', 'SSE.10003223'])
        self.assertEqual(at_options, ['SSE.10003481'])
        self.assertEqual(out_options, ['SSE.10003224', 'SSE.10003482', 'SSE.10003225', 'SSE.10003483', 'SSE.10003226', 'SSE.10003484', 'SSE.10003227', 'SSE.10003485', 'SSE.10003228', 'SSE.10003486', 'SSE.10003229', 'SSE.10003487', 'SSE.10003230', 'SSE.10003231', 'SSE.10003253'])
        df = api.query_symbol_info(in_options + at_options + out_options)

        print(df)
        api.close()
