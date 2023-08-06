import re
import itertools
import mpld3
import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from glycowork.glycan_data.loader import lib, unwrap
from glycowork.motif.graph import fast_compare_glycans, compare_glycans, glycan_to_nxGraph, graph_to_string, subgraph_isomorphism

def safe_compare(g1, g2, libr = None):
  """fast_compare_glycans with try/except error catch\n
  | Arguments:
  | :-
  | g1 (networkx object): glycan graph from glycan_to_nxGraph
  | g2 (networkx object): glycan graph from glycan_to_nxGraph
  | libr (list): library of monosaccharides; if you have one use it, otherwise a comprehensive lib will be used\n
  | Returns:
  | :-  
  | Returns True if two glycans are the same and False if not; returns False if 'except' is triggered
  """
  if libr is None:
    libr = lib
  try:
    return fast_compare_glycans(g1, g2, libr = lib)
  except:
    return False

def safe_max(diff_list):
  """returns max with try/except error catch to handle empty lists\n
  | Arguments:
  | :-
  | diff_list (list): list of length differences between glycan substructures\n
  | Returns:
  | :- 
  | Returns max length difference; returns 0 if 'except' is triggered
  """
  try:
    return max(diff_list)
  except:
    return 0

def subgraph_to_string(subgraph, libr = None):
  """converts glycan subgraph back to IUPAC-condensed format\n
  | Arguments:
  | :-
  | subgraph (networkx object): subgraph of one monosaccharide and its linkage
  | libr (list): library of monosaccharides; if you have one use it, otherwise a comprehensive lib will be used\n
  | Returns:
  | :-
  | Returns glycan motif in IUPAC-condensed format (string)
  """
  if libr is None:
    libr = lib
  glycan_motif = [libr[k] for k in list(sorted(list(nx.get_node_attributes(subgraph, 'labels').values())))]
  glycan_motif = glycan_motif[0] + '(' + glycan_motif[1] + ')'
  return glycan_motif

def get_neighbors(glycan, glycans, libr = None, graphs = None):
  """find (observed) biosynthetic precursors of a glycan\n
  | Arguments:
  | :-
  | glycan (string): glycan in IUPAC-condensed format
  | glycans (list): list of glycans in IUPAC-condensed format
  | libr (list): library of monosaccharides; if you have one use it, otherwise a comprehensive lib will be used
  | graphs (list): list of glycans in df as graphs; optional if you call get_neighbors often with the same df and want to provide it precomputed\n
  | Returns:
  | :-
  | (1) a list of direct glycan precursors in IUPAC-condensed
  | (2) a list of indices where each precursor from (1) can be found in glycans
  """
  if libr is None:
    libr = libr
  ggraph = glycan_to_nxGraph(glycan, libr = libr)
  ggraph_nb = create_neighbors(ggraph, libr = libr)
  if graphs is None:
    temp = [glycan_to_nxGraph(k, libr = libr) for k in glycans]
  else:
    temp = graphs
  idx = [np.where([safe_compare(k, j, libr = libr) for k in temp])[0].tolist() for j in ggraph_nb]
  nb = [glycans[k[0]] for k in idx if len(k)>0]
  return nb, idx

def create_adjacency_matrix(glycans, libr = None, virtual_nodes = False,
                            reducing_end = ['Glc', 'GlcNAc']):
  """creates a biosynthetic adjacency matrix from a list of glycans\n
  | Arguments:
  | :-
  | glycans (list): list of glycans in IUPAC-condensed format
  | libr (list): library of monosaccharides; if you have one use it, otherwise a comprehensive lib will be used
  | virtual_nodes (bool): whether to include virtual nodes in network; default:False
  | reducing_end (list): monosaccharides at the reducing end that are allowed; default:['Glc','GlcNAc']\n
  | Returns:
  | :-
  | (1) adjacency matrix (glycan X glycan) denoting whether two glycans are connected by one biosynthetic step
  | (2) list of which nodes are virtual nodes (empty list if virtual_nodes is False)
  """
  if libr is None:
    libr = lib
  df_out = pd.DataFrame(0, index = glycans, columns = glycans)
  graphs = [glycan_to_nxGraph(k, libr = libr) for k in glycans]
  neighbors_full = [get_neighbors(k, glycans, libr = libr, graphs = graphs) for k in glycans]
  neighbors = [k[0] for k in neighbors_full]
  idx = [k[1] for k in neighbors_full]
  for j in range(len(glycans)):
    if len(idx[j])>0:
      for i in range(len(idx[j])):
        if len(idx[j][i]) >= 1:
          inp = [idx[j][i], glycans.index(glycans[j])]
          df_out.iloc[inp[0], inp[1]] = 1
  new_nodes = []
  if virtual_nodes:
    virtual_edges = fill_with_virtuals(glycans, libr = libr, reducing_end = reducing_end)
    new_nodes = list(set([k[1] for k in virtual_edges]))
    new_nodes = [k for k in new_nodes if k not in df_out.columns.values.tolist()]
    idx = np.where([any([compare_glycans(k,j, libr = libr) for j in df_out.columns.values.tolist()]) for k in new_nodes])[0].tolist()
    if len(idx)>0:
      virtual_edges = [j for j in virtual_edges if j[1] not in [new_nodes[k] for k in idx]]
      new_nodes = [new_nodes[k] for k in range(len(new_nodes)) if k not in idx]
    for k in new_nodes:
      df_out[k] = 0
      df_out.loc[len(df_out)] = 0
      df_out.index = df_out.index.values.tolist()[:-1] + [k]
    for k in virtual_edges:
      df_out.loc[k[0], k[1]] = 1
  return df_out + df_out.T, new_nodes

def adjacencyMatrix_to_network(adjacency_matrix):
  """converts an adjacency matrix to a network\n
  | Arguments:
  | :-
  | adjacency_matrix (dataframe): denoting whether two glycans are connected by one biosynthetic step\n
  | Returns:
  | :-
  | Returns biosynthetic network as a networkx graph
  """
  network = nx.convert_matrix.from_numpy_array(adjacency_matrix.values)
  network = nx.relabel_nodes(network, {k:adjacency_matrix.columns.values.tolist()[k] for k in range(len(adjacency_matrix))})
  return network


def find_diff(glycan_a, glycan_b, libr = None):
  """finds the subgraph that differs between glycans and returns it, will only work if the differing subgraph is connected\n
  | Arguments:
  | :-
  | glycan_a (string): glycan in IUPAC-condensed format
  | glycan_b (string): glycan in IUPAC-condensed format
  | libr (list): library of monosaccharides; if you have one use it, otherwise a comprehensive lib will be used\n
  | Returns:
  | :-
  | Returns difference between glycan_a and glycan_b in IUPAC-condensed
  """
  if libr is None:
    libr = lib
  glycan_a = [libr[k] for k in list(sorted(list(nx.get_node_attributes(glycan_to_nxGraph(glycan_a, libr = libr), 'labels').values())))]
  glycan_b = [libr[k] for k in list(sorted(list(nx.get_node_attributes(glycan_to_nxGraph(glycan_b, libr = libr), 'labels').values())))]
  lens = [len(glycan_a), len(glycan_b)]
  graphs = [glycan_a, glycan_b]
  larger_graph = graphs[np.argmax(lens)]
  smaller_graph = graphs[np.argmin(lens)]
  for k in smaller_graph:
    try:
      larger_graph.remove(k)
    except:
      larger_graph = ['dis', 'regard']
  return "".join(larger_graph)

def construct_network(glycans, add_virtual_nodes = 'none', libr = None, reducing_end = ['Glc','GlcNAc'],
                 limit = 5):
  """visualize biosynthetic network\n
  | Arguments:
  | :-
  | glycans (list): list of glycans in IUPAC-condensed format
  | add_virtual_nodes (string): indicates whether no ('none'), proximal ('simple'), or all ('exhaustive') virtual nodes should be added; default:'none'
  | libr (list): library of monosaccharides; if you have one use it, otherwise a comprehensive lib will be used
  | reducing_end (list): monosaccharides at the reducing end that are allowed; default:['Glc','GlcNAc']
  | limit (int): maximum number of virtual nodes between observed nodes; default:5\n
  | Returns:
  | :-
  | Returns a networkx object of the network
  """
  if libr is None:
    libr = lib
  if add_virtual_nodes in ['simple', 'exhaustive']:
    virtuals = True
  else:
    virtuals = False
  adjacency_matrix, virtual_nodes = create_adjacency_matrix(glycans, libr = libr, virtual_nodes = virtuals,
                            reducing_end = reducing_end)
  network = adjacencyMatrix_to_network(adjacency_matrix)
  if add_virtual_nodes == 'exhaustive':
    unconnected_nodes = get_unconnected_nodes(network, list(network.nodes()))
    new_nodes = []
    new_edges = []
    new_edge_labels =  []
    for k in list(sorted(unconnected_nodes)):
      try:
        virtual_edges, edge_labels = find_shortest_path(k, [j for j in list(network.nodes()) if j != k], libr = libr,
                                                      reducing_end = reducing_end, limit = limit)
        total_nodes = list(set(list(sum(virtual_edges, ()))))
        new_nodes.append([j for j in total_nodes if j not in list(network.nodes())])
        new_edges.append(virtual_edges)
        new_edge_labels.append(edge_labels)
      except:
        pass
    network.add_edges_from(unwrap(new_edges), edge_labels = unwrap(new_edge_labels))
    virtual_nodes = virtual_nodes + list(set(unwrap(new_nodes)))
    for ed in (network.edges()):
      if ed[0] in virtual_nodes and ed[1] in virtual_nodes:
        larger_ed = np.argmax([len(e) for e in [ed[0], ed[1]]])
        if network.degree(ed[larger_ed]) == 1:
          network.remove_edge(ed[0], ed[1])
  edge_labels = {}
  for el in list(network.edges()):
    edge_labels[el] = find_diff(el[0], el[1], libr = libr)
  nx.set_edge_attributes(network, edge_labels, 'diffs')
  virtual_labels = {k:(1 if k in virtual_nodes else 0) for k in list(network.nodes())}
  nx.set_node_attributes(network, virtual_labels, 'virtual')
  network = filter_disregard(network)
  return network

def plot_network(network, plot_format = 'kamada_kawai', edge_label_draw = True):
  """visualizes biosynthetic network\n
  | Arguments:
  | :-
  | network (networkx object): biosynthetic network, returned from construct_network
  | plot_format (string): how to layout network, either 'kamada_kawai' or 'spring'; default:'kamada_kawai'
  | edge_label_draw (bool): draws edge labels if True; default:True\n
  """
  mpld3.enable_notebook()
  fig, ax = plt.subplots(figsize = (16,16))
  if plot_format == 'kamada_kawai':
    pos = nx.kamada_kawai_layout(network)
  elif plot_format == 'spring':
    pos = nx.spring_layout(network, k = 1/4)
  if len(list(nx.get_node_attributes(network, 'origin').values()))>0:
    node_origins = True
  else:
    node_origins = False
  if node_origins:
    alpha_map = [0.2 if k==1 else 1 for k in list(nx.get_node_attributes(network, 'virtual').values())]
    scatter = nx.draw_networkx_nodes(network, pos, node_size = 50, ax = ax,
                                       node_color = list(nx.get_node_attributes(network, 'origin').values()),
                                       alpha = alpha_map)
  else:
    color_map = ['darkorange' if k==1 else 'cornflowerblue' if k==0 else 'seagreen' for k in list(nx.get_node_attributes(network, 'virtual').values())]
    scatter = nx.draw_networkx_nodes(network, pos, node_size = 50, alpha = 0.7,
                                     node_color = color_map, ax = ax)
  labels = list(network.nodes())
  if edge_label_draw:
    nx.draw_networkx_edges(network, pos, ax = ax, edge_color = 'cornflowerblue')
    nx.draw_networkx_edge_labels(network, pos, edge_labels = nx.get_edge_attributes(network, 'diffs'), ax = ax)
  else:
    diffs = list(nx.get_edge_attributes(network, 'diffs').values())
    c_list = ['cornflowerblue' if 'Glc' in k else 'yellow' if 'Gal' in k else 'red' if 'Fuc' in k else 'mediumorchid' if '5Ac' in k \
              else 'turquoise' if '5Gc' in k else 'silver' for k in diffs]
    w_list = [1 if 'b1' in k else 3 for k in diffs]
    nx.draw_networkx_edges(network, pos, ax = ax, edge_color = c_list, width = w_list)
  [sp.set_visible(False) for sp in ax.spines.values()]
  ax.set_xticks([])
  ax.set_yticks([])
  tooltip = mpld3.plugins.PointLabelTooltip(scatter, labels = labels)
  mpld3.plugins.connect(fig, tooltip)

def find_shared_virtuals(glycan_a, glycan_b, libr = None, reducing_end = ['Glc', 'GlcNAc']):
  """finds virtual nodes that are shared between two glycans (i.e., that connect these two glycans)\n
  | Arguments:
  | :-
  | glycan_a (string): glycan in IUPAC-condensed format
  | glycan_b (string): glycan in IUPAC-condensed format
  | libr (list): library of monosaccharides; if you have one use it, otherwise a comprehensive lib will be used
  | reducing_end (list): monosaccharides at the reducing end that are allowed; default:['Glc','GlcNAc']\n
  | Returns:
  | :-
  | Returns list of edges between glycan and virtual node (if virtual node connects the two glycans)
  """
  if libr is None:
    libr = lib
  virtuals_a = get_virtual_nodes(glycan_a, libr = libr, reducing_end = reducing_end)
                                 
  virtuals_b = get_virtual_nodes(glycan_b, libr = libr, reducing_end = reducing_end)
  ggraph_nb_a = virtuals_a[0]
  ggraph_nb_b = virtuals_b[0]
  glycans_a = virtuals_a[1]
  glycans_b = virtuals_b[1]
  out = []
  if len(ggraph_nb_a)>0:
    for k in range(len(ggraph_nb_a)):
      for j in range(len(ggraph_nb_b)):
        if fast_compare_glycans(ggraph_nb_a[k], ggraph_nb_b[j], libr = libr):
          if [glycan_a, glycans_a[k]] not in [list(m) for m in out]:
            out.append((glycan_a, glycans_a[k]))
          if [glycan_b, glycans_b[j]] not in [list(m) for m in out]:
            out.append((glycan_b, glycans_a[k]))
  return out

def fill_with_virtuals(glycans, libr = None, reducing_end = ['Glc', 'GlcNAc']):
  """for a list of glycans, identify virtual nodes connecting observed glycans and return their edges\n
  | Arguments:
  | :-
  | glycans (list): list of glycans in IUPAC-condensed
  | libr (list): library of monosaccharides; if you have one use it, otherwise a comprehensive lib will be used
  | reducing_end (list): monosaccharides at the reducing end that are allowed; default:['Glc','GlcNAc']\n
  | Returns:
  | :-
  | Returns list of edges that connect observed glycans to virtual nodes
  """
  if libr is None:
    libr = lib
  v_edges = [find_shared_virtuals(k[0],k[1], libr = libr, reducing_end = reducing_end) for k in list(itertools.combinations(glycans, 2))]
  v_edges = unwrap(v_edges)
  return v_edges

def create_neighbors(ggraph, libr = None):
  """creates biosynthetic precursor glycans\n
  | Arguments:
  | :-
  | ggraph (networkx object): glycan graph from glycan_to_nxGraph
  | libr (list): library of monosaccharides; if you have one use it, otherwise a comprehensive lib will be used\n
  | Returns:
  | :-
  | Returns biosynthetic precursor glycans
  """
  if libr is None:
    libr = lib
  ra = range(len(ggraph.nodes()))
  ggraph_nb = [ggraph.subgraph(k) for k in itertools.combinations(ra, len(ggraph.nodes())-2) if safe_max(np.diff(k)) in [1,3]]
  ggraph_nb = [k for k in ggraph_nb if nx.is_connected(k)]
  for k in range(len(ggraph_nb)):
    if list(ggraph_nb[k].nodes())[0] == 2:
      ggraph_nb[k] = nx.relabel_nodes(ggraph_nb[k], {j:j-2 for j in list(ggraph_nb[k].nodes())})
    if any([j not in list(ggraph_nb[k].nodes()) for j in range(len(list(ggraph_nb[k].nodes())))]):
      which = np.min(np.where([j not in list(ggraph_nb[k].nodes()) for j in range(len(list(ggraph_nb[k].nodes())))])[0].tolist())
      diff = len(list(ggraph_nb[k].nodes()))-which
      current_nodes = list(ggraph_nb[k].nodes())
      ggraph_nb[k] = nx.relabel_nodes(ggraph_nb[k], {current_nodes[m]:current_nodes[m]-diff for m in range(which, len(current_nodes))})
  #ggraph_nb = [j for j in ggraph_nb if sum([nx.is_isomorphic(j, i, node_match = nx.algorithms.isomorphism.categorical_node_match('labels', len(libr))) for i in ggraph_nb]) <= 1]
  return ggraph_nb

def get_virtual_nodes(glycan, libr = None, reducing_end = ['Glc', 'GlcNAc']):
  """find unobserved biosynthetic precursors of a glycan\n
  | Arguments:
  | :-
  | glycan (string): glycan in IUPAC-condensed format
  | libr (list): library of monosaccharides; if you have one use it, otherwise a comprehensive lib will be used
  | reducing_end (list): monosaccharides at the reducing end that are allowed; default:['Glc','GlcNAc']\n
  | Returns:
  | :-
  | (1) list of virtual node graphs
  | (2) list of virtual nodes in IUPAC-condensed format
  """
  if libr is None:
    libr = lib
  try:
    ggraph = glycan_to_nxGraph(glycan, libr = libr)
  except:
    return [], []
  ggraph_nb = create_neighbors(ggraph, libr = libr)
  ggraph_nb_t = []
  for k in ggraph_nb:
    try:
      ggraph_nb_t.append(graph_to_string(k, libr = libr))
    except:
      pass
  ggraph_nb = []
  for k in list(set(ggraph_nb_t)):
    try:
      ggraph_nb.append(glycan_to_nxGraph(k, libr = libr))
    except:
      pass
  ggraph_nb_t = [graph_to_string(k,libr = libr) for k in ggraph_nb]
  ggraph_nb_t = [k if k[0] != '[' else k.replace('[','',1).replace(']','',1) for k in ggraph_nb_t]
  
  ggraph_nb_t = [k for k in ggraph_nb_t if any([k[-len(j):] == j for j in reducing_end])]
  ggraph_nb = [glycan_to_nxGraph(k, libr = libr) for k in ggraph_nb_t]
  diffs = [find_diff(glycan, k, libr = libr) for k in ggraph_nb_t]
  idx = [k for k in range(len(ggraph_nb_t)) if ggraph_nb_t[k][0] != '(']
  return [ggraph_nb[i] for i in idx], [ggraph_nb_t[i] for i in idx]
  
def propagate_virtuals(glycans, libr = None, reducing_end = ['Glc', 'GlcNAc']):
  """do one step of virtual node generation\n
  | Arguments:
  | :-
  | glycans (list): list of glycans in IUPAC-condensed format
  | libr (list): library of monosaccharides; if you have one use it, otherwise a comprehensive lib will be used
  | reducing_end (list): monosaccharides at the reducing end that are allowed; default:['Glc','GlcNAc']\n
  | Returns:
  | :-
  | (1) list of virtual node graphs
  | (2) list of virtual nodes in IUPAC-condensed format
  """
  if libr is None:
    libr = lib
  virtuals = [get_virtual_nodes(k, libr = libr, reducing_end = reducing_end) for k in glycans if k.count('(')>1]
  virtuals_t = [k[1] for k in virtuals]
  virtuals = [k[0] for k in virtuals]
  return virtuals, virtuals_t

def shells_to_edges(prev_shell, next_shell):
  """map virtual node generations to edges\n
  | Arguments:
  | :-
  | prev_shell (list): virtual node generation from previous run of propagate_virtuals
  | next_shell (list): virtual node generation from next run of propagate_virtuals\n
  | Returns:
  | :-
  | Returns mapped edges between two virtual node generations
  """
  edges_out = []
  for m in range(len(prev_shell)):
    edges_out.append(unwrap([[(prev_shell[m][k], next_shell[k][j]) for j in range(len(next_shell[k]))] for k in range(len(prev_shell[m]))]))
  return edges_out


def find_path(glycan_a, glycan_b, libr = None, reducing_end = ['Glc', 'GlcNAc'],
              limit = 5):
  """find virtual node path between two glycans\n
  | Arguments:
  | :-
  | glycan_a (string): glycan in IUPAC-condensed format
  | glycan_b (string): glycan in IUPAC-condensed format
  | libr (list): library of monosaccharides; if you have one use it, otherwise a comprehensive lib will be used
  | reducing_end (list): monosaccharides at the reducing end that are allowed; default:['Glc','GlcNAc']
  | limit (int): maximum number of virtual nodes between observed nodes; default:5\n
  | Returns:
  | :-
  | (1) list of edges to connect glycan_a and glycan_b via virtual nodes
  | (2) dictionary of edge labels detailing difference between two connected nodes
  """
  if libr is None:
    libr = lib
  virtual_shells_t = []
  true_nodes = [glycan_a, glycan_b]
  smaller_glycan = true_nodes[np.argmin([len(j) for j in true_nodes])]
  larger_glycan = true_nodes[np.argmax([len(j) for j in true_nodes])]
  virtual_shells = [glycan_to_nxGraph(larger_glycan, libr = libr)]
  virtual_shells_t = [[[larger_glycan]]]
  virtuals, virtuals_t = propagate_virtuals([larger_glycan], libr = libr, reducing_end = reducing_end)
  virtual_shells.append(virtuals)
  virtual_shells_t.append(virtuals_t)
  county = 0
  while ((not any([fast_compare_glycans(glycan_to_nxGraph(smaller_glycan, libr = libr), k) for k in unwrap(virtuals)])) and (county < limit)):
    virtuals, virtuals_t = propagate_virtuals(unwrap(virtuals_t), libr = libr, reducing_end = reducing_end)
    virtual_shells.append(virtuals)
    virtual_shells_t.append(virtuals_t)
    county += 1
  virtual_edges = unwrap([unwrap(shells_to_edges(virtual_shells_t[k], virtual_shells_t[k+1])) for k in range(len(virtual_shells_t)-1)])
  edge_labels = {}
  for el in virtual_edges:
    try:
      edge_labels[el] = find_diff(el[0], el[1], libr = libr)
    except:
      pass
  return virtual_edges, edge_labels

def make_network_from_edges(edges, edge_labels = None):
  """converts edge list to network\n
  | Arguments:
  | :-
  | edges (list): list of edges
  | edge_labels (dict): dictionary of edge labels (optional)\n
  | Returns:
  | :-
  | Returns networkx object
  """
  network = nx.from_edgelist(edges)
  if edge_labels is not None:
    nx.set_edge_attributes(network, edge_labels, 'diffs')
  return network

def find_shortest_path(goal_glycan, glycan_list, libr = None, reducing_end = ['Glc','GlcNAc'],
                       limit = 5):
  """finds the glycan with the shortest path via virtual nodes to the goal glycan\n
  | Arguments:
  | :-
  | goal_glycan (string): glycan in IUPAC-condensed format
  | glycan_list (list): list of glycans in IUPAC-condensed format
  | libr (list): library of monosaccharides; if you have one use it, otherwise a comprehensive lib will be used
  | reducing_end (list): monosaccharides at the reducing end that are allowed; default:['Glc','GlcNAc']
  | limit (int): maximum number of virtual nodes between observed nodes; default:5\n
  | Returns:
  | :-
  | (1) list of edges of shortest path to connect goal_glycan and glycan via virtual nodes
  | (2) dictionary of edge labels detailing difference between two connected nodes in shortest path
  """
  if libr is None:
    libr = lib
  path_lengths = []
  for k in glycan_list:
    if subgraph_isomorphism(goal_glycan, k, libr = libr) and goal_glycan[-3:] == k[-3:]:
      virtual_edges, edge_labels = find_path(goal_glycan, k, libr = libr,
                                                              reducing_end = reducing_end,
                                                               limit = limit)
      network = make_network_from_edges(virtual_edges)
      if k in list(network.nodes()) and goal_glycan in list(network.nodes()):
        path_lengths.append(len(nx.algorithms.shortest_paths.generic.shortest_path(network, source = k, target = goal_glycan)))
      else:
        path_lengths.append(99)
    else:
      path_lengths.append(99)
  idx = np.argmin(path_lengths)
  virtual_edges, edge_labels = find_path(goal_glycan, glycan_list[idx], libr = libr,
                                                             reducing_end = reducing_end,
                                                           limit = limit)
  return virtual_edges, edge_labels

def get_unconnected_nodes(network, glycan_list):
  """find nodes that are currently unconnected\n
  | Arguments:
  | :-
  | network (networkx object): biosynthetic network from construct_network
  | glycan_list (list): list of glycans in IUPAC-condensed format\n
  | Returns:
  | :-
  | Returns list of unconnected nodes
  """
  connected_nodes = list(network.edges())
  connected_nodes = list(sum(connected_nodes, ()))
  unconnected = [k for k in glycan_list if k not in connected_nodes]
  return unconnected

def network_alignment(network_a, network_b):
  """combines two networks into a new network
  | Arguments:
  | :-
  | network_a (networkx object): biosynthetic network from construct_network
  | network_b (networkx object): biosynthetic network from construct_network\n
  | Returns:
  | :-
  | Returns combined network as a networkx object
  """
  U = nx.Graph()
  all_nodes = list(network_a.nodes(data = True)) + list(network_b.nodes(data = True))
  network_a_nodes = [k[0] for k in list(network_a.nodes(data = True))]
  network_b_nodes =  [k[0] for k in list(network_b.nodes(data = True))]
  node_origin = ['cornflowerblue' if (k[0] in network_a_nodes and k[0] not in network_b_nodes) \
            else 'darkorange' if (k[0] in network_b_nodes and k[0] not in network_a_nodes) else 'saddlebrown' for k in all_nodes]
  U.add_nodes_from(all_nodes)
  U.add_edges_from(list(network_a.edges(data = True))+list(network_b.edges(data = True)))
  nx.set_node_attributes(U, {all_nodes[k][0]:node_origin[k] for k in range(len(all_nodes))}, name = 'origin')
  return U

def infer_virtual_nodes(network_a, network_b, combined = None):
  """identifies virtual nodes that have been observed in other species\n
  | Arguments:
  | :-
  | network_a (networkx object): biosynthetic network from construct_network
  | network_b (networkx object): biosynthetic network from construct_network
  | combined (networkx object): merged network of network_a and network_b from network_alignment; default:None\n
  | Returns:
  | :-
  | (1) tuple of (virtual nodes of network_a observed in network_b, virtual nodes occurring in both network_a and network_b)
  | (2) tuple of (virtual nodes of network_b observed in network_a, virtual nodes occurring in both network_a and network_b)
  """
  if combined is None:
    combined = network_alignment(network_a, network_b)
  a_nodes = list(network_a.nodes())
  b_nodes = list(network_b.nodes())
  supported_a = [k for k in a_nodes if nx.get_node_attributes(network_a, 'virtual')[k] == 1 and k in list(network_b.nodes())]
  supported_a = [k for k in supported_a if nx.get_node_attributes(network_b, 'virtual')[k] == 1]
  supported_b = [k for k in b_nodes if nx.get_node_attributes(network_b, 'virtual')[k] == 1 and k in list(network_a.nodes())]
  supported_b = [k for k in supported_b if nx.get_node_attributes(network_a, 'virtual')[k] == 1]
  inferred_a = [k for k in a_nodes if nx.get_node_attributes(network_a, 'virtual')[k] == 1 and nx.get_node_attributes(combined, 'virtual')[k] == 0]
  inferred_b = [k for k in b_nodes if nx.get_node_attributes(network_b, 'virtual')[k] == 1 and nx.get_node_attributes(combined, 'virtual')[k] == 0]
  return (inferred_a, supported_a), (inferred_b, supported_b)

def filter_disregard(network):
  """filters out mistaken edges\n
  | Arguments:
  | :-
  | network (networkx object): biosynthetic network from construct_network
  | Returns:
  | :-
  | Returns network without mistaken edges
  """
  for k in list(network.edges()):
    if nx.get_edge_attributes(network, 'diffs')[k] == 'disregard':
      network.remove_edge(k[0], k[1])
  return network

def infer_network(network, network_species, species_list, filepath = None, df = None,
                  add_virtual_nodes = 'exhaustive',
                  libr = None, reducing_end = ['Glc', 'GlcNAc'], limit = 5):
  """replaces virtual nodes if they are observed in other species\n
  | Arguments:
  | :-
  | network (networkx object): biosynthetic network that should be inferred
  | network_species (string): species from which the network stems
  | species_list (list): list of species to compare network to
  | filepath (string): filepath to load biosynthetic networks from other species, if precalculated (def. recommended, as calculation will take ~1.5 hours); default:None
  | df (dataframe): dataframe containing species-specific glycans, only needed if filepath=None;default:None
  | add_virtual_nodes (string): indicates whether no ('None'), proximal ('simple'), or all ('exhaustive') virtual nodes should be added;only needed if filepath=None;default:'exhaustive'
  | libr (list): library of monosaccharides; if you have one use it, otherwise a comprehensive lib will be used;only needed if filepath=None
  | reducing_end (list): monosaccharides at the reducing end that are allowed;only needed if filepath=None;default:['Glc','GlcNAc']
  | limit (int): maximum number of virtual nodes between observed nodes;only needed if filepath=None;default:5\n
  | Returns:
  | :-
  | Returns network with filled in virtual nodes
  """
  if libr is None:
    libr = lib
  inferences = []
  for k in species_list:
    if k != network_species:
      if filepath is None:
        temp_network = construct_network(df[df.Species == k].target.values.tolist(), add_virtual_nodes = add_virtual_nodes, libr = libr,
                                         reducing_end = reducing_end, limit = limit)
      else:
        temp_network = nx.read_gpickle(filepath + k + '_graph_exhaustive.pkl')
      temp_network = filter_disregard(temp_network)
      infer_network, infer_other = infer_virtual_nodes(network, temp_network)
      inferences.append(infer_network)
  network2 = network.copy()
  upd = {j:2 for j in list(set(unwrap([k[0] for k in inferences])))}
  nx.set_node_attributes(network2, upd, 'virtual')
  return network2

def retrieve_inferred_nodes(network, species = None):
  """returns the inferred virtual nodes of a network that has been used with infer_network\n
  | Arguments:
  | :-
  | network (networkx object): biosynthetic network with inferred virtual nodes
  | species (string): species from which the network stems (only relevant if multiple species in network); default:None\n
  | Returns:
  | :-
  | Returns inferred nodes as list or dictionary (if species argument is used)
  """
  inferred_nodes = nx.get_node_attributes(network, 'virtual')
  inferred_nodes = [k for k in list(inferred_nodes.keys()) if inferred_nodes[k] == 2]
  if species is None:
    return inferred_nodes
  else:
    return {species:inferred_nodes}
