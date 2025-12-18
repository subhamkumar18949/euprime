# EUPrime Lead Generation & Scoring Pipeline

An automated intelligence engine designed to identify, enrich, and rank scientific researchers specializing in **3D In-Vitro models** and **Toxicology**.



## 🚀 Features
- **PubMed Automation:** Fetches the latest research data and author affiliations directly from NCBI.
- **Clay Integration:** Streams leads via Webhooks for real-time LinkedIn enrichment and verified email discovery.
- **Probability Scoring:** A custom Python-based ranking system that prioritizes leads based on scientific intent and role fit.
- **CSV Export:** Generates clean, Excel-ready datasets for business development.

## 🛠️ Project Structure
- `final_lead.py`: Fetches researchers from PubMed and sends them to the Clay Webhook.
- `scoring.py`: Processes the enriched CSV and calculates the 0-100 probability score.
- `.gitignore`: Ensures sensitive `.env` keys and local environments are not uploaded to GitHub.
- `requirements.txt`: Lists all necessary Python libraries.

