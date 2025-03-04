import pandas as pd
from models.models import Session

class AppState:
    def __init__(self):
        self.session = Session()
        self.data = None
        self.data_file_path = None
        self.data_file_type = None
        self.selected_organisme = None
        self.selected_billet = None
        self.selected_critere = None