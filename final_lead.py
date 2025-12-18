import os
import requests
import csv
import time
import xml.etree.ElementTree as ET
from dotenv import load_dotenv

# Load API keys from your .env file
load_dotenv()

# --- CONFIGURATION ---
NCBI_KEY = os.getenv("NCBI_API_KEY")
# This is the Webhook URL you provided
CLAY_WEBHOOK_URL = "https://api.clay.com/v3/sources/webhook/pull-in-data-from-a-webhook-af62da5e-3897-4ff1-a0a7-34ed3f7fa44a"
CSV_FILE = "pubmed_leads_export.csv"

def fetch_pubmed_data(query="liver toxicity 3D in-vitro", limit=15):
    """Fetches researcher data from PubMed and returns a list of dictionaries."""
    print(f"📡 Step 1: Searching PubMed for: {query}...")
    
    search_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={query}&retmode=json&retmax={limit}&api_key={NCBI_KEY}"
    ids = requests.get(search_url).json().get("esearchresult", {}).get("idlist", [])
    
    if not ids:
        print("❌ No IDs found in PubMed.")
        return []
        
    fetch_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={','.join(ids)}&retmode=xml&api_key={NCBI_KEY}"
    root = ET.fromstring(requests.get(fetch_url).content)
    
    leads = []
    for article in root.findall(".//PubmedArticle"):
        auth = article.find(".//AuthorList/Author[last()]")
        if auth is None: continue
        
        # Extract name, title, and affiliation
        first = auth.find('ForeName').text if auth.find('ForeName') is not None else ""
        last = auth.find('LastName').text if auth.find('LastName') is not None else ""
        name = f"{first} {last}".strip()
        
        title = article.find(".//ArticleTitle").text
        aff = article.find(".//AffiliationInfo/Affiliation")
        org = aff.text if aff is not None else "Independent Researcher"
        
        leads.append({
            "Name": name,
            "Paper Title": title,
            "Affiliation": org,
            "Source": "PubMed Automated Script"
        })
    
    # Save a local backup to CSV
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["Name", "Paper Title", "Affiliation", "Source"])
        writer.writeheader()
        writer.writerows(leads)
        
    print(f"✅ Local backup saved to {CSV_FILE}")
    return leads

def send_to_clay_webhook(leads):
    """Sends each lead as a JSON object to the Clay Webhook endpoint."""
    print(f"🚀 Step 2: Streaming {len(leads)} leads to Clay via Webhook...")
    
    success_count = 0
    for lead in leads:
        try:
            # We send the dictionary directly; Clay's webhook parses the keys automatically
            response = requests.post(
                CLAY_WEBHOOK_URL,
                json=lead,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code in [200, 201]:
                print(f"✔ Successfully sent: {lead['Name']}")
                success_count += 1
            else:
                print(f"❌ Webhook Error for {lead['Name']}: {response.status_code} - {response.text}")
        
        except Exception as e:
            print(f"⚠️ Connection error for {lead['Name']}: {e}")
        
        # Optional: slow down slightly to respect Clay's rate limits
        time.sleep(0.5)

    print(f"\n💎 MISSION COMPLETE: {success_count} leads are now in your Clay table!")

if __name__ == "__main__":
    # 1. Run the fetch
    results = fetch_pubmed_data(limit=20)
    
    # 2. Trigger the delivery
    if results:
        send_to_clay_webhook(results)
    else:
        print("📭 No leads found to send.")