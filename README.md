# LangGu: Your All-In-One Language Buddy
> **Lang**uage + Chin**gu**(Korean word for 'friend') = **LangGu**

LangGu helps you with your journey of acquiring a new language.

## Features
- Sentence translation
- Sentence correction
- Sentence break-down (explanation)
- Separate prompt editor (marimo)

## To do
- Enhancement of existing features
- Personalized dictionary

---

## Setup
### 1. Install dependencies
`pip install uv; uv pip install -r pyproject.toml`
### 2. Create a `.env` file & add API key
`GOOGLE_API_KEY=your_api_key`
### 3. Run Streamlit page
`uv run streamlit run page.py`
### 4. (Optional) Edit system prompt & welcome message
`uv run marimo edit prompt_editor.py`

---
## Misc
### Locking requirements
Lock requirements defined in `pyproject.toml` to requirements.txt via
```uv pip compile pyproject.toml -o requirements.txt```