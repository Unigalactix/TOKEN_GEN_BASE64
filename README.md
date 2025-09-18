# Token Encoder/Decoder Streamlit App

This app allows you to encode and decode authentication tokens for multi-tenant organization access. It supports both plain and base64 token formats and can generate new authentication tokens.

## Features
- Input a token string (plain or base64)
- Auto-detects token type
- Shows plain and encoded token outputs
- Generates new authentication tokens
- Hides decoded fields for short tokens (3 fields)


## Usage
1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
2. Run the app locally:
   ```sh
   streamlit run streamlit_token_app.py
   ```
3. Open the provided local URL in your browser.

---

## Live Demo

Access the deployed Streamlit app here:
[unigalactix-token-gen-base64-streamlit-token-app-ig3q0z.streamlit.app](https://unigalactix-token-gen-base64-streamlit-token-app-ig3q0z.streamlit.app/)

---

## Token Format
- **Short Token:** `LoginMasterID&Database_Name&OrgID`
- **Auth Token:** `Expires&LoginMasterID&Database_Name&Issued&OrgID`

## License
MIT
