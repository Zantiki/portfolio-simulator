
from networkx import Graph
class StockNode:

    def __init__(self, ticker, percentage):
        # connections is a dict containing dependecies and corrolations to them
        self._connections = []
        self.ticker = ticker
        self.percentage = percentage

    def add_connection(self, stock_node, corrolation):
        self._connections.append((stock_node, corrolation))

    def get_connections(self):
        return self._connections

    def __str__(self):
        string = "{} is {}% and has connections: \n".format(self.ticker, self.percentage*100)
        for connection in self._connections:
            string += "  {} with corr {}\n".format(connection[0].ticker, connection[1])
        return string


class StockGraph:

    def __init__(self, name, corrolation_dict):
        self.name = name
        self.stock_list = []

        self.build_graph(corrolation_dict)

    def build_graph(self, corrolation_dict, current_node=None):

        if not current_node:
            first_key = iter(corrolation_dict).__next__()
            current_node = StockNode(first_key, corrolation_dict[first_key]["percentage"])
        else:
            first_key = current_node.ticker

        self.stock_list.append(current_node)

        for corrolation_ticker in corrolation_dict[first_key]["corrolations"]:
            ticker_list = [x.ticker for x in self.stock_list]

            if corrolation_ticker not in ticker_list:
                corrolation_node = StockNode(corrolation_ticker, corrolation_dict[corrolation_ticker]["percentage"])
                current_node.add_connection(corrolation_node, corrolation_dict[first_key]["corrolations"][corrolation_ticker])
                self.build_graph(corrolation_dict, corrolation_node)
            else:
                corrolation_node = self.stock_list[ticker_list.index(corrolation_ticker)]
                current_node.add_connection(corrolation_node, corrolation_dict[first_key]["corrolations"][corrolation_ticker])

        return current_node

    def __str__(self):
        string = "-- NODES IN {} --\n".format(self.name)
        for node in self.stock_list:
            string += node.__str__()

        return string

    @staticmethod
    def to_netX(stock_dict):
        net_x_g = Graph()
        for key in stock_dict:
            net_x_g.add_nodes_from([(key, {"percentage": stock_dict[key]["percentage"]})])

        for key in stock_dict:
            for corrolation in stock_dict[key]["corrolations"]:
                net_x_g.add_edges_from([(key, corrolation, {'corrolation': stock_dict[key]["corrolations"][corrolation]})])

        return net_x_g


    def walk(self):
        pass



if __name__ == "__main__":

    stock_dict = {
        "nel.ol": 0.5,
        "OSEEX.OL": 0.5
    }

    corr_dict = {
        "nel.ol": {
            "percentage": 0.5,
            "corrolations": {
                "OSEEX.OL": 0.9,
                "vix": 0.1
            }
        },
        "OSEEX.OL": {
            "percentage": 0.4,
            "corrolations": {
                "nel.ol": 0.8
            }
        },
        "vix": {
            "percentage": 0.1,
            "corrolations": {
                "OSEEX.OL": 0.8
            }
        }
    }
    corr_graph = StockGraph("TEST", corr_dict)
    print(corr_graph)

