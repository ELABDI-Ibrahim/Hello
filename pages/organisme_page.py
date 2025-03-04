from nicegui import ui
from models.models import Organisme

def create_organisme_page(app_state):
    """Create the organisme management page"""
    with ui.card().classes('w-full'):
        ui.label('Manage Organismes').classes('text-h6')
        ui.button('Add New Organisme', on_click=lambda: open_organisme_form(app_state))
    
    # Add a refreshable organisme list component
    organisme_list = ui.refreshable(create_organisme_list)
    organisme_list(app_state)

@ui.refreshable
def create_organisme_list(app_state):
    """Create a list of organismes"""
    with ui.card().classes('w-full'):
        if not app_state.session.list_organismes:
            ui.label('No organismes added').classes('text-italic')
        else:
            ui.label('Organismes List').classes('text-bold')
            table = ui.table(
                rows=[{
                    'id': org.id_organisme,
                    'nom': org.nom_organisme,
                    'billets': len(org.list_billets)
                } for org in app_state.session.list_organismes],
                columns=[
                    {'name': 'id', 'label': 'ID', 'field': 'id'},
                    {'name': 'nom', 'label': 'Nom', 'field': 'nom'},
                    {'name': 'billets', 'label': 'Billets', 'field': 'billets'},
                    {'name': 'actions', 'label': 'Actions', 'field': 'actions'},
                ]
            ).classes('w-full')
            
            # Add a custom slot for the actions column
            table.add_slot('body-cell-actions', '''
                <q-td :props="props">
                    <q-btn size="sm" label="Edit" @click="$parent.$emit('edit', props.row.id)" />
                    <q-btn size="sm" color="red" label="Delete" @click="$parent.$emit('delete', props.row.id)" />
                </q-td>
            ''')
            
            # Handle the custom events
            table.on('edit', lambda e: open_organisme_form(app_state, app_state.session.get_organisme_by_id(e.args)))
            table.on('delete', lambda e: delete_organisme(app_state, app_state.session.get_organisme_by_id(e.args)))

            
def open_organisme_form(app_state, organisme=None):
    """Open a form to add or edit an organisme"""
    is_edit = organisme is not None
    
    with ui.dialog() as dialog, ui.card().classes('w-96'):
        ui.label(f'{"Edit" if is_edit else "Add New"} Organisme').classes('text-h6')
        
        # Form fields
        nom = ui.input('Nom Organisme', value=organisme.nom_organisme if is_edit else '')
        code_mob = ui.input('Code Mobilisation', value=organisme.code_mobilisation if is_edit else '')
        colonne_mob = ui.input('Colonne Mobilisation Billet', value=organisme.colonne_mob_billet if is_edit else '')
        permanence = ui.checkbox('Permanence des Créances', value=organisme.permanence_creances if is_edit else True)
        
        with ui.row():
            ui.button('Cancel', on_click=dialog.close)
            ui.button('Save', on_click=lambda: save_organisme(
                app_state,
                nom.value, 
                code_mob.value, 
                colonne_mob.value, 
                permanence.value, 
                dialog,
                organisme if is_edit else None
            ))
    
    dialog.open()

def save_organisme(app_state, nom, code_mob, colonne_mob, permanence, dialog, existing_organisme=None):
    """Save an organisme (add new or update existing)"""
    if not nom:
        ui.notify('Nom Organisme is required', type='negative')
        return
    
    if existing_organisme:
        # Update existing
        existing_organisme.nom_organisme = nom
        existing_organisme.code_mobilisation = code_mob
        existing_organisme.colonne_mob_billet = colonne_mob
        existing_organisme.permanence_creances = permanence
    else:
        # Create new
        new_org = Organisme(
            nom_organisme=nom,
            code_mobilisation=code_mob,
            colonne_mob_billet=colonne_mob,
            permanence_creances=permanence
        )
        app_state.session.list_organismes.append(new_org)
    
    dialog.close()
    create_organisme_list.refresh(app_state)
    ui.notify(f'Organisme {"updated" if existing_organisme else "added"} successfully', type='positive')

def delete_organisme(app_state, organisme):
    """Delete an organisme after confirmation"""
    with ui.dialog() as dialog, ui.card():
        ui.label(f'Delete Organisme: {organisme.nom_organisme}?').classes('text-h6')
        ui.label('This will also delete all associated billets and criteria.')
        
        with ui.row():
            ui.button('Cancel', on_click=dialog.close)
            ui.button('Delete', color='red', on_click=lambda: confirm_delete_organisme(app_state, organisme, dialog))
    
    dialog.open()

def confirm_delete_organisme(app_state, organisme, dialog):
    """Confirm and process organisme deletion"""
    app_state.session.list_organismes.remove(organisme)
    dialog.close()
    create_organisme_list.refresh(app_state)
    ui.notify('Organisme deleted successfully', type='positive')