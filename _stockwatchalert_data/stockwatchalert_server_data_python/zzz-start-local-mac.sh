PRODUCTION=False uvicorn app.main:app --host=0.0.0.0 --port=9999 --workers=8 --reload
