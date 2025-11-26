
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

# === CONFIG ===
excel_file = 'data.xlsx'  # <-- Put the local path to your downloaded Excel file
sheet_beds = '3. Link of "Profiles" to beds'
sheet_profiles = '2. Creation of "profiles"'

# Threshold columns to display when present
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

# === DATA ACCESS ===
def load_data():
    try:
        beds = pd.read_excel(excel_file, sheet_name=sheet_beds, engine='openpyxl')
        beds = beds.loc[:, ~beds.columns.str.contains('^Unnamed')]
        beds.columns = beds.columns.str.strip()

        profiles = pd.read_excel(excel_file, sheet_name=sheet_profiles, engine='openpyxl')
        profiles = profiles.loc[:, ~profiles.columns.str.contains('^Unnamed')]
        profiles.columns = profiles.columns.str.strip()

        # Sanity-check key columns exist in profiles
        required_profiles_cols = {'Fields', 'snowmed CT Preferred name', 'Processing/Filtering', 'Rule/Workflow'}
        missing = required_profiles_cols - set(profiles.columns)
        if missing:
            messagebox.showerror("Error", f"Missing columns in profiles sheet:\n{missing}")

        return beds, profiles
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load Excel file: {e}")
        # Return empty frames with expected columns so UI doesn't break
        empty_beds = pd.DataFrame(columns=['Bed ID', 'Ward', 'Admission reason', 'Active conditions', 'Comorbidities', 'Predicted risks'])
        empty_profiles = pd.DataFrame(columns=['Fields', 'snowmed CT Preferred name', 'Processing/Filtering', 'Rule/Workflow'] + threshold_cols)
        return empty_beds, empty_profiles

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
root.geometry("1100x940")

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

# === SEARCH BAR ===
search_frame = tk.Frame(root)
search_frame.pack(pady=6, fill="x")
tk.Label(search_frame, text="Search by threshold parameter:", font=("Arial", 12)).pack(side="left", padx=6)
search_var = tk.StringVar()
search_entry = tk.Entry(search_frame, textvariable=search_var, width=30)
search_entry.pack(side="left", padx=6)

def apply_search():
    keyword = search_var.get().strip().lower()
    bed_id = bed_var.get()
    if bed_id and bed_id in df['Bed ID'].astype(str).values:
        show_processing_rules(bed_id, filter_keyword=(keyword if keyword else None))
    else:
        messagebox.showinfo("Info", "Please select a Bed ID first.")

def clear_search():
    search_var.set('')
    bed_id = bed_var.get()
    if bed_id and bed_id in df['Bed ID'].astype(str).values:
        show_processing_rules(bed_id, filter_keyword=None)

tk.Button(search_frame, text="Search", command=apply_search).pack(side="left", padx=6)
tk.Button(search_frame, text="Clear", command=clear_search).pack(side="left", padx=6)
search_entry.bind("<Return>", lambda e: apply_search())

# === PROCESSING & FILTERING RULES SECTION (Two side-by-side columns) ===
rules_frame = tk.Frame(root)
rules_frame.pack(pady=10, fill="both", expand=True)

# Section title
tk.Label(rules_frame, text="Related Rules", font=("Arial", 16, "bold")).pack(anchor="w")

# Scrollable container
canvas = tk.Canvas(rules_frame)
scrollbar = tk.Scrollbar(rules_frame, orient="vertical", command=canvas.yview)
rules_inner = tk.Frame(canvas)

rules_inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=rules_inner, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

def create_rule_card(parent: tk.Frame, mrow: pd.Series, header_bg="#F8F9FA"):
    """
    Creates a collapsible card inside `parent` for a single rule row (mrow).
    Displays Rule/Workflow in a header bar and, when expanded, shows thresholds
    directly BELOW the rule name (in the same card).
    """
    # Outer card
    card = tk.Frame(parent, relief="solid", borderwidth=1, padx=8, pady=8, bg="#FFFFFF")
    card.pack(fill="x", pady=6)

    # Header bar (rule name + toggle)
    header_bar = tk.Frame(card, bg=header_bg)
    header_bar.pack(fill="x")

    header_text = f"Rule: {mrow.get('Rule/Workflow', '')}"
    header_label = tk.Label(header_bar, text=header_text, font=("Arial", 10, "bold"), anchor="w", bg=header_bg)
    header_label.pack(side="left")

    toggle_btn = tk.Button(header_bar, text="Show Details", width=12)
    toggle_btn.pack(side="right")

    # Details area appears directly below the header bar
    details_frame = tk.Frame(card, bg="#FFFFFF")
    details_frame.pack(fill="x", pady=(8, 4))
    details_frame.pack_forget()  # hidden initially

    # Populate thresholds if present
    has_any_threshold = False
    for col in threshold_cols:
        if col in mrow.index and pd.notna(mrow[col]):
            has_any_threshold = True
            rowf = tk.Frame(details_frame, bg="#FFFFFF")
            rowf.pack(fill="x", anchor="w")
            tk.Label(rowf, text=f"{col}:", width=45, anchor="w", bg="#FFFFFF").pack(side="left")
            tk.Label(rowf, text=f"{mrow[col]}", anchor="w", bg="#FFFFFF").pack(side="left")

    if not has_any_threshold:
        tk.Label(details_frame, text=f"No threshold values", fg="gray", anchor="w", bg="#FFFFFF").pack(anchor="w")

    def toggle():
        if details_frame.winfo_ismapped():
            details_frame.pack_forget()
            toggle_btn.config(text="Show Details")
        else:
            details_frame.pack(fill="x", pady=(8, 4))
            toggle_btn.config(text="Hide Details")

    toggle_btn.config(command=toggle)

def filter_matches_by_keyword(df_subset: pd.DataFrame, keyword: str | None) -> pd.DataFrame:
    """
    Returns only rows where at least one threshold column:
      - exists in the DataFrame,
      - has a non-null value,
      - and its column name contains the keyword (case-insensitive).
    If keyword is None or empty, returns df_subset unchanged.
    """
    if not keyword:
        return df_subset
    kw = keyword.lower()
    mask = []
    for _, r in df_subset.iterrows():
        matched = False
        for col in threshold_cols:
            if col in df_subset.columns:
                val = r.get(col)
                if pd.notna(val) and kw in col.lower():
                    matched = True
                    break
        mask.append(matched)
    try:
        return df_subset[mask]
    except Exception:
        # If mask is wrong length or df_subset empty
        return df_subset

def show_processing_rules(bed_id: str, filter_keyword: str | None = None):
    """
    Renders two side-by-side columns:
      Left  = Processing rules (by field)
      Right = Filtering rules (by field)
    with equal column widths and centered alignment.
    When filter_keyword is provided, only rules with non-null values
    in threshold columns containing the keyword are shown.
    """
    # Clear previous content
    for widget in rules_inner.winfo_children():
        widget.destroy()

    # Container for two equal-width columns (grid)
    columns_container = tk.Frame(rules_inner)
    columns_container.pack(fill="both", expand=True, pady=4)

    # Column headers row
    left_header = tk.Label(columns_container, text="Processing Rules", font=("Arial", 14, "bold"), fg="#2E7D32")
    right_header = tk.Label(columns_container, text="Filtering Rules", font=("Arial", 14, "bold"), fg="#1565C0")
    left_header.grid(row=0, column=0, sticky="n", padx=10, pady=(4, 10))
    right_header.grid(row=0, column=1, sticky="n", padx=10, pady=(4, 10))

    # Make columns equal width and centered using uniform group
    columns_container.grid_columnconfigure(0, weight=1, uniform="rules_cols")
    columns_container.grid_columnconfigure(1, weight=1, uniform="rules_cols")

    if bed_id in df['Bed ID'].astype(str).values:
        bed_row = df[df['Bed ID'].astype(str) == bed_id].iloc[0]

        # Create two column frames (equal width cells)
        left_col = tk.Frame(columns_container)   # Processing
        right_col = tk.Frame(columns_container)  # Filtering
        left_col.grid(row=1, column=0, sticky="n", padx=10)
        right_col.grid(row=1, column=1, sticky="n", padx=10)

        # For each field, render field title and its rules in both columns
        for field in fields:
            field_value = str(bed_row.get(field, '')).strip()

            # Field title labels in both columns (to keep rows aligned)
            tk.Label(left_col, text=field, font=("Arial", 12, "bold")).pack(anchor="n")
            tk.Label(right_col, text=field, font=("Arial", 12, "bold")).pack(anchor="n")

            # Processing matches
            if field_value:
                proc_matches = df_profiles[
                    (df_profiles['Fields'].astype(str).str.strip().str.lower() == field.lower()) &
                    (df_profiles['snowmed CT Preferred name'].astype(str).str.strip().str.lower() == field_value.lower()) &
                    (df_profiles['Processing/Filtering'].astype(str).str.strip().str.lower() == 'processing')
                ]
            else:
                proc_matches = pd.DataFrame(columns=df_profiles.columns)

            # Filtering matches
            if field_value:
                filt_matches = df_profiles[
                    (df_profiles['Fields'].astype(str).str.strip().str.lower() == field.lower()) &
                    (df_profiles['snowmed CT Preferred name'].astype(str).str.strip().str.lower() == field_value.lower()) &
                    (df_profiles['Processing/Filtering'].astype(str).str.strip().str.lower() == 'filtering')
                ]
            else:
                filt_matches = pd.DataFrame(columns=df_profiles.columns)

            # Apply search filter (only rules having non-null thresholds in columns matching keyword)
            proc_matches = filter_matches_by_keyword(proc_matches, filter_keyword)
            filt_matches = filter_matches_by_keyword(filt_matches, filter_keyword)

            # Populate left column (Processing)
            if proc_matches.empty:
                tk.Label(left_col, text="No matching rules", fg="gray").pack(anchor="n", pady=(0, 6))
            else:
                for _, mrow in proc_matches.iterrows():
                    create_rule_card(left_col, mrow, header_bg="#E8F5E9")  # light green header

            # Populate right column (Filtering)
            if filt_matches.empty:
                tk.Label(right_col, text="No matching rules", fg="gray").pack(anchor="n", pady=(0, 6))
            else:
                for _, mrow in filt_matches.iterrows():
                    create_rule_card(right_col, mrow, header_bg="#E3F2FD")  # light blue header

# Load bed details
def load_bed_details(event=None):
    bed = bed_var.get()
    if bed in df['Bed ID'].astype(str).values:
        row = df[df['Bed ID'].astype(str) == bed].iloc[0]
        for field in fields:
            entries[field].delete(0, tk.END)
            entries[field].insert(0, str(row.get(field, '')))
        # Respect current search keyword when loading details
        kw = search_var.get().strip().lower()
        show_processing_rules(bed, filter_keyword=(kw if kw else None))
    else:
        for field in fields:
            entries[field].delete(0, tk.END)
        # Clear rules area
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
        # Refresh rules respecting current search keyword
        kw = search_var.get().strip().lower()
        show_processing_rules(bed, filter_keyword=(kw if kw else None))
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
tk.Button(btn_frame, text="Overview of All Beds", command=open_overview, width=20).grid(row=0, column=3, padx=6)

root.mainloop()
