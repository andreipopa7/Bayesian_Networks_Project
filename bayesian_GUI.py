import tkinter as tk
from tkinter import filedialog, messagebox
from bayesian_network import BayesianNetwork

class BayesianGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bayesian Network")
        self.network = None
        self.evidence = {}

        self.control_frame = tk.Frame(root)
        self.control_frame.pack(pady=10, fill=tk.X)

        self.load_button = tk.Button(self.control_frame, text="Load Network", command=self.load_network)
        self.load_button.grid(row=0, column=0, padx=5)

        self.nodes_label = tk.Label(root, text="Nodes in Network:")
        self.nodes_label.pack()
        self.nodes_text = tk.Text(root, height=10, width=60, state="disabled")
        self.nodes_text.pack(pady=10)

        self.evidence_label = tk.Label(root, text="Set Evidence (format: Node:Value, ...):")
        self.evidence_label.pack()
        self.evidence_entry = tk.Entry(root, width=50)
        self.evidence_entry.pack(pady=5)

        self.add_evidence_button = tk.Button(root, text="Add Evidence", command=self.add_evidence, state="disabled")
        self.add_evidence_button.pack(pady=5)

        self.query_label = tk.Label(root, text="Query Node:")
        self.query_label.pack()
        self.query_entry = tk.Entry(root, width=50)
        self.query_entry.pack(pady=5)

        self.query_button = tk.Button(root, text="Query", command=self.query_network, state="disabled")
        self.query_button.pack(pady=5)

        self.result_label = tk.Label(root, text="Result:")
        self.result_label.pack()
        self.result_text = tk.Text(root, height=5, width=60, state="disabled")
        self.result_text.pack(pady=10)

    def load_network(self):
        """
        functia aceasta incarca o retea B. dintr-un fisier JSON ales de utilizator
        """
        json_file = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if json_file:
            try:
                self.network = BayesianNetwork(json_file)
                self.update_nodes_display()
                self.add_evidence_button.config(state="normal")
                self.query_button.config(state="normal")
                messagebox.showinfo("Success", "Network loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load network: {e}")

    def update_nodes_display(self):
        """
        Afișeaz nodurile din retea in caseta specifica de text
        """
        self.nodes_text.config(state="normal")
        self.nodes_text.delete("1.0", tk.END)
        for node in self.network.network.keys():
            self.nodes_text.insert(tk.END, f"{node}\n")
        self.nodes_text.config(state="disabled")

    def add_evidence(self):
        """
        functia adauga evidentele pe baza textului introdus de utilizator
        """
        evidence_text = self.evidence_entry.get()
        if not evidence_text:
            messagebox.showwarning("Warning", "Please enter evidence in the correct format.")
            return
        try:
            evidence_pairs = evidence_text.split(",")
            for pair in evidence_pairs:
                node, value = pair.split(":")
                node, value = node.strip(), value.strip()
                if node not in self.network.network:
                    raise ValueError(f"Node '{node}' does not exist in the network.")
                self.evidence[node] = value
            messagebox.showinfo("Success", "Evidence added successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add evidence: {e}")

    def query_network(self):
        """
        Interoghez rețeaua B. pentru un nod dat
        """
        if not self.network:
            messagebox.showwarning("Warning", "Please load a network first!")
            return

        query_node = self.query_entry.get().strip()
        if not query_node:
            messagebox.showerror("Error", "Please enter a query node.")
            return
        if query_node not in self.network.network:
            messagebox.showerror("Error", f"Query node '{query_node}' does not exist in the network.")
            return

        try:
            self.network.set_evidence(self.evidence)
            result = self.network.enumeration_ask(query_node)

            # afisez rezultetele
            
            self.result_text.config(state="normal")
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, f"Probabilities for {query_node}:\n")
            for value, prob in result.items():
                self.result_text.insert(tk.END, f"{value}: {prob}\n")
            self.result_text.config(state="disabled")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to query network: {e}")