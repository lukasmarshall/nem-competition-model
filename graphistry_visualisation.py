import graphistry
import networkGraph
import networkx 

graphistry.register(key='555194151a1e7dd59b00ae0c4826d91b3bfbf4afac2239e05ec7180aa6f06e152d43ddea14a3616121b451cf00d150c1')


graph = networkGraph.getNetworkGraph()

graphistry.bind(source='src', destination='dst', node='nodeid').plot(graph)