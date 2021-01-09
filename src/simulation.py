
import yfinance as yf
from itertools import permutations
import matplotlib.pyplot as plt
from src.graph import StockGraph
import networkx as nx


start = "2010-01-01"
end = "2021-01-01"
period = "1mo"
interval = "1d"
auto_adjust = True
prepost = False


def get_data(stock):
    curr_ticker = yf.Ticker(stock)
    data = curr_ticker.history(period=period, interval=interval, start=start, end=end, prepost=prepost,
                               auto_adjust=auto_adjust,
                               actions=True)
    close_df = data["Close"].to_frame()
    close_df = close_df.rename(columns={'Close': 'close'})
    return close_df


def get_corrolation_table(stock_1, stock_2):

    stock_data1 = get_data(stock_1)
    stock_data2 = get_data(stock_2)
    return stock_data1.corrwith(stock_data2, axis=0, drop=False, method='pearson')["close"]


def get_graph_dict(stock_percentage_dict, graph_name="Test"):
    graph_dict = {}
    # Todo: what decides the movement?
    for stock_ticker1, stock_ticker2 in permutations(list(stock_percentage_dict.keys()), r=2):
        if stock_ticker1 not in graph_dict:
            graph_dict[stock_ticker1] = {
                "percentage": stock_percentage_dict[stock_ticker1]
            }

            graph_dict[stock_ticker1]["corrolations"] = {
                stock_ticker2: get_corrolation_table(stock_ticker1, stock_ticker2)
            }
        else:
            graph_dict[stock_ticker1]["corrolations"][stock_ticker2] = get_corrolation_table(stock_ticker1,
                                                                                             stock_ticker2)

    return graph_dict


if __name__ == "__main__":

    stock_dict = {
        "nel.ol": 0.5,
        "OSEEX.OL": 0.4,
        "spy": 0.1
    }

    graph_dict = get_graph_dict(stock_dict)
    graph = StockGraph("Test", graph_dict)
    print(graph)
    net_g = graph.to_netX(graph_dict)
    nx.write_gexf(net_g, path="test.gexf")
    nx.draw(net_g, with_labels=True)
    plt.show()


