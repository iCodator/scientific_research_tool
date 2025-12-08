"""
Modul: Datenbank-Adapter Interface
==================================
Zweck: Definiert eine Schablone (Interface), die alle Datenbank-Module einhalten müssen.

Warum machen wir das?
Damit unser Hauptprogramm später nicht wissen muss, ob es gerade mit Europe PMC
oder PubMed spricht. Es ruft einfach immer "search()" auf.

Konzepte:
- Abstrakte Klasse (ABC): Eine Klasse, von der man keine Objekte erzeugen kann.
- Abstrakte Methode: Eine Methode, die die Kind-Klasse (z.B. EuropePMC) zwingend
  programmieren MUSS.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any

class DatabaseAdapter(ABC):
    """
    Die abstrakte Basisklasse für alle wissenschaftlichen Datenbanken.
    
    Jede neue Datenbank (z.B. PubMed), die wir hinzufügen, MUSS von dieser
    Klasse erben und die Methode 'search' implementieren.
    """

    @abstractmethod
    def search(self, query: str, limit: int = 25) -> List[Dict[str, Any]]:
        """
        Führt eine Suche in der Datenbank durch.
        
        MUSS von der erbenden Klasse überschrieben werden!
        
        Argumente:
            query (str): Die bereinigte Suchanfrage (z.B. "(A OR B) AND C")
            limit (int): Maximale Anzahl der Ergebnisse (Standard: 25)
            
        Rückgabewert:
            List[Dict]: Eine Liste von Dictionaries. Jedes Dictionary steht für
                        einen Artikel und enthält Standard-Felder wie 'title',
                        'url', 'year', etc.
        """
        pass
