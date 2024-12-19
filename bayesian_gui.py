import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from bayesian_network import BayesianNetwork

"""
Clasa BayesianGUI se ocupa ce gestionarea aplicatiei
grafice pentru lucrul cu reteaua bayesiana.
"""
class BayesianGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bayesian Network Inference")
        self.network = None
        self.evidence = {}
        self.remaining_nodes = []

        # Top frame pentru controale
        self.control_frame = tk.Frame(root)
        self.control_frame.pack(pady=10, fill=tk.X)

        # Butoane
        self.load_button = tk.Button(self.control_frame, text="Load Network", command=self.load_network, width=15)
        self.load_button.grid(row=0, column=1, padx=5)

        self.reset_button = tk.Button(self.control_frame, text="Reset Evidence", command=self.reset_evidence,
                                      state="disabled", width=15)
        self.reset_button.grid(row=0, column=2, padx=5)

        self.delete_network_button = tk.Button(self.control_frame, text="Delete Network", command=self.delete_network,
                                               state="disabled", width=15)
        self.delete_network_button.grid(row=0, column=3, padx=5)

        self.add_evidence_button = tk.Button(self.control_frame, text="Add Evidence", command=self.add_evidence,
                                             state="disabled", width=15)
        self.add_evidence_button.grid(row=1, column=3, padx=5, pady=5)

        self.query_button = tk.Button(self.control_frame, text="Query", command=self.query_network,
                                      state="disabled", width=15)
        self.query_button.grid(row=2, column=2, padx=5, pady=5)

        self.pe_query_button = tk.Button(self.control_frame, text="P(e) Query", command=self.pe_query,
                                         state="disabled", width=15)
        self.pe_query_button.grid(row=2, column=3, padx=5, pady=5)

        # Dropdown pentru evidente
        self.evidence_label = tk.Label(self.control_frame, text="Set Evidence:")
        self.evidence_label.grid(row=1, column=0, padx=5, pady=5)

        self.evidence_node_var = tk.StringVar()
        self.evidence_node_dropdown = ttk.Combobox(self.control_frame, textvariable=self.evidence_node_var, state="disabled", width=20)
        self.evidence_node_dropdown.grid(row=1, column=1, padx=5, pady=5)
        self.evidence_node_dropdown.bind("<<ComboboxSelected>>", self.update_value_dropdown)

        # Dropdown pentru valorile nodului evidenta
        self.evidence_value_var = tk.StringVar()
        self.evidence_value_dropdown = ttk.Combobox(self.control_frame, textvariable=self.evidence_value_var, state="disabled", width=20)
        self.evidence_value_dropdown.grid(row=1, column=2, padx=5, pady=5)

        # Dropdown pentru query
        self.query_label = tk.Label(self.control_frame, text="Query Node:")
        self.query_label.grid(row=2, column=0, padx=5, pady=5)

        self.query_node_var = tk.StringVar()
        self.query_node_dropdown = ttk.Combobox(self.control_frame, textvariable=self.query_node_var, state="disabled", width=20)
        self.query_node_dropdown.grid(row=2, column=1, padx=5, pady=5)

        # Text Box pentru evidente
        self.evidence_display_label = tk.Label(root, text="Evidence:")
        self.evidence_display_label.pack()

        self.evidence_display_text = tk.Text(root, height=5, width=60, state="disabled")
        self.evidence_display_text.pack(pady=10)

        # Text Box pentru rezultate
        self.result_label = tk.Label(root, text="Result:")
        self.result_label.pack()
        self.result_text = tk.Text(root, height=5, width=60, state="disabled")
        self.result_text.pack(pady=10)






    def load_network(self):
        """
        Functie care incarca o retea bayesiana dintr-un fisier JSON ales de user.
        """
        json_file = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if json_file:
            try:
                self.network = BayesianNetwork(json_file)
                self.remaining_nodes = list(self.network.network.keys())
                self.update_dropdowns()
                self.reset_button.config(state="normal")


                self.pe_query_button.config(state="normal")


                self.delete_network_button.config(state="normal")
                messagebox.showinfo("Success", "Network loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load network: {e}")

    def reset_evidence(self):
        """
        Functie care reseteaza componentele grafice pentru a testa un nou caz in retea.
        """
        self.evidence = {}
        self.remaining_nodes = list(self.network.network.keys())

        # Goleste TextBox evidente
        self.evidence_display_text.config(state="normal")
        self.evidence_display_text.delete("1.0", tk.END)
        self.evidence_display_text.config(state="disabled")

        # Goleste TextBox rezultate
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.config(state="disabled")

        # Reactualizeaza dropdown-urile
        self.evidence_node_var.set("")
        self.evidence_value_var.set("")
        self.query_node_var.set("")

        self.update_dropdowns()

    def delete_network(self):
        """
        Functie care sterge reteaua curenta si reseteaza interfata la starea initiala.
        """
        self.network = None
        self.evidence = {}
        self.remaining_nodes = []

        self.evidence_node_dropdown.config(state="disabled")
        self.evidence_value_dropdown.config(state="disabled")
        self.query_node_dropdown.config(state="disabled")
        self.add_evidence_button.config(state="disabled")
        self.query_button.config(state="disabled")
        self.reset_button.config(state="disabled")
        self.delete_network_button.config(state="disabled")

        self.query_node_dropdown.set("")
        self.evidence_value_dropdown.set("")
        self.evidence_node_dropdown.set("")

        self.evidence_display_text.config(state="normal")
        self.evidence_display_text.delete("1.0", tk.END)
        self.evidence_display_text.config(state="disabled")

        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.config(state="disabled")

        messagebox.showinfo("Network Deleted", "The current network has been deleted. Please load a new network.")

    def update_dropdowns(self):
        """
        Functie care actualizeaza dropdown-urile pentru evidente si query.
        """
        if len(self.remaining_nodes) > 1:
            # pentru nodurile evidenta
            self.evidence_node_dropdown["values"] = self.remaining_nodes
            self.evidence_node_dropdown.config(state="readonly")

            # pentru nodurile query
            self.query_node_dropdown["values"] = self.remaining_nodes
            self.query_node_dropdown.config(state="readonly")
            self.query_button.config(state="normal")
        else:
            # se pastreaza cel putin un nod pentru query
            self.evidence_node_dropdown.config(state="disabled")
            self.query_node_dropdown["values"] = self.remaining_nodes
            self.query_node_dropdown.config(state="readonly")

    def update_value_dropdown(self, event):
        """
        Functie care actualizeaza dropdown-ul pentru valorile evidentelor.
        """
        selected_node = self.evidence_node_dropdown.get()
        probabilities = self.network.network[selected_node]["probabilities"]

        # extrag valorile posibile din chei
        if isinstance(probabilities, dict):
            first_key = next(iter(probabilities))
            if isinstance(probabilities[first_key], dict):
                possible_values = list(probabilities[first_key].keys())
            else:
                possible_values = list(probabilities.keys())
        else:
            possible_values = []

        # actualizez dropdown-ul
        self.evidence_value_dropdown["values"] = possible_values
        self.evidence_value_dropdown.config(state="readonly")

        # activez butonul pentru setarea evidentei
        self.add_evidence_button.config(state="normal")

    def add_evidence(self):
        """
        Functie care adauga o evidenta bazata pe valorile alese de user.
        """
        selected_node = self.evidence_node_var.get()
        selected_value = self.evidence_value_var.get()

        if selected_node and selected_value:
            self.evidence[selected_node] = selected_value
            self.remaining_nodes.remove(selected_node)
            self.update_dropdowns()

            # actualizare evidente in Text box
            self.update_evidence_display()

            self.evidence_value_dropdown.set("")
            self.evidence_node_dropdown.set("")
            self.query_node_dropdown.set("")
            self.add_evidence_button.config(state="disabled")
            self.evidence_value_dropdown.config(state="disabled")

            if len(self.remaining_nodes) <= 1:
                self.evidence_node_dropdown.config(state="disabled")
                self.add_evidence_button.config(state="disabled")
                messagebox.showinfo("Info", "All remaining nodes are reserved for query.")

    def update_evidence_display(self):
        """
        Fucntie care actualizeaza Textbox-ul cu evidentele curente.
        """
        evidence_text = "Selected evidence:\n"
        for node, value in self.evidence.items():
            evidence_text += f"{node}: {value}\n"

        self.evidence_display_text.config(state="normal")
        self.evidence_display_text.delete("1.0", tk.END)
        self.evidence_display_text.insert(tk.END, evidence_text)
        self.evidence_display_text.config(state="disabled")

    def query_network(self):
        """
        Functie care interogheaza reteaua pe baza nodului interogat si a evidentelor selectate de user.
        """
        if not self.network:
            messagebox.showwarning("Warning", "Please load a network first!")
            return

        query_node = self.query_node_var.get()
        if not query_node:
            messagebox.showerror("Error", "Please select a query node.")
            return

        try:
            self.network.set_evidence(self.evidence)
            result = self.network.enumeration_ask(query_node)

            self.result_text.config(state="normal")
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, f"Probabilities for {query_node}:\n")
            for value, prob in result.items():
                self.result_text.insert(tk.END, f"{value}: {prob}\n")
            self.result_text.config(state="disabled")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to query network: {e}")

    def pe_query(self):
        """
        Functie care interogheaza probabilitatea evidentelor curente
        """
        if not self.network:
            messagebox.showwarning("Warning", "Please load a network first!")
            return

        if not self.evidence:
            messagebox.showerror("Error", "No evidence set. Please add evidence first.")
            return

        try:
            result = self.network.p_e_query(self.evidence)
            self.result_text.config(state="normal")
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, f"P(e): {result:.4f}\n")
            self.result_text.config(state="disabled")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to compute P(e): {e}")


