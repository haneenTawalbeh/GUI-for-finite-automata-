import tkinter as tk
from tkinter import ttk
import os
from automata.fa.nfa import NFA
from automata.fa.dfa import DFA
from graphviz import Digraph
from tkinter import PhotoImage


class AutomataGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Regex to DFA/NFA")

        tk.Label(root, text="Enter Regex:").pack(pady=5)

        self.regex_entry = tk.Entry(root, width=40)
        self.regex_entry.pack(pady=5)

        ttk.Button(
            root,
            text="Generate NFA",
            command=self.generate_nfa
        ).pack(pady=5)

        ttk.Button(
            root,
            text="Generate DFA",
            command=self.generate_dfa
        ).pack(pady=5)

        self.image_label = tk.Label(root)
        self.image_label.pack(pady=10)

    def show_image(self, filename):
        # Tkinter native PNG support
        self.img = PhotoImage(file=filename)
        self.image_label.config(image=self.img)

    def build_nfa_graph(self, nfa):
        dot = Digraph()
        dot.attr(rankdir="LR")

        dot.node("", shape="none")
        dot.edge("", str(nfa.initial_state))

        for state in nfa.states:
            shape = "doublecircle" if state in nfa.final_states else "circle"
            dot.node(str(state), shape=shape)

        for state, transitions in nfa.transitions.items():
            for symbol, destinations in transitions.items():
                for dest in destinations:
                    label = symbol if symbol else "ε"
                    dot.edge(str(state), str(dest), label=label)

        return dot

    def build_dfa_graph(self, dfa):
        dot = Digraph()
        dot.attr(rankdir="LR")

        dot.node("", shape="none")
        dot.edge("", str(dfa.initial_state))

        for state in dfa.states:
            shape = "doublecircle" if state in dfa.final_states else "circle"
            dot.node(str(state), shape=shape)

        for state, transitions in dfa.transitions.items():
            for symbol, dest in transitions.items():
                dot.edge(str(state), str(dest), label=symbol)

        return dot

    def generate_nfa(self):
        regex = self.regex_entry.get()

        nfa = NFA.from_regex(regex)
        dot = self.build_nfa_graph(nfa)

        filename = "nfa_graph"
        dot.render(filename, format="png", cleanup=True)

        self.show_image(filename + ".png")

    def generate_dfa(self):
        regex = self.regex_entry.get()

        nfa = NFA.from_regex(regex)
        dfa = DFA.from_nfa(nfa)

        dot = self.build_dfa_graph(dfa)

        filename = "dfa_graph"
        dot.render(filename, format="png", cleanup=True)

        self.show_image(filename + ".png")


root = tk.Tk()
root.geometry("900x700")

app = AutomataGUI(root)

root.mainloop()
