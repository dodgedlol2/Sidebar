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
    """Add new user to session state config with proper password hashing"""
    if 'config' not in st.session_state:
        st.session_state.config = get_auth_config()
    
    if username not in st.session_state.config['credentials']['usernames']:
        # Hash the password using the same method as streamlit-authenticator
        import bcrypt
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        st.session_state.config['credentials']['usernames'][username] = {
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'password': hashed_password,  # Store hashed password
            'subscription': subscription,
            'failed_login_attempts': 0,
            'logged_in': False,
            'created_at': datetime.now().isoformat()
        }
        
        # Also update the global config variable
        global config
        config = st.session_state.config
        
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

.public-header {
    background: linear-gradient(135deg, #70C7BA 0%, #49A097 100%);
    padding: 1.5rem;
    border-radius: 12px;
    color: white;
    margin-bottom: 1.5rem;
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

.public-badge {
    background: #28a745;
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

.login-prompt {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 1.5rem;
    border-radius: 12px;
    color: white;
    text-align: center;
    margin: 1rem 0;
}

.public-cta {
    background: #f8f9fa;
    padding: 1.5rem;
    border-radius: 8px;
    border: 2px solid #70C7BA;
    margin: 1rem 0;
    text-align: center;
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
    if username == 'public':
        return 'public'
    user_config = config['credentials']['usernames'].get(username, {})
    return user_config.get('subscription', 'free')

def is_authenticated():
    """Check if user is authenticated"""
    return st.session_state.get('authentication_status') is True

def get_current_user():
    """Get current user info"""
    if is_authenticated():
        return {
            'name': st.session_state.get('name'),
            'username': st.session_state.get('username'),
            'subscription': get_user_subscription(st.session_state.get('username'))
        }
    return {
        'name': 'Public User',
        'username': 'public',
        'subscription': 'public'
    }

def show_login_prompt(feature_name="this feature"):
    """Show login prompt for premium features"""
    st.markdown('<div class="login-prompt">', unsafe_allow_html=True)
    st.markdown(f"### 🔐 Login Required")
    st.markdown(f"To access {feature_name}, please create a free account or login.")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    # Use feature_name to create unique keys
    safe_feature_name = feature_name.replace(" ", "_").replace("-", "_")
    
    with col1:
        if st.button("🚀 Create Free Account", type="primary", use_container_width=True, key=f"create_account_{safe_feature_name}"):
            st.session_state.show_auth = True
            st.session_state.auth_tab = 'Register'
            st.rerun()
    
    with col2:
        if st.button("🔑 Login", use_container_width=True, key=f"login_{safe_feature_name}"):
            st.session_state.show_auth = True
            st.session_state.auth_tab = 'Login'
            st.rerun()
    
    with col3:
        if st.button("ℹ️ Learn More", use_container_width=True, key=f"learn_more_{safe_feature_name}"):
            st.session_state.show_auth = True
            st.session_state.auth_tab = 'Pricing'
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_upgrade_prompt(current_subscription, required_subscription):
    """Show upgrade prompt for premium features"""
    st.markdown('<div class="paywall-container">', unsafe_allow_html=True)
    st.markdown(f"### ⭐ {required_subscription.title()} Feature")
    st.markdown(f"This feature requires a {required_subscription} subscription.")
    
    if current_subscription == 'free':
        price = "$29/month" if required_subscription == 'premium' else "$99/month"
    else:  # premium to pro
        price = "$99/month"
    
    st.markdown(f"**Upgrade to {required_subscription.title()} - {price}**")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button(f"⬆️ Upgrade to {required_subscription.title()}", type="primary", use_container_width=True, key=f"upgrade_to_{required_subscription}_{current_subscription}"):
            st.balloons()
            st.success(f"Redirecting to {required_subscription} upgrade...")
    
    with col2:
        if st.button("📋 View All Features", use_container_width=True, key=f"view_features_{required_subscription}_{current_subscription}"):
            st.session_state.show_pricing = True
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_public_header():
    """Render header for public users"""
    st.markdown('<div class="public-header">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown("# 💎 Kaspa Analytics Pro")
        st.markdown("*Professional blockchain analysis platform*")
    
    with col2:
        st.markdown('<span class="public-badge">PUBLIC ACCESS</span>', unsafe_allow_html=True)
        st.markdown("*Explore basic features*")
    
    with col3:
        col3a, col3b = st.columns(2)
        with col3a:
            if st.button("🔑 Login", type="secondary", use_container_width=True, key="header_login"):
                st.session_state.show_auth = True
                st.session_state.auth_tab = 'Login'
                st.rerun()
        with col3b:
            if st.button("🚀 Sign Up", type="primary", use_container_width=True, key="header_signup"):
                st.session_state.show_auth = True
                st.session_state.auth_tab = 'Register'
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_authenticated_header(user):
    """Render header for authenticated users"""
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown("# 💎 Kaspa Analytics Pro")
        st.markdown("*Professional blockchain analysis platform*")
    
    with col2:
        st.markdown(f"**Welcome, {user['name']}!**")
        subscription = user['subscription']
        if subscription == 'free':
            st.markdown('<span class="free-badge">FREE USER</span>', unsafe_allow_html=True)
        elif subscription == 'premium':
            st.markdown('<span class="premium-badge">PREMIUM</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="pro-badge">PRO</span>', unsafe_allow_html=True)
    
    with col3:
        logout_col1, logout_col2 = st.columns(2)
        with logout_col1:
            if st.button("⚙️ Profile", type="secondary", key="header_profile"):
                st.session_state.show_profile = True
                st.rerun()
        with logout_col2:
            if st.button("🚪 Logout", type="secondary", key="header_logout"):
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
                for key in ['show_profile', 'show_auth', 'auth_tab']:
                    if key in st.session_state:
                        del st.session_state[key]
                
                # Force rerun to show public page
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_public_sidebar():
    """Render sidebar for public users"""
    with st.sidebar:
        st.title("🌐 Public Access")
        st.markdown("*Explore Kaspa Analytics*")
        
        # Public menu items
        menu_items = [
            sac.MenuItem('overview', icon='house-fill', tag=sac.Tag('Free', color='green')),
            sac.MenuItem('price_charts', icon='graph-up', description='Basic price data'),
            sac.MenuItem('basic_analytics', icon='bar-chart', description='Simple analysis'),
            sac.MenuItem(type='divider'),
            sac.MenuItem('features', icon='star', tag=sac.Tag('Learn More', color='blue')),
            sac.MenuItem('pricing', icon='currency-dollar', description='View plans'),
            sac.MenuItem('login', icon='box-arrow-in-right', tag=sac.Tag('Sign In', color='orange')),
        ]
        
        selected = sac.menu(menu_items, open_all=True, key='public_menu')
        
        # Quick stats (public version)
        st.markdown("---")
        st.markdown("**⚡ Market Stats**")
        df = fetch_kaspa_price_data()
        if not df.empty:
            current_price = df['price'].iloc[-1]
            st.metric("KAS Price", f"${current_price:.4f}")
            st.metric("24h Change", "+2.1%", delta_color="normal")
        
        # Call to action
        st.markdown("---")
        st.markdown('<div class="public-cta">', unsafe_allow_html=True)
        st.markdown("### 🎯 Get Full Access")
        st.markdown("Unlock premium features:")
        st.markdown("• Advanced analytics")
        st.markdown("• Historical data")
        st.markdown("• Export capabilities")
        
        if st.button("🚀 Start Free Trial", type="primary", use_container_width=True, key="sidebar_free_trial"):
            st.session_state.show_auth = True
            st.session_state.auth_tab = 'Register'
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        return selected

def render_authenticated_sidebar(user):
    """Render sidebar for authenticated users"""
    with st.sidebar:
        st.title("📊 Analytics Menu")
        
        subscription_level = user['subscription']
        
        # Create menu based on subscription level
        if subscription_level == 'free':
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
            if user['username'] == 'admin':
                menu_items.append(sac.MenuItem('admin_panel', icon='shield-check', tag=sac.Tag('Admin', color='red')))
        
        selected = sac.menu(menu_items, open_all=True, key='main_menu')
        
        # Quick stats
        st.markdown("---")
        st.markdown("**⚡ Quick Stats**")
        df = fetch_kaspa_price_data()
        if not df.empty:
            current_price = df['price'].iloc[-1]
            st.metric("KAS Price", f"${current_price:.4f}")
            
        return selected

def show_authentication_page():
    """Enhanced authentication page with all login options"""
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    st.title("💎 Kaspa Analytics Pro")
    st.markdown("*Professional Kaspa blockchain analysis and research platform*")
    st.markdown("*Now with enhanced security and user management*")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Get the desired tab from session state
    default_tab = st.session_state.get('auth_tab', 'Login')
    tab_index = ['Login', 'Register', 'Pricing', 'Features'].index(default_tab) if default_tab in ['Login', 'Register', 'Pricing', 'Features'] else 0
    
    # Authentication tabs
    auth_tabs = sac.tabs([
        sac.TabsItem(label='Login', icon='box-arrow-in-right'),
        sac.TabsItem(label='Register', icon='person-plus'),
        sac.TabsItem(label='Pricing', icon='currency-dollar'),
        sac.TabsItem(label='Features', icon='star'),
    ], index=tab_index, key='auth_tabs')
    
    # Initialize return values
    name = None
    authentication_status = None
    username = None
    
    if auth_tabs == 'Login':
        name, authentication_status, username = render_login_section()
    elif auth_tabs == 'Register':
        render_registration_section()
    elif auth_tabs == 'Pricing':
        render_pricing_page()
    else:  # Features
        render_features_page()
    
    # If no authentication happened, get current session state
    if authentication_status is None:
        name = st.session_state.get('name')
        authentication_status = st.session_state.get('authentication_status')
        username = st.session_state.get('username')
    
    # Back to public site button
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("← Back to Public Site", use_container_width=True, key="auth_back_to_public"):
            # Clear auth display flags
            for key in ['show_auth', 'auth_tab']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    
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
        elif authentication_status == None:
            st.info("ℹ️ Please enter your credentials to access the platform.")
        
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
        st.info("🎉 Start with a free account - upgrade anytime!")
        
        # Manual registration form
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
            
            new_subscription = st.selectbox("Start with:", ['free'], 
                                           help="Free account with upgrade options")
            
            agree_terms = st.checkbox("I agree to the Terms of Service and Privacy Policy*")
            
            submit_registration = st.form_submit_button("🚀 Create Free Account", type="primary")
        
        # Handle form submission OUTSIDE the form
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
                    st.info("👈 Please use the Login tab to sign in with your new account")
                    st.balloons()
                    
                    # Show the created user details for confirmation
                    st.markdown("#### ✅ Registration Details:")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Username:** {new_username}")
                        st.write(f"**Email:** {new_email}")
                    with col2:
                        st.write(f"**Name:** {new_first_name} {new_last_name}")
                        st.write(f"**Account Type:** {new_subscription}")
                    
                else:
                    st.error("❌ Registration failed. Username may already exist.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Return None values since registration doesn't log in automatically
    return None, None, None

def render_pricing_page():
    """Render pricing information"""
    st.markdown("### 💰 Choose Your Plan")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        st.markdown("### 🆓 Free")
        st.markdown("**$0/month**")
        st.markdown("Perfect for getting started")
        st.markdown("---")
        st.markdown("**Features:**")
        st.write("• Basic price charts")
        st.write("• 30-day data history")
        st.write("• Simple power law analysis")
        st.write("• Community support")
        st.markdown("---")
        if st.button("🚀 Get Started Free", use_container_width=True, key="pricing_free"):
            st.session_state.auth_tab = 'Register'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        st.markdown("### ⭐ Premium")
        st.markdown("**$29/month**")
        st.markdown("Most popular choice")
        st.markdown("---")
        st.markdown("**Everything in Free, plus:**")
        st.write("• Advanced analytics")
        st.write("• Full historical data")
        st.write("• Data export capabilities")
        st.write("• Network metrics analysis")
        st.write("• Email support")
        st.markdown("---")
        if st.button("⭐ Upgrade to Premium", type="primary", use_container_width=True, key="pricing_premium"):
            st.balloons()
            st.success("Redirecting to premium signup...")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        st.markdown("### 👑 Pro")
        st.markdown("**$99/month**")
        st.markdown("For professional traders")
        st.markdown("---")
        st.markdown("**Everything in Premium, plus:**")
        st.write("• Research workspace")
        st.write("• Custom power law models")
        st.write("• API access")
        st.write("• Priority support")
        st.write("• White-label reports")
        st.markdown("---")
        if st.button("👑 Go Pro", use_container_width=True, key="pricing_pro"):
            st.balloons()
            st.success("Redirecting to pro signup...")
        st.markdown('</div>', unsafe_allow_html=True)

def render_features_page():
    """Render features showcase"""
    st.markdown("### ⭐ Platform Features")
    
    # Feature categories
    feature_tabs = sac.tabs([
        sac.TabsItem(label='Analytics', icon='graph-up'),
        sac.TabsItem(label='Data & Export', icon='download'),
        sac.TabsItem(label='Research Tools', icon='search'),
    ], key='feature_tabs')
    
    if feature_tabs == 'Analytics':
        st.markdown("#### 📊 Advanced Analytics")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Power Law Analysis**")
            st.write("• Multiple regression models")
            st.write("• Price prediction algorithms")
            st.write("• Trend deviation analysis")
            st.write("• Statistical confidence intervals")
            
            st.markdown("**Technical Indicators**")
            st.write("• RSI, MACD, Moving averages")
            st.write("• Custom indicator builder")
            st.write("• Multi-timeframe analysis")
        
        with col2:
            st.markdown("**Network Metrics**")
            st.write("• Hash rate tracking")
            st.write("• Active address analysis")
            st.write("• Transaction volume patterns")
            st.write("• Mining difficulty trends")
            
            st.markdown("**Market Intelligence**")
            st.write("• Supply/demand dynamics")
            st.write("• Exchange flow analysis")
            st.write("• Whale movement tracking")
    
    elif feature_tabs == 'Data & Export':
        st.markdown("#### 📋 Data Management")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Data Access**")
            st.write("• Real-time price feeds")
            st.write("• Historical data back to genesis")
            st.write("• High-frequency tick data")
            st.write("• Multiple data sources")
            
        with col2:
            st.markdown("**Export Capabilities**")
            st.write("• CSV, JSON, Excel formats")
            st.write("• Custom date ranges")
            st.write("• Automated reports")
            st.write("• API integration")
    
    else:  # Research Tools
        st.markdown("#### 🔬 Research Workspace")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Custom Models**")
            st.write("• Build your own indicators")
            st.write("• Backtesting framework")
            st.write("• Strategy optimization")
            st.write("• Performance analytics")
            
        with col2:
            st.markdown("**Collaboration**")
            st.write("• Share research publicly")
            st.write("• Team workspaces")
            st.write("• Version control")
            st.write("• Peer review system")

def render_public_overview():
    """Public overview page with limited features"""
    st.title("📊 Kaspa Market Overview")
    st.markdown("*Public access - Create an account for full features*")
    
    df = fetch_kaspa_price_data()
    if df.empty:
        st.error("Unable to load data")
        return
    
    # Key metrics row (limited)
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
        st.metric("Advanced Analytics", "🔒 Login Required", "")
    
    # Chart section (limited to 7 days for public)
    st.subheader("📈 Price Chart (Last 7 Days)")
    chart_data = df.tail(7)  # Only last 7 days for public
    
    if PLOTLY_AVAILABLE:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=chart_data['timestamp'], 
            y=chart_data['price'], 
            name='KAS Price',
            line=dict(color='#70C7BA', width=2)
        ))
        
        fig.update_layout(
            title="Kaspa Price - Last 7 Days (Public View)",
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            height=400,
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.line_chart(chart_data.set_index('timestamp')['price'])
    
    st.info("📊 Public users see last 7 days. Create a free account for 30+ days of data!")
    
    # Limited insights section
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Basic Market Info")
        st.markdown("#### 📊 Current Stats")
        st.write("• 7-day price range available")
        st.write("• Basic volume information")
        st.write("• Simple price metrics")
        
        st.markdown('<div class="login-prompt">', unsafe_allow_html=True)
        st.markdown("### 🔐 Want More Data?")
        st.markdown("Create a free account to access:")
        st.markdown("• 30+ days of price history")
        st.markdown("• Technical analysis tools")
        st.markdown("• Basic power law analysis")
        
        if st.button("🚀 Create Free Account", type="primary", use_container_width=True, key="overview_create_account"):
            st.session_state.show_auth = True
            st.session_state.auth_tab = 'Register'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.subheader("🎯 What You Can Do")
        
        st.markdown("#### 🌐 Public Access")
        st.write("✅ View current price")
        st.write("✅ See 7-day chart")
        st.write("✅ Basic market stats")
        st.write("✅ Learn about features")
        
        st.markdown("#### 🔒 Requires Account")
        st.write("🔒 30+ days of history")
        st.write("🔒 Technical indicators")
        st.write("🔒 Power law analysis")
        st.write("🔒 Data export")
        st.write("🔒 Advanced analytics")
        
        if st.button("📋 View All Features", use_container_width=True, key="overview_view_features"):
            st.session_state.show_auth = True
            st.session_state.auth_tab = 'Features'
            st.rerun()

def render_public_price_charts():
    """Public price charts with limitations"""
    st.title("📈 Price Charts")
    st.markdown("*Public view - Limited to basic charts*")
    
    df = fetch_kaspa_price_data()
    if df.empty:
        st.error("Unable to load data")
        return
    
    # Limited chart options for public
    col1, col2, col3 = st.columns(3)
    
    with col1:
        chart_type = st.selectbox("Chart Type", ["Line"])
    with col2:
        time_range = st.selectbox("Time Range", ["7D"])
    with col3:
        st.selectbox("Indicators", ["🔒 Login Required"])
    
    # Filter data to last 7 days only
    chart_data = df.tail(7)
    
    # Create basic chart
    if PLOTLY_AVAILABLE:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=chart_data['timestamp'], y=chart_data['price'], 
                               name='KAS Price', line=dict(color='#70C7BA')))
        fig.update_layout(title="Kaspa Price - Last 7 Days (Public Access)", height=500)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.line_chart(chart_data.set_index('timestamp')['price'])
    
    # Show what's available with an account
    show_login_prompt("advanced charting features")

def render_public_basic_analytics():
    """Basic analytics for public users"""
    st.title("📊 Basic Analytics")
    st.markdown("*Public access - Simple analysis tools*")
    
    df = fetch_kaspa_price_data()
    if not df.empty:
        # Very basic analytics
        chart_data = df.tail(7)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            price_avg = chart_data['price'].mean()
            st.metric("7-Day Average", f"${price_avg:.4f}")
        
        with col2:
            price_min = chart_data['price'].min()
            st.metric("7-Day Low", f"${price_min:.4f}")
        
        with col3:
            price_max = chart_data['price'].max()
            st.metric("7-Day High", f"${price_max:.4f}")
        
        # Simple trend analysis
        st.subheader("📈 Simple Trend Analysis")
        recent_trend = "Upward" if chart_data['price'].iloc[-1] > chart_data['price'].iloc[0] else "Downward"
        st.write(f"**7-Day Trend:** {recent_trend}")
        st.write(f"**Price Change:** {((chart_data['price'].iloc[-1] / chart_data['price'].iloc[0]) - 1) * 100:.2f}%")
    
    # Show what advanced analytics offers
    st.subheader("🔒 Advanced Analytics Available")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**With Free Account:**")
        st.write("• 30-day analysis")
        st.write("• Basic power law model")
        st.write("• Simple technical indicators")
        st.write("• Price trend analysis")
    
    with col2:
        st.markdown("**With Premium Account:**")
        st.write("• Advanced power law models")
        st.write("• Network metrics analysis")
        st.write("• Custom indicators")
        st.write("• Data export capabilities")
    
    show_login_prompt("advanced analytics")

# Admin panel and user management functions (same as before)
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

# Authenticated user functions (same as before but with subscription checks)
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
            # Free user upgrade prompt
            show_upgrade_prompt(subscription_level, 'premium')
    
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

# Additional authenticated functions (power law, network metrics, etc.) would be the same as before...
# For brevity, I'll include just the main navigation and structure

def main():
    """Enhanced main application entry point with public access"""
    
    # Initialize session state flags
    if 'show_auth' not in st.session_state:
        st.session_state.show_auth = False
    
    # Check if user wants to show auth page
    if st.session_state.get('show_auth'):
        # Show authentication page
        name, authentication_status, username = show_authentication_page()
        
        if authentication_status is True:
            # Clear auth flags and show main app
            st.session_state.show_auth = False
            if 'auth_tab' in st.session_state:
                del st.session_state['auth_tab']
            st.rerun()
        return
    
    # Check if user is authenticated
    user = get_current_user()
    
    if user['username'] == 'public':
        # PUBLIC ACCESS - Show header and public content
        render_public_header()
        
        # Public sidebar and navigation
        selected = render_public_sidebar()
        
        # Route public content
        if selected == 'overview':
            render_public_overview()
        elif selected == 'price_charts':
            render_public_price_charts()
        elif selected == 'basic_analytics':
            render_public_basic_analytics()
        elif selected == 'features':
            st.session_state.show_auth = True
            st.session_state.auth_tab = 'Features'
            st.rerun()
        elif selected == 'pricing':
            st.session_state.show_auth = True
            st.session_state.auth_tab = 'Pricing'
            st.rerun()
        elif selected == 'login':
            st.session_state.show_auth = True
            st.session_state.auth_tab = 'Login'
            st.rerun()
        else:
            render_public_overview()  # Default
    
    else:
        # AUTHENTICATED ACCESS - Show full app
        render_authenticated_header(user)
        
        # Check if user wants to see profile
        if st.session_state.get('show_profile'):
            render_user_profile(user['name'], user['username'])
            return
        
        # Authenticated sidebar and navigation
        selected = render_authenticated_sidebar(user)
        
        # Route authenticated content based on subscription
        subscription_level = user['subscription']
        
        if selected == 'account':
            render_user_profile(user['name'], user['username'])
        elif selected == 'admin_panel' and user['username'] == 'admin':
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

# Placeholder functions for authenticated features
def render_user_profile(name, username):
    st.title("👤 User Profile")
    st.write(f"Welcome {name}!")
    if st.button("← Back to Dashboard", key="profile_back"):
        st.session_state.show_profile = False
        st.rerun()

def render_price_charts(subscription_level):
    st.title("📈 Price Charts")
    if subscription_level == 'free':
        st.info("Free users get basic charts. Upgrade for advanced features!")
    else:
        st.success("Advanced charting available!")

def render_power_law_basic(subscription_level):
    st.title("📊 Basic Power Law")
    st.info("Basic power law analysis for free users")

def render_power_law_advanced(subscription_level):
    if subscription_level not in ['premium', 'pro']:
        show_upgrade_prompt(subscription_level, 'premium')
        return
    st.title("🔬 Advanced Power Law")
    st.success("Advanced power law analysis!")

def render_network_metrics(subscription_level):
    if subscription_level not in ['premium', 'pro']:
        show_upgrade_prompt(subscription_level, 'premium')
        return
    st.title("🌐 Network Metrics")
    st.success("Network metrics analysis!")

def render_data_export(subscription_level):
    if subscription_level not in ['premium', 'pro']:
        show_upgrade_prompt(subscription_level, 'premium')
        return
    st.title("📋 Data Export")
    st.success("Data export functionality!")

def render_upgrade_page(subscription_level):
    st.title("⭐ Upgrade Your Account")
    st.info(f"Current plan: {subscription_level}")

# Run the application
if __name__ == "__main__":
    main()
