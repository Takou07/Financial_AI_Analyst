import os
import pandas as pd
import io
from llama_index.llms.google_genai import GoogleGenerativeAI
from dotenv import load_dotenv

# 1. Charger les variables d'environnement (Clé API)
load_dotenv()

def extract_financials(ticker, file_content):
    # Utilisation du nouveau SDK stable de Google
    llm = GoogleGenerativeAI(
        model="models/gemini-1.5-flash", 
        api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # On limite le contexte pour éviter de saturer l'IA (le début du 10-K est le plus riche)
    context = file_content[:120000] 
    
    prompt = f"""
    Tu es un analyste financier expert chez BCG X. 
    Analyse le rapport 10-K de {ticker} et extrais les données pour 2023, 2024 et 2025.
    
    Retourne UNIQUEMENT un tableau au format CSV avec exactement ces colonnes :
    Company,Fiscal_Year,Total_Revenue,Net_Income,Total_Assets,Total_Liabilities,Cash_Flow_Ops
    
    Règles strictes :
    1. Valeurs en millions de dollars (ex: si tu vois 100 Billion, écris 100000).
    2. Aucun symbole ($ ou virgules) dans les chiffres.
    3. Si une donnée 2025 n'est pas encore publiée, écris "NaN".
    4. Réponds UNIQUEMENT avec le bloc CSV, sans texte avant ou après.
    
    TEXTE DU RAPPORT :
    {context}
    """
    
    try:
        response = llm.complete(prompt)
        return response.text
    except Exception as e:
        print(f"❌ Erreur lors de l'appel à Gemini pour {ticker}: {e}")
        return None

def run_pipeline():
    input_dir = "./data/raw"
    output_path = "./data/processed/metrics_2023_2025.csv"
    os.makedirs("./data/processed", exist_ok=True)
    
    all_rows = []
    
    print("🚀 Démarrage de l'extraction intelligente...")

    for file in os.listdir(input_dir):
        if file.endswith("_parsed.md"):
            ticker = file.split("_")[0]
            print(f"🧐 Analyse de {ticker} en cours...")
            
            with open(os.path.join(input_dir, file), "r", encoding="utf-8") as f:
                content = f.read()
            
            raw_csv = extract_financials(ticker, content)
            
            if raw_csv:
                # Nettoyage du bloc de code Markdown si présent
                clean_csv = raw_csv.replace("```csv", "").replace("```", "").strip()
                # On sépare les lignes et on ignore l'en-tête pour les fichiers suivants
                lines = clean_csv.split("\n")
                if len(lines) > 1:
                    # On garde les lignes de données (on saute la première ligne qui est l'en-tête)
                    all_rows.extend(lines[1:])

    # 2. Création du DataFrame final
    header = "Company,Fiscal_Year,Total_Revenue,Net_Income,Total_Assets,Total_Liabilities,Cash_Flow_Ops"
    final_content = header + "\n" + "\n".join(all_rows)
    
    # Sauvegarde
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_content)
    
    print(f"\n✅ Terminé ! Ton fichier est ici : {output_path}")
    print(pd.read_csv(output_path).head()) # Aperçu du résultat

if __name__ == "__main__":
    run_pipeline()