
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from typing import Optional

# === CONFIG ===
excel_file = 'Patients.xlsx'
medical_devices_file = 'Medical Devices.xlsx'

sheet_beds = '3. Link of "Profiles" to beds'
sheet_profiles = '2. Creation of "profiles"'

# Threshold columns to display when present (for rules)
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

# === NEW: Medical devices sheets & metric columns ===
sheet_devices_link   = 'Link of "Devices" to beds'
sheet_alarm_conditions = 'alarm conditions'
sheet_devices_list   = 'list medical devices'  # <<< NEW >>> (optional catalog sheet)

# Metric columns that may hold threshold values in the alarm sheet
device_metric_cols = [
    'SpO2', 'sys BP', 'dia BP', 'MAP', 'HR', 'Temp', 'RR',
    'Peak pressure', 'Circuit pressure', 'Line pressure', 'Volume'
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

        required_profiles_cols = {'Fields', 'snowmed CT Preferred name', 'Processing/Filtering', 'Rule/Workflow'}
        missing = required_profiles_cols - set(profiles.columns)
        if missing:
            messagebox.showerror("Error", f"Missing columns in profiles sheet:\n{missing}")

        return beds, profiles
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load Excel file: {e}")
        empty_beds = pd.DataFrame(columns=['Bed ID', 'Ward', 'Admission reason', 'Active conditions', 'Comorbidities', 'Predicted risks'])
        empty_profiles = pd.DataFrame(columns=['Fields', 'snowmed CT Preferred name', 'Processing/Filtering', 'Rule/Workflow'] + threshold_cols)
        return empty_beds, empty_profiles

def save_data(df):
    try:
        with pd.ExcelWriter(excel_file, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            df.to_excel(writer, sheet_name=sheet_beds, index=False)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save Excel file: {e}")

# === NEW: Load medical devices workbook (link + alarms + optional catalog) ===
def load_medical_devices():
    """Load device-to-bed links, alarm conditions, and optional catalog from Medical Devices.xlsx"""
    try:
        devices_link = pd.read_excel(medical_devices_file, sheet_name=sheet_devices_link, engine='openpyxl')
        devices_link = devices_link.loc[:, ~devices_link.columns.str.contains('^Unnamed')]
        devices_link.columns = devices_link.columns.str.strip()

        alarm_conditions = pd.read_excel(medical_devices_file, sheet_name=sheet_alarm_conditions, engine='openpyxl')
        alarm_conditions = alarm_conditions.loc[:, ~alarm_conditions.columns.str.contains('^Unnamed')]
        alarm_conditions.columns = alarm_conditions.columns.str.strip()

        # Catalog sheet is optional; if missing, we derive catalog from existing sheets
        try:
            devices_catalog = pd.read_excel(medical_devices_file, sheet_name=sheet_devices_list, engine='openpyxl')
            devices_catalog = devices_catalog.loc[:, ~devices_catalog.columns.str.contains('^Unnamed')]
            devices_catalog.columns = devices_catalog.columns.str.strip()
        except Exception:
            devices_catalog = pd.DataFrame()

        required_link_cols  = {'Bed ID', 'Device'}
        required_alarm_cols = {'alarm condition', 'Device'}
        missing_link  = required_link_cols - set(devices_link.columns)
        missing_alarm = required_alarm_cols - set(alarm_conditions.columns)
        if missing_link or missing_alarm:
            messagebox.showerror("Error",
                f"Missing columns in Medical Devices file:\n"
                f"Link sheet missing: {missing_link}\nAlarm sheet missing: {missing_alarm}"
            )

        return devices_link, alarm_conditions, devices_catalog
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load Medical Devices file: {e}")
        return (pd.DataFrame(columns=['Bed ID', 'Device']),
                pd.DataFrame(columns=['alarm condition', 'Device']),
                pd.DataFrame())

# === NEW: Save devices link sheet ===
def save_devices_data():
    """Write updated device links back to Medical Devices.xlsx (only the link sheet)."""
    try:
        with pd.ExcelWriter(medical_devices_file, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            df_devices_link.to_excel(writer, sheet_name=sheet_devices_link, index=False)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save Medical Devices file: {e}")

# === INIT DATA ===
df, df_profiles = load_data()
df_devices_link, df_alarm_conditions, df_devices_catalog = load_medical_devices()

# Build a catalog of known device names for convenience in the UI  # <<< NEW >>>
def build_available_devices():
    names = []
    # Prefer catalog sheet if present (column likely 'snowmed CT Preferred name')
    if not df_devices_catalog.empty:
        prefer_col = None
        # pick the first column that seems like a name column
        for c in df_devices_catalog.columns:
            if 'preferred' in c.lower() and 'name' in c.lower():
                prefer_col = c
                break
        if prefer_col is None:
            # fallback: any column named 'Device' or similar
            for c in df_devices_catalog.columns:
                if c.strip().lower() == 'device':
                    prefer_col = c
                    break
        if prefer_col:
            names.extend(df_devices_catalog[prefer_col].dropna().astype(str).str.strip().tolist())

    # Add devices seen in alarm conditions
    if 'Device' in df_alarm_conditions.columns:
        names.extend(df_alarm_conditions['Device'].dropna().astype(str).str.strip().tolist())
    # Add devices seen in link sheet
    names.extend(df_devices_link['Device'].dropna().astype(str).str.strip().tolist())

    # De-duplicate, case-insensitive, preserve order
    seen = set()
    ordered = []
    for n in names:
        key = n.lower()
        if key not in seen:
            seen.add(key)
            ordered.append(n)
    return ordered

AVAILABLE_DEVICES = build_available_devices()  # <<< NEW >>>



# Save changes
def save_changes():
    bed = bed_var.get()
    if bed in df['Bed ID'].astype(str).values:
        # 1) Save bed details to Patients.xlsx
        for field in fields:
            df.loc[df['Bed ID'].astype(str) == bed, field] = entries[field].get()
        save_data(df)

        # 2) Save connected devices to Medical Devices.xlsx (Link of "Devices" to beds)
        current_devices = listbox_items()
        # Order-preserving de-duplication (case-insensitive)
        seen = set()
        ordered_unique = []
        for d in current_devices:
            key = d.lower().strip()
            if key and key not in seen:
                seen.add(key)
                ordered_unique.append(d.strip())

        # Remove all old links for this bed
        df_devices_link.drop(df_devices_link[df_devices_link['Bed ID'].astype(str) == bed].index, inplace=True)
        # Add new links (one row per device)
        for device in ordered_unique:
            df_devices_link.loc[len(df_devices_link)] = {'Bed ID': bed, 'Device': device}
        save_devices_data()

        # 3) Refresh UI (device list + rules + alarms) and show success
        refresh_devices_list_ui(bed)
        kw = search_var.get().strip().lower()
        show_processing_rules(bed, filter_keyword=(kw if kw else None))
        messagebox.showinfo("Success", "Changes saved successfully!")
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

            # Also remove device links for this bed
            df_devices_link.drop(df_devices_link[df_devices_link['Bed ID'].astype(str) == bed].index, inplace=True)
            save_data(df)
            save_devices_data()

            for field in fields:
                entries[field].delete(0, tk.END)
            clear_devices_list_ui()
            for widget in rules_inner.winfo_children():
                widget.destroy()

            messagebox.showinfo("Success", f"Bed {bed} deleted.")
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
    overview.geometry("1180x720")

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

# === SEARCH AMONG RULES
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

# === MAIN UI ===
root = tk.Tk()

# Top header frame
header_frame = tk.Frame(root)
header_frame.pack(fill="x", pady=8)

# Title on the left
tk.Label(header_frame, text="Bed Profile Manager", font=("Arial", 18, "bold")).grid(row=0, column=0, sticky="w", padx=10)

# Buttons on the right
btn_frame = tk.Frame(header_frame)
btn_frame.grid(row=0, column=1, sticky="e", padx=10)

tk.Button(btn_frame, text="Save Changes", command=save_changes, width=16).grid(row=0, column=0, padx=6)
tk.Button(btn_frame, text="Delete Bed", command=delete_bed, width=16).grid(row=0, column=2, padx=6)
tk.Button(btn_frame, text="Create New Bed", command=open_new_bed_window, width=16).grid(row=0, column=1, padx=6)
tk.Button(btn_frame, text="Overview of All Beds", command=open_overview, width=20).grid(row=0, column=3, padx=6)


# Main form container using grid for a 2-column layout
form_frame = tk.Frame(root)
form_frame.pack(padx=12, pady=8, fill="both", expand=True)
form_frame.grid_columnconfigure(0, weight=1)
form_frame.grid_columnconfigure(1, weight=1)

entries = {}
fields = ['Ward', 'Admission reason', 'Active conditions', 'Comorbidities', 'Predicted risks']

# Row 1: Ward (left) and Bed ID dropdown (right)
ward_frame = tk.Frame(form_frame)
ward_frame.grid(row=0, column=0, sticky="nsew", padx=8, pady=6)
tk.Label(ward_frame, text="Ward:", width=18, anchor="w").grid(row=0, column=0, sticky="w")
entries['Ward'] = tk.Entry(ward_frame, width=40)
entries['Ward'].grid(row=0, column=1, sticky="ew", padx=6)
ward_frame.grid_columnconfigure(1, weight=1)

bed_frame = tk.Frame(form_frame)
bed_frame.grid(row=0, column=1, sticky="nsew", padx=8, pady=6)
tk.Label(bed_frame, text="Bed number (ID):", anchor="w").grid(row=0, column=0, sticky="w", padx=(0, 6))
bed_var = tk.StringVar()
bed_dropdown = ttk.Combobox(bed_frame, textvariable=bed_var, values=df['Bed ID'].astype(str).tolist(), width=20)
bed_dropdown.grid(row=0, column=1, sticky="ew")
bed_frame.grid_columnconfigure(1, weight=1)

# Row 2: Admission reason (left) and grouped fields (right)

"""
reason_frame = tk.Frame(form_frame)
reason_frame.grid(row=1, column=0, sticky="nsew", padx=8, pady=6)
tk.Label(reason_frame, text="Admission reason:", width=18, anchor="w").grid(row=0, column=0, sticky="w")
entries['Admission reason'] = tk.Entry(reason_frame, width=60)
entries['Admission reason'].grid(row=0, column=1, sticky="ew", padx=6)
reason_frame.grid_columnconfigure(1, weight=1)

group_frame = tk.LabelFrame(form_frame, text="Clinical summary", padx=8, pady=8)
group_frame.grid(row=1, column=1, sticky="nsew", padx=8, pady=6)
group_frame.grid_columnconfigure(1, weight=1)

for i, field in enumerate(['Active conditions', 'Comorbidities', 'Predicted risks']):
    tk.Label(group_frame, text=field + ":", width=18, anchor="w").grid(row=i, column=0, sticky="w", pady=(6 if i>0 else 0,0))
    entries[field] = tk.Entry(group_frame, width=60)
    entries[field].grid(row=i, column=1, sticky="ew", padx=6, pady=(6 if i>0 else 0,0))

"""


# Combined Clinical summary frame with two columns
combined_frame = tk.LabelFrame(form_frame, text="Clinical summary", padx=8, pady=8)
combined_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=8, pady=6)
combined_frame.grid_columnconfigure(0, weight=1)
combined_frame.grid_columnconfigure(1, weight=1)

# Left column: Admission reason
tk.Label(combined_frame, text="Admission reason:", width=18, anchor="w").grid(row=0, column=0, sticky="w")
entries['Admission reason'] = tk.Entry(combined_frame, width=40)
entries['Admission reason'].grid(row=0, column=0, sticky="ew", padx=(140, 6))

# Right column: Active conditions, Comorbidities, Predicted risks
for i, field in enumerate(['Active conditions', 'Comorbidities', 'Predicted risks']):
    tk.Label(combined_frame, text=field + ":", width=18, anchor="w").grid(row=i, column=1, sticky="w", pady=(6 if i > 0 else 0, 0))
    entries[field] = tk.Entry(combined_frame, width=60)
    entries[field].grid(row=i, column=1, sticky="ew", padx=6, pady=(6 if i > 0 else 0, 0))


# Row 3: Connected devices manager spanning both columns
devices_section = tk.LabelFrame(form_frame, text="Connected medical devices", padx=8, pady=8)
devices_section.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=8, pady=10)
devices_row = tk.Frame(devices_section)
devices_row.grid(row=0, column=0, sticky="nsew")

# Inside devices_row (Row 3)
tk.Label(devices_row, text="Connected devices:", width=18, anchor="w").grid(row=0, column=0, sticky="nw")
devices_listbox = tk.Listbox(devices_row, selectmode=tk.EXTENDED, width=50, height=3)
devices_listbox.grid(row=0, column=1, sticky="w")
current_devices_var = tk.StringVar(value="")


# === SEARCH BAR ===
search_frame = tk.Frame(root)
search_frame.pack(pady=6, fill="x")
tk.Label(search_frame, text="Search by threshold parameter:", font=("Arial", 12)).pack(side="left", padx=6)
search_var = tk.StringVar()
search_entry = tk.Entry(search_frame, textvariable=search_var, width=30)
search_entry.pack(side="left", padx=6)

tk.Button(search_frame, text="Search", command=apply_search).pack(side="left", padx=6)
tk.Button(search_frame, text="Clear", command=clear_search).pack(side="left", padx=6)
search_entry.bind("<Return>", lambda e: apply_search())

# === PROCESSING & FILTERING RULES SECTION (Two side-by-side columns) ===
rules_frame = tk.Frame(root)
rules_frame.pack(pady=10, fill="both", expand=True)

tk.Label(rules_frame, text="Related Rules", font=("Arial", 16, "bold")).pack(anchor="w")

canvas = tk.Canvas(rules_frame)
scrollbar = tk.Scrollbar(rules_frame, orient="vertical", command=canvas.yview)
rules_inner = tk.Frame(canvas)
rules_inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=rules_inner, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

def create_rule_card(parent: tk.Frame, mrow: pd.Series, header_bg="#F8F9FA"):
    card = tk.Frame(parent, relief="solid", borderwidth=1, padx=8, pady=8, bg="#FFFFFF")
    card.pack(fill="x", pady=6)

    header_bar = tk.Frame(card, bg=header_bg)
    header_bar.pack(fill="x")
    header_text = f"Rule: {mrow.get('Rule/Workflow', '')}"
    header_label = tk.Label(header_bar, text=header_text, font=("Arial", 10, "bold"), anchor="w", bg=header_bg)
    header_label.pack(side="left")
    toggle_btn = tk.Button(header_bar, text="Show Details", width=12)
    toggle_btn.pack(side="right")

    details_frame = tk.Frame(card, bg="#FFFFFF")
    details_frame.pack(fill="x", pady=(8, 4))
    details_frame.pack_forget()

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

def filter_matches_by_keyword(df_subset: pd.DataFrame, keyword: Optional[str] = None) -> pd.DataFrame:
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
        return df_subset

# === NEW: Alarm cards & helpers ===
def get_alarms_for_bed(bed_id: str) -> pd.DataFrame:
    linked = df_devices_link[df_devices_link['Bed ID'].astype(str) == str(bed_id)]
    if linked.empty:
        return pd.DataFrame(columns=df_alarm_conditions.columns)
    devices = linked['Device'].astype(str).str.strip().str.lower().unique()
    ac = df_alarm_conditions.copy()
    ac['Device_norm'] = ac['Device'].astype(str).str.strip().str.lower()
    result = ac[ac['Device_norm'].isin(devices)].drop(columns=['Device_norm'])
    return result

def filter_alarms_by_keyword(df_subset: pd.DataFrame, keyword: Optional[str] = None) -> pd.DataFrame:
    if not keyword:
        return df_subset
    kw = keyword.lower()
    mask = []
    for _, r in df_subset.iterrows():
        matched = False
        ac_name = str(r.get('alarm condition', '')).lower()
        if kw in ac_name:
            matched = True
        if not matched:
            for col in device_metric_cols:
                if col in df_subset.columns:
                    val = r.get(col)
                    if pd.notna(val) and kw in col.lower():
                        matched = True
                        break
        mask.append(matched)
    try:
        return df_subset[mask]
    except Exception:
        return df_subset

def create_alarm_card(parent: tk.Frame, arow: pd.Series, header_bg="#F3E5F5"):
    card = tk.Frame(parent, relief="solid", borderwidth=1, padx=8, pady=8, bg="#FFFFFF")
    card.pack(fill="x", pady=6)

    header_bar = tk.Frame(card, bg=header_bg)
    header_bar.pack(fill="x")

    title = f"Alarm: {arow.get('alarm condition', '')}  |  Device: {arow.get('Device', '')}"
    header_label = tk.Label(header_bar, text=title, font=("Arial", 10, "bold"), anchor="w", bg=header_bg)
    header_label.pack(side="left")

    toggle_btn = tk.Button(header_bar, text="Show Details", width=12)
    toggle_btn.pack(side="right")

    details_frame = tk.Frame(card, bg="#FFFFFF")
    details_frame.pack(fill="x", pady=(8, 4))
    details_frame.pack_forget()

    codes_frame = tk.Frame(details_frame, bg="#FFFFFF")
    codes_frame.pack(fill="x", anchor="w")
    tk.Label(codes_frame, text=f"Finding SNOMED: {arow.get('SNOMED CT code of finding', '')}",
             anchor="w", bg="#FFFFFF").pack(side="left", padx=(0, 10))
    tk.Label(codes_frame, text=f"Device SNOMED: {arow.get('SNOMED CT code of device', '')}",
             anchor="w", bg="#FFFFFF").pack(side="left")

    has_any_metric = False
    for col in device_metric_cols:
        if col in arow.index and pd.notna(arow[col]):
            has_any_metric = True
            rowf = tk.Frame(details_frame, bg="#FFFFFF")
            rowf.pack(fill="x", anchor="w")
            tk.Label(rowf, text=f"{col}:", width=20, anchor="w", bg="#FFFFFF").pack(side="left")
            tk.Label(rowf, text=f"{arow[col]}", anchor="w", bg="#FFFFFF").pack(side="left")

    if not has_any_metric:
        tk.Label(details_frame, text="No metric thresholds", fg="gray", anchor="w", bg="#FFFFFF").pack(anchor="w")

    def toggle():
        if details_frame.winfo_ismapped():
            details_frame.pack_forget()
            toggle_btn.config(text="Show Details")
        else:
            details_frame.pack(fill="x", pady=(8, 4))
            toggle_btn.config(text="Hide Details")
    toggle_btn.config(command=toggle)

def show_processing_rules(bed_id: str, filter_keyword: Optional[str] = None):
    # Clear previous content
    for widget in rules_inner.winfo_children():
        widget.destroy()

    columns_container = tk.Frame(rules_inner)
    columns_container.pack(fill="both", expand=True, pady=4)

    left_header = tk.Label(columns_container, text="Processing Rules", font=("Arial", 14, "bold"), fg="#2E7D32")
    right_header = tk.Label(columns_container, text="Filtering Rules", font=("Arial", 14, "bold"), fg="#1565C0")
    left_header.grid(row=0, column=0, sticky="n", padx=10, pady=(4, 10))
    right_header.grid(row=0, column=1, sticky="n", padx=10, pady=(4, 10))

    columns_container.grid_columnconfigure(0, weight=1, uniform="rules_cols")
    columns_container.grid_columnconfigure(1, weight=1, uniform="rules_cols")

    if bed_id in df['Bed ID'].astype(str).values:
        bed_row = df[df['Bed ID'].astype(str) == bed_id].iloc[0]

        # Keep devices UI synchronized for the selected bed  # <<< NEW >>>
        refresh_devices_list_ui(bed_id)

        left_col = tk.Frame(columns_container)
        right_col = tk.Frame(columns_container)
        left_col.grid(row=1, column=0, sticky="n", padx=10)
        right_col.grid(row=1, column=1, sticky="n", padx=10)

        for field in fields:
            field_value = str(bed_row.get(field, '')).strip()

            tk.Label(left_col, text=field, font=("Arial", 12, "bold")).pack(anchor="n")
            tk.Label(right_col, text=field, font=("Arial", 12, "bold")).pack(anchor="n")

            if field_value:
                proc_matches = df_profiles[
                    (df_profiles['Fields'].astype(str).str.strip().str.lower() == field.lower()) &
                    (df_profiles['snowmed CT Preferred name'].astype(str).str.strip().str.lower() == field_value.lower()) &
                    (df_profiles['Processing/Filtering'].astype(str).str.strip().str.lower() == 'processing')
                ]
            else:
                proc_matches = pd.DataFrame(columns=df_profiles.columns)

            if field_value:
                filt_matches = df_profiles[
                    (df_profiles['Fields'].astype(str).str.strip().str.lower() == field.lower()) &
                    (df_profiles['snowmed CT Preferred name'].astype(str).str.strip().str.lower() == field_value.lower()) &
                    (df_profiles['Processing/Filtering'].astype(str).str.strip().str.lower() == 'filtering')
                ]
            else:
                filt_matches = pd.DataFrame(columns=df_profiles.columns)

            proc_matches = filter_matches_by_keyword(proc_matches, filter_keyword)
            filt_matches = filter_matches_by_keyword(filt_matches, filter_keyword)

            if proc_matches.empty:
                tk.Label(left_col, text="No matching rules", fg="gray").pack(anchor="n", pady=(0, 6))
            else:
                for _, mrow in proc_matches.iterrows():
                    create_rule_card(left_col, mrow, header_bg="#E8F5E9")

            if filt_matches.empty:
                tk.Label(right_col, text="No matching rules", fg="gray").pack(anchor="n", pady=(0, 6))
            else:
                for _, mrow in filt_matches.iterrows():
                    create_rule_card(right_col, mrow, header_bg="#E3F2FD")

        alarms_header = tk.Label(columns_container, text="Connected Device Alarm Conditions",
                                 font=("Arial", 14, "bold"), fg="#7B1FA2")
        alarms_header.grid(row=2, column=0, columnspan=2, sticky="w", padx=10, pady=(18, 6))

        alarms_container = tk.Frame(columns_container)
        alarms_container.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=10, pady=(0, 10))
        columns_container.grid_rowconfigure(3, weight=1)

        alarms_df = get_alarms_for_bed(bed_id)
        alarms_df = filter_alarms_by_keyword(alarms_df, filter_keyword)

        if alarms_df.empty:
            tk.Label(alarms_container, text="No devices linked to this bed or no alarm conditions found", fg="gray").pack(anchor="w")
        else:
            for _, arow in alarms_df.iterrows():
                create_alarm_card(alarms_container, arow)
    else:
        clear_devices_list_ui()  # <<< NEW >>>
        tk.Label(columns_container, text="Selected bed not found.", fg="red").grid(row=1, column=0, columnspan=2, sticky="n")

# === NEW: Devices manager helpers ===
def listbox_items() -> list:
    """Return current devices from the listbox, in order."""
    return [devices_listbox.get(i) for i in range(devices_listbox.size())]

def update_current_devices_string():
    """Refresh the read-only comma view based on the listbox content."""
    current_devices_var.set(", ".join(listbox_items()))

def add_selected_device_from_combo():
    name = available_devices_cb.get().strip()
    if not name:
        return
    # Avoid duplicates (case-insensitive)
    existing_lower = [d.lower() for d in listbox_items()]
    if name.lower() not in existing_lower:
        devices_listbox.insert(tk.END, name)
        update_current_devices_string()

def add_custom_device():
    name = custom_device_var.get().strip()
    if not name:
        return
    existing_lower = [d.lower() for d in listbox_items()]
    if name.lower() not in existing_lower:
        devices_listbox.insert(tk.END, name)
        update_current_devices_string()
    custom_device_var.set("")  # clear input

def remove_selected_devices():
    sel = list(devices_listbox.curselection())
    if not sel:
        return
    # remove from bottom to top to keep indices valid
    for idx in reversed(sel):
        devices_listbox.delete(idx)
    update_current_devices_string()

def refresh_devices_list_ui(bed_id: str):
    """Populate the devices listbox for the selected bed."""
    clear_devices_list_ui()
    linked = df_devices_link[df_devices_link['Bed ID'].astype(str) == str(bed_id)]
    if not linked.empty:
        # preserve order of appearance, de-duplicate case-insensitive
        seen = set()
        ordered = []
        for d in linked['Device'].astype(str).str.strip().tolist():
            key = d.lower()
            if key not in seen:
                seen.add(key)
                ordered.append(d)
        for d in ordered:
            devices_listbox.insert(tk.END, d)
    update_current_devices_string()

def clear_devices_list_ui():
    devices_listbox.delete(0, tk.END)
    update_current_devices_string()

# Load bed details
def load_bed_details(event=None):
    bed = bed_var.get()
    if bed in df['Bed ID'].astype(str).values:
        row = df[df['Bed ID'].astype(str) == bed].iloc[0]
        for field in fields:
            entries[field].delete(0, tk.END)
            entries[field].insert(0, str(row.get(field, '')))
        refresh_devices_list_ui(bed)  # <<< NEW >>>
        kw = search_var.get().strip().lower()
        show_processing_rules(bed, filter_keyword=(kw if kw else None))
    else:
        for field in fields:
            entries[field].delete(0, tk.END)
        clear_devices_list_ui()  # <<< NEW >>>
        for widget in rules_inner.winfo_children():
            widget.destroy()
bed_dropdown.bind("<<ComboboxSelected>>", load_bed_details)


root.mainloop()
