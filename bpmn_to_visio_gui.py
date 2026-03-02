import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox

from bpmn_to_vsdx import convert_file


class BpmnToVisioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BPMN to Visio")
        self.root.resizable(False, False)

        self.selected_file = tk.StringVar()

        container = tk.Frame(root, padx=14, pady=14)
        container.pack(fill="both", expand=True)

        title = tk.Label(container, text="BPMN to Visio Converter", font=("Segoe UI", 11, "bold"))
        title.grid(row=0, column=0, columnspan=3, sticky="w")

        file_label = tk.Label(container, text="Input .bpmn file:")
        file_label.grid(row=1, column=0, columnspan=3, pady=(12, 6), sticky="w")

        file_entry = tk.Entry(container, textvariable=self.selected_file, width=58)
        file_entry.grid(row=2, column=0, columnspan=2, sticky="we")

        browse_button = tk.Button(container, text="Browse...", width=12, command=self.browse_file)
        browse_button.grid(row=2, column=2, padx=(8, 0), sticky="e")

        self.convert_button = tk.Button(
            container,
            text="Convert",
            width=12,
            state="disabled",
            command=self.convert_selected,
        )
        self.convert_button.grid(row=3, column=2, pady=(12, 0), sticky="e")

        file_entry.bind("<KeyRelease>", self.on_file_text_changed)

    def browse_file(self):
        selected = filedialog.askopenfilename(
            title="Select BPMN file",
            filetypes=[("BPMN files", "*.bpmn"), ("All files", "*.*")],
        )
        if selected:
            self.selected_file.set(selected)
            self.update_convert_state()

    def on_file_text_changed(self, _event):
        self.update_convert_state()

    def update_convert_state(self):
        file_path = self.selected_file.get().strip()
        is_valid = bool(file_path) and Path(file_path).is_file() and file_path.lower().endswith(".bpmn")
        self.convert_button.config(state="normal" if is_valid else "disabled")

    def convert_selected(self):
        bpmn_path = Path(self.selected_file.get().strip())

        if not bpmn_path.is_file() or bpmn_path.suffix.lower() != ".bpmn":
            messagebox.showerror("Invalid file", "Please select a valid .bpmn file.")
            self.update_convert_state()
            return

        output_path = bpmn_path.with_suffix(".vsdx")
        self.root.config(cursor="watch")
        self.convert_button.config(state="disabled")
        self.root.update_idletasks()

        try:
            success = convert_file(str(bpmn_path), None)
            if success and output_path.exists():
                messagebox.showinfo("Done", f"Conversion successful.\n\nOutput:\n{output_path}")
            else:
                messagebox.showerror("Conversion failed", "Could not convert the selected BPMN file.")
        except Exception as exc:
            messagebox.showerror("Error", f"Unexpected error:\n{exc}")
        finally:
            self.root.config(cursor="")
            self.update_convert_state()


def main():
    root = tk.Tk()
    BpmnToVisioApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()