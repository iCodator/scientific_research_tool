"""
Test-Skript: Einfacher Test für alle drei Datenbank-Adapter
===========================================================

Dieses Skript testet:
1. settings.py - Konfiguration
2. pubmed.py - PubMed Adapter
3. europe_pmc.py - Europe PMC Adapter

Mit einfachen Suchanfragen und übersichtlicher Ausgabe.
"""

import sys
import os

# Füge src zum Python-Path hinzu
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.config.settings import Settings
from src.databases.pubmed import PubMedAdapter
from src.databases.europe_pmc import EuropePMCAdapter


def print_header(text):
    """Druckt einen schönen Header"""
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80)


def print_article(article, index):
    """Druckt einen Artikel übersichtlich"""
    print(f"\n📄 Artikel {index}:")
    print(f"   Titel:    {article['title'][:70]}{'...' if len(article['title']) > 70 else ''}")
    print(f"   Jahr:     {article['year']}")
    print(f"   Journal:  {article['journal'][:50]}{'...' if len(article['journal']) > 50 else ''}")
    print(f"   Autoren:  {article['authors'][:60]}{'...' if len(article['authors']) > 60 else ''}")
    print(f"   DOI:      {article['doi']}")
    print(f"   Source:   {article['source']}")
    print(f"   ID:       {article['id']}")


def test_settings():
    """Test 1: Konfiguration validieren"""
    print_header("TEST 1: Konfiguration (settings.py)")
    
    try:
        # Validierung durchführen
        Settings.validate()
        print("✅ Konfiguration erfolgreich validiert!")
        
        # Wichtige Einstellungen anzeigen
        print(f"\n📋 Konfiguration:")
        print(f"   NCBI Email:        {Settings.NCBI_EMAIL}")
        print(f"   NCBI API Key:      {'✓ gesetzt' if Settings.NCBI_API_KEY else '✗ fehlt'}")
        print(f"   Europe PMC Email:  {Settings.EUROPE_PMC_EMAIL or '(nicht gesetzt)'}")
        print(f"   Request Timeout:   {Settings.REQUEST_TIMEOUT}s")
        print(f"   Rate Limit Delay:  {Settings.RATE_LIMIT_DELAY}s")
        
        return True
        
    except Exception as e:
        print(f"❌ Fehler bei Konfiguration: {e}")
        return False


def test_pubmed():
    """Test 2: PubMed Adapter"""
    print_header("TEST 2: PubMed Adapter (pubmed.py)")
    
    try:
        # Adapter erstellen
        adapter = PubMedAdapter()
        print("✅ PubMed Adapter erfolgreich initialisiert")
        
        # Einfache Testsuche: "aspirin headache" (sollte viele Ergebnisse geben)
        query = "aspirin AND headache"
        limit = 3
        
        print(f"\n🔍 Suche nach: '{query}'")
        print(f"   Limit: {limit} Artikel")
        
        # Suche durchführen
        results = adapter.search(query, limit=limit)
        
        # Ergebnisse prüfen
        if not results:
            print("⚠️  Keine Ergebnisse gefunden (das ist ungewöhnlich)")
            return False
        
        print(f"\n✅ {len(results)} Artikel gefunden!")
        
        # Erste paar Artikel anzeigen
        for i, article in enumerate(results, 1):
            print_article(article, i)
        
        # KRITISCHER TEST: Prüfe ob DOIs gefunden wurden
        dois_found = sum(1 for a in results if a['doi'] != 'N/A')
        print(f"\n📊 DOI-Statistik:")
        print(f"   DOIs gefunden: {dois_found}/{len(results)} ({dois_found/len(results)*100:.1f}%)")
        
        if dois_found == 0:
            print("   ⚠️  WARNUNG: Keine DOIs gefunden!")
            print("   ⚠️  Möglicherweise ist der DOI-Bug noch nicht behoben!")
            return False
        else:
            print(f"   ✅ DOI-Extraktion funktioniert!")
        
        return True
        
    except Exception as e:
        print(f"❌ Fehler bei PubMed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_europe_pmc():
    """Test 3: Europe PMC Adapter"""
    print_header("TEST 3: Europe PMC Adapter (europe_pmc.py)")
    
    try:
        # Adapter erstellen
        adapter = EuropePMCAdapter()
        print("✅ Europe PMC Adapter erfolgreich initialisiert")
        
        # Einfache Testsuche
        query = "covid-19 vaccine"
        limit = 3
        
        print(f"\n🔍 Suche nach: '{query}'")
        print(f"   Limit: {limit} Artikel")
        
        # Suche durchführen
        results = adapter.search(query, limit=limit)
        
        # Ergebnisse prüfen
        if not results:
            print("⚠️  Keine Ergebnisse gefunden (das ist ungewöhnlich)")
            return False
        
        print(f"\n✅ {len(results)} Artikel gefunden!")
        
        # Erste paar Artikel anzeigen
        for i, article in enumerate(results, 1):
            print_article(article, i)
        
        # DOI-Konsistenz prüfen
        dois_found = sum(1 for a in results if a['doi'] != 'N/A')
        print(f"\n📊 DOI-Statistik:")
        print(f"   DOIs gefunden: {dois_found}/{len(results)} ({dois_found/len(results)*100:.1f}%)")
        
        # Prüfe auf leere Strings (alter Bug)
        empty_dois = sum(1 for a in results if a['doi'] == '')
        if empty_dois > 0:
            print(f"   ⚠️  WARNUNG: {empty_dois} leere DOI-Strings gefunden!")
            print(f"   ⚠️  Sollte 'N/A' sein, nicht ''")
        else:
            print(f"   ✅ DOI-Konsistenz korrekt (alle 'N/A' statt '')")
        
        return True
        
    except Exception as e:
        print(f"❌ Fehler bei Europe PMC: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Hauptfunktion: Führt alle Tests aus"""
    
    print("=" * 80)
    print("🧪 DATENBANK-ADAPTER TEST SUITE")
    print("=" * 80)
    print("\nTeste alle drei Module:")
    print("  1. settings.py     - Konfiguration")
    print("  2. pubmed.py       - PubMed Datenbank")
    print("  3. europe_pmc.py   - Europe PMC Datenbank")
    print()
    
    # Teste alle Module
    results = {
        'settings': test_settings(),
        'pubmed': test_pubmed(),
        'europe_pmc': test_europe_pmc()
    }
    
    # Finale Zusammenfassung
    print_header("FINALE ERGEBNISSE")
    
    print("\n📊 Test-Zusammenfassung:")
    print(f"   settings.py:     {'✅ BESTANDEN' if results['settings'] else '❌ FEHLGESCHLAGEN'}")
    print(f"   pubmed.py:       {'✅ BESTANDEN' if results['pubmed'] else '❌ FEHLGESCHLAGEN'}")
    print(f"   europe_pmc.py:   {'✅ BESTANDEN' if results['europe_pmc'] else '❌ FEHLGESCHLAGEN'}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n🎉 ALLE TESTS BESTANDEN!")
        print("✅ Alle Datenbank-Adapter funktionieren korrekt!")
        print("✅ Bereit für Production!")
    else:
        failed = [name for name, passed in results.items() if not passed]
        print(f"\n⚠️  {len(failed)} TEST(S) FEHLGESCHLAGEN:")
        for name in failed:
            print(f"   ❌ {name}")
        print("\n💡 Bitte Fehler oben prüfen und beheben.")
    
    print("\n" + "=" * 80)
    
    # Exit-Code setzen (0 = Erfolg, 1 = Fehler)
    sys.exit(0 if all_passed else 1)


if __name__ == '__main__':
    main()
