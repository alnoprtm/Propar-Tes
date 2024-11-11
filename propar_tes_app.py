import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from streamlit_option_menu import option_menu  # Import library option menu

# Mengatur koneksi ke Google Sheets
def connect_to_gsheets():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        st.secrets["gcp_service_account"], scope
    )
    client = gspread.authorize(creds)
    return client

# Menyimpan data ke Google Sheets (menambah data di row yang kosong)
def save_data(data):
    client = connect_to_gsheets()
    sheet = client.open("PROPAR Tes").worksheet("Sheet1")
    
    # Mendapatkan jumlah baris yang ada pada worksheet untuk mengetahui baris kosong
    row_count = len(sheet.get_all_values())  # Menghitung jumlah baris yang ada
    
    # Menambahkan data ke baris berikutnya yang kosong
    sheet.append_row(data)
    
    return row_count + 1  # Mengembalikan nomor baris yang baru ditambahkan

# Menampilkan rules pengisian
def show_rules():
    st.subheader("Rules Pengisian Data")
    st.write("""
    1. **Pengisian sesuai dengan kaidah**:
       - Pastikan setiap kolom diisi dengan data yang sesuai dengan format yang diminta.
       - Pilih opsi yang sudah disediakan untuk pilihan yang terbatas, seperti "WK/Field" atau "System Source".
    
    2. **Data akan tersimpan**:
       - Setelah data dimasukkan dan tombol "Submit Data" ditekan, data akan langsung disimpan ke Google Sheets.
       - Pastikan untuk mengisi semua kolom yang diperlukan sebelum menyimpan data.

    3. **Jangan sembarangan**:
       - Hindari mengisi data yang tidak relevan atau tidak sesuai dengan konteks.
       - Jika Anda tidak yakin dengan nilai yang dimasukkan, konsultasikan dengan tim atau supervisor.
    """)

# Menampilkan aplikasi
st.title("PENGISIAN PROPAR ZONA 1")

# Navigasi menggunakan Streamlit Option Menu
with st.sidebar:
    menu_option = option_menu(
        "Menu",  # Menu title
        ["Rules Pengisian", "PROPAR Zona 1"],  # Menu options
        icons=["list", "plus"],  # Icon options (you can customize these icons)
        default_index=0,  # Default selected menu option (first option)
        orientation="vertical"  # Options layout
    )

# Menampilkan halaman sesuai dengan pilihan menu
if menu_option == "Rules Pengisian":
    show_rules()

if menu_option == "PROPAR Zona 1":
    st.subheader("PROPAR")

    wk_field = st.selectbox("WK/Field", ["Jambi", "Kampar", "Lirik", "Pangkalan Susu", "Rantau", "Siak"])

    # Input untuk persentase PI
    pi_percent = st.number_input("PI%", min_value=0.0, step=0.1)

    # Bagian 2: Structure/PF, berubah sesuai WK/Field yang dipilih
    structure_choices = {
        "Jambi": ["BBT", "BJG", "BTJ", "KAS", "KTB", "KTT", "PPS", "SG", "SGL", "SKB", "STT", "TPN"],
        "Kampar": ["Binio", "EKA", "Gemuruh", "Kerumutan", "Merbau", "North Merbau", "Panduk", "Parum", "Pekan"],
        "Lirik": ["Andan/Ukui", "Lirik", "Molek", "North Pulai", "Sago", "South Pulai"],
        "Pangkalan Susu": ["Benggala", "Gebang", "Paluh Tabuhan Timur", "Pantai Pakam Timur", "Pulau Panjang"],
        "Rantau": ["Kuala Dalam", "Kuala Simpang Barat", "Pematang Panjang", "Rantau", "Serang Jaya", "Sungai Buluh"],
        "Siak": ["Batang", "Lindai"]
    }
    structure = st.selectbox("Structure/PF", structure_choices[wk_field])

    # Event Date
    event_date = st.date_input("Event Date", datetime.now())

    # Bagian produksi struktur
    prod_struc_oil = st.number_input("Prod Struc Oil (BOPD)", min_value=0)
    prod_struc_gas = st.number_input("Prod Struc Gas (MMSCFD)", min_value=0.0, step=0.1)
    prod_struc_cond_pf = st.number_input("Prod Struc Condensate Structure/PF (BCPD)", min_value=0)
    prod_struc_cond_plant = st.number_input("Prod Struc Condensate Plant (BCPD)", min_value=0)

    # Input untuk Well Name
    well_name = st.text_input("Well Name (Contoh GBG-22)")

    # Lifting Method
    lifting_method = st.selectbox("Lifting Method", [
        "Electric Submersible Pump (ESP)",
        "Gas Jack Compressor",
        "Gas Lift",
        "Hydraulic Pump Unit",
        "Natural Flow",
        "Natural Flow Gas",
        "Natural Flow Oil",
        "Progressive Cavity Pump (PCP)",
        "Sucker Rod Pump (SRP)"
    ])

    # Potensi
    potensi_oil = st.number_input("Potensi Oil (BOPD)", min_value=0)
    potensi_gas = st.number_input("Potensi Gas (MMSCFD)", min_value=0.0)
    condensate = st.number_input("Condensate (BCPD)", min_value=0)
    condensate_struc_pf = st.number_input("Condensate Structure/PF (BCPD)", min_value=0)
    condensate_plant = st.number_input("Condensate Plant (BCPD)", min_value=0)

    # Test Date
    tes_date = st.date_input("Test Date", datetime.now())

    # Operasi (Ops)
    ops_oil = st.number_input("Ops Oil (BOPD)", min_value=0)
    ops_gas = st.number_input("Ops Gas (MMSCFD)", min_value=0.0, step=0.1)
    ops_condensate = st.number_input("Ops Condensate (BCPD)", min_value=0)

    # Well Running dan Well Down Time dalam jam
    well_running_hours = st.selectbox("Well Running - Pilih waktu dalam jam", [f"{i} jam" for i in range(1, 25)])
    well_down_time_hours = st.selectbox("Well Down Time - Pilih waktu dalam jam", [f"{i} jam" for i in range(1, 25)])

    # Low
    low_oil = st.number_input("Low Oil (BOPD)", min_value=0)
    low_gas = st.number_input("Low Gas (MMSCFD)", min_value=0.0, step=0.1)
    low_condensate = st.number_input("Low Condensate (BCPD)", min_value=0)
    low_cond_struc_pf = st.number_input("Low Condensate Structure/PF (BCPD)", min_value=0)
    low_cond_plant = st.number_input("Low Condensate Plant (BCPD)", min_value=0)

    # Off
    off_oil = st.number_input("Off Oil (BOPD)", min_value=0)
    off_gas = st.number_input("Off Gas (MMSCFD)", min_value=0.0, step=0.1)
    off_condensate = st.number_input("Off Condensate (BCPD)", min_value=0)

    # System Source dan Equipment Source
    system_source = st.selectbox("System Source", ["Plant", "Reservoir", "Terminal", "Well"])
    equipment_source_options = {
        "Plant": ["Piping", "Pipeline", "Central Power Generator", "Gas Compressors", "Air Compressor", 
                "Fin Fan Cooler", "Heat Exchanger", "Tanks", "Pressure Vessel", "Pig Receiver Launcher", 
                "Instrumentation and Controls", "Pre-Production", "Safety System", "Total Assets", 
                "Structure / Platform and Civil", "Main Pump", "Pump Others", "Third Party Equipment"],
        "Reservoir": ["Gas Zone", "Oil Zone"],
        "Terminal": ["Floating Storage and Offloading", "Single Point Mooring", "Onshore Terminal", "Onshore Receiving Facility"],
        "Well": ["Progressive Cavity Pump", "Electrical Submersible Pump", "Oil Natural Flow", "Gas Natural Flow", 
                "Gas Lift", "Hydraulic Jet Pump", "Sucker Rod Pump", "Hydraulic Pumping Unit", "Plunger Lift", 
                "Injection Well", "Other Artificial Lift", "Pre-Production"]
    }
    equipment_source = st.selectbox("Equipment Source", equipment_source_options[system_source])

    # Type Cause, Family Cause, dan Parent Cause
    type_cause = st.radio("Type Cause", ["Planned", "Unplanned"])

    family_cause_options = [
        "Reservoir Intervention", "Reservoir Issues", "Well Program & Surveillance", "Well Integrity", 
        "External Issue", "Artificial Lift & Downhole Problem", "Rotating & Machinery Integrity", 
        "Inspection & Maintenance", "Static & Facility Integrity", "Process Issues", "Power & Electrical Integrity", 
        "Turn Around & Modification"
    ]
    family_cause = st.selectbox("Family Cause", family_cause_options)

    parent_cause_options = {
        "Reservoir Intervention": ["Well Surveillance / Data Acquisition / Survey / Inspection"],
        "Reservoir Issues": ["Reservoir Properties", "Formation Damage", "Pressure Depletion", "Water Cut Increase", 
                            "Gas Oil Ratio (GOR) Increase", "Formation Integrity", "Production Fluctuation", 
                            "Condensate Gas Ratio (CGR) Increase"],
        "Well Program & Surveillance": ["Well Surveillance / Data Acquisition / Survey / Inspection", "Optimization / Construction",
                                        "Project Schedule Delays", "Wells Schedule Delays", "Facilities Schedule Delays"],
        "Well Integrity": ["Well Integrity", "Flow Assurance"],
        "External Issue": ["Natural Events", "Security & Regulation", "Material Availability issue", 
                        "Curtailment / Top Tank"],
        "Artificial Lift & Downhole Problem": ["Artificial Lift Downhole Problem", "Artificial Lift Surface Equipment Problem"],
        "Rotating & Machinery Integrity": ["General Machinery Problem", "Fuel System Problem", "Optimization / Construction",
                                        "Project Schedule Delays", "Facilities Schedule Delays", "Turbomachinery Problem"],
        "Inspection & Maintenance": ["Inspection & Maintenance", "Static/Dynamic Measurement & Calculation"],
        "Static & Facility Integrity": ["Optimization / Construction", "Facility Integrity Problem", 
                                        "Project Schedule Delays", "Facilities Schedule Delays", 
                                        "Static Measurement & Calculation", "Dynamic Measurement & Calculation", 
                                        "General Machinery Problem", "Gas Measurements & Calculations"],
        "Process Issues": ["Bottle Neck", "Flow Assurance", "Water Handling Problem"],
        "Power & Electrical Integrity": ["Optimization / Construction", "Instrument & Control Systems", 
                                        "Electrical Distribution & Transmission Problem", 
                                        "Project Schedule Delays", "Facilities Schedule Delays"],
        "Turn Around & Modification": ["Turnaround"]
    }
    parent_cause = st.selectbox("Parent Cause", parent_cause_options.get(family_cause, ["N/A"]))

    child_cause_options = {
        "Artificial Lift Downhole Problem": [
            "Abrasives", "Ball And Seat", "Bumper Spring (Broken / Failure)", "Cable Problem", "Coupling / Centralizer",
            "Elastomer", "ESP Packer (Gas Tube Plugging / Leak)", "Fishing", "Gas / Liquid Lock / Pound", "Gas Lock",
            "Leak / Plugging on Nozzle (Fluid Deposit)", "Leak on Barrel Pump", "Leak on Standing / Traveling Valve",
            "Motor (Burned, Overload, High Temperature, Underload, Stall)", "Operating Valve Leaked / Plugged",
            "Others Downhole Problem", "Plunger Pump Problem (Stuck)", "Pump Problem (Corrosion, Abrasive, Scale, Stuck, Up/Downtrust)",
            "Pump Spacing", "Rod (Broken, Unscrew) Problem", "Rod String", "Rotor (Broken, Stuck, Rubbing, Etc)",
            "Stator (Wear Out, Oversize, Abrasive, Corrosion)", "Sucker Rod (Broken, Unscrew) Problem", "Unloading Valve Leaked / Plugged"
        ],
        "Artificial Lift Surface Equipment Problem": [
            "Catcher Damage", "Controller Problem", "Electrical and Instrument Problem", "Fluid Injection Pump Problem",
            "Gearbox Problem", "High Ampere", "High Pressure Hose Leak", "Indirect Impact After Power Outage", "Junction Box Problem",
            "Leak on BOP Rubber", "Leak on Stuffing Box", "Line Gas Injection Leaked / Plugged", "Low Reading", "Lubricator Problem",
            "Motor Valve Problem (Pneumatic, Leak, Valve Size, Etc)", "Others Surface Equipment Problem", "Overload",
            "Pneumatic Instrumentation Problem", "Polished Rod Problem", "Primover Problem", "Problem in Hydraulic System",
            "Sensor Problem (Velocity / Arrival Sensor)", "Switch Box Problem", "Unbalanced Counter Weight", "Unbalanced Reading",
            "Under Load", "Variable Frequency Drive (VFD) Problem", "Variable Speed Drive (VSD) Problem", "Vibration Switch Problem",
            "Wellhead Drive Problem"
        ],
        "Bottle Necking": [
            "Capacitation Limit in Facility", "Capacity Limitation in Facilities", "Others Bottle Necking",
            "Process Upset / Overcapacity"
        ],
        "Condensate Gas Ratio (CGR) Increase": [
            "Change of Bottom Hole Temperature", "Condensate Banking"
        ],
        "Curtailment / Top Tank": [
            "Buyer Low Demand", "Inaccurate Metering System Operation", "OPEC",
            "Process Disruption at Buyer / Customer Facilities", "Regulatory Change / Other", "Transportation Delay"
        ],
        "Dynamic Measurement & Calculation": [
            "Fail on Reading ASTM Table and Oil Volume Calculation", "Oil Analysis is Not Accurate"
        ],
        "Electrical Distribution & Transmission Problem": [
            "Disturbance on Offshore Transmission (Underwater Transmission Cable)",
            "Disturbance on Onshore Transmission (Electrical Pole, Transmission Cable, Etc)",
            "Disturbance on Power Supply (Internal / Eksternal)", "Electrical System Problem (Supply / Connect / Panel / Cable / Switch / JB)",
            "Electrical and Instrument Problem", "Gas Shortage", "Others Electrical Distribution & Transmission Problem"
        ],
        "Facilities Schedule Delays": [
            "Facilities Schedule Day"
        ],
        "Facility Integrity Problem": [
            "Construction Activity (SIMOPS)", "Corrosion / Thinning / Fatigue / Crack",
            "Erosion / Abrasive Prevention", "Leaks at Facility Equipment", "Others Facility Integrity Problem",
            "Problem on Hose Connection", "Structural Damage (Foundation / Skid / Frame / Shelter)"
        ],
        "Flow Assurance": [
            "Anorganic Scale (CaCO3, Mg2CO3, BaSO4)", "Fine Solids (Sand, Salt)", "Fluid not Support", "Free Water in Tanks",
            "Hydrates", "Liquid (Condensate / Hydrate)", "Not Pumping", "Organic Scale (Paraffin, Wax, Asphaltene)",
            "Others Flow Assurance Problem", "Problem on Hose Connection", "Sand Problem in Tank", "Scale / Deposit / Plugging In Production Pipeline",
            "Sludge / Wax in Tank", "Solid Particles in Pipeline", "Water handling problem"
        ],
        "Formation Damage": [
            "Anorganic Scale (CaCO3, Mg2CO3, BaSO4)", "Drilling Damage (Clay Swelling, Mud Filtrate Skin)",
            "Fine Solids (Sand, Salt)", "Organic Scale (Paraffin, Wax, Asphaltene)"
        ],
        "Formation Integrity": [
            "Cap Rock Failure", "Fault Failure", "Induced Fracture"
        ],
        "Fuel System Problem": [
            "Gas Shortage", "High Impurities Composition", "Low Calorific / Heat Gas Value", "Others Fuel System Problem"
        ],
        "Gas Measurements & Calculations": [
            "Fail on Reading TABLE AGA-3, AGA-7, AGA-9, Gas Rate Calculation", "Gas Analysis is Not Accurate",
            "Inaccurate Metering System Operation"
        ],
        "Gas Oil Ratio (GOR) Increase": [
            "Gas Breakthrough", "Gas Cap Expansion", "Gas Coning", "Poor Cement Bonding", "Saturated Reservoir (Pr below Pb)"
        ],
        "General Machinery Problem": [
            "Anomaly Temperature", "Electrical and Instrument Problem", "High Vibration", "Others General Machinery Problem",
            "Problem in Lubrication System", "Problem in Mechanical System", "Problem on Hose Connection",
            "Problem on Process Supply (Water / Air / Rate / Volume / Pressure / Temperature / Density)",
            "Problem with Cooling & Sealing Air System", "Vibration Monitoring"
        ],
        "Inspection & Maintenance": [
            "Fail on Reading TABLE AGA-3, AGA-7, AGA-9, Gas Rate Calculation", "Failure in Control Room Building",
            "Modifications / Upgrade", "New Installation", "Others Inspection & Maintenance",
            "Planned Repair Work (TAR)", "PM / Inspection / Testing / Recertification Jobs",
            "Predictive Maintenance (PdM) Jobs", "Safety Testing", "Solid / Debris / Plug", "Well Testing"
        ],
        "Instrument & Control Systems": [
            "Air Supply (Engine Starting) Problem", "Automation Control / Safety Device problem",
            "Field Instrument (PI, TI, PT, TT, FT, meter unit) Problem", "Malfunction Fire Gas System (False Alarm, Fire Gas Detector)",
            "Metering System Problem & Expired", "Others Instrument & Control System Problem", "Pneumatic Instrumentation Problem",
            "Tubing Instrument & Connection Problem", "Wiring Instrumentation System Problem"
        ],
        "Material Availability Issue": [
            "Contract Issue", "Material / Tools / Equipment / Transport, etc", "Supply Gas Limitation", "Support Boat Problem"
        ],
        "Natural Events": [
            "Earthquake / Landslide / Subsidence", "Lightning", "Others Natural Event", "Safety and Environmental",
            "Seas / Waves", "Weather / Storms / Floods", "Wild Fires", "Wildlife / Animal Disturbance"
        ],
        "Optimization / Construction": [
            "Capacity Change", "Change of Choke / Bean size", "Corrosion / Thinning / Fatigue / Crack",
            "Erosion / Abrasive Prevention", "Fishing", "Modifications / Upgrade", "New Installation", "Replacement Artificial Lift",
            "Replacement Tubular", "SIMOPS On Well Work", "Treating - Emulsion", "Treating - Hydrates", "Treating - Paraffin",
            "Treating - Scale", "Well Services", "Workover"
        ],
        "Pressure Depletion": [
            "Change of Reservoir Drive Mechanism", "Gas Shortage", "Injectivity Problems",
            "Reservoir Pressure Decline", "Small Compartmentalization"
        ],
        "Production Fluctuation": [
            "Production Fluctuation"
        ],
        "Project Schedule Delays": [
            "Project Schedule Delays"
        ],
        "Reservoir Properties": [
            "Heavy Oil / Highly Viscous Oil / Congealing", "Low Permeability / Low Influx"
        ],
        "Security & Regulation": [
            "Authority Restrictions", "Environmental Permits / Limits", "Leaks at Facility Equipment",
            "Material / Tools / Equipment / Transport, etc", "Others Security & Regulation",
            "Sabotage / Security Breach / Stealing / Fire", "Social Problem", "Support Boat Problem"
        ],
        "Static / Dynamic Measurement & Calculation": [
            "Fail on Reading ASTM Table and Oil Volume Calculation", "Inaccurate Measurement of Level & Oil Temperature in Tanks",
            "Inaccurate Metering System Operation", "Inaccurate Vessel Positioning (Draft, Inclination)",
            "Inappropriate Oil Sampling in Floating Tanks", "Measuring Instrument in Tanks and Labs Below The Standard",
            "Oil Analysis is not Accurate", "Problem on Measurement / Instrument Tools in Tank & Labs / Expired"
        ],
        "Static Measurement & Calculation": [
            "Inaccurate Measurement of Level & Oil Temperature in Tanks", "Inaccurate Vessel Positioning (Draft, Inclination)",
            "Inappropriate Oil Sampling in Floating Tanks"
        ],
        "Turbomachinery Problem": [
            "Air Inlet System Problem",
            "Anomaly Temperature",
            "High Vibration",
            "Problem in Hydraulic System",
            "Problem in Lubrication System",
            "Problem in Mechanical System",
            "Problem on Process Supply (Water / Air / Rate / Volume / Pressure / Temperature / Density)",
            "Problem with Cooling & Sealing Air System"
        ],
        "Turnaround & Modification": [
            "Turnaround"
        ],
        "Water Cut Increase": [
            "Liquid Hold Up / Liquid Loading",
            "Poor Cement Bonding",
            "Water Blocking",
            "Water Breakthrough",
            "Water Channeling",
            "Water Coning"
        ],
        "Water Handling Problem": [
            "Problem on Oil dehydration process",
            "Wastewater Quality Below The Standard"
        ],
        "Well Integrity": [
            "Anorganic Scale (CaCO3, Mg2CO3, BaSO4)",
            "Fine Solids (Sand, Salt)",
            "Hydrates",
            "Leak / Corroded On Production Pipe (RPP, Packer, SSDV, Tubing Liner, Downhole Central Line)",
            "Leak / Corrosion on Casing (Surface / Intermediate / Production Casing / Liner)",
            "Leak / Corrosion on Wellhead & XM Tree (C / W Accessories)",
            "Maximum Allowable Annulus Surface Pressure (MAASP)",
            "Maximum Allowable Surface Pressure (MASP)",
            "Maximum Allowable Wellhead Operating Pressure (MAWOP)",
            "Organic Scale (Paraffin, Wax, Asphaltene)",
            "Poor Cement Bonding"
        ],
        "Well Surveillance / Data Acquisition / Survey / Inspection": [
            "Caliper / Corrosion / Restriction",
            "Compliance Testing",
            "Depth / Fill",
            "Logging",
            "Others Log or Survey",
            "PLT / Temperature / Tracer",
            "Pressure Survey",
            "Saturation",
            "Static, Flowing, Temperature, Bottom Hole Pressure (BHP Survey) Measurement",
            "Temperature Survey",
            "Vertical Seismic Profile Log",
            "Well Testing"
        ],
        "Wells Schedule Delays": [
            "Wells Schedule Delays"
        ]
    }

    child_cause = st.selectbox("Child Cause", child_cause_options.get(parent_cause, ["N/A"]))

    # Diagnostic Status, Priority, Remedial Status
    diagnostic_status = st.selectbox("Diagnostic Status", ["Approved", "Blanks"])
    priority = st.selectbox("Priority", ["Drop", "High", "Medium"])
    remedial_status = st.selectbox("Remedial Status", ["Approved", "Blanks"])
    asking_for_help = st.selectbox("Asking for Help", ["Yes", "No"])
    tracking_remedial_status = st.selectbox("Tracking Remedial Status", ["Closed", "Job in Progress", "Job Issue", "Job Overdue"])

    # Jika tombol submit ditekan, data akan ditambahkan ke Google Sheets
    if st.button("Simpan Data"):
        data = [
            wk_field, 
            pi_percent, 
            structure,
            event_date.strftime('%Y-%m-%d'), 
            prod_struc_oil, 
            prod_struc_gas, 
            prod_struc_cond_pf,
            prod_struc_cond_plant,
            well_name,
            lifting_method,
            potensi_oil,
            potensi_gas,
            condensate,
            condensate_struc_pf,
            condensate_plant,
            tes_date.strftime('%Y-%m-%d'),
            ops_oil,
            ops_gas,
            ops_condensate,
            well_running_hours,
            well_down_time_hours,
            low_oil,
            low_gas,
            low_condensate,
            low_cond_struc_pf,
            low_cond_plant,
            off_oil,
            off_gas,
            off_condensate,
            system_source, 
            equipment_source,
            type_cause, 
            family_cause,
            parent_cause,
            child_cause,
            diagnostic_status,
            priority,
            remedial_status,
            asking_for_help,
            tracking_remedial_status
        ]
        save_data(data)
