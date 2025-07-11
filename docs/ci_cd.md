# CI / CD

GitHub Actions pipeline складається з двох етапів:

1. **lint-and-test**
   - Install dependencies  
   - Lint (flake8)  
   - Format check (black)  
   - Type check (mypy)  
   - Unit & integration tests (pytest)  
   - Streamlit smoke-test (Playwright)  

2. **build-and-push** (лише на main)  
   - Build multi-stage Docker image  
   - Push на Docker Hub  

```yaml
jobs:
  lint-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.13'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip setuptools wheel
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      - name: Lint
        run: flake8 app ingest interface
      - name: Format
        run: black --check .
      - name: Type
        run: mypy .
      - name: Run tests
        run: pytest --maxfail=1 --disable-warnings -q
      - name: Smoke-test Streamlit
        run: pytest tests/e2e/test_streamlit_smoke.py -q

  build-and-push:
    needs: lint-and-test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
      - uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: |
            ${{ secrets.DOCKERHUB_USERNAME }}/legal_ai_agent:latest
            ${{ secrets.DOCKERHUB_USERNAME }}/legal_ai_agent:${{ github.sha }}