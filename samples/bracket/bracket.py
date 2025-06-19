#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
#
# Copyright (C) 2015-2023 Daniel Rodriguez
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)


import argparse
import datetime

import backtrader as bt


class St(bt.Strategy):
    params = dict(
        ma=bt.ind.SMA,
        p1=5,
        p2=15,
        limit=0.005,
        limdays=3,
        limdays2=1000,
        hold=10,
        usebracket=False,  # 使用 order_target_size
        switchp1p2=False,  # 切换 order1 和 order2 的价格
    )

    def notify_order(self, order):
        print('{}: Order ref: {} / Type {} / Status {}'.format(
            self.data.datetime.date(0),
            order.ref, 'Buy' * order.isbuy() or 'Sell',
            order.getstatusname()))

        if order.status == order.Completed:
            self.holdstart = len(self)

        if not order.alive() and order.ref in self.orefs:
            self.orefs.remove(order.ref)

    def __init__(self):
        ma1, ma2 = self.p.ma(period=self.p.p1), self.p.ma(period=self.p.p2)
        self.cross = bt.ind.CrossOver(ma1, ma2)

        self.orefs = list()

        if self.p.usebracket:
            print('-' * 5, '使用 buy_bracket')

    def next(self):
        if self.orefs:
            return  # 待处理订单不执行任何操作

        if not self.position:
            if self.cross > 0.0:  # 向上穿越

                close = self.data.close[0]
                p1 = close * (1.0 - self.p.limit)
                p2 = p1 - 0.02 * close
                p3 = p1 + 0.02 * close

                valid1 = datetime.timedelta(self.p.limdays)
                valid2 = valid3 = datetime.timedelta(self.p.limdays2)

                if self.p.switchp1p2:
                    p1, p2 = p2, p1
                    valid1, valid2 = valid2, valid1

                if not self.p.usebracket:
                    o1 = self.buy(exectype=bt.Order.Limit,
                                  price=p1,
                                  valid=valid1,
                                  transmit=False)

                    print('{}: Oref {} / 买入价格 {}'.format(
                        self.datetime.date(), o1.ref, p1))

                    o2 = self.sell(exectype=bt.Order.Stop,
                                   price=p2,
                                   valid=valid2,
                                   parent=o1,
                                   transmit=False)

                    print('{}: Oref {} / 止损卖出价格 {}'.format(
                        self.datetime.date(), o2.ref, p2))

                    o3 = self.sell(exectype=bt.Order.Limit,
                                   price=p3,
                                   valid=valid3,
                                   parent=o1,
                                   transmit=True)

                    print('{}: Oref {} / 限价卖出价格 {}'.format(
                        self.datetime.date(), o3.ref, p3))

                    self.orefs = [o1.ref, o2.ref, o3.ref]

                else:
                    os = self.buy_bracket(
                        price=p1, valid=valid1,
                        stopprice=p2, stopargs=dict(valid=valid2),
                        limitprice=p3, limitargs=dict(valid=valid3),)

                    self.orefs = [o.ref for o in os]

        else:  # 在市场中有持仓
            if (len(self) - self.holdstart) >= self.p.hold:
                pass  # 在这种情况下不执行任何操作


def runstrat(args=None):
    args = parse_args(args)

    cerebro = bt.Cerebro()

    # 数据源参数
    kwargs = dict()

    # 解析开始/结束日期
    dtfmt, tmfmt = '%Y-%m-%d', 'T%H:%M:%S'
    for a, d in ((getattr(args, x), x) for x in ['fromdate', 'todate']):
        if a:
            strpfmt = dtfmt + tmfmt * ('T' in a)
            kwargs[d] = datetime.datetime.strptime(a, strpfmt)

    # 数据源
    data0 = bt.feeds.BacktraderCSVData(dataname=args.data0, **kwargs)
    cerebro.adddata(data0)

    # 经纪人
    cerebro.broker = bt.brokers.BackBroker(**eval('dict(' + args.broker + ')'))

    # 仓位管理器
    cerebro.addsizer(bt.sizers.FixedSize, **eval('dict(' + args.sizer + ')'))

    # 策略
    cerebro.addstrategy(St, **eval('dict(' + args.strat + ')'))

    # 执行
    cerebro.run(**eval('dict(' + args.cerebro + ')'))

    if args.plot:  # 如果请求则绘图
        cerebro.plot(**eval('dict(' + args.plot + ')'))


def parse_args(pargs=None):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=(
            '样本框架'
        )
    )

    parser.add_argument('--data0', default='../../datas/2005-2006-day-001.txt',
                        required=False, help='要读取的数据')

    # 日期默认值
    parser.add_argument('--fromdate', required=False, default='',
                        help='YYYY-MM-DD[THH:MM:SS] 格式的日期[时间]')

    parser.add_argument('--todate', required=False, default='',
                        help='YYYY-MM-DD[THH:MM:SS] 格式的日期[时间]')

    parser.add_argument('--cerebro', required=False, default='',
                        metavar='kwargs', help='key=value 格式的参数')

    parser.add_argument('--broker', required=False, default='',
                        metavar='kwargs', help='key=value 格式的参数')

    parser.add_argument('--sizer', required=False, default='',
                        metavar='kwargs', help='key=value 格式的参数')

    parser.add_argument('--strat', required=False, default='',
                        metavar='kwargs', help='key=value 格式的参数')

    parser.add_argument('--plot', required=False, default='',
                        nargs='?', const='{}',
                        metavar='kwargs', help='key=value 格式的参数')

    return parser.parse_args(pargs)


if __name__ == '__main__':
    runstrat()
