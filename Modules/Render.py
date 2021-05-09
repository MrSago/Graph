
import networkx as nx
graph_test = {1:{3: 228}, 2:{4:12, 5: 512}}



def drawDefault(view, graph):
    view.figure.clf()
    adj, is_dir, weighted = graph.getFields()
    
    if (is_dir):
        G = nx.DiGraph()
    else:
        G = nx.Graph()

    for i in adj:
        for j in adj[i]:
            G.add_edge(i, j, weight=adj[i][j])

    pos = nx.kamada_kawai_layout(G)

    nx.draw(G, pos=pos, with_labels=True, node_color='#003473', font_color='white', font_weight='bold', alpha=0.9)
    nx.draw_networkx_edge_labels(G, pos=pos, font_color='black', font_weight=700,
                                edge_labels=nx.get_edge_attributes(G, 'weight'))
    nx.draw_networkx_edges(G, pos=pos, width=2, edge_color='#750000')

    view.canvas.draw()


def drawMinPath():
    pass


def drawColoring():
    pass


def chooseDrawType(graphctrl):
    algo = graphctrl._view.comboBoxAlgo.currentText()
    if algo == "Default":
        drawDefault(graphctrl._view, graphctrl._model.graph)
    elif algo == "Min Path Finding":
        pass
    elif algo == "Coloring":
        pass
