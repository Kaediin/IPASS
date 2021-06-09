import csv
import random

from dataclasses import dataclass

TRAIT_KEYWORDS = ['Aanzien', 'Beheerst', 'Behoudend', 'Belangstellend', 'Bemiddelaar', 'Bestuurder', 'Betrokken',
                  'Carriere', 'Commerciele_instelling', 'Communiceren', 'Competitie', 'Constructief', 'Contactgericht',
                  'Controleur', 'Coordinator', 'Doelgericht', 'Doortastend', 'Energiek', 'Evenwichtig', 'Expertise',
                  'Extravert', 'Flexibiliteit', 'Gedreven', 'Gefocust', 'Geinteresseerd', 'Georganiseerd',
                  'Gestructureerd', 'Helpen', 'Initiatief', 'Inlevingsvermogen', 'Innovatief', 'Innovator',
                  'Inspirerend', 'Invloed', 'Klantgerichte_instelling', 'Klantgerichtheid', 'Koersvast', 'Leergierig',
                  'Leiderschap', 'Leren', 'Materiele_beloning', 'Mentor', 'Moedig', 'Omgevingsbewustzijn',
                  'Ontwikkelen_van_anderen', 'Organisatiecommitment', 'Overtuigend', 'Overtuigingskracht', 'Perfectie',
                  'Plannen_en_organiseren', 'Prestatiemotivatie', 'Proactieve_instelling', 'Probleemorientatie',
                  'Probleemverkenning', 'Producent', 'Relatiebeheer', 'Relatiegericht', 'Resultaatgerichtheid',
                  'Ruimdenkend', 'Samenwerken', 'Sensatie', 'Sociaal_handig', 'Sociale_wenselijkheid', 'Stabiel',
                  'Stimulator', 'Sympathiek', 'Tactvol', 'Toegewijd', 'Tolerant', 'Verbindend', 'Vindingrijk',
                  'Vriendelijk', 'Waardering', 'Wilskrachtig', 'Zelfbeheersing', 'Zelfvertrouwen', 'Zelfverzekerd',
                  'Zingeving', 'Zorgvuldig']


@dataclass(frozen=False)
class Dataset:
    paths: list
    candidates = []

    def load(self):
        candidates_models = []
        for file in self.paths:
            with open(file, newline='') as f:
                reader = csv.reader(f, delimiter=';')
                candidates_models += [Candidate(row[0], row[1], TraitScores(*row[2:])) for i, row in enumerate(reader)
                                      if
                                      i != 0]
        self.candidates = candidates_models
        return self.candidates

    def getRandomUserEmptyTraits(self):
        candidate = random.choice(self.candidates)
        self.candidates.remove(candidate)
        for i, row in enumerate(candidate.scores.__dict__.items()):
            if i >= len(candidate.scores.__dict__) / 2:
                candidate.scores.__dict__[row[0]] = 0
        return candidate


@dataclass(frozen=False)
class TraitScores:
    Aanzien: int
    Beheerst: int
    Behoudend: int
    Belangstellend: int
    Bemiddelaar: int
    Bestuurder: int
    Betrokken: int
    Carriere: int
    Commerciele_instelling: int
    Communiceren: int
    Competitie: int
    Constructief: int
    Contactgericht: int
    Controleur: int
    Coordinator: int
    Doelgericht: int
    Doortastend: int
    Energiek: int
    Evenwichtig: int
    Expertise: int
    Extravert: int
    Flexibiliteit: int
    Gedreven: int
    Gefocust: int
    Geinteresseerd: int
    Georganiseerd: int
    Gestructureerd: int
    Helpen: int
    Initiatief: int
    Inlevingsvermogen: int
    Innovatief: int
    Innovator: int
    Inspirerend: int
    Invloed: int
    Klantgerichte_instelling: int
    Klantgerichtheid: int
    Koersvast: int
    Leergierig: int
    Leiderschap: int
    Leren: int
    Materiele_beloning: int
    Mentor: int
    Moedig: int
    Omgevingsbewustzijn: int
    Ontwikkelen_van_anderen: int
    Organisatiecommitment: int
    Overtuigend: int
    Overtuigingskracht: int
    Perfectie: int
    Plannen_en_organiseren: int
    Prestatiemotivatie: int
    Proactieve_instelling: int
    Probleemorientatie: int
    Probleemverkenning: int
    Producent: int
    Relatiebeheer: int
    Relatiegericht: int
    Resultaatgerichtheid: int
    Ruimdenkend: int
    Samenwerken: int
    Sensatie: int
    Sociaal_handig: int
    Sociale_wenselijkheid: int
    Stabiel: int
    Stimulator: int
    Sympathiek: int
    Tactvol: int
    Toegewijd: int
    Tolerant: int
    Verbindend: int
    Vindingrijk: int
    Vriendelijk: int
    Waardering: int
    Wilskrachtig: int
    Zelfbeheersing: int
    Zelfvertrouwen: int
    Zelfverzekerd: int
    Zingeving: int
    Zorgvuldig: int


@dataclass(frozen=True)
class Candidate:
    id: int
    research_id: str
    scores: TraitScores
