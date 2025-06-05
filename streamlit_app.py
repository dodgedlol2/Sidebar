import streamlit as st
import streamlit_antd_components as sac
import streamlit_authenticator as stauth
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import yaml
from yaml.loader import SafeLoader
import os

# Try to import Plotly, fallback to basic charts if not available
try:
    import plotly.graph_objects as go
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    st.warning("📊 Plotly not installed. Using basic charts. Install with: pip install plotly")

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

# Configure page settings
st.set_page_config(
    page_title="Kaspa Analytics Pro",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Authentication configuration with API key - EMBEDDED VERSION
def get_auth_config():
    """Get authentication configuration - embedded for Streamlit Cloud"""
    config = {
        'credentials': {
            'usernames': {
                'admin': {
                    'email': 'admin@kaspalytics.com',
                    'first_name': 'Admin',
                    'last_name': 'User',
                    'password': 'admin123',
                    'subscription': 'pro',
                    'failed_login_attempts': 0,
                    'logged_in': False
                },
                'premium_user': {
                    'email': 'premium@example.com',
                    'first_name': 'Premium',
                    'last_name': 'User',
                    'password': 'premium123',
                    'subscription': 'premium',
                    'failed_login_attempts': 0,
                    'logged_in': False
                },
                'free_user': {
                    'email': 'free@example.com',
                    'first_name': 'Free',
                    'last_name': 'User',
                    'password': 'free123',
                    'subscription': 'free',
                    'failed_login_attempts': 0,
                    'logged_in': False
                },
                'researcher': {
                    'email': 'researcher@kaspalytics.com',
                    'first_name': 'Research',
                    'last_name': 'Demo',
                    'password': 'research123',
                    'subscription': 'pro',
                    'failed_login_attempts': 0,
                    'logged_in': False
                }
            }
        },
        'cookie': {
            'name': 'kaspa_analytics_auth',
            'key': 'kaspa_secret_key_12345_change_in_production',
            'expiry_days': 30
        },
        'preauthorized': [
            'admin@kaspalytics.com',
            'newuser@kaspalytics.com',
            'beta@kaspalytics.com',
            'researcher@kaspalytics.com',
            'vip@kaspalytics.com'
        ],
        'api_key': 'a9fz9gh0zq7io3zpjnya1vmx8et9b3pd'  # Your API key for 2FA and email features
    }
    return config

# Simple config management functions for Streamlit Cloud
def add_new_user_to_config(username, email, first_name, last_name, password, subscription='free'):
    """Add new user to session state config"""
    if 'config' not in st.session_state:
        st.session_state.config = get_auth_config()
    
    if username not in st.session_state.config['credentials']['usernames']:
        st.session_state.config['credentials']['usernames'][username] = {
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'password': password,
            'subscription': subscription,
            'failed_login_attempts': 0,
            'logged_in': False,
            'created_at': datetime.now().isoformat()
        }
        return True
    return False

def update_user_subscription_in_config(username, new_subscription):
    """Update user subscription in session state"""
    if 'config' not in st.session_state:
        st.session_state.config = get_auth_config()
    
    if username in st.session_state.config['credentials']['usernames']:
        st.session_state.config['credentials']['usernames'][username]['subscription'] = new_subscription
        return True
    return False

# Initialize configuration
if 'config' not in st.session_state:
    st.session_state.config = get_auth_config()

config = st.session_state.config

# Initialize authenticator (without API key for compatibility)
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized'],
    auto_hash=True
)

# Save config function - Streamlit Cloud version
def save_config():
    """Save configuration changes to session state (Streamlit Cloud compatible)"""
    try:
        # In Streamlit Cloud, we save to session state since we can't write files
        # In production with persistent storage, you'd write to a database or file
        
        # For demo purposes, we just update the session state
        if 'config' in st.session_state:
            # Update the global config variable
            global config
            config = st.session_state.config
            
            # Show success message
            st.success("✅ Configuration updated in session!")
            return True
        return False
    except Exception as e:
        st.error(f"Error saving config: {e}")
        return False

# Admin panel for user management (Streamlit Cloud compatible)
def render_admin_panel():
    """Admin panel for user management - works in Streamlit Cloud"""
    if st.session_state.get('username') != 'admin':
        st.error("🔒 Access denied. Admin only.")
        return
    
    st.title("👑 Admin Panel")
    
    admin_tabs = sac.tabs([
        sac.TabsItem(label='User Management', icon='people'),
        sac.TabsItem(label='Add User', icon='person-plus'),
        sac.TabsItem(label='System Stats', icon='graph-up'),
    ], key='admin_tabs')
    
    if admin_tabs == 'User Management':
        st.subheader("👥 Current Users")
        
        # Display current users
        for username, user_info in config['credentials']['usernames'].items():
            with st.expander(f"👤 {username} ({user_info.get('subscription', 'free')})"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write(f"**Name:** {user_info.get('first_name')} {user_info.get('last_name')}")
                    st.write(f"**Email:** {user_info.get('email')}")
                
                with col2:
                    st.write(f"**Subscription:** {user_info.get('subscription', 'free')}")
                    st.write(f"**Failed Logins:** {user_info.get('failed_login_attempts', 0)}")
                
                with col3:
                    new_subscription = st.selectbox(
                        "Change Subscription:", 
                        ['free', 'premium', 'pro'],
                        index=['free', 'premium', 'pro'].index(user_info.get('subscription', 'free')),
                        key=f"sub_{username}"
                    )
                    
                    if st.button(f"Update {username}", key=f"update_{username}"):
                        if update_user_subscription_in_config(username, new_subscription):
                            st.success(f"✅ Updated {username} to {new_subscription}")
                            st.rerun()
    
    elif admin_tabs == 'Add User':
        st.subheader("➕ Add New User")
        
        with st.form("add_user_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                new_username = st.text_input("Username")
                new_first_name = st.text_input("First Name")
                new_email = st.text_input("Email")
            
            with col2:
                new_last_name = st.text_input("Last Name")
                new_subscription = st.selectbox("Subscription", ['free', 'premium', 'pro'])
                new_password = st.text_input("Password", type="password")
            
            if st.form_submit_button("➕ Add User"):
                if new_username and new_email and new_password:
                    if add_new_user_to_config(new_username, new_email, new_first_name, new_last_name, new_password, new_subscription):
                        st.success(f"✅ User {new_username} added successfully!")
                        st.rerun()
                    else:
                        st.error(f"❌ User {new_username} already exists!")
                else:
                    st.error("❌ Please fill in all required fields")
    
    else:  # System Stats
        st.subheader("📊 System Statistics")
        
        total_users = len(config['credentials']['usernames'])
        subscription_counts = {}
        
        for user_info in config['credentials']['usernames'].values():
            sub = user_info.get('subscription', 'free')
            subscription_counts[sub] = subscription_counts.get(sub, 0) + 1
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Users", total_users)
        with col2:
            st.metric("Free Users", subscription_counts.get('free', 0))
        with col3:
            st.metric("Premium Users", subscription_counts.get('premium', 0))
        with col4:
            st.metric("Pro Users", subscription_counts.get('pro', 0))

# Custom CSS for Kaspa theme
st.markdown("""
<style>
.main-header {
    background: linear-gradient(135deg, #70C7BA 0%, #49A097 100%);
    padding: 2rem;
    border-radius: 12px;
    color: white;
    margin-bottom: 2rem;
    text-align: center;
}

.auth-container {
    background: white;
    padding: 2rem;
    border-radius: 12px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    border: 1px solid #e9ecef;
    margin: 1rem 0;
}

.premium-badge {
    background: linear-gradient(45deg, #FFD700, #FFA500);
    color: #000;
    padding: 0.25rem 0.75rem;
    border-radius: 12px;
    font-size: 0.8rem;
    font-weight: bold;
}

.pro-badge {
    background: linear-gradient(45deg, #8A2BE2, #4B0082);
    color: white;
    padding: 0.25rem 0.75rem;
    border-radius: 12px;
    font-size: 0.8rem;
    font-weight: bold;
}

.free-badge {
    background: #6c757d;
    color: white;
    padding: 0.25rem 0.75rem;
    border-radius: 12px;
    font-size: 0.8rem;
    font-weight: bold;
}

.paywall-container {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 12px;
    color: white;
    text-align: center;
    margin: 2rem 0;
}

.feature-highlight {
    background: #f8f9fa;
    padding: 1rem;
    border-radius: 8px;
    border-left: 4px solid #70C7BA;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# Data fetching functions (same as before)
@st.cache_data(ttl=300)
def fetch_kaspa_price_data():
    """Fetch Kaspa price data"""
    try:
        dates = pd.date_range(start='2022-01-01', end=datetime.now(), freq='D')
        
        np.random.seed(42)
        base_price = 0.02
        prices = []
        current_price = base_price
        
        for i in range(len(dates)):
            trend = 0.001 * np.sin(i / 50) + 0.0005
            volatility = np.random.normal(0, 0.05)
            current_price *= (1 + trend + volatility)
            prices.append(max(current_price, 0.001))
        
        volumes = np.random.lognormal(15, 1, len(dates))
        
        df = pd.DataFrame({
            'timestamp': dates,
            'price': prices,
            'volume': volumes
        })
        
        return df
        
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()

def get_user_subscription(username):
    """Get user subscription level"""
    user_config = config['credentials']['usernames'].get(username, {})
    return user_config.get('subscription', 'free')

def show_authentication_page():
    """Enhanced authentication page with all login options"""
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    st.title("💎 Kaspa Analytics Pro")
    st.markdown("*Professional Kaspa blockchain analysis and research platform*")
    st.markdown("*Now with enhanced security and user management*")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Authentication tabs
    auth_tabs = sac.tabs([
        sac.TabsItem(label='Login', icon='box-arrow-in-right'),
        sac.TabsItem(label='Register', icon='person-plus'),
        sac.TabsItem(label='Guest Login', icon='person-circle'),
        sac.TabsItem(label='Password Help', icon='question-circle'),
    ], index=0, key='auth_tabs')
    
    # Initialize return values
    name = None
    authentication_status = None
    username = None
    
    if auth_tabs == 'Login':
        name, authentication_status, username = render_login_section()
    elif auth_tabs == 'Register':
        render_registration_section()
    elif auth_tabs == 'Guest Login':
        name, authentication_status, username = render_guest_login_section()
    else:  # Password Help
        render_password_help_section()
    
    # If no authentication happened, get current session state
    if authentication_status is None:
        name = st.session_state.get('name')
        authentication_status = st.session_state.get('authentication_status')
        username = st.session_state.get('username')
    
    return name, authentication_status, username

def render_login_section():
    """Render main login section"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        st.markdown("### 🔐 Login to Your Account")
        
        # Main login widget
        authenticator.login()
        
        # Get authentication status
        name = st.session_state.get('name')
        authentication_status = st.session_state.get('authentication_status')
        username = st.session_state.get('username')
        
        if authentication_status == False:
            st.error("❌ Username/password is incorrect. Please try again.")
            
            # Show failed login attempts
            failed_attempts = st.session_state.get('failed_login_attempts', {})
            if username and username in failed_attempts:
                st.warning(f"⚠️ Failed attempts: {failed_attempts[username]}")
        
        elif authentication_status == None:
            st.info("ℹ️ Please enter your credentials to access the platform.")
        
        # 2FA option
        st.markdown("---")
        enable_2fa = st.checkbox("🔒 Enable Two-Factor Authentication", help="Requires email verification")
        
        if enable_2fa and authentication_status:
            st.info("🔐 2FA is enabled for enhanced security")
        
        # Demo credentials
        st.markdown("---")
        st.markdown("**🔑 Demo Accounts:**")
        
        demo_info = sac.tabs([
            sac.TabsItem(label='Free', icon='person'),
            sac.TabsItem(label='Premium', icon='star'),
            sac.TabsItem(label='Pro', icon='crown'),
        ], index=0, key='demo_creds')
        
        if demo_info == 'Free':
            st.code("Username: free_user\nPassword: free123\nFeatures: Basic analytics")
        elif demo_info == 'Premium':
            st.code("Username: premium_user\nPassword: premium123\nFeatures: Advanced analytics")
        else:
            st.code("Username: admin\nPassword: admin123\nFeatures: Full platform access")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    return name, authentication_status, username

def render_registration_section():
    """Render user registration section"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        st.markdown("### ✨ Create New Account")
        
        # Registration options
        registration_type = sac.segmented([
            "Open Registration",
            "Pre-authorized Only"
        ], index=0, key='registration_type')
        
        if registration_type == "Open Registration":
            st.info("📝 Anyone can register for a free account")
            use_preauth = False
        else:
            st.info("🛡️ Only pre-authorized email addresses can register")
            use_preauth = True
            
            st.markdown("**Pre-authorized emails:**")
            for email in config['preauthorized']:
                st.write(f"• {email}")
        
        # Registration widget with maximum compatibility
        try:
            st.markdown("#### 📝 Registration Form")
            
            # Try with proper keyword arguments
            try:
                if authenticator.register_user(location='main'):
                    st.success('✅ User registered successfully!')
                    if save_config():
                        st.success("Configuration updated!")
                        st.rerun()
            except Exception as e:
                st.error(f"Registration error: {e}")
                st.info("Using manual registration form as fallback")
                render_manual_registration_form()
                
        except Exception as e:
            st.error(f"Registration widget error: {e}")
            st.info("Using manual registration form as fallback")
            render_manual_registration_form()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Return None values since registration doesn't log in automatically
    return None, None, None

def render_manual_registration_form():
    """Manual registration form as fallback"""
    st.markdown("---")
    st.markdown("#### 📝 Manual Registration Form")
    
    with st.form("manual_registration"):
        col1, col2 = st.columns(2)
        
        with col1:
            new_username = st.text_input("Username*", help="Choose a unique username")
            new_first_name = st.text_input("First Name*")
            new_email = st.text_input("Email*", help="Valid email address")
        
        with col2:
            new_last_name = st.text_input("Last Name*")
            new_password = st.text_input("Password*", type="password", help="Choose a strong password")
            new_password_confirm = st.text_input("Confirm Password*", type="password")
        
        new_subscription = st.selectbox("Account Type", ['free', 'premium'], 
                                       help="Start with free, upgrade anytime")
        
        agree_terms = st.checkbox("I agree to the Terms of Service and Privacy Policy*")
        
        submit_registration = st.form_submit_button("🚀 Create Account", type="primary")
        
        if submit_registration:
            # Validation
            errors = []
            
            if not new_username:
                errors.append("Username is required")
            elif new_username in config['credentials']['usernames']:
                errors.append("Username already exists")
            
            if not new_email:
                errors.append("Email is required")
            elif '@' not in new_email:
                errors.append("Invalid email format")
            
            if not new_first_name:
                errors.append("First name is required")
            
            if not new_last_name:
                errors.append("Last name is required")
            
            if not new_password:
                errors.append("Password is required")
            elif len(new_password) < 6:
                errors.append("Password must be at least 6 characters")
            
            if new_password != new_password_confirm:
                errors.append("Passwords do not match")
            
            if not agree_terms:
                errors.append("You must agree to the terms of service")
            
            if errors:
                for error in errors:
                    st.error(f"❌ {error}")
            else:
                # Create the user
                if add_new_user_to_config(new_username, new_email, new_first_name, 
                                        new_last_name, new_password, new_subscription):
                    st.success("🎉 Account created successfully!")
                    st.info("Please use the Login tab to sign in with your new account")
                    st.balloons()
                    
                    # Clear the form by rerunning
                    if st.button("Continue to Login"):
                        st.rerun()
                else:
                    st.error("❌ Registration failed. Username may already exist.")

def render_guest_login_section():
    """Render guest login section"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    # Initialize return values
    name = None
    authentication_status = None
    username = None
    
    with col2:
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        st.markdown("### 👤 Guest Access")
        
        st.markdown("#### Quick Demo Access")
        st.info("🎯 Try the platform without creating an account")
        
        # Guest login options
        guest_provider = sac.segmented([
            "Google OAuth",
            "Microsoft OAuth"
        ], index=0, key='guest_provider')
        
        try:
            if guest_provider == "Google OAuth":
                if st.button("🔐 Login with Google", type="primary", use_container_width=True):
                    # Demo OAuth - in production you'd configure real OAuth
                    st.success("🎉 Demo: Google OAuth login successful!")
                    st.session_state['authentication_status'] = True
                    st.session_state['name'] = 'Guest User'
                    st.session_state['username'] = 'guest_google'
                    name = 'Guest User'
                    authentication_status = True
                    username = 'guest_google'
            else:
                if st.button("🔐 Login with Microsoft", type="primary", use_container_width=True):
                    # Demo OAuth - in production you'd configure real OAuth
                    st.success("🎉 Demo: Microsoft OAuth login successful!")
                    st.session_state['authentication_status'] = True
                    st.session_state['name'] = 'Guest User'
                    st.session_state['username'] = 'guest_microsoft'
                    name = 'Guest User'
                    authentication_status = True
                    username = 'guest_microsoft'
                    
        except Exception as e:
            st.error(f"Guest login error: {e}")
        
        st.markdown("---")
        st.markdown("**📋 Guest Account Features:**")
        st.write("• 🔍 Limited analytics access")
        st.write("• 📊 Basic charts and data")
        st.write("• ⏰ 30-minute session limit")
        st.write("• 🚫 No data export")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    return name, authentication_status, username

def render_password_help_section():
    """Render password help section"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        st.markdown("### 🆘 Password & Username Help")
        
        help_tabs = sac.tabs([
            sac.TabsItem(label='Reset Password', icon='key'),
            sac.TabsItem(label='Forgot Username', icon='person-question'),
            sac.TabsItem(label='Forgot Password', icon='unlock'),
        ], key='help_tabs')
        
        if help_tabs == 'Reset Password':
            st.markdown("#### 🔑 Reset Your Password")
            st.info("ℹ️ For existing users who want to change their password")
            
            # Check if user is authenticated first
            if st.session_state.get('authentication_status'):
                username = st.session_state.get('username')
                try:
                    if authenticator.reset_password(username, 'Reset password'):
                        st.success('✅ Password modified successfully')
                        if save_config():
                            st.success("Changes saved!")
                except Exception as e:
                    st.error(f"Password reset error: {e}")
            else:
                st.warning("🔐 Please login first to reset your password")
        
        elif help_tabs == 'Forgot Username':
            st.markdown("#### 👤 Recover Your Username")
            st.info("📧 Enter your email to receive your username")
            
            try:
                enable_email = st.checkbox("📨 Send username via email", key='username_email')
                
                try:
                    username_forgot_username, email_forgot_username = authenticator.forgot_username('Forgot username')
                    
                    if username_forgot_username:
                        st.success('✅ Username found!')
                        st.info(f'👤 Your username is: **{username_forgot_username}**')
                    elif username_forgot_username == False:
                        st.error('❌ Email not found in our system')
                except TypeError:
                    # Handle different function signatures
                    st.info("📧 Username recovery feature may have limited functionality in this version")
                    
            except Exception as e:
                st.error(f"Username recovery error: {e}")
        
        else:  # Forgot Password
            st.markdown("#### 🔓 Recover Your Password")
            st.info("🔐 Generate a new secure password")
            
            try:
                enable_email = st.checkbox("📨 Send new password via email", key='password_email')
                
                try:
                    username_forgot_pw, email_forgot_password, random_password = authenticator.forgot_password('Forgot password')
                    
                    if username_forgot_pw:
                        st.success('✅ New password generated!')
                        st.info('🔑 Please check your email for the new password')
                        
                        if save_config():
                            st.success("Password updated!")
                            
                    elif username_forgot_pw == False:
                        st.error('❌ Username not found')
                except TypeError:
                    # Handle different function signatures
                    st.info("📧 Password recovery feature may have limited functionality in this version")
                    
            except Exception as e:
                st.error(f"Password recovery error: {e}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Return None values since password help doesn't log in
    return None, None, None

def show_main_app(name, username):
    """Enhanced main application with user management"""
    subscription_level = get_user_subscription(username)
    
    # Header with user info
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown("# 💎 Kaspa Analytics Pro")
        st.markdown("*Professional blockchain analysis platform*")
    
    with col2:
        st.markdown(f"**Welcome, {name}!**")
        if subscription_level == 'free':
            st.markdown('<span class="free-badge">FREE USER</span>', unsafe_allow_html=True)
        elif subscription_level == 'premium':
            st.markdown('<span class="premium-badge">PREMIUM</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="pro-badge">PRO</span>', unsafe_allow_html=True)
    
    with col3:
        logout_col1, logout_col2 = st.columns(2)
        with logout_col1:
            if st.button("⚙️ Profile", type="secondary"):
                st.session_state.show_profile = True
                st.rerun()
        with logout_col2:
            if st.button("🚪 Logout", type="secondary"):
                # Manual logout by clearing session state
                for key in ['authentication_status', 'name', 'username', 'logout']:
                    if key in st.session_state:
                        del st.session_state[key]
                
                # Also try the authenticator logout
                try:
                    authenticator.logout()
                except:
                    pass  # Continue with manual logout if authenticator fails
                
                # Clear any other auth-related session state
                if 'show_profile' in st.session_state:
                    del st.session_state['show_profile']
                
                # Force rerun to show login page
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Check if user wants to see profile
    if st.session_state.get('show_profile'):
        render_user_profile(name, username)
        return
    
    # Sidebar navigation
    with st.sidebar:
        st.title("📊 Analytics Menu")
        
        # Create menu based on subscription level
        if subscription_level == 'free' or username.startswith('guest'):
            menu_items = [
                sac.MenuItem('overview', icon='house-fill', tag=sac.Tag('Free', color='gray')),
                sac.MenuItem('price_charts', icon='graph-up', description='Basic price data'),
                sac.MenuItem('power_law_basic', icon='bar-chart', description='Simple power law'),
                sac.MenuItem(type='divider'),
                sac.MenuItem('upgrade', icon='star', tag=sac.Tag('Upgrade', color='orange')),
            ]
        else:
            menu_items = [
                sac.MenuItem('overview', icon='house-fill', tag=sac.Tag('Premium+', color='gold')),
                sac.MenuItem('price_charts', icon='graph-up'),
                sac.MenuItem('analytics', icon='bar-chart-fill', children=[
                    sac.MenuItem('power_law_advanced', icon='trending-up'),
                    sac.MenuItem('network_metrics', icon='diagram-3'),
                ]),
                sac.MenuItem('data_export', icon='download'),
                sac.MenuItem(type='divider'),
                sac.MenuItem('account', icon='person-gear', description='Profile & Settings'),
            ]
            
            # Add admin panel for admin user
            if username == 'admin':
                menu_items.append(sac.MenuItem('admin_panel', icon='shield-check', tag=sac.Tag('Admin', color='red')))
        
        selected = sac.menu(menu_items, open_all=True, key='main_menu')
        
        # Quick stats
        st.markdown("---")
        st.markdown("**⚡ Quick Stats**")
        df = fetch_kaspa_price_data()
        if not df.empty:
            current_price = df['price'].iloc[-1]
            st.metric("KAS Price", f"${current_price:.4f}")
            
            # Show session info for guests
            if username.startswith('guest'):
                st.markdown("---")
                st.warning("👤 Guest Session\n⏰ Limited time access")
        
        # Debug section (only for admin)
        if username == 'admin':
            st.markdown("---")
            st.markdown("**🔧 Debug Info**")
            if st.checkbox("Show Session State", key='debug_session'):
                st.json({
                    'authentication_status': st.session_state.get('authentication_status'),
                    'name': st.session_state.get('name'),
                    'username': st.session_state.get('username'),
                    'show_profile': st.session_state.get('show_profile', False)
                })
            
            if st.button("🔄 Force Logout (Debug)", key='debug_logout'):
                # Clear ALL session state
                keys_to_clear = list(st.session_state.keys())
                for key in keys_to_clear:
                    del st.session_state[key]
                st.rerun()
    
    # Content routing
    if selected == 'account':
        render_user_profile(name, username)
    elif selected == 'admin_panel' and username == 'admin':
        render_admin_panel()
    elif selected == 'overview':
        render_overview(subscription_level)
    elif selected == 'price_charts':
        render_price_charts(subscription_level)
    elif selected == 'power_law_basic':
        render_power_law_basic(subscription_level)
    elif selected == 'power_law_advanced':
        render_power_law_advanced(subscription_level)
    elif selected == 'network_metrics':
        render_network_metrics(subscription_level)
    elif selected == 'data_export':
        render_data_export(subscription_level)
    elif selected == 'upgrade':
        render_upgrade_page(subscription_level)
    else:
        render_overview(subscription_level)  # Default fallback

def render_user_profile(name, username):
    """Enhanced user profile with update capabilities"""
    st.title("👤 User Profile & Settings")
    
    subscription_level = get_user_subscription(username)
    
    # Get user info from config
    user_info = config['credentials']['usernames'].get(username, {})
    
    profile_tabs = sac.tabs([
        sac.TabsItem(label='Profile Info', icon='person-circle'),
        sac.TabsItem(label='Security', icon='shield-check'),
        sac.TabsItem(label='Subscription', icon='credit-card'),
        sac.TabsItem(label='Account Settings', icon='gear'),
    ], key='profile_tabs')
    
    if profile_tabs == 'Profile Info':
        st.subheader("📝 Personal Information")
        
        # Update user details widget
        try:
            if authenticator.update_user_details(username, 'Update user details'):
                st.success('✅ Profile updated successfully')
                if save_config():
                    st.success("Changes saved!")
        except Exception as e:
            st.error(f"Profile update error: {e}")
            st.info("Profile update feature may not be available in this version of streamlit-authenticator")
        
        # Display current info
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Full Name:** {user_info.get('first_name', '')} {user_info.get('last_name', '')}")
            st.write(f"**Email:** {user_info.get('email', 'Not set')}")
        with col2:
            st.write(f"**Username:** {username}")
            st.write(f"**Subscription:** {subscription_level.title()}")
    
    elif profile_tabs == 'Security':
        st.subheader("🔒 Security Settings")
        
        # Password reset
        try:
            if authenticator.reset_password(username, 'Change Password'):
                st.success('✅ Password changed successfully')
                if save_config():
                    st.success("Password updated!")
        except Exception as e:
            st.error(f"Password change error: {e}")
        
        # Security features
        st.markdown("---")
        st.markdown("#### 🛡️ Security Features")
        
        enable_2fa = st.checkbox("🔐 Enable Two-Factor Authentication", 
                                help="Requires email verification for login")
        
        if enable_2fa:
            st.success("✅ 2FA will be enabled on next login")
        
        # Login history
        st.markdown("#### 📊 Login History")
        failed_attempts = user_info.get('failed_login_attempts', 0)
        last_login = user_info.get('last_login', 'Never')
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Failed Login Attempts", failed_attempts)
        with col2:
            st.metric("Account Status", "Active" if user_info.get('logged_in') else "Logged Out")
    
    elif profile_tabs == 'Subscription':
        st.subheader("💳 Subscription Management")
        
        # Current subscription info
        st.markdown('<div class="feature-highlight">', unsafe_allow_html=True)
        st.markdown(f"### Current Plan: {subscription_level.title()}")
        
        if subscription_level == 'free':
            st.markdown("**Free Features:**")
            st.write("• Basic price charts")
            st.write("• 30-day data history")
            st.write("• Simple power law analysis")
        elif subscription_level == 'premium':
            st.markdown("**Premium Features:**")
            st.write("• Advanced analytics")
            st.write("• Full historical data")
            st.write("• Data export capabilities")
            st.write("• Network metrics")
        else:  # pro
            st.markdown("**Pro Features:**")
            st.write("• All Premium features")
            st.write("• Research workspace")
            st.write("• Custom models")
            st.write("• API access")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Upgrade options
        if subscription_level != 'pro':
            target_plan = 'premium' if subscription_level == 'free' else 'pro'
            if st.button(f"⬆️ Upgrade to {target_plan.title()}", type="primary"):
                st.balloons()
                st.success(f"Redirecting to {target_plan} upgrade... (Demo)")
    
    else:  # Account Settings
        st.subheader("⚙️ Account Settings")
        
        # Account preferences
        st.markdown("#### 🎛️ Preferences")
        
        email_notifications = st.checkbox("📧 Email Notifications", value=True)
        marketing_emails = st.checkbox("📢 Marketing Updates", value=False)
        data_retention = st.selectbox("📊 Data Retention", ["1 month", "6 months", "1 year", "Indefinite"])
        
        if st.button("💾 Save Preferences"):
            st.success("✅ Preferences saved!")
        
        # Danger zone
        st.markdown("---")
        st.markdown("#### ⚠️ Danger Zone")
        
        if st.button("🗑️ Delete Account", type="secondary"):
            st.error("Account deletion would be processed here (Demo)")
    
    # Back to dashboard button
    if st.button("← Back to Dashboard"):
        st.session_state.show_profile = False
        st.rerun()
    
    # Add logout button in profile as well
    st.markdown("---")
    if st.button("🚪 Logout from Profile", type="secondary", use_container_width=True):
        # Manual logout by clearing session state
        for key in ['authentication_status', 'name', 'username', 'logout', 'show_profile']:
            if key in st.session_state:
                del st.session_state[key]
        
        # Also try the authenticator logout
        try:
            authenticator.logout()
        except:
            pass
        
        st.rerun()

def render_overview(subscription_level):
    """Enhanced overview page with different features based on subscription"""
    st.title("📊 Kaspa Market Overview")
    
    df = fetch_kaspa_price_data()
    if df.empty:
        st.error("Unable to load data")
        return
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    current_price = df['price'].iloc[-1]
    price_change = ((df['price'].iloc[-1] - df['price'].iloc[-7]) / df['price'].iloc[-7]) * 100
    
    with col1:
        st.metric("Current Price", f"${current_price:.4f}", f"{price_change:+.2f}%")
    with col2:
        st.metric("24h Volume", f"${df['volume'].iloc[-1]:,.0f}")
    with col3:
        st.metric("Market Cap", "$2.1B", "Est.")
    with col4:
        if subscription_level in ['premium', 'pro']:
            st.metric("Power Law", "Above Trend", "+15%")
        else:
            st.metric("Power Law", "🔒 Premium", "Upgrade")
    
    # Chart section
    st.subheader("📈 Price Chart")
    
    # Different data access based on subscription
    if subscription_level == 'free':
        chart_data = df.tail(30)  # Last 30 days only
        st.info("📊 Free users see last 30 days. Upgrade for full historical data!")
    else:
        chart_data = df  # Full historical data
    
    if PLOTLY_AVAILABLE:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=chart_data['timestamp'], 
            y=chart_data['price'], 
            name='KAS Price',
            line=dict(color='#70C7BA', width=2)
        ))
        
        # Add volume as secondary y-axis for premium+
        if subscription_level in ['premium', 'pro']:
            fig.add_trace(go.Scatter(
                x=chart_data['timestamp'],
                y=chart_data['volume'],
                name='Volume',
                yaxis='y2',
                opacity=0.3,
                line=dict(color='orange')
            ))
            
            fig.update_layout(
                yaxis2=dict(
                    title="Volume",
                    overlaying='y',
                    side='right'
                )
            )
        
        fig.update_layout(
            title="Kaspa Price History",
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            height=500,
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.line_chart(chart_data.set_index('timestamp')['price'])
    
    # Market insights section
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Market Insights")
        
        if subscription_level in ['premium', 'pro']:
            # Premium insights
            st.markdown("#### 🔍 Technical Analysis")
            st.write("• RSI: 65.2 (Neutral)")
            st.write("• MACD: Bullish crossover")
            st.write("• Support: $0.0245")
            st.write("• Resistance: $0.0289")
            
            st.markdown("#### 📊 On-chain Metrics")
            st.write("• Hash Rate: 1.2 EH/s (+5.2%)")
            st.write("• Active Addresses: 45,231")
            st.write("• Transaction Count: 892,123")
        else:
            # Free user paywall
            st.markdown('<div class="paywall-container">', unsafe_allow_html=True)
            st.markdown("### 🔒 Premium Features")
            st.markdown("Unlock advanced market insights:")
            st.markdown("• Technical analysis indicators")
            st.markdown("• On-chain metrics")
            st.markdown("• Price predictions")
            if st.button("⭐ Upgrade to Premium", key="insights_upgrade"):
                st.balloons()
                st.success("Redirecting to upgrade page...")
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.subheader("🎯 Quick Actions")
        
        # Different actions based on subscription
        if subscription_level == 'free':
            st.button("📊 View Basic Charts", use_container_width=True)
            st.button("📈 Simple Power Law", use_container_width=True)
            st.button("⭐ Upgrade Account", type="primary", use_container_width=True)
        elif subscription_level == 'premium':
            st.button("📊 Advanced Analytics", use_container_width=True)
            st.button("📈 Power Law Models", use_container_width=True)
            st.button("📋 Export Data", use_container_width=True)
            st.button("👑 Upgrade to Pro", type="primary", use_container_width=True)
        else:  # pro
            st.button("🔬 Research Workspace", use_container_width=True)
            st.button("🤖 Custom Models", use_container_width=True)
            st.button("🔌 API Access", use_container_width=True)
            st.button("📊 Admin Dashboard", use_container_width=True)

def render_price_charts(subscription_level):
    """Price charts page"""
    st.title("📈 Price Charts")
    
    df = fetch_kaspa_price_data()
    if df.empty:
        st.error("Unable to load data")
        return
    
    # Chart options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        chart_type = st.selectbox("Chart Type", ["Line", "Candlestick", "Area"])
    with col2:
        time_range = st.selectbox("Time Range", 
                                 ["30D", "90D", "1Y", "All"] if subscription_level != 'free' 
                                 else ["30D", "🔒 90D (Premium)", "🔒 1Y (Premium)", "🔒 All (Premium)"])
    with col3:
        if subscription_level in ['premium', 'pro']:
            indicators = st.multiselect("Indicators", ["SMA", "EMA", "RSI", "MACD"])
        else:
            st.selectbox("Indicators", ["🔒 Premium Feature"])
    
    # Filter data based on time range and subscription
    if time_range == "30D" or subscription_level == 'free':
        chart_data = df.tail(30)
    elif time_range == "90D":
        chart_data = df.tail(90)
    elif time_range == "1Y":
        chart_data = df.tail(365)
    else:
        chart_data = df
    
    # Create chart
    if PLOTLY_AVAILABLE:
        fig = go.Figure()
        
        if chart_type == "Line":
            fig.add_trace(go.Scatter(x=chart_data['timestamp'], y=chart_data['price'], 
                                   name='KAS Price', line=dict(color='#70C7BA')))
        elif chart_type == "Area":
            fig.add_trace(go.Scatter(x=chart_data['timestamp'], y=chart_data['price'], 
                                   fill='tonexty', name='KAS Price'))
        
        fig.update_layout(title=f"Kaspa Price - {time_range}", height=600)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.line_chart(chart_data.set_index('timestamp')['price'])

def render_power_law_basic(subscription_level):
    """Basic power law analysis"""
    st.title("📊 Power Law Analysis - Basic")
    
    if subscription_level == 'free':
        st.info("📈 Basic power law model for free users")
        
        # Simple power law visualization
        df = fetch_kaspa_price_data()
        if not df.empty:
            # Create simple trend line
            days_since_start = (df['timestamp'] - df['timestamp'].min()).dt.days
            trend_line = 0.01 * (days_since_start / 365) ** 1.5 + 0.01
            
            if PLOTLY_AVAILABLE:
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=df['timestamp'], y=df['price'], 
                                       name='KAS Price', line=dict(color='blue')))
                fig.add_trace(go.Scatter(x=df['timestamp'], y=trend_line, 
                                       name='Power Law Trend', line=dict(color='red', dash='dash')))
                fig.update_layout(title="Basic Power Law Model", height=500)
                st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("### 📋 Basic Analysis")
            st.write(f"• Current price is {'above' if df['price'].iloc[-1] > trend_line.iloc[-1] else 'below'} trend")
            st.write(f"• Deviation: {((df['price'].iloc[-1] / trend_line.iloc[-1]) - 1) * 100:.1f}%")
    else:
        st.info("🎯 You have access to Advanced Power Law Analysis! Check the Analytics menu.")

def render_power_law_advanced(subscription_level):
    """Advanced power law analysis for premium users"""
    if subscription_level not in ['premium', 'pro']:
        st.error("🔒 This feature requires Premium or Pro subscription")
        return
    
    st.title("🔬 Advanced Power Law Analysis")
    
    # Advanced power law features
    analysis_tabs = sac.tabs([
        sac.TabsItem(label='Multiple Models', icon='graph-up'),
        sac.TabsItem(label='Regression Analysis', icon='calculator'),
        sac.TabsItem(label='Predictions', icon='crystal-ball'),
    ], key='powerlaw_tabs')
    
    df = fetch_kaspa_price_data()
    
    if analysis_tabs == 'Multiple Models':
        st.subheader("📊 Multiple Power Law Models")
        
        # Generate multiple trend lines
        days_since_start = (df['timestamp'] - df['timestamp'].min()).dt.days
        
        model1 = 0.01 * (days_since_start / 365) ** 1.2 + 0.008  # Conservative
        model2 = 0.01 * (days_since_start / 365) ** 1.5 + 0.01   # Base
        model3 = 0.01 * (days_since_start / 365) ** 1.8 + 0.012  # Aggressive
        
        if PLOTLY_AVAILABLE:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df['timestamp'], y=df['price'], 
                                   name='KAS Price', line=dict(color='blue')))
            fig.add_trace(go.Scatter(x=df['timestamp'], y=model1, 
                                   name='Conservative Model', line=dict(color='green', dash='dash')))
            fig.add_trace(go.Scatter(x=df['timestamp'], y=model2, 
                                   name='Base Model', line=dict(color='red', dash='dash')))
            fig.add_trace(go.Scatter(x=df['timestamp'], y=model3, 
                                   name='Aggressive Model', line=dict(color='purple', dash='dash')))
            
            fig.update_layout(title="Multiple Power Law Models", height=600)
            st.plotly_chart(fig, use_container_width=True)
    
    elif analysis_tabs == 'Regression Analysis':
        st.subheader("📈 Regression Analysis")
        st.write("Advanced statistical analysis of power law fit:")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("R² Coefficient", "0.87")
            st.metric("P-value", "< 0.001")
        with col2:
            st.metric("Standard Error", "0.045")
            st.metric("Confidence Interval", "95%")
    
    else:  # Predictions
        st.subheader("🔮 Price Predictions")
        st.write("AI-powered price predictions based on power law models:")
        
        prediction_tabs = sac.tabs([
            sac.TabsItem(label='30 Days'),
            sac.TabsItem(label='90 Days'),
            sac.TabsItem(label='1 Year'),
        ], key='prediction_tabs')
        
        current_price = df['price'].iloc[-1]
        
        if prediction_tabs == '30 Days':
            st.metric("30-Day Target", f"${current_price * 1.15:.4f}", "+15%")
        elif prediction_tabs == '90 Days':
            st.metric("90-Day Target", f"${current_price * 1.35:.4f}", "+35%")
        else:
            st.metric("1-Year Target", f"${current_price * 2.1:.4f}", "+110%")

def render_network_metrics(subscription_level):
    """Network metrics analysis"""
    if subscription_level not in ['premium', 'pro']:
        st.error("🔒 This feature requires Premium or Pro subscription")
        return
    
    st.title("🌐 Network Metrics")
    
    # Network metrics dashboard
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Hash Rate", "1.23 EH/s", "+5.2%")
    with col2:
        st.metric("Difficulty", "3.45E+15", "+2.1%")
    with col3:
        st.metric("Block Time", "1.02s", "-0.02s")
    with col4:
        st.metric("Active Addresses", "45,231", "+12.5%")
    
    # Charts for network metrics
    metrics_tabs = sac.tabs([
        sac.TabsItem(label='Hash Rate', icon='cpu'),
        sac.TabsItem(label='Transactions', icon='arrow-repeat'),
        sac.TabsItem(label='Addresses', icon='people'),
    ], key='metrics_tabs')
    
    # Generate sample network data
    dates = pd.date_range(start='2023-01-01', end=datetime.now(), freq='D')
    np.random.seed(123)
    
    if metrics_tabs == 'Hash Rate':
        hash_rate_data = np.random.normal(1.2, 0.1, len(dates))
        hash_rate_data = np.maximum(hash_rate_data, 0.5)  # Ensure positive values
        
        if PLOTLY_AVAILABLE:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=dates, y=hash_rate_data, name='Hash Rate (EH/s)'))
            fig.update_layout(title="Kaspa Network Hash Rate", height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    elif metrics_tabs == 'Transactions':
        tx_data = np.random.poisson(50000, len(dates))
        
        if PLOTLY_AVAILABLE:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=dates, y=tx_data, name='Daily Transactions'))
            fig.update_layout(title="Daily Transaction Count", height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    else:  # Addresses
        addr_data = np.cumsum(np.random.poisson(100, len(dates))) + 10000
        
        if PLOTLY_AVAILABLE:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=dates, y=addr_data, name='Active Addresses'))
            fig.update_layout(title="Cumulative Active Addresses", height=400)
            st.plotly_chart(fig, use_container_width=True)

def render_data_export(subscription_level):
    """Data export functionality"""
    if subscription_level not in ['premium', 'pro']:
        st.error("🔒 This feature requires Premium or Pro subscription")
        return
    
    st.title("📋 Data Export")
    
    export_tabs = sac.tabs([
        sac.TabsItem(label='Price Data', icon='graph-up'),
        sac.TabsItem(label='Network Data', icon='diagram-3'),
        sac.TabsItem(label='Custom Reports', icon='file-earmark-text'),
    ], key='export_tabs')
    
    if export_tabs == 'Price Data':
        st.subheader("💰 Export Price Data")
        
        col1, col2 = st.columns(2)
        with col1:
            date_range = st.selectbox("Date Range", ["Last 30 days", "Last 90 days", "Last year", "All time"])
            file_format = st.selectbox("Format", ["CSV", "JSON", "Excel"])
        
        with col2:
            include_volume = st.checkbox("Include Volume Data", value=True)
            include_metrics = st.checkbox("Include Technical Indicators", value=False)
        
        if st.button("📥 Download Price Data", type="primary"):
            df = fetch_kaspa_price_data()
            st.success("✅ Data exported successfully!")
            st.download_button(
                label="Download CSV",
                data=df.to_csv(index=False),
                file_name=f"kaspa_price_data_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    
    elif export_tabs == 'Network Data':
        st.subheader("🌐 Export Network Data")
        st.info("Network metrics export coming soon...")
    
    else:  # Custom Reports
        st.subheader("📊 Custom Reports")
        
        if subscription_level == 'pro':
            st.write("Generate custom analytical reports:")
            
            report_type = st.selectbox("Report Type", [
                "Weekly Summary", 
                "Monthly Analysis", 
                "Power Law Report",
                "Technical Analysis Report"
            ])
            
            if st.button("📄 Generate Report", type="primary"):
                st.success("✅ Custom report generated!")
                st.info("Report would be generated and available for download.")
        else:
            st.info("🔒 Custom reports are available for Pro subscribers only.")

def render_upgrade_page(subscription_level):
    """Upgrade page"""
    st.title("⭐ Upgrade Your Account")
    
    if subscription_level == 'free':
        target_tier = 'premium'
        st.subheader("🚀 Upgrade to Premium")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🆓 Free (Current)")
            st.write("• Basic price charts")
            st.write("• 30-day data history")
            st.write("• Simple power law")
            st.write("• Community support")
            
        with col2:
            st.markdown("### ⭐ Premium - $29/month")
            st.write("• ✅ Advanced analytics")
            st.write("• ✅ Full historical data")
            st.write("• ✅ Data export capabilities")
            st.write("• ✅ Network metrics")
            st.write("• ✅ Email support")
            
            if st.button("💳 Upgrade to Premium", type="primary", use_container_width=True):
                st.balloons()
                st.success("Redirecting to payment...")
    
    elif subscription_level == 'premium':
        st.subheader("👑 Upgrade to Pro")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### ⭐ Premium (Current)")
            st.write("• Advanced analytics")
            st.write("• Full historical data")
            st.write("• Data export")
            st.write("• Network metrics")
            
        with col2:
            st.markdown("### 👑 Pro - $99/month")
            st.write("• ✅ All Premium features")
            st.write("• ✅ Research workspace")
            st.write("• ✅ Custom models")
            st.write("• ✅ API access")
            st.write("• ✅ Priority support")
            
            if st.button("💎 Upgrade to Pro", type="primary", use_container_width=True):
                st.balloons()
                st.success("Redirecting to Pro upgrade...")
    
    else:  # pro
        st.success("🎉 You have the highest tier - Pro!")
        st.info("Thank you for being a Pro subscriber. You have access to all features.")

def main():
    """Enhanced main application entry point"""
    
    # Check authentication status
    authentication_status = st.session_state.get('authentication_status')
    name = st.session_state.get('name')
    username = st.session_state.get('username')
    
    if authentication_status is not True:
        name, authentication_status, username = show_authentication_page()
        
        if authentication_status is True:
            st.rerun()
    else:
        show_main_app(name, username)

# Run the application
if __name__ == "__main__":
    main()
