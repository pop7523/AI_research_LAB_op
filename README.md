# AI Newsroom

AI 기반 뉴스룸 + 리서치센터 백엔드입니다. 목표는 기사 원문, 사실, 주장, 분석,
불확실성, 검증 상태를 분리해 관리하는 것입니다.

## Development

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python -m pip install -U pip
.\.venv\Scripts\python -m pip install -e ".[dev]"
.\.venv\Scripts\python -m pytest
```

## Run API

```powershell
.\.venv\Scripts\python -m uvicorn app.main:app --app-dir backend --reload
```

