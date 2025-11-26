
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

# === CONFIG ===
excel_file = 'data.xlsx'  # <-- Local path to your Excel file
sheet_beds = '3. Link of "Profiles" to beds'
sheet_profiles = '2. Creation of "profiles"'

# === DATA ACCESS ===
def load_data():
    try:
        beds = pd.read_excel(excel_file, sheet_name=sheet_beds, engine='openpyxl')
        beds = beds.loc[:, ~beds.columns.str.contains('^Unnamed')]
        profiles = pd.read_excel(excel_file, sheet_name=sheet_profiles, engine='openpyxl')
        profiles = profiles.loc[:, ~profiles.columns.str.contains('^Unnamed')]
        profiles.columns = profiles.columns.str.strip()  # normalize headers
        print(profiles.columns)
        return beds, profiles
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load Excel file: {e}")
        return pd.DataFrame(), pd.DataFrame()

def save_data(df):
    try:
        with pd.ExcelWriter(excel_file, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            df.to_excel(writer, sheet_name=sheet_beds, index=False)
        messagebox.showinfo("Success", "Data saved successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save Excel file: {e}")

# === INIT DATA ===
df, df_profiles = load_data()

# === MAIN UI ===
root = tk.Tk()
root.title("Bed Profile Manager")
root.geometry("1000x850")

tk.Label(root, text="Bed Profile Manager", font=("Arial", 18, "bold")).pack(pady=8)

# Dropdown for existing beds
tk.Label(root, text="Select Existing Bed ID:", font=("Arial", 12)).pack()
bed_var = tk.StringVar()
bed_dropdown = ttk.Combobox(root, textvariable=bed_var, values=df['Bed ID'].astype(str).tolist(), width=20)
bed_dropdown.pack(pady=4)

# Fields for details
fields = ['Ward', 'Admission reason', 'Active conditions', 'Comorbidities', 'Predicted risks']
entries = {}
form_frame = tk.Frame(root)
form_frame.pack(pady=8)

for i, field in enumerate(fields):
    row = tk.Frame(form_frame)
    row.grid(row=i, column=0, sticky="w", pady=3)
    tk.Label(row, text=field + ":", width=18, anchor="w").pack(side="left")
    ent = tk.Entry(row, width=80)
    ent.pack(side="left")
    entries[field] = ent

# === Processing Rules Section ===
rules_frame = tk.Frame(root)
rules_frame.pack(pady=10, fill="both", expand=True)
tk.Label(rules_frame, text="Related Processing Rules:", font=("Arial", 14, "bold")).pack(anchor="w")

# Scrollable frame for grouped rules
canvas = tk.Canvas(rules_frame)
scrollbar = tk.Scrollbar(rules_frame, orient="vertical", command=canvas.yview)
rules_inner = tk.Frame(canvas)

rules_inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=rules_inner, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")


threshold_cols = [
    'low SpO2 threshold',
    'low SpO2 riemann integral threshold',
    'low HR threshold',
    'high HR threshold',
    'low ABP threshold',
    'high ABP threshold',
    'low average ABP threshold',
    'low average ABP threshold.1',
    'high MEWS score threshold',
    'high HR MEWS attribute threshold',
    'high RR MEWS attribute threshold',
    'high Temp MEWS attribute threshold',
    'high SpO2 MEWS attribute threshold',
    'high BP MEWS attribute threshold'
]

def show_processing_rules(bed_id):
    for widget in rules_inner.winfo_children():
        widget.destroy()

    if bed_id in df['Bed ID'].astype(str).values:
        row = df[df['Bed ID'].astype(str) == bed_id].iloc[0]
        for field in fields:
            value = str(row.get(field, '')).strip()
            if value:
                matches = df_profiles[
                    (df_profiles['Fields'].str.strip().str.lower() == field.lower()) &
                    (df_profiles['snowmed CT Preferred name'].str.strip().str.lower() == value.lower()) &
                    (df_profiles['Processing/Filtering'].str.strip().str.lower() == 'processing')
                ]
                # Field header
                header = tk.Label(rules_inner, text=field, font=("Arial", 12, "bold"), pady=4)
                header.pack(anchor="w")

                if matches.empty:
                    tk.Label(rules_inner, text="  No rules found", fg="gray").pack(anchor="w")
                else:
                    for _, mrow in matches.iterrows():
                        # Rule frame
                        rule_frame = tk.Frame(rules_inner, relief="solid", borderwidth=1, padx=5, pady=5)
                        rule_frame.pack(fill="x", pady=4)

                        # Header with toggle
                        header_text = f"Code: {mrow['Rule/Workflow']}"
                        header_label = tk.Label(rule_frame, text=header_text, font=("Arial", 10, "bold"), anchor="w")
                        header_label.pack(side="left")

                        toggle_btn = tk.Button(rule_frame, text="Show Details", width=12)
                        toggle_btn.pack(side="right")

                        # Details frame (initially hidden)
                        details_frame = tk.Frame(rule_frame)
                        details_frame.pack(fill="x", pady=2)
                        details_frame.pack_forget()  # hide initially

                        # Populate thresholds
                        for col in threshold_cols:
                            if col in mrow and pd.notna(mrow[col]):
                                tk.Label(details_frame, text=f"{col}: {mrow[col]}", anchor="w").pack(anchor="w")

                        # Toggle logic
                        def toggle():
                            if details_frame.winfo_ismapped():
                                details_frame.pack_forget()
                                toggle_btn.config(text="Show Details")
                            else:
                                details_frame.pack(fill="x", pady=2)
                                toggle_btn.config(text="Hide Details")

                        toggle_btn.config(command=toggle)

def show_filtering_rules(bed_id):
    for widget in rules_inner.winfo_children():
        widget.destroy()

    if bed_id in df['Bed ID'].astype(str).values:
        row = df[df['Bed ID'].astype(str) == bed_id].iloc[0]
        for field in fields:
            value = str(row.get(field, '')).strip()
            if value:
                matches = df_profiles[
                    (df_profiles['Fields'].str.strip().str.lower() == field.lower()) &
                    (df_profiles['snowmed CT Preferred name'].str.strip().str.lower() == value.lower()) &
                    (df_profiles['Processing/Filtering'].str.strip().str.lower() == 'filtering')
                ]
                # Field header
                header = tk.Label(rules_inner, text=field, font=("Arial", 12, "bold"), pady=4)
                header.pack(anchor="w")

                if matches.empty:
                    tk.Label(rules_inner, text="  No rules found", fg="gray").pack(anchor="w")
                else:
                    for _, mrow in matches.iterrows():
                        # Rule frame
                        rule_frame = tk.Frame(rules_inner, relief="solid", borderwidth=1, padx=5, pady=5)
                        rule_frame.pack(fill="x", pady=4)

                        # Header with toggle
                        header_text = f"Code: {mrow['Rule/Workflow']}"
                        header_label = tk.Label(rule_frame, text=header_text, font=("Arial", 10, "bold"), anchor="w")
                        header_label.pack(side="left")

                        toggle_btn = tk.Button(rule_frame, text="Show Details", width=12)
                        toggle_btn.pack(side="right")

                        # Details frame (initially hidden)
                        details_frame = tk.Frame(rule_frame)
                        details_frame.pack(fill="x", pady=2)
                        details_frame.pack_forget()  # hide initially

                        # Populate thresholds
                        for col in threshold_cols:
                            if col in mrow and pd.notna(mrow[col]):
                                tk.Label(details_frame, text=f"{col}: {mrow[col]}", anchor="w").pack(anchor="w")

                        # Toggle logic
                        def toggle():
                            if details_frame.winfo_ismapped():
                                details_frame.pack_forget()
                                toggle_btn.config(text="Show Details")
                            else:
                                details_frame.pack(fill="x", pady=2)
                                toggle_btn.config(text="Hide Details")

                        toggle_btn.config(command=toggle)



# Load bed details
def load_bed_details(event=None):
    bed = bed_var.get()
    if bed in df['Bed ID'].astype(str).values:
        row = df[df['Bed ID'].astype(str) == bed].iloc[0]
        for field in fields:
            entries[field].delete(0, tk.END)
            entries[field].insert(0, str(row.get(field, '')))
        show_processing_rules(bed)
    else:
        for field in fields:
            entries[field].delete(0, tk.END)
        for widget in rules_inner.winfo_children():
            widget.destroy()

bed_dropdown.bind("<<ComboboxSelected>>", load_bed_details)

# Save changes
def save_changes():
    bed = bed_var.get()
    if bed in df['Bed ID'].astype(str).values:
        for field in fields:
            df.loc[df['Bed ID'].astype(str) == bed, field] = entries[field].get()
        save_data(df)
    else:
        messagebox.showerror("Error", "Bed not found!")

# Delete bed
def delete_bed():
    bed = bed_var.get()
    if bed in df['Bed ID'].astype(str).values:
        confirm = messagebox.askyesno("Confirm Delete", f"Delete bed {bed}?")
        if confirm:
            df.drop(df[df['Bed ID'].astype(str) == bed].index, inplace=True)
            bed_dropdown['values'] = df['Bed ID'].astype(str).tolist()
            bed_var.set('')
            for field in fields:
                entries[field].delete(0, tk.END)
            for widget in rules_inner.winfo_children():
                widget.destroy()
            save_data(df)
    else:
        messagebox.showerror("Error", "Bed not found!")

# Create new bed popup
def open_new_bed_window():
    new_window = tk.Toplevel(root)
    new_window.title("Add New Bed")
    new_window.geometry("500x420")

    tk.Label(new_window, text="Create New Bed", font=("Arial", 14, "bold")).pack(pady=8)
    id_row = tk.Frame(new_window)
    id_row.pack(pady=4, anchor="w")
    tk.Label(id_row, text="New Bed ID:", width=16, anchor="w").pack(side="left")
    new_bed_var = tk.StringVar()
    new_bed_entry = tk.Entry(id_row, textvariable=new_bed_var, width=20)
    new_bed_entry.pack(side="left")

    new_entries = {}
    for field in fields:
        r = tk.Frame(new_window)
        r.pack(pady=4, anchor="w")
        tk.Label(r, text=field + ":", width=16, anchor="w").pack(side="left")
        ent = tk.Entry(r, width=50)
        ent.pack(side="left")
        new_entries[field] = ent

    def save_new_bed():
        new_bed = new_bed_var.get().strip()
        if not new_bed:
            messagebox.showerror("Error", "Bed ID cannot be empty.")
            return
        if new_bed in df['Bed ID'].astype(str).values:
            messagebox.showerror("Error", "Bed ID already exists.")
            return
        new_row = {'Bed ID': new_bed}
        for field in fields:
            new_row[field] = new_entries[field].get()
        df.loc[len(df)] = new_row
        bed_dropdown['values'] = df['Bed ID'].astype(str).tolist()
        save_data(df)
        messagebox.showinfo("Success", f"New bed {new_bed} added!")
        new_window.destroy()

    tk.Button(new_window, text="Save New Bed", command=save_new_bed).pack(pady=12)

# === Overview with clickable cards ===
def open_overview():
    overview = tk.Toplevel(root)
    overview.title("Beds Overview by Ward")
    overview.geometry("1100x700")

    container = tk.Frame(overview)
    container.pack(fill="both", expand=True)

    canvas = tk.Canvas(container)
    v_scroll = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas)

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=v_scroll.set)

    canvas.pack(side="left", fill="both", expand=True)
    v_scroll.pack(side="right", fill="y")

    selected_card = {'widget': None}

    def on_card_click(bed_id, card_widget):
        bed_var.set(str(bed_id))
        load_bed_details()
        if selected_card['widget']:
            selected_card['widget'].configure(bg="#F8F9FA")
        card_widget.configure(bg="#E2F0D9")
        selected_card['widget'] = card_widget

    work_df = df.copy()
    work_df['Ward'] = work_df['Ward'].fillna('Unknown ward')

    for ward, group in work_df.groupby('Ward'):
        tk.Label(scroll_frame, text=f"Ward: {ward}", font=("Arial", 16, "bold"), pady=10).pack(anchor="w")
        ward_frame = tk.Frame(scroll_frame)
        ward_frame.pack(fill="x", pady=5)

        col_count = 3
        row_idx = 0
        col_idx = 0

        for _, row in group.iterrows():
            bed_id_str = str(row.get('Bed ID', ''))
            card = tk.Frame(ward_frame, relief="solid", borderwidth=1, padx=10, pady=10, bg="#F8F9FA", cursor="hand2")
            tk.Label(card, text=f"Bed ID: {bed_id_str}", font=("Arial", 12, "bold"), bg="#F8F9FA").pack(anchor="w")
            tk.Label(card, text=f"Ward: {row.get('Ward', '')}", bg="#F8F9FA").pack(anchor="w")
            tk.Label(card, text=f"Admission reason: {row.get('Admission reason', '')}", wraplength=300, bg="#F8F9FA").pack(anchor="w")
            tk.Label(card, text=f"Active conditions: {row.get('Active conditions', '')}", wraplength=300, bg="#F8F9FA").pack(anchor="w")
            tk.Label(card, text=f"Comorbidities: {row.get('Comorbidities', '')}", wraplength=300, bg="#F8F9FA").pack(anchor="w")
            tk.Label(card, text=f"Predicted risks: {row.get('Predicted risks', '')}", wraplength=300, bg="#F8F9FA").pack(anchor="w")

            card.bind("<Button-1>", lambda e, bid=bed_id_str, w=card: on_card_click(bid, w))
            for child in card.winfo_children():
                child.bind("<Button-1>", lambda e, bid=bed_id_str, w=card: on_card_click(bid, w))

            card.grid(row=row_idx, column=col_idx, padx=10, pady=10, sticky="n")
            col_idx += 1
            if col_idx >= col_count:
                col_idx = 0
                row_idx += 1

# Buttons
btn_frame = tk.Frame(root)
btn_frame.pack(pady=12)
tk.Button(btn_frame, text="Save Changes", command=save_changes, width=16).grid(row=0, column=0, padx=6)
tk.Button(btn_frame, text="Create New Bed", command=open_new_bed_window, width=16).grid(row=0, column=1, padx=6)
tk.Button(btn_frame, text="Delete Bed", command=delete_bed, width=16).grid(row=0, column=2, padx=6)
tk.Button(btn_frame, text="Overview of All Beds", command=open_overview, width=18).grid(row=0, column=3, padx=6)

root.mainloop()
