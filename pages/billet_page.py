from nicegui import ui
from models.models import Billet


def create_billet_page(app_state):
    """Create the billet management page"""
    with ui.card().classes("w-full"):
        ui.label("Manage Billets").classes("text-h6")

        # Organisme selector
        org_selector = ui.select(
            label="Select Organisme",
            options=[],
            with_input=True,
            on_change=lambda e: update_selected_organisme(app_state, e.value),
        )

        # Function to update organisme selector options
        def update_org_options():
            options = [
                (org.id_organisme, org.nom_organisme)
                for org in app_state.session.list_organismes
            ]
            org_selector.options = options
            if not options:
                org_selector.value = None
                app_state.selected_organisme = None

        update_org_options()

        # Refresh button for organisme selector
        ui.button("Refresh Organismes", on_click=update_org_options)

        # Add billet button (disabled if no organisme selected)
        add_billet_button = ui.button(
            "Add New Billet", on_click=lambda: open_billet_form(app_state)
        )
        add_billet_button.disable()

        # Update button state based on selected organisme
        def update_button_state():
            if app_state.selected_organisme is None:
                add_billet_button.disable()
            else:
                add_billet_button.enable()

        # Function to handle organisme selection
        def update_selected_organisme(app_state, org_id):
            if org_id:
                app_state.selected_organisme = app_state.session.get_organisme_by_id(
                    org_id
                )
                update_button_state()
                billet_list.refresh(app_state)
            else:
                app_state.selected_organisme = None
                update_button_state()
                billet_list.refresh(app_state)

    # Add a refreshable billet list component
    billet_list = ui.refreshable(create_billet_list)
    billet_list(app_state)


@ui.refreshable
def create_billet_list(app_state):
    """Create a list of billets for the selected organisme"""
    with ui.card().classes("w-full"):
        if app_state.selected_organisme is None:
            ui.label("Please select an organisme to see its billets").classes(
                "text-italic"
            )
        elif not app_state.selected_organisme.list_billets:
            ui.label(
                f"No billets added for organisme: {app_state.selected_organisme.nom_organisme}"
            ).classes("text-italic")
        else:
            ui.label(
                f"Billets for: {app_state.selected_organisme.nom_organisme}"
            ).classes("text-bold")
            with ui.table(rows=[]).classes('w-full'):
                with ui.thead():
                    with ui.tr():
                        ui.th().text("ID")
                        ui.th().text("Nom")
                        ui.th().text("Montant Cible")
                        ui.th().text("Critères")
                        ui.th().text("Actions")
                with ui.tbody():
                    for billet in app_state.selected_organisme.list_billets:
                        with ui.tr():
                            ui.td().text(billet.id_billet)
                            ui.td().text(billet.nom_billet)
                            ui.td().text(f"{billet.montant_cible_billet:.2f}")
                            ui.td().text(billet.count_critere())
                            with ui.td():
                                with ui.row():
                                    ui.button(
                                        "Edit",
                                        size="sm",
                                        on_click=lambda b=billet: open_billet_form(
                                            app_state, b
                                        ),
                                    )
                                    ui.button(
                                        "Delete",
                                        size="sm",
                                        color="red",
                                        on_click=lambda b=billet: delete_billet(
                                            app_state, b
                                        ),
                                    )


def open_billet_form(app_state, billet=None):
    """Open a form to add or edit a billet"""
    if app_state.selected_organisme is None and billet is None:
        ui.notify("Please select an organisme first", type="warning")
        return

    is_edit = billet is not None

    with ui.dialog() as dialog, ui.card().classes("w-96"):
        ui.label(f'{"Edit" if is_edit else "Add New"} Billet').classes("text-h6")

        if is_edit:
            ui.label(f"For Organisme: {app_state.selected_organisme.nom_organisme}")

        # Form fields
        nom = ui.input("Nom Billet", value=billet.nom_billet if is_edit else "")
        montant = ui.number(
            "Montant Cible", value=billet.montant_cible_billet if is_edit else 0.0
        )

        with ui.row():
            ui.button("Cancel", on_click=dialog.close)
            ui.button(
                "Save",
                on_click=lambda: save_billet(
                    app_state,
                    nom.value,
                    montant.value,
                    dialog,
                    billet if is_edit else None,
                ),
            )

    dialog.open()


def save_billet(app_state, nom, montant, dialog, existing_billet=None):
    """Save a billet (add new or update existing)"""
    if not nom:
        ui.notify("Nom Billet is required", type="negative")
        return

    if existing_billet:
        # Update existing
        existing_billet.nom_billet = nom
        existing_billet.montant_cible_billet = montant
    else:
        # Create new
        new_billet = Billet(nom_billet=nom, montant_cible_billet=montant)
        app_state.selected_organisme.list_billets.append(new_billet)

    dialog.close()
    create_billet_list.refresh(app_state)
    ui.notify(
        f'Billet {"updated" if existing_billet else "added"} successfully',
        type="positive",
    )


def delete_billet(app_state, billet):
    """Delete a billet after confirmation"""
    with ui.dialog() as dialog, ui.card():
        ui.label(f"Delete Billet: {billet.nom_billet}?").classes("text-h6")
        ui.label("This will also delete all associated criteria and tranches.")

        with ui.row():
            ui.button("Cancel", on_click=dialog.close)
            ui.button(
                "Delete",
                color="red",
                on_click=lambda: confirm_delete_billet(app_state, billet, dialog),
            )

    dialog.open()


def confirm_delete_billet(app_state, billet, dialog):
    """Confirm and process billet deletion"""
    app_state.selected_organisme.list_billets.remove(billet)
    dialog.close()
    create_billet_list.refresh(app_state)
    ui.notify("Billet deleted successfully", type="positive")
