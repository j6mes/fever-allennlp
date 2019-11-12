from allennlp.common import Registrable
from fever.reader import FEVERDocumentDatabase


class RetrievalMethod(Registrable):

    def __init__(self,database:FEVERDocumentDatabase):
        self.database = database

    def get_sentences_for_claim(self,claim_text,include_text=False):
        pass
