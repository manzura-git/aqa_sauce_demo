pip install -r requirements.txt

pytest

pytest tests/test_auth.py
pytest tests/test_e2e.py

pytest tests/test_auth.py::TestAuth::test_auth_001

pytest -v
