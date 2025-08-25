import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from core.analysis import StudentPerformanceAnalyzer
from core.visuals import plot_subject_averages, plot_distribution, plot_grade_distribution


class StudentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📊 Student Performance Analyzer")
        self.root.geometry("1000x650")

        # Apply ttk theme
        style = ttk.Style()
        style.theme_use("clam")

        # Main layout
        main_frame = tk.Frame(root)
        main_frame.pack(fill="both", expand=True)

        # Sidebar (menu)
        left_frame = tk.Frame(main_frame, bg="#2c3e50", width=200)
        left_frame.pack(side="left", fill="y")

        # Right content area
        right_frame = tk.Frame(main_frame, bg="white")
        right_frame.pack(side="right", fill="both", expand=True)

        # Sidebar buttons
        button_cfg = {
            "bg": "#34495e",
            "fg": "white",
            "font": ("Arial", 12),
            "relief": "flat",
            "width": 20,
            "pady": 5
        }
        tk.Button(left_frame, text="📂 Upload CSV", command=self.load_file, **button_cfg).pack(pady=10)
        tk.Button(left_frame, text="📊 Show Averages", command=self.show_averages, **button_cfg).pack(pady=5)
        tk.Button(left_frame, text="🏆 Top Performers", command=self.show_top, **button_cfg).pack(pady=5)
        tk.Button(left_frame, text="📈 Subject Averages", command=self.plot_averages, **button_cfg).pack(pady=5)
        tk.Button(left_frame, text="📊 Subject Distribution", command=self.ask_subject, **button_cfg).pack(pady=5)
        tk.Button(left_frame, text="🎯 Grade Breakdown", command=self.plot_grades, **button_cfg).pack(pady=5)

        # Notebook (tabs)
        self.notebook = ttk.Notebook(right_frame)
        self.notebook.pack(fill="both", expand=True)

        self.table_frame = tk.Frame(self.notebook, bg="white")
        self.chart_frame = tk.Frame(self.notebook, bg="white")

        self.notebook.add(self.table_frame, text="📑 Data Table")
        self.notebook.add(self.chart_frame, text="📉 Charts")

        # Placeholder for analyzer
        self.analyzer = None
        self.current_chart = None

    # ---------------- CSV Loader ----------------
    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.analyzer = StudentPerformanceAnalyzer(file_path)
            self.analyzer.clean_data()
            messagebox.showinfo("Success", "CSV Loaded Successfully!")

    # ---------------- Table Display ----------------
    def render_table(self, columns, rows):
        # Clear old widgets
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        tree = ttk.Treeview(self.table_frame, columns=columns, show="headings")

        # Scrollbars
        vsb = ttk.Scrollbar(self.table_frame, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(self.table_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        self.table_frame.grid_rowconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)

        # Add columns
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")

        # Add rows
        for row in rows:
            tree.insert("", "end", values=row)

        self.notebook.select(self.table_frame)

    def show_averages(self):
        if not self.analyzer:
            return
        averages = self.analyzer.subject_averages()
        rows = [(subject, round(avg, 2)) for subject, avg in averages.items()]
        self.render_table(["Subject", "Average"], rows)

    def show_top(self):
        if not self.analyzer:
            return
        top_students = self.analyzer.top_performers()
        rows = [list(row) for _, row in top_students.iterrows()]
        self.render_table(list(top_students.columns), rows)

    # ---------------- Chart Display ----------------
    def render_chart(self, fig):
        # Clear old chart
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        self.notebook.select(self.chart_frame)

    def plot_averages(self):
        if not self.analyzer:
            return
        fig = plot_subject_averages(self.analyzer.data, return_fig=True)
        self.render_chart(fig)

    def ask_subject(self):
        if not self.analyzer:
            return

        popup = tk.Toplevel(self.root)
        popup.title("Choose Subject")
        tk.Label(popup, text="Enter Subject Name:").pack(pady=5)

        entry = tk.Entry(popup)
        entry.pack(pady=5)

        def submit():
            subject = entry.get().strip()
            if subject in self.analyzer.data.columns:
                fig = plot_distribution(self.analyzer.data, subject=subject, return_fig=True)
                self.render_chart(fig)
                popup.destroy()
            else:
                messagebox.showerror("Error", f"Subject '{subject}' not found!")

        tk.Button(popup, text="Plot", command=submit).pack(pady=5)

    def plot_grades(self):
        if not self.analyzer:
            return
        self.analyzer.grade_distribution()
        fig = plot_grade_distribution(self.analyzer.data, return_fig=True)
        self.render_chart(fig)


if __name__ == "__main__":
    root = tk.Tk()
    app = StudentApp(root)
    root.mainloop()
