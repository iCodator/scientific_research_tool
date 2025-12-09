# Scientific Research Tool 🔬

A Python tool for searching large scientific databases (PubMed, Europe PMC, Cochrane) with **structured queries**.

![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Status](https://img.shields.io/badge/Status-Active-green.svg)

## 🎯 What is this?

Instead of searching PubMed manually online, use this tool to programmatically search multiple scientific databases with **structured queries**:

```bash
python main.py --query "(cancer OR tumor) AND (immunotherapy OR immune checkpoint)" --source pubmed --limit 100 --output results.csv
```

## ✨ Features

- 🔍 **Multiple Databases**: PubMed (34M+ articles), Europe PMC (42M+ articles), Cochrane (Systematic Reviews)
- 📋 **Structured Queries**: AND, OR, NOT operators with proper syntax validation
- 📊 **Multiple Formats**: Export to CSV or JSON
- 🔐 **API Integration**: Optional API keys for higher rate limits
- 📝 **Full Logging**: Track all searches in automatic logs
- 🛡️ **Query Validation**: Prevents malformed searches before hitting the API
- 🌍 **Multi-language Support**: German and English documentation

## 🚀 Quick Start

### 1. Install

```bash
# Clone the repository
git clone https://github.com/yourusername/scientific_research.git
cd scientific_research

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # or: venv\Scripts\activate (Windows)

# Install dependencies
pip install -r requirements.txt
```

### 2. First Search

```bash
# Simple test query
python main.py --query "cancer AND therapy" --source pubmed --limit 10

# With export
python main.py --query "cancer AND therapy" --source pubmed --limit 50 --output results.csv
```

### 3. Complex Query

```bash
python main.py \
  --query "((cancer OR tumor) AND (therapy OR treatment)) NOT animal" \
  --source pubmed \
  --limit 100 \
  --output cancer_research.json
```

## 📚 Documentation

- **[INSTALL.md](INSTALL.md)** - Detailed installation guide for all systems
- **[QUERIES.md](QUERIES.md)** - Complete query syntax reference with examples
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - German quick overview
- **[GITHUB_SETUP.md](GITHUB_SETUP.md)** - How to set up on GitHub
- **[PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)** - File structure overview

## 📖 Usage Examples

### Basic Search

```bash
python main.py --query "cancer" --source pubmed --limit 25
```

### With Field Tags (PubMed)

```bash
python main.py \
  --query "cancer[TitleAbstract] AND 2023:2025[pdat]" \
  --source pubmed \
  --limit 100
```

### Europe PMC Search

```bash
python main.py \
  --query "TITLE_ABSTRACT:covid AND PUBYEAR:2020-2025 AND ISOPENACCESSY:Y" \
  --source europepmc \
  --limit 100
```

### Cochrane Search

```bash
python main.py --query "cancer AND immunotherapy" --source cochrane --limit 10
```

### From Query File

```bash
# Create query file
echo "(female OR woman) AND (masturbation OR self-stimulation) NOT animal" > my_query.txt

# Execute search
python main.py --query-file my_query.txt --source pubmed --output results.csv
```

## 🗄️ Supported Databases

| Database   | Source     | Size            | Access                                                              |
|-----------|------------|-----------------|------------------------------------------------------------------------|
| **PubMed** | NCBI (USA) | 34M+ articles   | [NCBI Query](https://www.ncbi.nlm.nih.gov/books/NBK3827/) via JSON API |
| **Europe PMC** | EBI (Europe) | 42M+ articles | [Europe PMC API](https://europepmc.org/api)                            |
| **Cochrane** | Europe PMC¹ | Systematic Reviews | [Europe PMC](https://europepmc.org/api) with Auto-Filter           |

¹ **Note on Cochrane**: Cochrane reviews are accessed via Europe PMC API for maximum reliability. Queries use broad search (`AND Cochrane`) with automatic client-side filtering for precision.

## 💡 Query Syntax

### Allowed Formats ✅

```bash
✅ cancer AND therapy
✅ (cancer OR tumor) AND (therapy OR treatment)
✅ cancer AND NOT animal
✅ "Coenzyme Q10" AND mitochondria
✅ cancer[TitleAbstract] AND 2020:2025[pdat]
✅ TITLE_ABSTRACT:cancer AND PUBYEAR:2020-2025
```

### NOT Allowed ❌

```bash
❌ "Which therapies are most effective for cancer?"  # Natural language questions
❌ "Benefits of acupuncture for back pain"           # Natural language statements
❌ "Is therapy A more effective than therapy B?"     # Comparisons as questions
```

See **[QUERIES.md](QUERIES.md)** for complete syntax documentation.

## 🔐 API Configuration (Optional)

Works without API keys, but limits are stricter. To get API keys:

### PubMed/NCBI

1. Go to: https://www.ncbi.nlm.nih.gov/account/
2. Sign up/login
3. Get your API key from dashboard
4. Create `config.env`:

```bash
PUBMED_API_KEY=your_api_key_here
PUBMED_EMAIL=your_email@example.com
```

### Europe PMC

1. Get key from: https://europepmc.org/api
2. Add to `config.env`:

```bash
EUROPEPMC_API_KEY=your_key_here
```

**Important**: Never commit `config.env` to GitHub! Use `config.env.template` as template.

## 📊 Output Formats

### CSV Export

```csv
title,authors,year,journal,url,abstract
"Cancer Immunotherapy","Smith J, Jones A",2024,"Nature","https://...",
"Tumor Mechanism","Brown B",2023,"Cell","https://...",
```

### JSON Export

```json
[
  {
    "title": "Cancer Immunotherapy",
    "authors": ["Smith J", "Jones A"],
    "year": 2024,
    "journal": "Nature",
    "url": "https://...",
    "abstract": "..."
  }
]
```

## 🛠️ Commands

```bash
# Show help
python main.py --help

# Simple search
python main.py --query "cancer" --source pubmed

# From file
python main.py --query-file my_query.txt --source pubmed

# With export
python main.py --query "cancer" --source pubmed --output results.csv

# Debug mode (shows logs in terminal)
python main.py --query "cancer" --source pubmed --verbose

# Custom limit
python main.py --query "cancer" --source pubmed --limit 1000
```

## ❓ FAQ

### Do I need API keys?

No, the tool works without them. But with keys, you get:
- Higher rate limits
- Faster searches
- More advanced features

### What query formats are allowed?

Only **structured queries** with AND, OR, NOT operators. Natural language questions are NOT allowed. See [QUERIES.md](QUERIES.md) for full documentation.

### How many articles can I download?

Depends on the database:
- PubMed: Up to 100,000 via API
- Europe PMC: Up to 1,000–10,000 depending on account
- Cochrane: Up to 10,000

### Where are the logs?

All searches are logged to `logs/search_*.log` automatically. Use `--verbose` flag to also see output in terminal.

### How does Cochrane differ from Europe PMC?

- **Europe PMC**: Searches all article types across 42M+ articles
- **Cochrane**: Filtered specifically for **Systematic Reviews** via automated detection (journal name + DOI prefix + title keywords)

## 🐛 Troubleshooting

### "Query validation failed"

Your query is not structured. Use AND, OR, NOT operators.

```text
❌ "What role does Coenzyme Q10 play?"
✅ "(Coenzyme Q10) AND role"
```

### "No results found"

Try:
1. Simplify the query (remove too many AND conditions)
2. Use synonyms: `(cancer OR carcinoma OR tumor)`
3. Check spelling
4. Increase the `--limit`

### "Connection timeout"

The database is not responding. Try again later or use an API key.

## 📁 Project Structure

See **[PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)** for detailed file structure documentation.

## 🤝 Contributing

We welcome contributions! See **[CONTRIBUTING.md](CONTRIBUTING.md)** for guidelines.

## 📄 License

This project is licensed under the MIT License - see **[LICENSE](LICENSE)** file for details.

## 📞 Support

- 📖 Read the [documentation](https://github.com/yourusername/scientific_research#readme)
- 🐛 Report bugs via GitHub Issues
- 💬 Discuss features in GitHub Discussions

---

**Built with ❤️ for open science** 🔬
