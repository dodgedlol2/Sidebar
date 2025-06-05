import streamlit as st
import streamlit_antd_components as sac
import streamlit_authenticator as stauth
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Try to import Plotly, fallback to basic charts if not available
try:
    import plotly.graph_objects as go
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    st.warning("📊 Plotly not installed. Using basic charts. Install with: pip install plotly")

# Configure page settings
st.set_page_config(
    page_title="Kaspa Analytics Pro",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Authentication configuration
def get_auth_config():
    """Get authentication configuration"""
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
            'beta@kaspalytics.com'
        ]
    }
    return config

# Initialize configuration
if 'config' not in st.session_state:
    st.session_state.config = get_auth_config()

config = st.session_state.config

# Initialize authenticator
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized'],
    auto_hash=True
)

# User management functions
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

def get_user_subscription(username):
    """Get user subscription level"""
    user_config = config['credentials']['usernames'].get(username, {})
    return user_config.get('subscription', 'free')

# Custom CSS
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
</style>
""", unsafe_allow_html=True)

# Data fetching function
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

def show_authentication_page():
    """Authentication page"""
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    st.title("💎 Kaspa Analytics Pro")
    st.markdown("*Professional Kaspa blockchain analysis platform*")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Authentication tabs
    auth_tabs = sac.tabs([
        sac.TabsItem(label='Login', icon='box-arrow-in-right'),
        sac.TabsItem(label='Register', icon='person-plus'),
    ], index=0, key='auth_tabs')
    
    if auth_tabs == 'Login':
        render_login_section()
    else:
        render_registration_section()

def render_login_section():
    """Render login section"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        st.markdown("### 🔐 Login to Your Account")
        
        # Main login widget
        authenticator.login()
        
        # Demo credentials
        st.markdown("---")
        st.markdown("**🔑 Demo Accounts:**")
        
        demo_info = sac.tabs([
            sac.TabsItem(label='Free', icon='person'),
            sac.TabsItem(label='Premium', icon='star'),
            sac.TabsItem(label='Pro', icon='crown'),
        ], index=0, key='demo_creds')
        
        if demo_info == 'Free':
            st.code("Username: free_user\nPassword: free123")
        elif demo_info == 'Premium':
            st.code("Username: premium_user\nPassword: premium123")
        else:
            st.code("Username: admin\nPassword: admin123")
        
        st.markdown('</div>', unsafe_allow_html=True)

def render_registration_section():
    """Render registration section"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        st.markdown("### ✨ Create New Account")
        
        # Registration widget
        try:
            if authenticator.register_user(form_name='Register User', location='main', preauthorization=False):
                st.success('✅ User registered successfully!')
        except Exception as e:
            st.error(f"Registration error: {e}")
            # Fallback manual registration
            render_manual_registration_form()
        
        st.markdown('</div>', unsafe_allow_html=True)

def render_manual_registration_form():
    """Manual registration form"""
    st.markdown("#### 📝 Manual Registration")
    
    with st.form("manual_registration"):
        col1, col2 = st.columns(2)
        
        with col1:
            new_username = st.text_input("Username*")
            new_first_name = st.text_input("First Name*")
            new_email = st.text_input("Email*")
        
        with col2:
            new_last_name = st.text_input("Last Name*")
            new_password = st.text_input("Password*", type="password")
            new_password_confirm = st.text_input("Confirm Password*", type="password")
        
        submit_registration = st.form_submit_button("🚀 Create Account")
        
        if submit_registration:
            if new_username and new_email and new_password and new_password == new_password_confirm:
                if add_new_user_to_config(new_username, new_email, new_first_name, new_last_name, new_password):
                    st.success("🎉 Account created successfully!")
                else:
                    st.error("❌ Username already exists!")
            else:
                st.error("❌ Please fill all fields and ensure passwords match")

def show_main_app(name, username):
    """Main application"""
    subscription_level = get_user_subscription(username)
    
    # Header
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown("# 💎 Kaspa Analytics Pro")
        st.markdown("*Professional blockchain analysis platform*")
    
    with col2:
        st.markdown(f"**Welcome, {name}!**")
        if subscription_level == 'free':
            st.markdown('<span class="free-badge">FREE</span>', unsafe_allow_html=True)
        elif subscription_level == 'premium':
            st.markdown('<span class="premium-badge">PREMIUM</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="pro-badge">PRO</span>', unsafe_allow_html=True)
    
    with col3:
        if st.button("🚪 Logout"):
            for key in ['authentication_status', 'name', 'username']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.title("📊 Analytics Menu")
        
        menu_items = [
            sac.MenuItem('overview', icon='house-fill'),
            sac.MenuItem('price_charts', icon='graph-up'),
        ]
        
        if subscription_level in ['premium', 'pro']:
            menu_items.append(sac.MenuItem('advanced', icon='bar-chart-fill'))
        
        selected = sac.menu(menu_items, key='main_menu')
    
    # Content
    render_overview(subscription_level)

def render_overview(subscription_level):
    """Overview page"""
    st.title("📊 Kaspa Market Overview")
    
    df = fetch_kaspa_price_data()
    if df.empty:
        st.error("Unable to load data")
        return
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    current_price = df['price'].iloc[-1]
    
    with col1:
        st.metric("Current Price", f"${current_price:.4f}")
    with col2:
        st.metric("24h Volume", f"${df['volume'].iloc[-1]:,.0f}")
    with col3:
        st.metric("Market Cap", "$2.1B")
    with col4:
        if subscription_level in ['premium', 'pro']:
            st.metric("Power Law", "Above Trend")
        else:
            st.metric("Power Law", "🔒 Premium")
    
    # Chart
    st.subheader("📈 Price Chart")
    chart_data = df.tail(30 if subscription_level == 'free' else len(df))
    
    if PLOTLY_AVAILABLE:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=chart_data['timestamp'], y=chart_data['price'], name='KAS Price'))
        fig.update_layout(title="Kaspa Price", height=400)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.line_chart(chart_data.set_index('timestamp')['price'])

def main():
    """Main application entry point"""
    # Check authentication
    if st.session_state.get('authentication_status') is True:
        name = st.session_state.get('name')
        username = st.session_state.get('username')
        show_main_app(name, username)
    elif st.session_state.get('authentication_status') is False:
        st.error('❌ Username/password is incorrect')
        show_authentication_page()
    else:
        show_authentication_page()

if __name__ == "__main__":
    main()
