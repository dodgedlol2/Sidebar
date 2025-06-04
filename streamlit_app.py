import streamlit as st
import streamlit_antd_components as sac
import streamlit_authenticator as stauth
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import requests

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
.main-header {
    background: linear-gradient(135deg, #70C7BA 0%, #49A097 100%);
    padding: 2rem;
    border-radius: 12px;
    color: white;
    margin-bottom: 2rem;
    text-align: center;
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
</style>
""", unsafe_allow_html=True)

# Data fetching functions
@st.cache_data(ttl=300)
def fetch_kaspa_price_data():
    """Fetch Kaspa price data"""
    try:
        # Generate synthetic data for demo
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

def calculate_power_law_metrics(df, subscription_level):
    """Calculate power law analysis metrics"""
    if df.empty:
        return pd.DataFrame(), {}
    
    df = df.copy()
    df['days_since_start'] = (df['timestamp'] - df['timestamp'].min()).dt.days + 1
    df['log_price'] = np.log(df['price'])
    df['log_days'] = np.log(df['days_since_start'])
    
    # Simple linear regression for log-log plot
    coeffs = np.polyfit(df['log_days'], df['log_price'], 1)
    df['power_law_fit'] = np.exp(coeffs[1]) * (df['days_since_start'] ** coeffs[0])
    
    if subscription_level in ['premium', 'pro']:
        # Add advanced metrics
        df['price_deviation'] = (df['price'] - df['power_law_fit']) / df['power_law_fit']
        df['support_level'] = df['power_law_fit'] * 0.5
        df['resistance_level'] = df['power_law_fit'] * 2.0
        
        metrics = {
            'slope': coeffs[0],
            'intercept': coeffs[1],
            'r_squared': np.corrcoef(df['log_days'], df['log_price'])[0, 1] ** 2,
            'current_deviation': df['price_deviation'].iloc[-1],
            'avg_deviation': df['price_deviation'].mean()
        }
    else:
        metrics = {'slope': coeffs[0], 'intercept': coeffs[1]}
    
    return df, metrics

def get_user_subscription(username):
    """Get user subscription level"""
    user_config = config['credentials']['usernames'].get(username, {})
    return user_config.get('subscription', 'free')

def show_paywall(feature_name, required_tier):
    """Display paywall for premium features"""
    st.markdown('<div class="paywall-container">', unsafe_allow_html=True)
    st.markdown(f"## 🔒 {feature_name}")
    st.markdown(f"This feature requires a **{required_tier.title()}** subscription.")
    
    if required_tier == 'premium':
        benefits = [
            "📊 Advanced Power Law Analysis",
            "📈 Full Historical Data Access",
            "💾 Data Export Capabilities", 
            "🔔 Real-time Alerts"
        ]
        price = "$29/month"
    else:  # pro
        benefits = [
            "🔬 Research-Grade Analysis",
            "🤖 API Access",
            "👨‍💼 Priority Support",
            "🎯 Custom Indicators"
        ]
        price = "$99/month"
    
    for benefit in benefits:
        st.markdown(f"- {benefit}")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button(f"Upgrade to {required_tier.title()} - {price}", type="primary"):
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
            st.code("Username: free_user\nPassword: free123\nAccess: Basic charts")
        elif demo_tabs == 'Premium':
            st.code("Username: premium_user\nPassword: premium123\nAccess: Advanced analytics")
        else:
            st.code("Username: admin\nPassword: admin123\nAccess: Full platform")
    
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
        
        # Create menu based on subscription level
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
                sac.MenuItem('analytics', icon='bar-chart-fill', children=[
                    sac.MenuItem('power_law_advanced', icon='trending-up'),
                    sac.MenuItem('network_metrics', icon='diagram-3'),
                ]),
                sac.MenuItem('data_export', icon='download'),
                sac.MenuItem(type='divider'),
                sac.MenuItem('upgrade_pro', icon='crown', tag=sac.Tag('Pro', color='purple')),
            ]
        else:  # pro
            menu_items = [
                sac.MenuItem('overview', icon='house-fill', tag=sac.Tag('Pro', color='purple')),
                sac.MenuItem('price_charts', icon='graph-up'),
                sac.MenuItem('analytics', icon='bar-chart-fill', children=[
                    sac.MenuItem('power_law_advanced', icon='trending-up'),
                    sac.MenuItem('network_metrics', icon='diagram-3'),
                    sac.MenuItem('custom_indicators', icon='sliders'),
                ]),
                sac.MenuItem('research', icon='book', children=[
                    sac.MenuItem('power_law_research', icon='graph-up-arrow'),
                    sac.MenuItem('reports', icon='file-earmark-text'),
                ]),
                sac.MenuItem('data_export', icon='download'),
                sac.MenuItem(type='divider'),
                sac.MenuItem('settings', icon='gear'),
            ]
        
        selected = sac.menu(menu_items, open_all=True, key='main_menu')
        
        # Quick stats sidebar
        st.markdown("---")
        st.markdown("**⚡ Quick Stats**")
        
        df = fetch_kaspa_price_data()
        if not df.empty:
            current_price = df['price'].iloc[-1]
            price_change = ((current_price - df['price'].iloc[-2]) / df['price'].iloc[-2]) * 100
            
            st.metric("KAS Price", f"${current_price:.4f}", f"{price_change:+.2f}%")
            st.metric("24h Volume", f"${df['volume'].iloc[-1]:,.0f}")
    
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
    elif selected == 'custom_indicators':
        render_custom_indicators(subscription_level)
    elif selected == 'power_law_research':
        render_power_law_research(subscription_level)
    elif selected == 'reports':
        render_reports(subscription_level)
    elif selected == 'data_export':
        render_data_export(subscription_level)
    elif selected == 'upgrade':
        render_upgrade_page('premium')
    elif selected == 'upgrade_pro':
        render_upgrade_page('pro')
    elif selected == 'settings':
        render_settings()
    else:
        render_overview(subscription_level)

def render_overview(subscription_level):
    """Render overview dashboard"""
    st.title("📊 Kaspa Market Overview")
    
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
    
    if subscription_level == 'free':
        chart_df = df.tail(30)
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
        height=400
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
    
    fig.add_trace(go.Scatter(
        x=power_law_df['timestamp'],
        y=power_law_df['price'],
        mode='lines',
        name='Actual Price',
        line=dict(color='#70C7BA', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=power_law_df['timestamp'],
        y=power_law_df['power_law_fit'],
        mode='lines',
        name='Power Law Trend',
        line=dict(color='red', width=2, dash='dash')
    ))
    
    if subscription_level in ['premium', 'pro']:
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
    
    chart_type = st.selectbox("Chart Type", ["Line", "Area"])
    
    if chart_type == "Line":
        fig = px.line(df, x='timestamp', y='price', title="Kaspa Price")
    else:
        fig = px.area(df, x='timestamp', y='price', title="Kaspa Price")
    
    st.plotly_chart(fig, use_container_width=True)

def render_power_law_basic(subscription_level):
    """Render basic power law analysis"""
    st.title("📊 Basic Power Law Analysis")
    
    if subscription_level == 'free':
        df = fetch_kaspa_price_data()
        power_law_df, coeffs = calculate_power_law_metrics(df.tail(90), subscription_level)
        
        st.info("📅 Free tier: Basic power law with 90 days of data")
        
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
        st.info("You have premium access! Visit 'Analytics > Power Law Advanced' for full features.")

def render_power_law_advanced(subscription_level):
    """Render advanced power law analysis"""
    if subscription_level == 'free':
        show_paywall("Advanced Power Law Analysis", "premium")
        return
    
    st.title("🔬 Advanced Power Law Analysis")
    
    df = fetch_kaspa_price_data()
    power_law_df, metrics = calculate_power_law_metrics(df, subscription_level)
    
    fig = go.Figure()
    
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
    
    fig.add_trace(go.Scatter(
        x=power_law_df['timestamp'],
        y=power_law_df['support_level'],
        mode='lines',
        name='Support',
        line=dict(color='green', width=1),
        opacity=0.3
    ))
    
    fig.add_trace(go.Scatter(
        x=power_law_df['timestamp'],
        y=power_law_df['resistance_level'],
        mode='lines',
        name='Resistance',
        line=dict(color='red', width=1),
        opacity=0.3
    ))
    
    fig.update_layout(
        title="Advanced Power Law Analysis",
        yaxis_type="log",
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Power Law Slope", f"{metrics['slope']:.4f}")
    with col2:
        st.metric("R-Squared", f"{metrics['r_squared']:.4f}")
    with col3:
        st.metric("Current Deviation", f"{metrics['current_deviation']:+.1%}")
    with col4:
        st.metric("Average Deviation", f"{metrics['avg_deviation']:+.1%}")

def render_network_metrics(subscription_level):
    """Render network metrics analysis"""
    if subscription_level == 'free':
        show_paywall("Network Metrics Analysis", "premium")
        return
    
    st.title("🌐 Kaspa Network Metrics")
    st.info("Network metrics would show hash rate, difficulty, block time, and transaction data.")

def render_custom_indicators(subscription_level):
    """Render custom indicators page"""
    if subscription_level != 'pro':
        show_paywall("Custom Indicators", "pro")
        return
    
    st.title("🎯 Custom Indicators")
    st.info("Build and test your own custom technical indicators for Kaspa.")

def render_power_law_research(subscription_level):
    """Render power law research page"""
    if subscription_level != 'pro':
        show_paywall("Power Law Research", "pro")
        return
    
    st.title("🔬 Power Law Research Hub")
    st.markdown("*Your personal research workspace for Kaspa power law analysis*")
    
    research_tabs = sac.tabs([
        sac.TabsItem(label='Research Notes', icon='journal-text'),
        sac.TabsItem(label='Custom Models', icon='gear'),
        sac.TabsItem(label='Publications', icon='book'),
    ], key='research_tabs')
    
    if research_tabs == 'Research Notes':
        st.subheader("📝 Research Notes & Observations")
        
        if 'research_notes' not in st.session_state:
            st.session_state.research_notes = """
# Kaspa Power Law Research Notes

## Key Findings
- Power law regression shows strong correlation
- Deviation cycles correlate with market sentiment
- Support levels hold during corrections

## Research Questions
1. How does Kaspa compare to Bitcoin's power law?
2. What influences deviation from trend?
3. Can we predict cycle tops/bottoms?
            """
        
        notes = st.text_area("Research Notes", value=st.session_state.research_notes, height=400)
        
        if st.button("💾 Save Notes"):
            st.session_state.research_notes = notes
            st.success("Research notes saved!")
        
        st.markdown("### Preview:")
        st.markdown(notes)
    
    elif research_tabs == 'Custom Models':
        st.subheader("🔧 Custom Power Law Models")
        st.info("Build custom power law models with adjustable parameters.")
    
    else:  # Publications
        st.subheader("📚 Research Publications")
        st.info("Manage and publish your Kaspa research papers.")

def render_reports(subscription_level):
    """Render reports page"""
    if subscription_level != 'pro':
        show_paywall("Research Reports", "pro")
        return
    
    st.title("📑 Research Reports")
    st.info("Generate comprehensive research reports based on your analysis.")

def render_data_export(subscription_level):
    """Render data export page"""
    if subscription_level == 'free':
        show_paywall("Data Export", "premium")
        return
    
    st.title("💾 Data Export")
    
    export_tabs = sac.tabs([
        sac.TabsItem(label='Price Data', icon='graph-up'),
        sac.TabsItem(label='Power Law Analysis', icon='trending-up'),
        sac.TabsItem(label='Network Metrics', icon='diagram-3'),
    ], key='export_tabs')
    
    if export_tabs == 'Price Data':
        st.subheader("📈 Export Price Data")
        
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", value=datetime.now() - timedelta(days=365))
        with col2:
            end_date = st.date_input("End Date", value=datetime.now())
        
        file_format = st.selectbox("Format", ["CSV", "JSON", "Excel"])
        
        if st.button("📊 Generate Export"):
            df = fetch_kaspa_price_data()
            df_filtered = df[
                (df['timestamp'] >= pd.Timestamp(start_date)) & 
                (df['timestamp'] <= pd.Timestamp(end_date))
            ]
            
            st.success(f"Generated {len(df_filtered)} records for export")
            
            if file_format == "CSV":
                csv = df_filtered.to_csv(index=False)
                st.download_button(
                    "⬇️ Download CSV",
                    csv,
                    f"kaspa_price_data_{start_date}_{end_date}.csv",
                    "text/csv"
                )
    
    elif export_tabs == 'Power Law Analysis':
        st.subheader("📊 Export Power Law Analysis")
        st.info("Export power law analysis data and metrics.")
    
    else:  # Network Metrics
        st.subheader("🌐 Export Network Metrics")
        st.info("Export network hash rate, difficulty, and transaction data.")

def render_upgrade_page(target_tier):
    """Render upgrade page"""
    st.title(f"⭐ Upgrade to {target_tier.title()}")
    
    if target_tier == 'premium':
        features = [
            "📊 Advanced Power Law Analysis",
            "📈 Full Historical Data Access",
            "💾 Data Export Capabilities",
            "🔔 Real-time Price Alerts"
        ]
        price = "$29/month"
    else:  # pro
        features = [
            "🔬 All Premium Features",
            "🛠️ Custom Power Law Models",
            "📚 Research Workspace",
            "🤖 API Access"
        ]
        price = "$99/month"
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### What you'll get:")
        for feature in features:
            st.markdown(f"✅ {feature}")
    
    with col2:
        st.markdown(f"### {price}")
        st.markdown("*Billed monthly*")
        
        if st.button(f"🚀 Upgrade to {target_tier.title()}", type="primary"):
            st.success("Redirecting to payment... (Demo)")
            st.balloons()

def render_settings():
    """Render settings page"""
    st.title("⚙️ Settings")
    st.info("Account settings and preferences would be configured here.")

# Main application logic
def main():
    """Main application entry point"""
    
    # Check authentication status
    authentication_status = st.session_state.get('authentication_status')
    name = st.session_state.get('name')
    username = st.session_state.get('username')
    
    if authentication_status is not True:
        name, authentication_status, username = show_login_page()
        
        if authentication_status is True:
            st.rerun()
    else:
        show_main_app(name, username)

# Run the application
if __name__ == "__main__":
    main()
