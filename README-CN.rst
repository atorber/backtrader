backtrader
==========

.. image:: https://img.shields.io/pypi/v/backtrader.svg
   :alt: PyPi 版本
   :scale: 100%
   :target: https://pypi.python.org/pypi/backtrader/

..  .. image:: https://img.shields.io/pypi/dm/backtrader.svg
       :alt: PyPi 月度下载量
       :scale: 100%
       :target: https://pypi.python.org/pypi/backtrader/

.. image:: https://img.shields.io/pypi/l/backtrader.svg
   :alt: 许可证
   :scale: 100%
   :target: https://github.com/backtrader/backtrader/blob/master/LICENSE
.. image:: https://travis-ci.org/backtrader/backtrader.png?branch=master
   :alt: Travis-ci 构建状态
   :scale: 100%
   :target: https://travis-ci.org/backtrader/backtrader
.. image:: https://img.shields.io/pypi/pyversions/backtrader.svg
   :alt: Python 版本
   :scale: 100%
   :target: https://pypi.python.org/pypi/backtrader/

**Yahoo API 说明**:

  [2018-11-16] 经过一些测试，似乎可以通过网络界面（或 API ``v7``）再次可靠地下载数据

**问题反馈**

  问题反馈系统（实际上曾经）经常被滥用，用来询问关于示例的建议。

对于**反馈/问题/...**请使用 `社区 <https://community.backtrader.com>`_

这里是一个简单移动平均线交叉的代码片段。可以用几种不同的方式实现。使用文档（和示例）吧，卢克！
::

  from datetime import datetime
  import backtrader as bt

  class SmaCross(bt.SignalStrategy):
      def __init__(self):
          sma1, sma2 = bt.ind.SMA(period=10), bt.ind.SMA(period=30)
          crossover = bt.ind.CrossOver(sma1, sma2)
          self.signal_add(bt.SIGNAL_LONG, crossover)

  cerebro = bt.Cerebro()
  cerebro.addstrategy(SmaCross)

  data0 = bt.feeds.YahooFinanceData(dataname='MSFT', fromdate=datetime(2011, 1, 1),
                                    todate=datetime(2012, 12, 31))
  cerebro.adddata(data0)

  cerebro.run()
  cerebro.plot()

包含完整功能的图表。试试看！这个示例包含在示例文件夹中，文件名为 ``sigsmacross/sigsmacross2.py``。同时还有 ``sigsmacross.py``，可以通过命令行进行参数化。

功能特性:
=========

用Python编写的实时交易和回测平台。

  - 实时数据源和交易支持

    - Interactive Brokers（需要 ``IbPy``，安装 ``pytz`` 会大大受益）
    - *Visual Chart*（需要 ``comtypes`` 的分支版本，直到拉取请求集成到发布版本中，安装 ``pytz`` 会受益）
    - *Oanda*（需要 ``oandapy``）（仅支持 REST API - v20 在实现时不支持流式传输）

  - 从 csv/文件、在线源或 *pandas* 和 *blaze* 获取数据源
  - 数据过滤器，如将日线分解为块以模拟日内交易或使用 Renko 砖块
  - 支持多个数据源和多个策略
  - 同时支持多个时间框架
  - 集成重采样和回放功能
  - 逐步回测或一次性回测（除了策略评估中）
  - 集成指标库
  - *TA-Lib* 指标支持（需要 python *ta-lib* / 查看文档）
  - 轻松开发自定义指标
  - 分析器（例如：TimeReturn、夏普比率、SQN）和 ``pyfolio`` 集成（**已弃用**）
  - 灵活定义佣金方案
  - 集成经纪商模拟，支持 *市价*、*收盘价*、*限价*、*止损*、*止损限价*、*跟踪止损*、*跟踪止损限价* 和 *OCO* 订单、括号订单、滑点、成交量填充策略以及期货类工具的连续现金调整
  - 自动仓位管理的尺寸器
  - 收盘作弊和开盘作弊模式
  - 调度器
  - 交易日历
  - 绘图功能（需要 matplotlib）

文档
=============

博客：

  - `博客 <http://www.backtrader.com/blog>`_

阅读完整文档：

  - `文档 <http://www.backtrader.com/docu>`_

内置指标列表（122个）

  - `指标参考 <http://www.backtrader.com/docu/indautoref.html>`_

Python 2/3 支持
==================

  - Python >= ``3.2``

  - 也适用于 ``pypy`` 和 ``pypy3``（不支持绘图 - ``matplotlib`` 在 *pypy* 下不受支持）

安装
============

``backtrader`` 是自包含的，没有外部依赖（除非您想要绘图）

从 *pypi* 安装：

  - ``pip install backtrader``

  - ``pip install backtrader[plotting]``

    如果 ``matplotlib`` 未安装且您希望进行一些绘图

.. note:: matplotlib 最低版本要求是 ``1.4.1``

*IB* 数据源/交易示例：

  - ``IbPy`` 似乎不在 PyPi 中。请执行以下任一操作：::

      pip install git+https://github.com/blampe/IbPy.git

    或（如果您的系统中没有 ``git``）：::

      pip install https://github.com/blampe/IbPy/archive/master.zip

对于其他功能，如：``Visual Chart``、``Oanda``、``TA-Lib``，请查看文档中的依赖项。

从源码安装：

  - 将源码中找到的 *backtrader* 目录放在您的项目内

版本编号
=================

X.Y.Z.I

  - X：主版本号。除非有重大更改（如彻底改造以使用 ``numpy``），否则应保持稳定
  - Y：次版本号。在添加完整新功能或（但愿不会）不兼容的 API 更改时更改
  - Z：修订版本号。在文档更新、小更改、小错误修复时更改
  - I：已内置到平台中的指标数量
