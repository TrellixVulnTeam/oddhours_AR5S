from lib2to3.pygram import pattern_grammar
import spacy
import spacy.cli
spacy.cli.download('es_core_news_sm')
import es_core_news_sm
from spacy.matcher import Matcher
from collections import Counter
nlp = es_core_news_sm.load()

class Story:
    
    def __init__(self, 
                text, 
                characters, 
                concepts=None, 
                distance_threshold=None):
        """ Create a Story object.
        text: a string containing the story's text
        characters: a list of strings with story's characters names
        concepts: a list of strings with story's relevant ocncepts (optional)
        distance_threshold: an integer defining a span to find connection between concepts anp characters (default: 15)
        """
        self.text = text
        self.characters = characters
        self.concepts = concepts
        self.concept_dict = []
        self.person_dict = []
        self.doc = nlp(self.text)
        self.tokens = [t.text for t in self.doc]
        self.lemmas = [t.lemma_ for t in self.doc]
        if self.concepts is None:
            concepts = dict()
            manual_filer = ['Tal', 'coser', 'pretextar', 'fijarla', 'tal', 'mandándolos', 'sonreías', 'ponerme',  'escribiéndolas', 'escribiéndola', 'retabas', 'esquiv', 'fuera', 'mandándolos', 'reconocí', 'acordarme', 'aguar', 'tenerlas', 'silenciar', 'bañar', 'oler', 'vender', 'venir', 'trabajar', 'ver', 'barrer', 'callar', 'cambiar', 'caminar', 'casar', 'cenar', 'centrar', 'coleccionar', 'consultarlos', 'cuartar', 'culpar', 'curar', 'curándolo', 'dañar', 'dejarme', 'distanciar', 'encontrar', 'entrar', 'jugar', 'llamarlos', 'mirarme', 'mirarte', 'pasar']
            for token in self.doc:
                if token.pos_ == "NOUN" and token.text not in manual_filer:
                    h = nlp(token.text)
                    if h[0].pos_ == "NOUN":
                        if token.lemma_ not in concepts.keys():
                            concepts.update({token.lemma_: token.text})
                        else:
                            concepts[token.lemma_] = token.text
            self.concepts = concepts
        if distance_threshold is None:
            self.distance_threshold = 15
        else:
            self.distance_threshold = distance_threshold     
    
    def __getitem__(self, items):
        return self.text[items]  

    @staticmethod
    def get_matcher_pattern(concept):
        return [{'LOWER':concept.lower()}]
    
    @property
    def concept_matcher(self):
        for concept in list(self.concepts.keys()):
            mt = Matcher(nlp.vocab)
            pattern = self.get_matcher_pattern(concept)
            mt.add(concept, [pattern])
            matches = mt(self.doc)
            for match_id, start, end in matches:
                string_id = nlp.vocab.strings[match_id]  # Get string representation
                self.concept_dict.append({'string_id':string_id, 'match_id':match_id, 'start':start, 'end': end})
        print(f'\n{len(self.concept_dict)} concept matches found')
        return self.concept_dict
    
    @property
    def person_matcher(self):
        for char in self.characters:
            mt = Matcher(nlp.vocab)
            pattern = self.get_matcher_pattern(char)
            mt.add(char, [pattern])
            matches = mt(self.doc)
            for match_id, start, end in matches:
                string_id = nlp.vocab.strings[match_id]  # Get string representation
                self.person_dict.append({'string_id':string_id, 'match_id':match_id, 'start':start, 'end': end})
        print(f'\n{len(self.person_dict)} person matches found')
        return self.person_dict


    def get_distances(self, sources, targets):
        index = 0
        distances = list()
        #iterate over all concepts
        for source in sources[:-1]:
            # compare with concepts that come after the given one
            for target in targets[index+1:]:
                if (source['string_id'] != target['string_id']) and (abs(source['end'] - target['start']) < self.distance_threshold):
                    link = sorted([source['string_id'], target['string_id']])
                    distances.append(link)
                else:
                    pass
        #count the number of interactions
        return Counter(map(tuple, distances)) 


    