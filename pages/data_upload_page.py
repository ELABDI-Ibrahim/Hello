from nicegui import ui
from utils.data_utils import handle_upload

def create_data_upload_page(app_state):
    """Create the data upload page"""
    with ui.card().classes('w-full'):
        ui.label('Upload Data File').classes('text-h6')
        ui.label('Upload a CSV, Excel, or SAS data file to use with the optimizer')
        ui.upload(
            label="Upload file", 
            auto_upload=True, 
            on_upload=lambda e: handle_upload(e, app_state)
        ).props('accept=".csv,.xlsx,.xls,.sas7bdat"')
    
    # Add a refreshable data preview component
    data_preview = ui.refreshable(create_data_preview)
    data_preview(app_state)
    
    # Add refresh button
    ui.button('Refresh Preview', on_click=lambda: data_preview.refresh(app_state))

@ui.refreshable
def create_data_preview(app_state):
    """Create a preview of the uploaded data"""
    with ui.card().classes('w-full'):
        if app_state.data is not None:
            ui.label(f"Data Preview: {app_state.data_file_path}").classes('text-h6')
            df_sample = app_state.data.head(5)
            
            # Create a table fosr preview
            with ui.table(rows=[]).classes('w-full'):
                with ui.thead():
                    with ui.tr():
                        for col in df_sample.columns:
                            ui.th().text(col)
                with ui.tbody():
                    for _, row in df_sample.iterrows():
                        with ui.tr():
                            for val in row:
                                ui.td().text(str(val))
        else:
            ui.label("No data loaded. Upload a file to see preview.").classes('text-italic')