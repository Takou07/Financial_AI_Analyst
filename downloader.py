from sec_edgar_downloader import Downloader
import os

def download_financial_reports(tickers):
    # 1. Initialiser le downloader
    # IMPORTANT : La SEC exige une chaîne d'identification (Nom + Email)
    dl = Downloader("financial_analyst", "takouboirs79@gmail.com")

    print(f"--- Démarrage du téléchargement pour : {', '.join(tickers)} ---")

    for ticker in tickers:
        print(f"\n[+] Récupération du dernier 10-K pour {ticker}...")
        
        # 2. Télécharger le dernier rapport annuel (10-K)
        # after="2023-01-01" permet de limiter aux rapports récents
        dl.get("10-K", ticker, after="2023-01-01", limit=1)
        
        print(f"✅ Terminé pour {ticker}")

    print("\n--- Tous les fichiers sont dans le dossier 'sec-edgar-filings' ---")

if __name__ == "__main__":
    # Liste des entreprises cibles pour ton projet
    companies = ["AAPL", "TSLA" , "MSFT"]
    download_financial_reports(companies)