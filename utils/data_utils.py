import os
import pandas as pd
from nicegui import ui

def load_data(file_path: str, file_type: str) -> pd.DataFrame:
    """Load data from file"""
    try:
        if file_type == 'csv':
            return pd.read_csv(file_path)
        elif file_type == 'excel':
            return pd.read_excel(file_path)
        elif file_type == 'sasdat':
            # This would need the pyreadstat or another SAS reader library
            # For simplicity, let's just show an error message
            ui.notify("SAS data files require additional libraries", type="warning")
            return None
        else:
            ui.notify(f"Unsupported file type: {file_type}", type="negative")
            return None
    except Exception as e:
        ui.notify(f"Error loading file: {str(e)}", type="negative")
        return None

def handle_upload(e, app_state):
    """Handle file upload event"""
    file_path = e.name
    file_type = file_path.split('.')[-1].lower()
    
    if file_type not in ['csv', 'xlsx', 'xls', 'sas7bdat']:
        ui.notify("Please upload a CSV, Excel, or SAS data file", type="negative")
        return
    
    if file_type == 'sas7bdat':
        file_type = 'sasdat'
    elif file_type in ['xlsx', 'xls']:
        file_type = 'excel'
    
    # Save the uploaded file
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    saved_path = os.path.join(upload_dir, e.name)
    
    with open(saved_path, 'wb') as f:
        f.write(e.content)
    
    app_state.data_file_path = saved_path
    app_state.data_file_type = file_type
    
    # Load the data
    app_state.data = load_data(saved_path, file_type)
    
    if app_state.data is not None:
        ui.notify(f"File uploaded and loaded successfully: {e.name}", type="positive")
        return True
    else:
        ui.notify("Failed to load data from file", type="negative")
        return False