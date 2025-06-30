Write-Host "🫒 Lancement de Olive Oil Tracker..." -ForegroundColor Green
Write-Host ""
python -m streamlit run app.py --server.port 8501
Read-Host "Appuyez sur Entrée pour fermer" 