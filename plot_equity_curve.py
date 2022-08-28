import warnings
import pandas as pd
import numpy as np
from highcharts import Highstock


# 将价格数据转换为收益率数据
def returns_from_prices(prices, log_returns=False):
    """
    Calculate the returns given prices.
    :param prices: adjusted (daily) closing prices of the asset, each row is a
                   date and each column is a ticker/id.
    :type prices: pd.DataFrame
    :param log_returns: whether to compute using log returns
    :type log_returns: bool, defaults to False
    :return: (daily) returns
    :rtype: pd.DataFrame
    """
    if log_returns:
        returns = np.log(1 + prices.pct_change()).dropna(how="all")
    else:
        returns = prices.pct_change().dropna(how="all")
    return returns


# 将收益率数据转换为价格数据
def prices_from_returns(returns, log_returns=False):
    """
    Calculate the pseudo-prices given returns. These are not true prices because
    the initial prices are all set to 1, but it behaves as intended when passed
    to any PyPortfolioOpt method.
    :param returns: (daily) percentage returns of the assets
    :type returns: pd.DataFrame
    :param log_returns: whether to compute using log returns
    :type log_returns: bool, defaults to False
    :return: (daily) pseudo-prices.
    :rtype: pd.DataFrame
    """
    if log_returns:
        ret = np.exp(returns)
    else:
        ret = 1 + returns
    ret.iloc[0] = 1  # set first day pseudo-price
    return ret.cumprod()


# 根据价格数据或收益率数据，绘制可交互的净值曲线
def draw_equity_curve(prices, returns_data=False, title='Equity Curve', output_path=None):
    # 将传入的数据修改为数据框
    if not isinstance(prices, pd.DataFrame):
        warnings.warn("prices are not in a dataframe", RuntimeWarning)
        prices = pd.DataFrame(prices)
    # 将索引修改为日期时间格式
    if not isinstance(prices.index, pd.DatetimeIndex):
        prices.index = pd.to_datetime(prices.index)
    # 如果传入的是收益率数据，则需要转换成价格数据
    if returns_data:
        prices = prices_from_returns(prices)
    # 初始化绘图对象
    H = Highstock()
    # 导入每一个资产的价格数据
    for column in prices.columns:
        H.add_data_set(data=prices[column].reset_index(
        ).values.tolist(), series_type='line', name=column)
    # 设置绘图参数
    options = {
        'title': {
            'text': title
        },
        'rangeSelector': {
            'selected': 5  # 1-5的数字代表默认观察窗口为1m、3m、6m、YTM、1y和All
        },
        'yAxis': {
            'labels': {
                'formatter': "function () {\
                                return (this.value > 0 ? ' + ' : '') + this.value + '%';\
                            }"
            },  # this.value > 0 ? ' + '可以在正收益的数值前加上“+”
            # 绘制纵轴为0的横线
            'plotLines': [{
                'value': 0,
                'width': 2,
                'color': 'silver'
            }]
        },
        'plotOptions': {
            'series': {
                'compare': 'percent'
            }
        },
        'tooltip': {
            'pointFormat': '<span style="color:{series.color}">{series.name}:</span> <b>{point.y}</b> ({point.change}%)<br/>',
            'valueDecimals': 2  # 默认显示的小数位
        },
    }
    # 应用绘图参数
    H.set_dict_options(options)
    # 如果指定了输出路径，则输出html文件到这个路径
    if output_path:
        f = open("{}.html".format(output_path), 'w')
        f.write(H.htmlcontent)
        f.close()
    return H.htmlcontent
