import os
from nicegui import ui
from pages.data_upload_page import create_data_upload_page
from pages.organisme_page import create_organisme_page
from pages.billet_page import create_billet_page
from pages.critere_page import create_critere_page
from pages.tranche_page import create_tranche_page
from pages.summary_page import create_summary_page
from utils.app_state import AppState

# Create app state
app_state = AppState()

# Ensure upload directory exists
os.makedirs("uploads", exist_ok=True)

# Create main layout with navigation
def create_main_layout():
    with ui.header().classes('bg-blue-800 text-white'):
        ui.label('Optimizer Configuration Tool').classes('text-h5 q-px-md q-py-sm')
    
    # Create tabs for navigation
    with ui.tabs().classes('w-full') as tabs:
        data_tab = ui.tab('Data Upload')
        organisme_tab = ui.tab('Organismes')
        billet_tab = ui.tab('Billets')
        critere_tab = ui.tab('Critères de Profilage')
        tranche_tab = ui.tab('Tranches')
        summary_tab = ui.tab('Summary')
    
    # Create tab panels with content
    with ui.tab_panels(tabs, value=data_tab).classes('w-full'):
        with ui.tab_panel(data_tab):
            create_data_upload_page(app_state)
        
        with ui.tab_panel(organisme_tab):
            create_organisme_page(app_state)
        
        with ui.tab_panel(billet_tab):
            create_billet_page(app_state)
        
        with ui.tab_panel(critere_tab):
            create_critere_page(app_state)
        
        with ui.tab_panel(tranche_tab):
            create_tranche_page(app_state)
        
        with ui.tab_panel(summary_tab):
            create_summary_page(app_state)

# Create and run the app
create_main_layout()

ui.run(title="Optimizer Configuration Tool", favicon="📊")