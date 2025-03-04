from nicegui import ui
import pandas as pd

def create_summary_page(app_state):
    """Create the summary page showing the overall configuration"""
    with ui.card().classes('w-full'):
        ui.label('Configuration Summary').classes('text-h6')
        
        # Add refresh button
        ui.button('Refresh Summary', on_click=lambda: summary_content.refresh(app_state))
        
        # Add export configuration button
        ui.button('Export Configuration', on_click=lambda: export_configuration(app_state))
    
    # Add a refreshable summary content component
    summary_content = ui.refreshable(create_summary_content)
    summary_content(app_state)

@ui.refreshable
def create_summary_content(app_state):
    """Create the summary content showing the hierarchical configuration"""
    with ui.card().classes('w-full'):
        org_count = len(app_state.session.list_organismes)
        
        if org_count == 0:
            ui.label('No configuration data available').classes('text-italic')
            return
        
        # Count totals
        billet_count = sum(org.count_billet() for org in app_state.session.list_organismes)
        critere_count = sum(sum(b.count_critere() for b in org.list_billets) for org in app_state.session.list_organismes)
        tranche_count = sum(sum(sum(c.count_tranche() for c in b.list_criteres_profilages) for b in org.list_billets) for org in app_state.session.list_organismes)
        
        # Display counts
        ui.label(f'Total Organismes: {org_count}')
        ui.label(f'Total Billets: {billet_count}')
        ui.label(f'Total Critères: {critere_count}')
        ui.label(f'Total Tranches: {tranche_count}')
        
        # Display hierarchical configuration
        for org in app_state.session.list_organismes:
            with ui.expansion(f"{org.nom_organisme} ({org.count_billet()} billets)").classes('w-full'):
                ui.label(f'ID: {org.id_organisme}')
                ui.label(f'Code Mobilisation: {org.code_mobilisation}')
                ui.label(f'Colonne Mobilisation: {org.colonne_mob_billet}')
                ui.label(f'Permanence Créances: {"Oui" if org.permanence_creances else "Non"}')
                
                if org.list_billets:
                    ui.label('Billets:').classes('font-bold mt-2')
                    for billet in org.list_billets:
                        with ui.expansion(f"{billet.nom_billet} ({billet.count_critere()} critères)").classes('w-full ml-4'):
                            ui.label(f'ID: {billet.id_billet}')
                            ui.label(f'Montant Cible: {billet.montant_cible_billet:.2f}')
                            
                            if billet.list_criteres_profilages:
                                ui.label('Critères:').classes('font-bold mt-2')
                                for critere in billet.list_criteres_profilages:
                                    with ui.expansion(f"{critere.nom_critere_profilage} ({critere.count_tranche()} tranches)").classes('w-full ml-4'):
                                        ui.label(f'ID: {critere.id_critere_profilage}')
                                        
                                        if critere.list_tranches:
                                            ui.label('Tranches:').classes('font-bold mt-2')
                                            with ui.table(rows=[]).classes('w-full'):
                                                with ui.thead():
                                                    with ui.tr():
                                                        ui.th().text('ID')
                                                        ui.th().text('Nom')
                                                        ui.th().text('Condition')
                                                        ui.th().text('Pourcentage')
                                                        ui.th().text('Priorité')
                                                with ui.tbody():
                                                    for tranche in critere.list_tranches:
                                                        with ui.tr():
                                                            ui.td().text(tranche.id_tranche)
                                                            ui.td().text(tranche.nom_tranche)
                                                            ui.td().text(tranche.condition_tranche)
                                                            ui.td().text(f"{tranche.pourcentage_tranche:.2f}%" if tranche.pourcentage_tranche is not None else "N/A")
                                                            ui.td().text(str(tranche.priorite_tranche) if tranche.priorite_tranche is not None else "N/A")

def export_configuration(app_state):
    """Export the current configuration to a JSON file"""
    import json
    from datetime import datetime
    
    # Convert objects to serializable dictionaries
    def obj_to_dict(obj):
        if hasattr(obj, '__dict__'):
            result = {}
            for key, value in obj.__dict__.items():
                if isinstance(value, list):
                    result[key] = [obj_to_dict(item) for item in value]
                elif isinstance(value, pd.DataFrame):
                    # Skip DataFrames or convert to dict if needed
                    continue
                else:
                    result[key] = value
            return result
        return obj
    
    # Try to serialize the session object
    try:
        session_dict = obj_to_dict(app_state.session)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"config_export_{timestamp}.json"
        
        # Write to file
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(session_dict, f, indent=2, ensure_ascii=False)
        
        ui.notify(f"Configuration exported to {filename}", type="positive")
    except Exception as e:
        ui.notify(f"Export failed: {str(e)}", type="negative")