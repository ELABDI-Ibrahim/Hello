from nicegui import ui
from models.models import Tranche


def create_tranche_page(app_state):
    # Create refreshable component first
    tranche_list = ui.refreshable(create_tranche_list)

    with ui.card().classes("w-full"):
        ui.label("Manage Tranches").classes("text-h6")

        # Create selectors without disabled parameter
        org_selector = ui.select(
            label="Select Organisme",
            options=[],
            with_input=True,
            on_change=lambda e: update_selected_organisme(app_state, e.value),
        )

        billet_selector = ui.select(
            label="Select Billet",
            options=[],
            with_input=True,
            on_change=lambda e: update_selected_billet(app_state, e.value),
        )
        billet_selector.disable()  # Disable after creation

        critere_selector = ui.select(
            label="Select Critère",
            options=[],
            with_input=True,
            on_change=lambda e: update_selected_critere(app_state, e.value),
        )
        critere_selector.disable()  # Disable after creation

        add_tranche_button = ui.button(
            "Add New Tranche", on_click=lambda: open_tranche_form(app_state)
        )
        add_tranche_button.disable()

        # Define functions in the right order
        def update_button_state():
            if app_state.selected_critere is None:
                add_tranche_button.disable()
            else:
                add_tranche_button.enable()

        def update_critere_options():
            if app_state.selected_billet:
                options = [
                    (critere.id_critere_profilage, critere.nom_critere_profilage)
                    for critere in app_state.selected_billet.list_criteres_profilages
                ]
                critere_selector.options = options
                critere_selector.enable()
                if not options:
                    critere_selector.value = None
                    app_state.selected_critere = None
            else:
                critere_selector.options = []
                critere_selector.disable()
                critere_selector.value = None
                app_state.selected_critere = None

            update_button_state()
            tranche_list.refresh(app_state)

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
                app_state.selected_billet = None
                app_state.selected_critere = None
                update_billet_options()

        # Function to update billet selector options
        def update_billet_options():
            if app_state.selected_organisme:
                options = [
                    (billet.id_billet, billet.nom_billet)
                    for billet in app_state.selected_organisme.list_billets
                ]
                billet_selector.options = options
                billet_selector.enable()
                if not options:
                    billet_selector.value = None
                    app_state.selected_billet = None
                    app_state.selected_critere = None
            else:
                billet_selector.options = []
                billet_selector.disable()
                billet_selector.value = None
                app_state.selected_billet = None
                app_state.selected_critere = None

            update_critere_options()

        # Function to update critère selector options
        def update_critere_options():
            if app_state.selected_billet:
                options = [
                    (critere.id_critere_profilage, critere.nom_critere_profilage)
                    for critere in app_state.selected_billet.list_criteres_profilages
                ]
                critere_selector.options = options
                critere_selector.enable()
                if not options:
                    critere_selector.value = None
                    app_state.selected_critere = None
            else:
                critere_selector.options = []
                critere_selector.disable()
                critere_selector.value = None
                app_state.selected_critere = None

            update_button_state()
            tranche_list.refresh(app_state)

        update_org_options()

        # Add tranche button (disabled if no critère selected)
        add_tranche_button = ui.button(
            "Add New Tranche",
            on_click=lambda: open_tranche_form(app_state),
        ).disable()

        # Update button state based on selections
        def update_button_state():
            if app_state.selected_critere is None:
                add_tranche_button.disable()
            else:
                add_tranche_button.enable()

        # Function to handle organisme selection
        def update_selected_organisme(app_state, org_id):
            if org_id:
                app_state.selected_organisme = app_state.session.get_organisme_by_id(
                    org_id
                )
                app_state.selected_billet = None
                app_state.selected_critere = None
                update_billet_options()
            else:
                app_state.selected_organisme = None
                app_state.selected_billet = None
                app_state.selected_critere = None
                update_billet_options()

        # Function to handle billet selection
        def update_selected_billet(app_state, billet_id):
            if billet_id and app_state.selected_organisme:
                app_state.selected_billet = (
                    app_state.selected_organisme.get_billet_by_id(billet_id)
                )
                app_state.selected_critere = None
                update_critere_options()
            else:
                app_state.selected_billet = None
                app_state.selected_critere = None
                update_critere_options()

        # Function to handle critère selection
        def update_selected_critere(app_state, critere_id):
            if critere_id and app_state.selected_billet:
                app_state.selected_critere = (
                    app_state.selected_billet.get_critere_by_id(critere_id)
                )
                update_button_state()
                tranche_list.refresh(app_state)
            else:
                app_state.selected_critere = None
                update_button_state()
                tranche_list.refresh(app_state)

        # Refresh buttons
        with ui.row():
            ui.button("Refresh Organismes", on_click=update_org_options)
            ui.button("Refresh Billets", on_click=update_billet_options)
            ui.button("Refresh Critères", on_click=update_critere_options)

    # Add a refreshable tranche list component
    tranche_list = ui.refreshable(create_tranche_list)
    tranche_list(app_state)


@ui.refreshable
def create_tranche_list(app_state):
    """Create a list of tranches for the selected critère"""
    with ui.card().classes("w-full"):
        if app_state.selected_critere is None:
            ui.label(
                "Please select an organisme, billet, and critère to see tranches"
            ).classes("text-italic")
        elif not app_state.selected_critere.list_tranches:
            ui.label(
                f"No tranches added for critère: {app_state.selected_critere.nom_critere_profilage}"
            ).classes("text-italic")
        else:
            ui.label(
                f"Tranches for critère: {app_state.selected_critere.nom_critere_profilage}"
            ).classes("text-bold")
            with ui.table(rows=[]).classes('w-full'):
                with ui.thead():
                    with ui.tr():
                        ui.th().text("ID")
                        ui.th().text("Nom")
                        ui.th().text("Condition")
                        ui.th().text("Pourcentage")
                        ui.th().text("Priorité")
                        ui.th().text("Actions")
                with ui.tbody():
                    for tranche in app_state.selected_critere.list_tranches:
                        with ui.tr():
                            ui.td().text(tranche.id_tranche)
                            ui.td().text(tranche.nom_tranche)
                            ui.td().text(tranche.condition_tranche)
                            ui.td().text(
                                f"{tranche.pourcentage_tranche:.2f}%"
                                if tranche.pourcentage_tranche is not None
                                else "N/A"
                            )
                            ui.td().text(
                                str(tranche.priorite_tranche)
                                if tranche.priorite_tranche is not None
                                else "N/A"
                            )
                            with ui.td():
                                with ui.row():
                                    ui.button(
                                        "Edit",
                                        size="sm",
                                        on_click=lambda t=tranche: open_tranche_form(
                                            app_state, t
                                        ),
                                    )
                                    ui.button(
                                        "Delete",
                                        size="sm",
                                        color="red",
                                        on_click=lambda t=tranche: delete_tranche(
                                            app_state, t
                                        ),
                                    )


def open_tranche_form(app_state, tranche=None):
    """Open a form to add or edit a tranche"""
    if app_state.selected_critere is None and tranche is None:
        ui.notify("Please select a critère first", type="warning")
        return

    is_edit = tranche is not None

    with ui.dialog() as dialog, ui.card().classes("w-96"):
        ui.label(f'{"Edit" if is_edit else "Add New"} Tranche').classes("text-h6")

        if is_edit:
            ui.label(f"For Critère: {app_state.selected_critere.nom_critere_profilage}")

        # Form fields
        nom = ui.input("Nom Tranche", value=tranche.nom_tranche if is_edit else "")
        condition = ui.input(
            "Condition Tranche", value=tranche.condition_tranche if is_edit else ""
        )
        pourcentage = ui.number(
            "Pourcentage Tranche",
            value=(
                tranche.pourcentage_tranche
                if is_edit and tranche.pourcentage_tranche is not None
                else 0.0
            ),
        )
        priorite = ui.number(
            "Priorité Tranche",
            value=(
                tranche.priorite_tranche
                if is_edit and tranche.priorite_tranche is not None
                else 1
            ),
            format="%d",
        )

        with ui.row():
            ui.button("Cancel", on_click=dialog.close)
            ui.button(
                "Save",
                on_click=lambda: save_tranche(
                    app_state,
                    nom.value,
                    condition.value,
                    pourcentage.value,
                    int(priorite.value),
                    dialog,
                    tranche if is_edit else None,
                ),
            )

    dialog.open()


def save_tranche(
    app_state, nom, condition, pourcentage, priorite, dialog, existing_tranche=None
):
    """Save a tranche (add new or update existing)"""
    if not nom:
        ui.notify("Nom Tranche is required", type="negative")
        return

    if existing_tranche:
        # Update existing
        existing_tranche.nom_tranche = nom
        existing_tranche.condition_tranche = condition
        existing_tranche.pourcentage_tranche = pourcentage
        existing_tranche.priorite_tranche = priorite
    else:
        # Create new
        new_tranche = Tranche(
            nom_tranche=nom,
            condition_tranche=condition,
            pourcentage_tranche=pourcentage,
            priorite_tranche=priorite,
        )
        app_state.selected_critere.list_tranches.append(new_tranche)

    dialog.close()
    create_tranche_list.refresh(app_state)
    ui.notify(
        f'Tranche {"updated" if existing_tranche else "added"} successfully',
        type="positive",
    )


def delete_tranche(app_state, tranche):
    """Delete a tranche after confirmation"""
    with ui.dialog() as dialog, ui.card():
        ui.label(f"Delete Tranche: {tranche.nom_tranche}?").classes("text-h6")

        with ui.row():
            ui.button("Cancel", on_click=dialog.close)
            ui.button(
                "Delete",
                color="red",
                on_click=lambda: confirm_delete_tranche(app_state, tranche, dialog),
            )

    dialog.open()


def confirm_delete_tranche(app_state, tranche, dialog):
    """Confirm and process tranche deletion"""
    app_state.selected_critere.list_tranches.remove(tranche)
    dialog.close()
    create_tranche_list.refresh(app_state)
    ui.notify("Tranche deleted successfully", type="positive")
