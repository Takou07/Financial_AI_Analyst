import os
from llama_parse import LlamaParse
from dotenv import load_dotenv

load_dotenv()

def parse_financial_docs():
    # 1. Initialiser le parser
    # result_type="markdown" est crucial pour que l'IA comprenne les tableaux
    parser = LlamaParse(
        api_key=os.getenv("LLAMA_CLOUD_API_KEY"),
        result_type="markdown",
        verbose=True
    )

    # Chemin vers les fichiers téléchargés par le Script 1
    input_dir = "./sec-edgar-filings"
    output_dir = "./data/raw"
    os.makedirs(output_dir, exist_ok=True)

    print("--- Démarrage du Parsing Intelligent ---")

    # Parcourir les dossiers pour trouver les rapports 10-K
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".txt") or file.endswith(".html"):
                file_path = os.path.join(root, file)
                ticker = root.split(os.sep)[1] # Récupère le nom de l'entreprise (ex: AAPL)
                
                print(f"[+] Analyse du rapport pour {ticker}...")
                
                # 2. Lancer le parsing (conversion en Markdown)
                documents = parser.load_data(file_path)
                
                # 3. Sauvegarder le résultat
                output_filename = f"{ticker}_10K_parsed.md"
                with open(os.path.join(output_dir, output_filename), "w", encoding="utf-8") as f:
                    for doc in documents:
                        f.write(doc.text)
                
                print(f"✅ Converti : {output_filename}")

if __name__ == "__main__":
    parse_financial_docs()