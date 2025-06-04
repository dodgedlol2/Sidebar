import streamlit as st
import streamlit_antd_components as sac
import streamlit_authenticator as stauth
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import requests
import time

# Configure page settings
st.set_page_config(
    page_title="Kaspa Analytics Pro",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Authentication configuration
@st.cache_data
def load_auth_config():
    """Load authentication configuration"""
    config = {
        'credentials': {
            'usernames': {
                'admin': {
                    'email': 'admin@kaspalytics.com',
                    'first_name': 'Admin',
                    'last_name': 'User',
                    'password': 'admin123',
                    'subscription': 'pro'
                },
                'premium_user': {
                    'email': 'premium@example.com',
                    'first_name': 'Premium',
                    'last_name': 'User',
                    'password': 'premium123',
                    'subscription': 'premium'
                },
                'free_user': {
                    'email': 'free@example.com',
                    'first_name': 'Free',
                    'last_name': 'User',
                    'password': 'free123',
                    'subscription': 'free'
                }
            }
        },
        'cookie': {
            'name': 'kaspa_analytics_auth',
            'key': 'kaspa_secret_key_12345',
            'expiry_days': 30
        },
        'preauthorized': ['admin@kaspalytics.com']
    }
    return config

# Initialize authenticator
config = load_auth_config()
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized'],
    auto_hash=True
)

# Custom CSS for Kaspa theme
st.markdown("""
<style>
/* Kaspa-themed styling */
:root {
    --kaspa-blue: #70C7BA;
    --kaspa-dark: #1a1a1a;
    --kaspa-light: #f8f9fa;
    --kaspa-accent: #49A097;
}

.main-header {
    background: linear-gradient(135deg, var(--kaspa-blue) 0%, var(--kaspa-accent) 100%);
    padding: 2rem;
    border-radius: 12px;
    color: white;
    margin-bottom: 2rem;
    text-align: center;
}

.metric-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 1.5rem;
    border-radius: 12px;
    color: white;
    text-align: center;
    margin: 0.5rem 0;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
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
    background: #gray;
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

.data-section {
    background: white;
    padding: 1.5rem;
    border-radius: 12px;
    margin: 1rem 0;
    border: 1px solid #e9ecef;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}
</style>
""", unsafe_allow_html=True)

# Kaspa data fetching functions
@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_kaspa_price_data():
    """Fetch Kaspa price data from API"""
    try:
        # Using CoinGecko API for demo (replace with real Kaspa API)
        url = "https://api.coingecko.com/api/v3/coins/kaspa/market_chart"
        params = {"vs_currency": "usd", "days": "365"}
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            
            # Convert to DataFrame
            prices = data['prices']
            volumes = data['total_volumes']
            
            df = pd.DataFrame(prices, columns=['timestamp', 'price'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df['volume'] = [vol[1] for vol in volumes]
            
            return df
        else:
            # Fallback: Generate synthetic data for demo
            return generate_synthetic_kaspa_data()
            
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return generate_synthetic_kaspa_data()

def generate_synthetic_kaspa_data():
    """Generate synthetic Kaspa data for demo purposes"""
    dates = pd.date_range(start='2022-01-01', end=datetime.now(), freq='D')
    
    # Generate price data with some realistic patterns
    np.random.seed(42)
    base_price = 0.02
    prices = []
    current_price = base_price
    
    for i in range(len(dates)):
        # Add trend and volatility
        trend = 0.001 * np.sin(i / 50) + 0.0005
        volatility = np.random.normal(0, 0.05)
        current_price *= (1 + trend + volatility)
        prices.append(max(current_price, 0.001))  # Ensure positive prices
    
    volumes = np.random.lognormal(15, 1, len(dates))
    
    df = pd.DataFrame({
        'timestamp': dates,
        'price': prices,
        'volume': volumes
    })
    
    return df

@st.cache_data
def calculate_power_law_metrics(df, subscription_level):
    """Calculate power law analysis metrics"""
    if subscription_level == 'free':
        # Free users get basic power law data
        return calculate_basic_power_law(df)
    else:
        # Premium users get advanced analysis
        return calculate_advanced_power_law(df)

def calculate_basic_power_law(df):
    """Basic power law calculation for free users"""
    # Simple power law regression
    df = df.copy()
    df['days_since_start'] = (df['timestamp'] - df['timestamp'].min()).dt.days + 1
    df['log_price'] = np.log(df['price'])
    df['log_days'] = np.log(df['days_since_start'])
    
    # Simple linear regression for log-log plot
    coeffs = np.polyfit(df['log_days'], df['log_price'], 1)
    df['power_law_fit'] = np.exp(coeffs[1]) * (df['days_since_start'] ** coeffs[0])
    
    return df, coeffs

def calculate_advanced_power_law(df):
    """Advanced power law analysis for premium users"""
    df, basic_coeffs = calculate_basic_power_law(df)
    
    # Add advanced metrics
    df['price_deviation'] = (df['price'] - df['power_law_fit']) / df['power_law_fit']
    df['rolling_correlation'] = df['price'].rolling(30).corr(df['power_law_fit'])
    
    # Calculate support and resistance levels
    df['support_level'] = df['power_law_fit'] * 0.5
    df['resistance_level'] = df['power_law_fit'] * 2.0
    
    # Advanced coefficients with confidence intervals
    advanced_metrics = {
        'slope': basic_coeffs[0],
        'intercept': basic_coeffs[1],
        'r_squared': np.corrcoef(df['log_days'], df['log_price'])[0, 1] ** 2,
        'current_deviation': df['price_deviation'].iloc[-1],
        'avg_deviation': df['price_deviation'].mean()
    }
    
    return df, advanced_metrics

def get_user_subscription(username):
    """Get user subscription level"""
    user_config = config['credentials']['usernames'].get(username, {})
    return user_config.get('subscription', 'free')

def show_paywall(feature_name, required_tier):
    """Display paywall for premium features"""
    st.markdown('<div class="paywall-container">', unsafe_allow_html=True)
    st.markdown(f"## 🔒 {feature_name}")
    st.markdown(f"This feature requires a **{required_tier.title()}** subscription.")
    st.markdown("### Upgrade to unlock:")
    
    if required_tier == 'premium':
        benefits = [
            "📊 Advanced Power Law Analysis",
            "📈 Full Historical Data Access",
            "💾 Data Export Capabilities", 
            "🔔 Real-time Alerts",
            "📑 Custom Reports"
        ]
    else:  # pro
        benefits = [
            "🔬 Research-Grade Analysis",
            "🤖 API Access",
            "👨‍💼 Priority Support",
            "🎯 Custom Indicators",
            "📊 White-label Reports"
        ]
    
    for benefit in benefits:
        st.markdown(f"- {benefit}")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button(f"Upgrade to {required_tier.title()}", type="primary"):
            st.success("Redirecting to payment page... (Demo)")
    with col2:
        if st.button("Learn More"):
            st.info("More information about pricing and features.")
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_login_page():
    """Display login page"""
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    st.title("💎 Kaspa Analytics Pro")
    st.markdown("*Professional Kaspa blockchain analysis and research platform*")
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🔐 Login to Access Analytics")
        
        # Login widget
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
        
        demo_tabs = sac.tabs([
            sac.TabsItem(label='Free Tier', icon='person'),
            sac.TabsItem(label='Premium', icon='star'),
            sac.TabsItem(label='Pro', icon='crown'),
        ], index=0, key='demo_accounts')
        
        if demo_tabs == 'Free Tier':
            st.code("Username: free_user\nPassword: free123\nAccess: Basic charts and data")
        elif demo_tabs == 'Premium':
            st.code("Username: premium_user\nPassword: premium123\nAccess: Advanced analytics")
        else:
            st.code("Username: admin\nPassword: admin123\nAccess: Full platform access")
    
    return name, authentication_status, username

def show_main_app(name, username):
    """Display main application"""
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
        if st.button("🚪 Logout", type="secondary"):
            authenticator.logout()
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Sidebar navigation
    with st.sidebar:
        st.title("📊 Analytics Menu")
        
        # Navigation based on subscription level
        if subscription_level == 'free':
            menu_items = [
                sac.MenuItem('overview', icon='house-fill', tag=sac.Tag('Free', color='gray')),
                sac.MenuItem('price_charts', icon='graph-up', description='Basic price data'),
                sac.MenuItem('power_law_basic', icon='bar-chart', description='Simple power law'),
                sac.MenuItem(type='divider'),
                sac.MenuItem('upgrade', icon='star', tag=sac.Tag('Upgrade', color='orange')),
            ]
        elif subscription_level == 'premium':
            menu_items = [
                sac.MenuItem('overview', icon='house-fill', tag=sac.Tag('Premium', color='gold')),
                sac.MenuItem('price_charts', icon='graph-up'),
                sac.MenuItem('advanced_analytics', icon='bar-chart-fill', children=[
                    sac.MenuItem('power_law_advanced', icon='trending-up', description='Advanced power law'),
                    sac.MenuItem('network_metrics', icon='diagram-3', description='Network analysis'),
                    sac.MenuItem('correlation_analysis', icon='arrow-left-right'),
                ]),
                sac.MenuItem('data_export', icon='download', description='Export data'),
                sac.MenuItem('alerts', icon='bell', description='Price alerts'),
                sac.MenuItem(type='divider'),
                sac.MenuItem('upgrade_pro', icon='crown', tag=sac.Tag('Pro', color='purple')),
            ]
        else:  # pro
            menu_items = [
                sac.MenuItem('overview', icon='house-fill', tag=sac.Tag('Pro', color='purple')),
                sac.MenuItem('price_charts', icon='graph-up'),
                sac.MenuItem('advanced_analytics', icon='bar-chart-fill', children=[
                    sac.MenuItem('power_law_advanced', icon='trending-up'),
                    sac.MenuItem('network_metrics', icon='diagram-3'),
                    sac.MenuItem('correlation_analysis', icon='arrow-left-right'),
                    sac.MenuItem('custom_indicators', icon='sliders'),
                ]),
                sac.MenuItem('research', icon='book', children=[
                    sac.MenuItem('power_law_research', icon='graph-up-arrow', description='Your research'),
                    sac.MenuItem('reports', icon='file-earmark-text'),
                    sac.MenuItem('api_access', icon='code-square'),
                ]),
                sac.MenuItem('data_export', icon='download'),
                sac.MenuItem('alerts', icon='bell'),
                sac.MenuItem(type='divider'),
                sac.MenuItem('settings', icon='gear'),
            ]
        
        selected = sac.menu(menu_items, open_all=True, key='main_menu')
        
        # Quick stats sidebar
        st.markdown("---")
        st.markdown("**⚡ Quick Stats**")
        
        # Fetch and display current Kaspa data
        df = fetch_kaspa_price_data()
        if not df.empty:
            current_price = df['price'].iloc[-1]
            price_change = ((current_price - df['price'].iloc[-2]) / df['price'].iloc[-2]) * 100
            
            st.metric(
                "KAS Price", 
                f"${current_price:.4f}", 
                f"{price_change:+.2f}%"
            )
            
            st.metric(
                "24h Volume",
                f"${df['volume'].iloc[-1]:,.0f}",
                "Volume"
            )
    
    # Main content routing
    if not selected:
        selected = 'overview'
    
    if selected == 'overview':
        render_overview(subscription_level)
    elif selected == 'price_charts':
        render_price_charts(subscription_level)
    elif selected == 'power_law_basic':
        render_power_law_basic(subscription_level)
    elif selected == 'power_law_advanced':
        render_power_law_advanced(subscription_level)
    elif selected == 'network_metrics':
        render_network_metrics(subscription_level)
    elif selected == 'power_law_research':
        render_power_law_research(subscription_level)
    elif selected == 'data_export':
        render_data_export(subscription_level)
    elif selected == 'upgrade':
        render_upgrade_page('premium')
    elif selected == 'upgrade_pro':
        render_upgrade_page('pro')
    else:
        render_overview(subscription_level)

def render_overview(subscription_level):
    """Render overview dashboard"""
    st.title("📊 Kaspa Market Overview")
    
    # Fetch data
    df = fetch_kaspa_price_data()
    
    if df.empty:
        st.error("Unable to load market data. Please try again later.")
        return
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    current_price = df['price'].iloc[-1]
    price_change_24h = ((current_price - df['price'].iloc[-2]) / df['price'].iloc[-2]) * 100
    price_change_7d = ((current_price - df['price'].iloc[-7]) / df['price'].iloc[-7]) * 100
    
    with col1:
        st.metric("Current Price", f"${current_price:.4f}", f"{price_change_24h:+.2f}%")
    
    with col2:
        st.metric("7D Change", f"{price_change_7d:+.2f}%")
    
    with col3:
        st.metric("Market Cap", "$2.1B", "Est.")
    
    with col4:
        if subscription_level != 'free':
            st.metric("Power Law Position", "Above Trend", "+15%")
        else:
            st.metric("Power Law", "🔒 Premium", "Upgrade")
    
    # Price chart
    st.subheader("📈 Price Chart")
    
    # Limit data for free users
    if subscription_level == 'free':
        chart_df = df.tail(30)  # Last 30 days only
        st.info("📅 Free users see last 30 days. Upgrade for full historical data.")
    else:
        chart_df = df
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=chart_df['timestamp'],
        y=chart_df['price'],
        mode='lines',
        name='KAS Price',
        line=dict(color='#70C7BA', width=2)
    ))
    
    fig.update_layout(
        title="Kaspa Price History",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        height=400,
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Power law preview
    if subscription_level == 'free':
        st.subheader("🔒 Power Law Analysis Preview")
        show_paywall("Advanced Power Law Analysis", "premium")
    else:
        st.subheader("📊 Power Law Analysis")
        render_power_law_preview(df, subscription_level)

def render_power_law_preview(df, subscription_level):
    """Render power law analysis preview"""
    power_law_df, metrics = calculate_power_law_metrics(df, subscription_level)
    
    fig = go.Figure()
    
    # Actual price
    fig.add_trace(go.Scatter(
        x=power_law_df['timestamp'],
        y=power_law_df['price'],
        mode='lines',
        name='Actual Price',
        line=dict(color='#70C7BA', width=2)
    ))
    
    # Power law trend
    fig.add_trace(go.Scatter(
        x=power_law_df['timestamp'],
        y=power_law_df['power_law_fit'],
        mode='lines',
        name='Power Law Trend',
        line=dict(color='red', width=2, dash='dash')
    ))
    
    if subscription_level in ['premium', 'pro']:
        # Support and resistance levels
        fig.add_trace(go.Scatter(
            x=power_law_df['timestamp'],
            y=power_law_df['support_level'],
            mode='lines',
            name='Support',
            line=dict(color='green', width=1, dash='dot'),
            opacity=0.7
        ))
        
        fig.add_trace(go.Scatter(
            x=power_law_df['timestamp'],
            y=power_law_df['resistance_level'],
            mode='lines',
            name='Resistance',
            line=dict(color='red', width=1, dash='dot'),
            opacity=0.7
        ))
    
    fig.update_layout(
        title="Kaspa Power Law Analysis",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        yaxis_type="log",
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Metrics display
    if subscription_level in ['premium', 'pro']:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Power Law Slope", f"{metrics['slope']:.3f}")
        with col2:
            st.metric("R-Squared", f"{metrics['r_squared']:.3f}")
        with col3:
            st.metric("Current Deviation", f"{metrics['current_deviation']:+.1%}")

def render_price_charts(subscription_level):
    """Render price charts page"""
    st.title("📈 Price Charts")
    
    df = fetch_kaspa_price_data()
    
    if subscription_level == 'free':
        df = df.tail(30)
        st.warning("📅 Free tier: Limited to 30 days of data")
    
    # Chart controls
    col1, col2, col3 = st.columns(3)
    
    with col1:
        chart_type = st.selectbox("Chart Type", ["Line", "Candlestick", "Area"])
    
    with col2:
        if subscription_level != 'free':
            timeframe = st.selectbox("Timeframe", ["1D", "7D", "30D", "90D", "1Y", "All"])
        else:
            timeframe = st.selectbox("Timeframe", ["1D", "7D", "30D"])
    
    with col3:
        show_volume = st.checkbox("Show Volume", value=True)
    
    # Create chart based on selection
    if chart_type == "Line":
        fig = px.line(df, x='timestamp', y='price', title="Kaspa Price")
    elif chart_type == "Area":
        fig = px.area(df, x='timestamp', y='price', title="Kaspa Price")
    else:
        if subscription_level == 'free':
            st.info("🔒 Candlestick charts available in Premium")
            fig = px.line(df, x='timestamp', y='price', title="Kaspa Price")
        else:
            # Would implement proper OHLC data here
            fig = px.line(df, x='timestamp', y='price', title="Kaspa Price (Candlestick mode)")
    
    st.plotly_chart(fig, use_container_width=True)
    
    if show_volume and subscription_level != 'free':
        vol_fig = px.bar(df, x='timestamp', y='volume', title="Trading Volume")
        st.plotly_chart(vol_fig, use_container_width=True)

def render_power_law_basic(subscription_level):
    """Render basic power law analysis"""
    st.title("📊 Power Law Analysis")
    
    if subscription_level == 'free':
        df = fetch_kaspa_price_data()
        power_law_df, coeffs = calculate_basic_power_law(df.tail(90))  # Limited data
        
        st.info("📅 Free tier: Basic power law with 90 days of data")
        
        # Simple chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=power_law_df['timestamp'],
            y=power_law_df['price'],
            name='Price',
            line=dict(color='#70C7BA')
        ))
        fig.add_trace(go.Scatter(
            x=power_law_df['timestamp'],
            y=power_law_df['power_law_fit'],
            name='Power Law Fit',
            line=dict(color='red', dash='dash')
        ))
        
        fig.update_layout(title="Basic Power Law Analysis", yaxis_type="log")
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("### 🔒 Advanced Features")
        show_paywall("Advanced Power Law Analysis", "premium")
    else:
        st.info("You have premium access! Visit 'Advanced Analytics > Power Law Advanced' for full features.")

def render_power_law_advanced(subscription_level):
    """Render advanced power law analysis"""
    if subscription_level == 'free':
        show_paywall("Advanced Power Law Analysis", "premium")
        return
    
    st.title("🔬 Advanced Power Law Analysis")
    
    df = fetch_kaspa_price_data()
    power_law_df, metrics = calculate_advanced_power_law(df)
    
    # Advanced visualization
    fig = go.Figure()
    
    # Price and trend
    fig.add_trace(go.Scatter(
        x=power_law_df['timestamp'],
        y=power_law_df['price'],
        name='Actual Price',
        line=dict(color='#70C7BA', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=power_law_df['timestamp'],
        y=power_law_df['power_law_fit'],
        name='Power Law Trend',
        line=dict(color='red', width=2, dash='dash')
    ))
    
    # Support/Resistance bands
    fig.add_trace(go.Scatter(
        x=power_law_df['timestamp'],
        y=power_law_df['support_level'],
        fill=None,
        mode='lines',
        name='Support',
        line=dict(color='green', width=1),
        opacity=0.3
    ))
    
    fig.add_trace(go.Scatter(
        x=power_law_df['timestamp'],
        y=power_law_df['resistance_level'],
        fill='tonexty',
        mode='lines',
        name='Resistance',
        line=dict(color='red', width=1),
        opacity=0.3
    ))
    
    fig.update_layout(
        title="Advanced Power Law Analysis with Support/Resistance",
        yaxis_type="log",
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Advanced metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Power Law Slope", f"{metrics['slope']:.4f}")
    with col2:
        st.metric("R-Squared", f"{metrics['r_squared']:.4f}")
    with col3:
