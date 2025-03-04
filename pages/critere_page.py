from nicegui import ui
from models.models import CritereProfilage

def create_critere_page(app_state):
    """Create the critere management page"""
    with ui.card().classes('w-full'):
        ui.label('Manage Critères').classes('text-h6')
        
        critere_list = ui.refreshable(create_critere_list)
        # Organisme selector
        org_selector = ui.select(
            label='Select Organisme',
            options=[],
            with_input=True,
            on_change=lambda e: update_selected_organisme(app_state, e.value)
        )
        
        # Billet selector (dependent on organisme)
        billet_selector = ui.select(
            label='Select Billet',
            options=[],
            with_input=True,
            on_change=lambda e: update_selected_billet(app_state, e.value)
        )
        billet_selector.disable()
        
        # Add critere button (disabled if no billet selected)
        add_critere_button = ui.button(
            'Add New Critère', 
            on_click=lambda: open_critere_form(app_state)
        )
        add_critere_button.disable()
        
        # Define update_button_state BEFORE it's called
        def update_button_state():
            if app_state.selected_billet is None:
                add_critere_button.disable()
            else:
                add_critere_button.enable()
        
        # Function to update organisme selector options
        def update_org_options():
            options = [(org.id_organisme, org.nom_organisme) for org in app_state.session.list_organismes]
            org_selector.options = options
            if not options:
                org_selector.value = None
                app_state.selected_organisme = None
                app_state.selected_billet = None
                update_billet_options()
        
        # Function to update billet selector options
        def update_billet_options():
            if app_state.selected_organisme:
                options = [(billet.id_billet, billet.nom_billet) for billet in app_state.selected_organisme.list_billets]
                billet_selector.options = options
                billet_selector.enable()
                if not options:
                    billet_selector.value = None
                    app_state.selected_billet = None
            else:
                billet_selector.options = []
                billet_selector.disable()
                billet_selector.value = None
                app_state.selected_billet = None
            
            update_button_state()
            critere_list.refresh(app_state)
        
        update_org_options()

        # Add critere button (disabled if no billet selected)
        add_critere_button = ui.button(
            "Add New Critère",
            on_click=lambda: open_critere_form(app_state),
            
        ).disable()

        # Update button state based on selections
        def update_button_state():
            if app_state.selected_billet is None :
                add_critere_button.disable()
            else :
                add_critere_button.enable()

        # Function to handle organisme selection
        def update_selected_organisme(app_state, org_id):
            if org_id:
                app_state.selected_organisme = app_state.session.get_organisme_by_id(
                    org_id
                )
                app_state.selected_billet = None
                update_billet_options()
            else:
                app_state.selected_organisme = None
                app_state.selected_billet = None
                update_billet_options()

        # Function to handle billet selection
        def update_selected_billet(app_state, billet_id):
            if billet_id and app_state.selected_organisme:
                app_state.selected_billet = (
                    app_state.selected_organisme.get_billet_by_id(billet_id)
                )
                update_button_state()
                critere_list.refresh(app_state)
            else:
                app_state.selected_billet = None
                update_button_state()
                critere_list.refresh(app_state)

        # Refresh buttons
        with ui.row():
            ui.button("Refresh Organismes", on_click=update_org_options)
            ui.button("Refresh Billets", on_click=update_billet_options)

    # Add a refreshable critere list component
    critere_list = ui.refreshable(create_critere_list)
    critere_list(app_state)


@ui.refreshable
def create_critere_list(app_state):
    """Create a list of critères for the selected billet"""
    with ui.card().classes("w-full"):
        if app_state.selected_billet is None:
            ui.label("Please select an organisme and billet to see critères").classes(
                "text-italic"
            )
        elif not app_state.selected_billet.list_criteres_profilages:
            ui.label(
                f"No critères added for billet: {app_state.selected_billet.nom_billet}"
            ).classes("text-italic")
        else:
            ui.label(
                f"Critères for billet: {app_state.selected_billet.nom_billet}"
            ).classes("text-bold")
            with ui.table(rows=[]).classes('w-full'):
                with ui.thead():
                    with ui.tr():
                        ui.th().text("ID")
                        ui.th().text("Nom")
                        ui.th().text("Tranches")
                        ui.th().text("Actions")
                with ui.tbody():
                    for critere in app_state.selected_billet.list_criteres_profilages:
                        with ui.tr():
                            ui.td().text(critere.id_critere_profilage)
                            ui.td().text(critere.nom_critere_profilage)
                            ui.td().text(critere.count_tranche())
                            with ui.td():
                                with ui.row():
                                    ui.button(
                                        "Edit",
                                        size="sm",
                                        on_click=lambda c=critere: open_critere_form(
                                            app_state, c
                                        ),
                                    )
                                    ui.button(
                                        "Delete",
                                        size="sm",
                                        color="red",
                                        on_click=lambda c=critere: delete_critere(
                                            app_state, c
                                        ),
                                    )


def open_critere_form(app_state, critere=None):
    """Open a form to add or edit a critère"""
    if app_state.selected_billet is None and critere is None:
        ui.notify("Please select a billet first", type="warning")
        return

    is_edit = critere is not None

    with ui.dialog() as dialog, ui.card().classes("w-96"):
        ui.label(f'{"Edit" if is_edit else "Add New"} Critère de Profilage').classes(
            "text-h6"
        )

        if is_edit:
            ui.label(f"For Billet: {app_state.selected_billet.nom_billet}")

        # Form fields
        nom = ui.input(
            "Nom Critère", value=critere.nom_critere_profilage if is_edit else ""
        )

        with ui.row():
            ui.button("Cancel", on_click=dialog.close)
            ui.button(
                "Save",
                on_click=lambda: save_critere(
                    app_state, nom.value, dialog, critere if is_edit else None
                ),
            )

    dialog.open()


def save_critere(app_state, nom, dialog, existing_critere=None):
    """Save a critère (add new or update existing)"""
    if not nom:
        ui.notify("Nom Critère is required", type="negative")
        return

    if existing_critere:
        # Update existing
        existing_critere.nom_critere_profilage = nom
    else:
        # Create new
        new_critere = CritereProfilage(nom_critere_profilage=nom)
        app_state.selected_billet.list_criteres_profilages.append(new_critere)

    dialog.close()
    create_critere_list.refresh(app_state)
    ui.notify(
        f'Critère {"updated" if existing_critere else "added"} successfully',
        type="positive",
    )


def delete_critere(app_state, critere):
    """Delete a critère after confirmation"""
    with ui.dialog() as dialog, ui.card():
        ui.label(f"Delete Critère: {critere.nom_critere_profilage}?").classes("text-h6")
        ui.label("This will also delete all associated tranches.")

        with ui.row():
            ui.button("Cancel", on_click=dialog.close)
            ui.button(
                "Delete",
                color="red",
                on_click=lambda: confirm_delete_critere(app_state, critere, dialog),
            )

    dialog.open()


def confirm_delete_critere(app_state, critere, dialog):
    """Confirm and process critère deletion"""
    app_state.selected_billet.list_criteres_profilages.remove(critere)
    dialog.close()
    create_critere_list.refresh(app_state)
    ui.notify("Critère deleted successfully", type="positive")
