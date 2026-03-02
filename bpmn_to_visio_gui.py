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
        self.selected_files = []

        container = tk.Frame(root, padx=14, pady=14)
        container.pack(fill="both", expand=True)

        title = tk.Label(
            container, text="BPMN to Visio Converter", font=("Segoe UI", 11, "bold")
        )
        title.grid(row=0, column=0, columnspan=3, sticky="w")

        file_label = tk.Label(container, text="Input .bpmn file(s):")
        file_label.grid(row=1, column=0, columnspan=3, pady=(12, 6), sticky="w")

        file_entry = tk.Entry(container, textvariable=self.selected_file, width=58)
        file_entry.grid(row=2, column=0, columnspan=2, sticky="we")

        browse_button = tk.Button(
            container, text="Browse...", width=12, command=self.browse_file
        )
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
        selected = filedialog.askopenfilenames(
            title="Select BPMN file(s)",
            filetypes=[("BPMN files", "*.bpmn"), ("All files", "*.*")],
        )
        if selected:
            self.selected_files = [Path(path) for path in selected]
            if len(self.selected_files) == 1:
                self.selected_file.set(str(self.selected_files[0]))
            else:
                first = str(self.selected_files[0])
                self.selected_file.set(
                    f"{first} (+{len(self.selected_files) - 1} more)"
                )
            self.update_convert_state()

    def on_file_text_changed(self, _event):
        self.selected_files = []
        self.update_convert_state()

    def update_convert_state(self):
        if self.selected_files:
            is_valid = all(
                bpmn_path.is_file() and bpmn_path.suffix.lower() == ".bpmn"
                for bpmn_path in self.selected_files
            )
        else:
            file_path = self.selected_file.get().strip()
            is_valid = (
                bool(file_path)
                and Path(file_path).is_file()
                and file_path.lower().endswith(".bpmn")
            )
        self.convert_button.config(state="normal" if is_valid else "disabled")

    def convert_selected(self):
        if self.selected_files:
            bpmn_paths = self.selected_files
        else:
            bpmn_path = Path(self.selected_file.get().strip())
            if not bpmn_path.is_file() or bpmn_path.suffix.lower() != ".bpmn":
                messagebox.showerror(
                    "Invalid file", "Please select a valid .bpmn file."
                )
                self.update_convert_state()
                return
            bpmn_paths = [bpmn_path]

        self.root.config(cursor="watch")
        self.convert_button.config(state="disabled")
        self.root.update_idletasks()

        try:
            success_paths = []
            failed_paths = []

            for bpmn_path in bpmn_paths:
                output_path = bpmn_path.with_suffix(".vsdx")
                success = convert_file(str(bpmn_path), None)
                if success and output_path.exists():
                    success_paths.append(output_path)
                else:
                    failed_paths.append(bpmn_path)

            if failed_paths:
                failed_names = "\n".join(str(path.name) for path in failed_paths[:8])
                extra = ""
                if len(failed_paths) > 8:
                    extra = f"\n...and {len(failed_paths) - 8} more"
                messagebox.showinfo(
                    "Conversion finished",
                    (
                        f"Converted: {len(success_paths)}\n"
                        f"Failed: {len(failed_paths)}\n\n"
                        f"Failed files:\n{failed_names}{extra}"
                    ),
                )
            else:
                if len(success_paths) == 1:
                    messagebox.showinfo(
                        "Done", f"Conversion successful.\n\nOutput:\n{success_paths[0]}"
                    )
                else:
                    messagebox.showinfo(
                        "Done",
                        (
                            f"Conversion successful for {len(success_paths)} files.\n\n"
                            f"Output files are saved next to each input BPMN file."
                        ),
                    )
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
