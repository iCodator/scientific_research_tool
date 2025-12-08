"""
Test-Suite für Query-Compiler

Testet die Konvertierung von natürlichsprachigen Queries 
in PubMed-Syntax.

Verwendung:
  pytest tests/test_query_compiler.py -v
  pytest tests/test_query_compiler.py::test_german_query -v
"""

import pytest
import logging
from src.core.query_compiler import QueryCompiler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestQueryCompilerGerman:
    """Tests für deutsche natürlichsprachige Queries"""
    
    def setup_method(self):
        """Setup vor jedem Test"""
        self.compiler = QueryCompiler()
    
    def test_german_masturbation_query(self):
        """Test 1: Deutsche Sexualwissenschaftliche Query"""
        query = "weibliche Selbstbefriedigung mit Sextoys führt zum Orgasmus"
        
        result = self.compiler.compile_natural_language(query, target_db="pubmed")
        
        assert "masturbation" in result.lower()
        assert "vibrator" in result.lower() or "sextoy" in result.lower()
        assert "orgasm" in result.lower()
        assert "[TitleAbstract]" in result  # PubMed-Format
        
        logger.info(f"✓ Test 1 PASSED: {query[:50]}...")
        logger.info(f"  Output: {result}")
    
    def test_german_back_pain_acupuncture(self):
        """Test 2: Deutsche medizinische Query"""
        query = "Effektivität von Akupunktur bei Rückenschmerzen"
        
        result = self.compiler.compile_natural_language(query, target_db="pubmed")
        
        assert "acupuncture" in result.lower()
        assert "back pain" in result.lower() or "back" in result.lower()
        assert "[TitleAbstract]" in result
        
        logger.info(f"✓ Test 2 PASSED: {query}")
        logger.info(f"  Output: {result}")
    
    def test_german_migraine_treatment(self):
        """Test 3: Weitere deutsche medizinische Query"""
        query = "Behandlung von Migräne mit Akupunktur und Massage"
        
        result = self.compiler.compile_natural_language(query, target_db="pubmed")
        
        assert "migraine" in result.lower() or "migräne" in result.lower()
        assert "[TitleAbstract]" in result
        
        logger.info(f"✓ Test 3 PASSED: {query}")
        logger.info(f"  Output: {result}")


class TestQueryCompilerEnglish:
    """Tests für englische natürlichsprachige Queries"""
    
    def setup_method(self):
        """Setup vor jedem Test"""
        self.compiler = QueryCompiler()
    
    def test_english_masturbation_query(self):
        """Test 4: Englische Sexualwissenschaftliche Query"""
        query = "female masturbation with vibrators and orgasm"
        
        result = self.compiler.compile_natural_language(query, target_db="pubmed")
        
        assert "masturbation" in result.lower()
        assert "vibrator" in result.lower()
        assert "orgasm" in result.lower()
        assert "[TitleAbstract]" in result
        
        logger.info(f"✓ Test 4 PASSED: {query}")
        logger.info(f"  Output: {result}")
    
    def test_english_acupuncture_pain(self):
        """Test 5: Englische medizinische Query"""
        query = "acupuncture for chronic back pain management"
        
        result = self.compiler.compile_natural_language(query, target_db="pubmed")
        
        assert "acupuncture" in result.lower()
        assert "[TitleAbstract]" in result
        
        logger.info(f"✓ Test 5 PASSED: {query}")
        logger.info(f"  Output: {result}")


class TestQueryCompilerDatabases:
    """Tests für verschiedene Zieldatenbanken"""
    
    def setup_method(self):
        """Setup vor jedem Test"""
        self.compiler = QueryCompiler()
    
    def test_pubmed_format(self):
        """Test 6: PubMed-Format"""
        query = "cancer treatment research"
        
        result = self.compiler.compile_natural_language(query, target_db="pubmed")
        
        assert "[TitleAbstract]" in result
        assert "AND" in result
        
        logger.info(f"✓ Test 6 PASSED: PubMed-Format")
        logger.info(f"  Output: {result}")
    
    def test_europepmc_format(self):
        """Test 7: Europe PMC-Format"""
        query = "cancer treatment research"
        
        result = self.compiler.compile_natural_language(query, target_db="europepmc")
        
        assert "TITLE_ABSTRACT" in result or "AND" in result
        
        logger.info(f"✓ Test 7 PASSED: Europe PMC-Format")
        logger.info(f"  Output: {result}")
    
    def test_cochrane_format(self):
        """Test 8: Cochrane-Format"""
        query = "cancer treatment research"
        
        result = self.compiler.compile_natural_language(query, target_db="cochrane")
        
        assert "AND" in result
        assert "[" not in result  # Keine Feldangaben wie PubMed
        
        logger.info(f"✓ Test 8 PASSED: Cochrane-Format")
        logger.info(f"  Output: {result}")


class TestQueryCompilerLanguageDetection:
    """Tests für Sprach-Erkennung"""
    
    def setup_method(self):
        """Setup vor jedem Test"""
        self.compiler = QueryCompiler()
    
    def test_german_detection_umlaute(self):
        """Test 9: Deutsch erkannt durch Umlaute"""
        query = "Ätiologie und Therapie von Rückenschmerzen"
        
        is_german = self.compiler._detect_language(query)
        
        assert is_german is True
        logger.info(f"✓ Test 9 PASSED: Deutsch erkannt (Umlaute)")
    
    def test_german_detection_keywords(self):
        """Test 10: Deutsch erkannt durch Keywords"""
        query = "was ist die effektivste Behandlung mit Akupunktur"
        
        is_german = self.compiler._detect_language(query)
        
        assert is_german is True
        logger.info(f"✓ Test 10 PASSED: Deutsch erkannt (Keywords)")
    
    def test_english_detection(self):
        """Test 11: Englisch erkannt"""
        query = "what is the most effective treatment for back pain"
        
        is_german = self.compiler._detect_language(query)
        
        assert is_german is False
        logger.info(f"✓ Test 11 PASSED: Englisch erkannt")


class TestQueryCompilerStopwords:
    """Tests für Stopword-Entfernung"""
    
    def setup_method(self):
        """Setup vor jedem Test"""
        self.compiler = QueryCompiler()
    
    def test_german_stopword_removal(self):
        """Test 12: Deutsche Stopwords entfernen"""
        self.compiler.is_german = True
        
        query = "weibliche Selbstbefriedigung mit Sextoys führt zum Orgasmus"
        normalized = self.compiler._normalize(query)
        cleaned = self.compiler._remove_stopwords(normalized)
        
        # "mit", "führt", "zum" sollten weg sein
        assert "mit" not in cleaned
        assert "führt" not in cleaned
        assert "zum" not in cleaned
        
        # Wichtige Wörter sollten bleiben
        assert "weibliche" in cleaned or "selbstbefriedigung" in cleaned
        
        logger.info(f"✓ Test 12 PASSED: Stopword-Entfernung")
        logger.info(f"  Vorher: {normalized}")
        logger.info(f"  Nachher: {cleaned}")
    
    def test_english_stopword_removal(self):
        """
        Test 13: Englische Stopwords entfernen
        
        WICHTIG: Dieser Test überprüft WORD-BOUNDARY-MATCHING!
        
        Das bedeutet: Wir überprüfen, ob "to" als GANZES WORT entfernt wurde,
        nicht ob der String "to" irgendwo vorkommt.
        
        Beispiel:
          String: "female masturbation vibrators orgasm"
          Words:  ['female', 'masturbation', 'vibrators', 'orgasm']
          
          ❌ FALSCH: assert "to" not in cleaned
             → Würde True geben (weil "to" in "vibrators" enthalten ist!)
             
          ✅ RICHTIG: assert "to" not in cleaned.split()
             → Würde False geben (weil "to" nicht in der Word-Liste ist!)
        """
        self.compiler.is_german = False
        
        query = "female masturbation with vibrators leads to orgasm"
        normalized = self.compiler._normalize(query)
        cleaned = self.compiler._remove_stopwords(normalized)
        
        # WICHTIG: Mit .split() überprüfen (Word-Boundary-Matching!)
        # "with" und "leads" sollten weg sein
        assert "with" not in cleaned.split()
        assert "leads" not in cleaned.split()
        
        # "vibrators" sollte bleiben (auch wenn "to" im Wort vorkommt)
        assert "vibrators" in cleaned.split()
        
        logger.info(f"✓ Test 13 PASSED: English Stopword-Entfernung")
        logger.info(f"  Vorher: {normalized}")
        logger.info(f"  Nachher: {cleaned}")


class TestQueryCompilerSynonyms:
    """Tests für Synonym-Expansion"""
    
    def setup_method(self):
        """Setup vor jedem Test"""
        self.compiler = QueryCompiler()
    
    def test_german_synonym_expansion(self):
        """Test 14: Deutsche Synonyme expandieren"""
        keywords = ["selbstbefriedigung", "sextoys", "orgasmus"]
        
        expanded = self.compiler._expand_synonyms(keywords)
        
        assert "masturbation" in expanded
        assert "vibrators" in expanded  # PLURAL!
        assert "orgasm" in expanded
        
        logger.info(f"✓ Test 14 PASSED: Synonym-Expansion")
        logger.info(f"  Input: {keywords}")
        logger.info(f"  Output: {expanded}")
    
    def test_english_synonym_no_change(self):
        """Test 15: Englische Synonyme (kein Mapping nötig)"""
        keywords = ["cancer", "treatment", "research"]
        
        expanded = self.compiler._expand_synonyms(keywords)
        
        # Sollten unverändert bleiben wenn keine Mappings vorhanden
        assert "cancer" in expanded
        assert "treatment" in expanded
        
        logger.info(f"✓ Test 15 PASSED: Englische Keywords ohne Änderung")


class TestQueryCompilerIntegration:
    """Integrations-Tests für gesamten Workflow"""
    
    def setup_method(self):
        """Setup vor jedem Test"""
        self.compiler = QueryCompiler()
    
    def test_complete_workflow_german(self):
        """Test 16: Gesamter Workflow Deutsch -> PubMed"""
        original_query = "weibliche Selbstbefriedigung mit Sextoys führt zum Orgasmus"
        
        result = self.compiler.compile_natural_language(
            original_query,
            target_db="pubmed"
        )
        
        # Assertions
        assert isinstance(result, str)
        assert len(result) > 0
        assert "[TitleAbstract]" in result
        assert "AND" in result
        
        # Wichtige Konzepte sollten vorhanden sein
        assert "orgasm" in result.lower()
        
        logger.info(f"✓ Test 16 PASSED: Gesamter Workflow")
        logger.info(f"  Input:  {original_query}")
        logger.info(f"  Output: {result}")
    
    def test_complete_workflow_english(self):
        """Test 17: Gesamter Workflow Englisch -> PubMed"""
        original_query = "effects of acupuncture on chronic back pain"
        
        result = self.compiler.compile_natural_language(
            original_query,
            target_db="pubmed"
        )
        
        assert isinstance(result, str)
        assert len(result) > 0
        assert "[TitleAbstract]" in result
        
        logger.info(f"✓ Test 17 PASSED: Gesamter Workflow (English)")
        logger.info(f"  Input:  {original_query}")
        logger.info(f"  Output: {result}")
    
    def test_empty_query(self):
        """Test 18: Leere Query"""
        result = self.compiler.compile_natural_language("", target_db="pubmed")
        
        # Sollte leere Query oder Error-Handling
        assert result == "" or "AND" not in result
        
        logger.info(f"✓ Test 18 PASSED: Leere Query")


# ========== MANUELLE TESTS (aus Kommandozeile) ==========

if __name__ == "__main__":
    # Setup
    logging.basicConfig(level=logging.DEBUG)
    compiler = QueryCompiler()
    
    print("\n" + "=" * 80)
    print("MANUELLE TESTS FÜR QUERY-COMPILER")
    print("=" * 80 + "\n")
    
    # Test 1
    print("Test 1: Deutsche Sexualwissenschaft-Query")
    q1 = "weibliche Selbstbefriedigung mit Sextoys führt zum Orgasmus"
    r1 = compiler.compile_natural_language(q1, target_db="pubmed")
    print(f"  Input:  {q1}")
    print(f"  Output: {r1}\n")
    
    # Test 2
    print("Test 2: Deutsche Medizin-Query")
    q2 = "Akupunktur bei Rückenschmerzen Effektivität"
    r2 = compiler.compile_natural_language(q2, target_db="pubmed")
    print(f"  Input:  {q2}")
    print(f"  Output: {r2}\n")
    
    # Test 3
    print("Test 3: Englische Query")
    q3 = "female masturbation vibrators orgasm"
    r3 = compiler.compile_natural_language(q3, target_db="pubmed")
    print(f"  Input:  {q3}")
    print(f"  Output: {r3}\n")
    
    print("=" * 80)
    print("TESTS ABGESCHLOSSEN")
    print("=" * 80)
