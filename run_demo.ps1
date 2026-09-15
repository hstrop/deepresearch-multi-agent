$env:PYTHONPATH = "src"
python -m uvicorn deepresearch.api:app --host 127.0.0.1 --port 8030
