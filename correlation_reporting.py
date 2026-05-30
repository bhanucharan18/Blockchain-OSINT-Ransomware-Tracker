import networkx as nx
import matplotlib.pyplot as plt
import json


def correlate_darkweb(wallet):
    hits = {
        "13AM4VW2dhxYgXeQepoHkHSQuy6NgaEb94":
        "Mentioned in ransomware forum (2024)"
    }
    return hits.get(wallet, "No dark web data")


def visualize(wallet, related):
    G = nx.DiGraph()
    G.add_node(wallet, color="red")

    for w in related:
        G.add_edge(wallet, w)

    colors = [G.nodes[n].get("color", "skyblue") for n in G.nodes]
    nx.draw(G, with_labels=True, node_color=colors)
    plt.show()


def export_report(wallet, data):
    with open(f"{wallet}_report.json", "w") as f:
        json.dump(data, f, indent=4)
