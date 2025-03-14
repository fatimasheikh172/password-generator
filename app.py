import streamlit as st
import random
import string

common_passwords = [
    'password', '123456', '12345678', '123456789', 'qwerty',
    'abc123', 'password1', '12345', '1234567', 'admin', 'welcome',
    'letmein', 'monkey', 'password123', 'dragon', 'sunshine'
]

def evaluate_password(password):
    if password.lower() in common_passwords:
        return 'Weak', ["This password is too common and easily guessable!"]
    
    length = len(password) >= 8
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in '!@#$%^&*' for c in password)
    
    score = sum([length, has_upper, has_lower, has_digit, has_special])
    
    if score <= 2:
        strength = 'Weak'
    elif score <= 4:
        strength = 'Moderate'
    else:
        strength = 'Strong'
    
    feedback = []
    if not length:
        feedback.append("Password should be at least 8 characters long")
    if not has_upper:
        feedback.append("Include at least one uppercase letter (A-Z)")
    if not has_lower:
        feedback.append("Include at least one lowercase letter (a-z)")
    if not has_digit:
        feedback.append("Add at least one number (0-9)")
    if not has_special:
        feedback.append("Include at least one special character (!@#$%^&*)")
    
    return strength, feedback

def generate_strong_password(length=12):
    if length < 8:
        length = 8
    chars = (
        string.ascii_uppercase + 
        string.ascii_lowercase + 
        string.digits + 
        '!@#$%^&*'
    )
    while True:
        password = ''.join(random.choice(chars) for _ in range(length))
        if (any(c.isupper() for c in password)) and \
           (any(c.islower() for c in password)) and \
           (any(c.isdigit() for c in password)) and \
           (any(c in '!@#$%^&*' for c in password)):
            return password

def main():
    st.title("🔐 Password Strength Checker")
    st.markdown("---")
    
    password = st.text_input(
        "Enter your password:", 
        type="password",
        placeholder="Type your password here...",
        help="We'll never store or share your password"
    )
    
    if password:
        strength, feedback = evaluate_password(password)
        
        st.markdown("---")
        if strength == 'Strong':
            st.success("## ✅ Excellent Password Strength!")
            st.balloons()
            st.markdown("Your password meets all security requirements!")
        else:
            if "too common" in feedback[0]:
                st.error("## ❌ Extremely Weak Password!")
                st.error(feedback[0])
                st.markdown("---")
            else:
                st.subheader(f"Password Strength: {strength}")
                if strength == 'Weak':
                    st.error("This password is vulnerable to attacks!")
                else:
                    st.warning("Almost there! Let's make it stronger!")
                
                st.markdown("### 🔍 Security Recommendations:")
                for suggestion in feedback:
                    st.warning(f"- {suggestion}")
            
            st.markdown("---")
            if st.button("🛡️ Generate Strong Password"):
                new_pass = generate_strong_password()
                st.success("### 🔒 Try This Strong Password:")
                st.code(new_pass, language="text")
                st.info("Copy and paste this password somewhere safe!")

if __name__ == "__main__":
    main()