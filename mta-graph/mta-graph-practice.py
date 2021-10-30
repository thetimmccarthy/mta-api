import pandas as pd
import time
import datetime
from collections import defaultdict
import heapq

# Uncomment to read edges (instead of building whole  edge file from stop_times file)
# edges = pd.read_csv('./edges.csv')

# read the 'stop_times' file and build a csv of edges
# easier to build the csv once and then read in edges than continuously build list of edges
def build_edges_csv():

    stop_times = pd.read_csv('./stop_times.csv')

    edges_dict = set()
    edges = []
    start_time = time.time()


    def get_time_since_zero(s):
        hours, mins, secs = [int(x) for x in s.split(':')]
        result = (hours * 3600) + (mins * 60) + secs
        return result


    for index, value in stop_times.iterrows():
        if index == 0:
            continue
        else :
            s2 = stop_times.loc[index]
            s1 = stop_times.loc[index - 1]
        if (s2['stop_sequence'] - s1['stop_sequence']) == 1 & (s1['trip_id'] == s2['trip_id']):

            s1_secs = get_time_since_zero(s1['departure_time'])
            s2_secs = get_time_since_zero(s2['departure_time'])

            weight = s2_secs - s1_secs
            pair = (s1['stop_id'][0:3], s2['stop_id'][0:3])
            pair2 = pair[::-1]

            pair_weighted = (pair[0], pair[1], weight)
            if pair not in edges_dict and pair2 not in edges_dict:
                print(index)
                edges_dict.add(pair)
                edges.append(pair_weighted)


        pd.DataFrame(edges, columns=['from', 'to', 'weight']).to_csv('edges.csv')


class Station:
    def __init__(self):
        self.station_id = ""
        self.weight = 0
        self.next_station = None

class Graph:
    def __init__(self):
        self.edges = {}
        # degree is number of edges connected to given vertex
        self.degrees = {}
        self.nvertices = 0
        self.nedges = 0
        self.directed = False


def read_graph(g, edges, directed):

    g.directed = directed

    for edge in edges:
        x = edge[0]
        y = edge[1]
        w = edge[2]
        insert_edge(g, x, y, w, directed)

    g.vertices = len(g.edges.keys())

def insert_edge(g, start_station, end_station, weight, directed):

    end = Station()
    end.station_id = end_station
    end.weight = weight

    if start_station in g.edges:

        temp = g.edges[start_station]
        end.next_station = temp
        g.edges[start_station] = end
        g.degrees[start_station] += 1
    else:
        g.edges[start_station] = end
        g.degrees[start_station] = 1

    if not directed:
        insert_edge(g, end_station, start_station, weight, True)
    else:
        g.nedges += 1


def print_graph(g):

    for key in g.edges.keys():
        print('V: ', key)
        print('-----')
        val = g.edges[key]
        while val is not None:
            print(' - ', val.station_id)
            val = val.next_station
        print('-----')


# Dijkstra's algorithm implemented using python's heapq module
def find_shortest_path(qraph, start, end):
    shortest_path = defaultdict(lambda: float('inf'))
    shortest_path[start] = 0

    parent = defaultdict(str)

    q = []
    heapq.heappush(q,(0, start))

    while len(q) != 0:
        curr = heapq.heappop(q)
        while curr[0] < shortest_path[curr[1]]:
            curr = heapq.heappop(q)

        curr = curr[1]
        curr_edge = qraph.edges[curr]



        while curr_edge is not None:
            dist = shortest_path[curr] + curr_edge.weight

            if dist < shortest_path[curr_edge.station_id]:
                shortest_path[curr_edge.station_id] = dist
                parent[curr_edge.station_id] = curr
                heapq.heappush(q, (shortest_path[curr_edge.station_id], curr_edge.station_id))

            curr_edge = curr_edge.next_station

    return shortest_path, parent

# practice edges for testing dijkstra's/graph
ab = ('A', 'B', 2)
ad = ('A', 'D', 8)
bd = ('B', 'D', 5)
be = ('B', 'E', 6)
df = ('D', 'F', 2)
de = ('D', 'E', 3)
ef = ('E', 'F', 1)
ec = ('E', 'C', 9)
fc = ('F', 'C', 3)

edges = [ab, ad, bd, be, df, de, ef, ec, fc]

graph = Graph()
read_graph(graph, edges, False)
p, j = find_shortest_path(graph, 'A', 'C')

# print key: val where key = vertex, val = distance (or cost or time) from start vertex
print('{')
for key, value in p.items():
    print(key, ': ', int(value), ',')
print('}')

# print out the path taken from start to end
# with subway trains, we can edit this to print path of stations needed
# i.e. start_station -> intermediate stations -> end
# can update to only get station if changing trains
def print_path(res, start, end):
    if start == end:
        return []
    path = [end]

    x = return_prev(res, end)
    while x != start:
        path.append(x)
        x = return_prev(res, x)
    path.append(x)
    return path[::-1]

def return_prev(res, end):
    return res[end]

print(print_path(j, 'A', 'C'))
