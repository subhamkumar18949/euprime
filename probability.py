import pandas as pd

def calculate_lead_score(row):
    score = 0
    
    # 1. Scientific Intent (+40) - Based on Paper Title
    # Keywords: Liver, Toxicology, DILI, Hepatic, 3D
    paper_title = str(row['Paper Title']).lower()
    intent_keywords = ['liver', 'toxicology', 'dili', 'hepat', '3d']
    if any(word in paper_title for word in intent_keywords):
        score += 40

    # 2. Role Fit (+30) - Based on Job Title
    # Keywords: Toxicology, Safety, Hepatic, 3D
    job_title = str(row['Current Position']).lower()
    role_keywords = ['toxicology', 'safety', 'hepatic', '3d']
    if any(word in job_title for word in role_keywords):
        score += 30

    # 3. Technographic (+15) - Based on Methodology
    # Keywords: In Vitro, NAMs, Organoid, Millifluidics
    tech_keywords = ['in vitro', 'in-vitro', 'nam', 'organoid', 'millifluidic']
    if any(word in paper_title for word in tech_keywords) or any(word in job_title for word in tech_keywords):
        score += 15

    # 4. Location Hub (+10) - Based on Locality
    # Hubs: Boston, Cambridge, Bay Area, Basel, UK Golden Triangle
    location = str(row['Locality']).lower()
    hubs = ['boston', 'cambridge', 'bay area', 'basel', 'uk', 'london', 'oxford']
    if any(hub in location for hub in hubs):
        score += 10

    return score

# --- MAIN EXECUTION ---

# 1. Load your data (Change 'leads.csv' to your actual filename)
df = pd.read_csv('leads.csv')

# 2. Apply the scoring function
df['Probability Score'] = df.apply(calculate_lead_score, axis=1)

# 3. Rank leads from highest to lowest probability
df = df.sort_values(by='Probability Score', ascending=False)

# 4. Save to a new CSV file
df.to_csv('scored_leads.csv', index=False)

print("✅ Scoring complete! Check 'scored_leads.csv' for the results.")