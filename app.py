import re
import streamlit as st
from crypto_utils import encrypt_data, decrypt_data
from database import init_db, register_user, fetch_user_data

MASTER_SECRET = "SuperSecretMasterKey2026"

# Initialize database on launch
init_db()

# Common SQL Injection patterns to block
SQLI_PATTERNS = [
    r"(\bOR\b|\bAND\b)\s+['\"]?1['\"]?\s*=\s*['\"]?1['\"]?",
    r"(\bOR\b|\bAND\b)\s+\d+=\d+",
    r"UNION\s+SELECT",
    r"--",
    r";",
    r"DROP\s+TABLE",
    r"INSERT\s+INTO"
]

def detect_sqli(input_str: str) -> bool:
    """Detects malicious SQL injection payloads."""
    if not input_str:
        return False
    for pattern in SQLI_PATTERNS:
        if re.search(pattern, input_str, re.IGNORECASE):
            return True
    return False

# Ensure sample user exists for testing
try:
    register_user("alice", encrypt_data("Confidential Record #4921", MASTER_SECRET), "CAP-1002")
except Exception:
    pass

st.set_page_config(page_title="SQL Leak Detector", page_icon="🛡️")

st.title("🛡️ Secure Auth & SQL Leak Detector")
st.subheader("Task 2: SQL Injection Prevention System")

# Session state to manage input box autofill from test buttons
if "username_input" not in st.session_state:
    st.session_state.username_input = ""
if "code_input" not in st.session_state:
    st.session_state.code_input = ""

# Form Inputs
with st.form("login_form"):
    username = st.text_input("Username", value=st.session_state.username_input, placeholder="Enter username")
    capability_code = st.text_input("Capability Code / Payload", value=st.session_state.code_input, placeholder="Enter token or injection payload")
    submit_button = st.form_submit_button("Login / Access Data")

st.markdown("### 🧪 Quick Test Cases")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Valid User Test"):
        st.session_state.username_input = "alice"
        st.session_state.code_input = "CAP-1002"
        st.rerun()

with col2:
    if st.button("SQLi Test: OR 1==1"):
        st.session_state.username_input = "admin"
        st.session_state.code_input = "OR 1==1"
        st.rerun()

with col3:
    if st.button("SQLi Test: Comments"):
        st.session_state.username_input = "user"
        st.session_state.code_input = "' OR '1'='1' --"
        st.rerun()

# Processing Login / Security Validation
if submit_button:
    st.divider()
    
    # Layer 1: Security Inspection against SQLi
    if detect_sqli(username) or detect_sqli(capability_code):
        st.error("⚠️ **SQL Injection Attempt Detected!**\n\nTransaction suspended immediately to prevent unauthorized data access.")
    else:
        # Layer 2: Parameterized SQL Query
        encrypted_info = fetch_user_data(username, capability_code)
        
        if not encrypted_info:
            st.warning("❌ **Access Denied:** Invalid username or capability code token.")
        else:
            try:
                decrypted_info = decrypt_data(encrypted_info, MASTER_SECRET)
                st.success("✅ **Login Successful!**")
                st.json({
                    "Status": "Authorized",
                    "Encrypted DB Record": encrypted_info,
                    "Decrypted Payload": decrypted_info
                })
            except Exception:
                st.error("❌ **Error:** Unable to decrypt record payload.")