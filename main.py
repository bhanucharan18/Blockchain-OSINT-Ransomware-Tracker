import tkinter as tk
from tkinter import messagebox, scrolledtext
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import requests
import threading
import webbrowser
import os
import re

class BlockchainOSINT:
    def __init__(self, root):
        self.root = root
        self.root.title("ADVANCED BLOCKCHAIN OSINT - Supraja Technologies v4.0")
        self.root.geometry("1100x850")
        self.root.configure(bg="#1e1e1e")

        # --- UI ELEMENTS ---
        tk.Label(root, text="Target Wallet Address (BTC/ETH):", fg="white", bg="#1e1e1e", font=("Arial", 12, "bold")).pack(pady=10)
        self.address_entry = tk.Entry(root, width=65, font=("Consolas", 10))
        self.address_entry.pack(pady=5)
        self.address_entry.insert(0, "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa")

        btn_frame = tk.Frame(root, bg="#1e1e1e")
        btn_frame.pack(pady=10)
        
        self.trace_btn = tk.Button(btn_frame, text="🔍 Start AML Trace", command=self.start_thread, bg="#4CAF50", fg="white", width=20, font=("Arial", 10, "bold"))
        self.trace_btn.pack(side=tk.LEFT, padx=10)

        self.info_btn = tk.Button(btn_frame, text="ℹ️ Project Info", command=self.open_project_info, bg="#d9534f", fg="white", width=15)
        self.info_btn.pack(side=tk.LEFT, padx=10)

        self.log_area = scrolledtext.ScrolledText(root, height=10, width=120, font=("Consolas", 9), bg="#121212", fg="#00ff00")
        self.log_area.pack(pady=10, padx=20)

        # Matplotlib Visualization
        self.fig = Figure(figsize=(10, 5), facecolor='#1e1e1e')
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor('#1e1e1e')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    # --- THE MISSING LOG METHOD ---
    def log(self, msg):
        """Appends text to the GUI log area safely."""
        self.log_area.insert(tk.END, f"{msg}\n")
        self.log_area.see(tk.END)

    def detect_currency(self, address):
        if re.match(r"^(1|3|bc1)[a-zA-HJ-NP-Z0-9]{25,39}$", address):
            return "BTC"
        elif re.match(r"^0x[a-fA-F0-9]{40}$", address):
            return "ETH"
        return "Unknown"

    def check_reputation(self, address):
        if "1A1z" in address:
            return "SAFE (Genesis Block)"
        return "UNVERIFIED (High Risk)"

    def open_project_info(self):
        html_code = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Project Information</title>
            <style>
                body { font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px; }
                .container { max-width: 800px; margin: 0 auto; background: #fff; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                h1 { color: #d9534f; text-align: center; }
                table { width: 100%; border-collapse: collapse; margin-top: 20px; }
                th, td { border: 1px solid #ddd; padding: 10px; text-align: left; }
                th { background-color: #d9534f; color: white; }
                .footer { text-align: center; margin-top: 30px; font-size: 0.8em; color: #777; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Project Information</h1>
                <p>Developing <b>Blockchain OSINT Tracer</b> to map Ransomware trails and avoid Cyber Attacks.</p>
                <table>
                    <tr><th>Detail</th><th>Value</th></tr>
                    <tr><td>Project Name</td><td>Blockchain OSINT Tracker</td></tr>
                    <tr><td>Status</td><td>Completed</td></tr>
                    <tr><td>Company</td><td>Supraja Technologies</td></tr>
                </table>
                <h2>Developer Team</h2>
                <table>
                    <tr><td>Ch.Pavan</td><td>ST#IS#7470</td></tr>
                    <tr><td>Sadhupally Saivarun</td><td>ST#IS#7455</td></tr>
                    <tr><td>Dappu Bhanu Charan</td><td>ST#IS#7475</td></tr>
                    <tr><td>Vaishnavi Pratha</td><td>ST#IS#7471</td></tr>
                    <tr><td>Sai Kumar</td><td>ST#IS#7473</td></tr>

                </table>
                <div class="footer">&copy; 2025 Supraja Technologies.</div>
            </div>
        </body>
        </html>
        """
        with open("project_info.html", "w") as f:
            f.write(html_code)
        webbrowser.open('file://' + os.path.realpath("project_info.html"))

    def start_thread(self):
        address = self.address_entry.get().strip()
        if not address: return
        self.trace_btn.config(state=tk.DISABLED)
        threading.Thread(target=self.run_analysis, args=(address,), daemon=True).start()

    def run_analysis(self, address):
        self.log_area.delete('1.0', tk.END)
        coin = self.detect_currency(address)
        rep = self.check_reputation(address)
        
        self.log(f"[*] Detected Currency: {coin}")
        self.log(f"[*] AML Reputation: {rep}")
        
        try:
            if coin == "BTC":
                url = f"https://blockchain.info/rawaddr/{address}?limit=3"
            else:
                url = f"https://api.blockcypher.com/v1/eth/main/addrs/{address}"
            
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                data = r.json()
                txs = data.get('txs', []) if coin == "BTC" else []
                self.root.after(0, self.update_graph, address, txs, coin)
                self.log("[+] OSINT Trace Completed.")
                messagebox.showinfo("Trace Complete", f"Analysis for {coin} address is finished.")
            else:
                self.log("[-] Error: API could not reach ledger.")
        except Exception as e:
            self.log(f"[-] Connection Failure: {e}")
        
        self.trace_btn.config(state=tk.NORMAL)

    def update_graph(self, target_addr, transactions, coin):
        self.ax.clear()
        G = nx.DiGraph()
        labels = {}
        
        root_node = target_addr[:8] + ".."
        G.add_node(root_node)
        labels[root_node] = f"TARGET\n({coin})"

        for i, tx in enumerate(transactions[:3]):
            tx_node = f"TX_{i+1}"
            G.add_node(tx_node)
            labels[tx_node] = f"TX_{tx['hash'][:5]}"
            G.add_edge(root_node, tx_node)
            for out in tx.get('out', [])[:1]:
                if 'addr' in out:
                    recv = out['addr'][:8] + ".."
                    G.add_node(recv)
                    labels[recv] = f"RECEIVER\n{recv}"
                    G.add_edge(tx_node, recv)

        pos = nx.spring_layout(G)
        colors = ['#27ae60' if "TARGET" in labels[n] else '#f1c40f' if "TX" in labels[n] else '#e74c3c' for n in G]
        nx.draw(G, pos, ax=self.ax, node_color=colors, node_size=3000, arrowsize=20)
        nx.draw_networkx_labels(G, pos, labels=labels, font_size=8, font_color="white", ax=self.ax)
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = BlockchainOSINT(root)
    root.mainloop()