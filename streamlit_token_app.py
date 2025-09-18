
import streamlit as st
import base64
from datetime import datetime, timezone, timedelta

def encode_base64(text: str) -> str:
    if text is None:
        return None
    text_bytes = text.encode('utf-8')
    return base64.b64encode(text_bytes).decode('utf-8')

def decode(encoded_string):
    """
    Decode a base64 encoded string.
    Returns dict with LoginMasterID, Database_Name, OrgID
    """
    decoded_bytes = base64.b64decode(encoded_string)
    decoded_string = decoded_bytes.decode('utf-8')
    decoded_items = decoded_string.split('&')    
    # If token is full auth token, handle 5 fields
    if len(decoded_items) == 5:
        return {
            "Expires": decoded_items[0],
            "LoginMasterID": decoded_items[1],
            "Database_Name": decoded_items[2],
            "Issued": decoded_items[3],
            "OrgID": decoded_items[4]
        }
    # If short token, handle 3 fields
    return {
        "LoginMasterID": decoded_items[0] if len(decoded_items)>0 else "",
        "Database_Name": decoded_items[1] if len(decoded_items)>1 else "",
        "OrgID": decoded_items[2] if len(decoded_items)>2 else ""
    }

def generate_auth_token(login_master_id, database_name, org_id):
    """
    Generate authentication token for API calls
    Returns base64 encoded authentication token
    """
    now_utc = datetime.now(timezone.utc)
    date_plus_one = (now_utc + timedelta(days=1)).isoformat()
    date_now = now_utc.isoformat()
    token_str = f"{date_plus_one}&{login_master_id}&{database_name}&{date_now}&{org_id}"
    return token_str, encode_base64(token_str)

def auto_normalize_token(token: str):
    """
    Detects if token is base64 or plain and returns both forms and fields.
    """
    try:
        # Try to decode as base64
        fields = decode(token)
        plain_token = base64.b64decode(token).decode('utf-8')
        encoded_token = token
    except Exception:
        # Assume it's plain
        plain_token = token
        encoded_token = encode_base64(token)
        parts = token.split('&')
        if len(parts) == 5:
            fields = {
                "Expires": parts[0],
                "LoginMasterID": parts[1],
                "Database_Name": parts[2],
                "Issued": parts[3],
                "OrgID": parts[4]
            }
        else:
            fields = {
                "LoginMasterID": parts[0] if len(parts)>0 else "",
                "Database_Name": parts[1] if len(parts)>1 else "",
                "OrgID": parts[2] if len(parts)>2 else ""
            }
    return {
        "plain_token": plain_token,
        "encoded_token": encoded_token,
        "fields": fields,
    }

st.title("Token Encoder/Decoder App")
st.write("""
Paste your token string (plain or base64) below. The app will auto-detect and show both forms.
""")

input_token = st.text_area("Enter token string (plain or base64):", "")


if input_token:
    result = auto_normalize_token(input_token.strip())
    st.subheader("Plain Token")
    st.code(result["plain_token"], language="text")
    st.subheader("Base64 Encoded Token")
    st.code(result["encoded_token"], language="text")

    # Only show decoded fields if token has 5 fields (full auth token)
    if len(result["fields"]) == 5:
        st.subheader("Decoded Token Fields")
        for k, v in result["fields"].items():
            st.write(f"**{k}**: {v}")

    # Optionally, generate a new token from decoded fields if possible
    if all(key in result["fields"] for key in ["LoginMasterID", "Database_Name", "OrgID"]):
        st.markdown("---")
        st.subheader("Generate New Auth Token")
        plain, encoded = generate_auth_token(
            result["fields"].get("LoginMasterID"),
            result["fields"].get("Database_Name"),
            result["fields"].get("OrgID")
        )
        st.write("**Plain Auth Token:**")
        st.code(plain, language="text")
        st.write("**Encoded Auth Token:**")
        st.code(encoded, language="text")
else:
    st.info("Enter a token string above to see results.")
