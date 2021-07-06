## Usage
### 0. Create virtual environment and apply
```
python -m venv knime-web
source knime-web/bin/activate
```

### 1. Install dependencies
```
pip install -r requirements.txt
```

### 2. Run server
```
uvicorn --reload main:app
```

Then server will be started at localhost:8000

### 3. Visit testing page
Open browser and then visit `http://localhost:8000/docs`
