import streamlit as st
import streamlit_antd_components as sac
import pandas as pd
import numpy as np

# Try to import hover tabs with error handling
try:
    from st_on_hover_tabs import on_hover_tabs
    HOVER_TABS_AVAILABLE = True
except ImportError:
    HOVER_TABS_AVAILABLE = False
    st.error("❌ streamlit-on-Hover-tabs not available. Install with: pip install streamlit-on-Hover-tabs")

# Configure page settings
st.set_page_config(
    page_title="Hybrid Navigation App",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling and hover tabs
st.markdown("""
<style>
/* Import Google Fonts for icons */
@import url('https://fonts.googleapis.com/icon?family=Material+Icons');

/* Hover tabs styling fallback */
.stTabs [data-baseweb="tab-list"] {
    gap: 2px;
}

.stTabs [data-baseweb="tab"] {
    height: 50px;
    padding-left: 20px;
    padding-right: 20px;
    background-color: #f0f2f6;
    border-radius: 4px 4px 0px 0px;
    gap: 1px;
    padding-top: 10px;
    padding-bottom: 10px;
}

.stTabs [aria-selected="true"] {
    background-color: #4CAF50;
    color: white;
}

/* Custom styles */
.nav-separator {
    margin: 1rem 0;
    padding: 0.5rem 0;
    border-top: 1px solid #333;
    border-bottom: 1px solid #333;
}

.section-header {
    font-size: 0.8rem;
    color: #888;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin: 1rem 0 0.5rem 0;
}

.metric-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 1rem;
    border-radius: 10px;
    color: white;
    text-align: center;
    margin: 0.5rem 0;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'main_section' not in st.session_state:
    st.session_state.main_section = 'Dashboard'
if 'sub_navigation' not in st.session_state:
    st.session_state.sub_navigation = 'home'

# Main header
st.title("🎯 Hybrid Navigation Demo")
if HOVER_TABS_AVAILABLE:
    st.markdown("*✅ Combining Hover Tabs + Antd Components for Ultimate Navigation*")
else:
    st.markdown("*⚠️ Using Streamlit Tabs + Antd Components (Hover tabs unavailable)*")

# Sidebar with navigation
with st.sidebar:
    st.title("🚀 Navigation Hub")
    
    # PRIMARY NAVIGATION
    st.markdown('<div class="section-header">Main Sections</div>', unsafe_allow_html=True)
    
    if HOVER_TABS_AVAILABLE:
        # Use hover tabs if available
        try:
            main_tabs = on_hover_tabs(
                tabName=['Dashboard', 'Analytics', 'Products', 'Reports', 'Settings'],
                iconName=['dashboard', 'bar_chart', 'inventory_2', 'description', 'settings'],
                default_choice=0,
                key="main_navigation"
            )
            
            if main_tabs:
                st.session_state.main_section = main_tabs
        except Exception as e:
            st.error(f"Hover tabs error: {e}")
            HOVER_TABS_AVAILABLE = False
    
    if not HOVER_TABS_AVAILABLE:
        # Fallback to regular selectbox
        main_sections = ['Dashboard', 'Analytics', 'Products', 'Reports', 'Settings']
        selected_section = st.selectbox(
            "Choose Section:",
            main_sections,
            index=main_sections.index(st.session_state.main_section) if st.session_state.main_section in main_sections else 0,
            key="main_section_select"
        )
        st.session_state.main_section = selected_section
    
    # SEPARATOR
    st.markdown('<div class="nav-separator"></div>', unsafe_allow_html=True)
    
    # SECONDARY NAVIGATION - Using Antd Components (context-dependent)
    st.markdown('<div class="section-header">Quick Actions</div>', unsafe_allow_html=True)
    
    if st.session_state.main_section == 'Dashboard':
        # Dashboard-specific antd navigation
        dashboard_menu = sac.menu([
            sac.MenuItem('home', icon='house-fill', tag=sac.Tag('Main', color='blue')),
            sac.MenuItem('metrics', icon='speedometer2', tag=sac.Tag('Live', color='green')),
            sac.MenuItem('alerts', icon='bell-fill', tag=sac.Tag('3', color='red')),
            sac.MenuItem(type='divider'),
            sac.MenuItem('recent', type='group', children=[
                sac.MenuItem('activity', icon='activity'),
                sac.MenuItem('notifications', icon='envelope'),
            ]),
        ], open_all=True, key='dashboard_menu')
        
        if dashboard_menu:
            st.session_state.sub_navigation = dashboard_menu
    
    elif st.session_state.main_section == 'Analytics':
        # Analytics-specific antd navigation
        analytics_menu = sac.menu([
            sac.MenuItem('overview', icon='graph-up', tag=sac.Tag('New', color='purple')),
            sac.MenuItem('reports', icon='file-earmark-text'),
            sac.MenuItem('data', icon='database', children=[
                sac.MenuItem('users', icon='people'),
                sac.MenuItem('sales', icon='currency-dollar'),
                sac.MenuItem('traffic', icon='bar-chart'),
            ]),
            sac.MenuItem(type='divider'),
            sac.MenuItem('tools', type='group', children=[
                sac.MenuItem('export', icon='download'),
                sac.MenuItem('filters', icon='funnel'),
            ]),
        ], open_all=True, key='analytics_menu')
        
        if analytics_menu:
            st.session_state.sub_navigation = analytics_menu
    
    elif st.session_state.main_section == 'Products':
        # Products-specific antd navigation
        products_menu = sac.menu([
            sac.MenuItem('catalog', icon='grid', tag=sac.Tag('1.2k', color='orange')),
            sac.MenuItem('categories', icon='tags', children=[
                sac.MenuItem('electronics', icon='laptop'),
                sac.MenuItem('clothing', icon='bag'),
                sac.MenuItem('books', icon='book'),
                sac.MenuItem('home', icon='house'),
            ]),
            sac.MenuItem('inventory', icon='boxes'),
            sac.MenuItem(type='divider'),
            sac.MenuItem('management', type='group', children=[
                sac.MenuItem('add_product', icon='plus-circle'),
                sac.MenuItem('bulk_edit', icon='pencil-square'),
            ]),
        ], open_all=True, key='products_menu')
        
        if products_menu:
            st.session_state.sub_navigation = products_menu
    
    elif st.session_state.main_section == 'Reports':
        # Reports-specific antd navigation
        reports_menu = sac.menu([
            sac.MenuItem('generate', icon='file-plus', tag=sac.Tag('Quick', color='cyan')),
            sac.MenuItem('templates', icon='files', children=[
                sac.MenuItem('sales_report', icon='graph-up-arrow'),
                sac.MenuItem('user_activity', icon='person-lines-fill'),
                sac.MenuItem('financial', icon='calculator'),
            ]),
            sac.MenuItem('scheduled', icon='clock'),
            sac.MenuItem(type='divider'),
            sac.MenuItem('archive', type='group', children=[
                sac.MenuItem('recent', icon='clock-history'),
                sac.MenuItem('favorites', icon='star'),
            ]),
        ], open_all=True, key='reports_menu')
        
        if reports_menu:
            st.session_state.sub_navigation = reports_menu
    
    else:  # Settings
        # Settings-specific antd navigation
        settings_menu = sac.menu([
            sac.MenuItem('profile', icon='person-circle'),
            sac.MenuItem('preferences', icon='sliders', children=[
                sac.MenuItem('appearance', icon='palette'),
                sac.MenuItem('notifications', icon='bell'),
                sac.MenuItem('privacy', icon='shield-check'),
            ]),
            sac.MenuItem('account', icon='key'),
            sac.MenuItem(type='divider'),
            sac.MenuItem('system', type='group', children=[
                sac.MenuItem('backup', icon='cloud-arrow-up'),
                sac.MenuItem('logs', icon='journal-text'),
            ]),
        ], open_all=True, key='settings_menu')
        
        if settings_menu:
            st.session_state.sub_navigation = settings_menu
    
    # ADDITIONAL ANTD COMPONENTS
    st.markdown('<div class="nav-separator"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Quick Tools</div>', unsafe_allow_html=True)
    
    # Antd Buttons for quick actions
    quick_action = sac.buttons([
        sac.ButtonsItem(label='Export', icon='download'),
        sac.ButtonsItem(label='Refresh', icon='arrow-clockwise'),
        sac.ButtonsItem(label='Help', icon='question-circle'),
    ], index=None, format_func='title', align='center', key='quick_buttons')
    
    # Antd Switch for preferences
    st.markdown("**Preferences:**")
    dark_mode = sac.switch(label='Dark Mode', value=True, key='dark_mode')
    auto_refresh = sac.switch(label='Auto Refresh', value=False, key='auto_refresh')

# MAIN CONTENT AREA
def render_dashboard_content():
    current_sub = st.session_state.sub_navigation
    
    if current_sub == 'home':
        st.title("🏠 Dashboard Home")
        
        # Use Antd Rate component
        st.subheader("Rate Your Experience")
        rating = sac.rate(label='How satisfied are you?', value=3, key='satisfaction_rating')
        if rating:
            st.write(f"You rated: {rating}/5 stars")
        
        # Metrics with Antd Tags
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Users", "1,234", "12%")
            st.write(sac.Tag("Active", color='green'))
        with col2:
            st.metric("Revenue", "$45,678", "8%")
            st.write(sac.Tag("Growing", color='blue'))
        with col3:
            st.metric("Orders", "567", "-2%")
            st.write(sac.Tag("Monitor", color='orange'))
        with col4:
            st.metric("Conversion", "3.2%", "0.8%")
            st.write(sac.Tag("Optimizing", color='purple'))
    
    elif current_sub == 'metrics':
        st.title("📊 Live Metrics")
        
        # Antd Steps component for process tracking
        st.subheader("Data Processing Pipeline")
        sac.steps(
            items=[
                sac.StepsItem(title='Data Collection', description='Gathering user data'),
                sac.StepsItem(title='Processing', description='Analyzing patterns'),
                sac.StepsItem(title='Visualization', description='Creating charts'),
                sac.StepsItem(title='Reporting', description='Generating insights'),
            ],
            index=2,
            key='pipeline_steps'
        )
        
        # Sample metrics chart
        chart_data = pd.DataFrame(
            np.random.randn(20, 3),
            columns=['Sales', 'Users', 'Revenue']
        )
        st.line_chart(chart_data)
    
    elif current_sub == 'alerts':
        st.title("🔔 Alerts & Notifications")
        
        # Antd Alert components
        sac.alert(label='System Update Available', description='A new version is ready to install.', 
                  banner=True, icon=True, type='info', key='update_alert')
        
        sac.alert(label='High Traffic Detected', description='Your site is experiencing 300% more traffic than usual.', 
                  banner=True, icon=True, type='warning', key='traffic_alert')
        
        sac.alert(label='Backup Completed', description='Daily backup completed successfully at 3:00 AM.', 
                  banner=True, icon=True, type='success', key='backup_alert')
    
    elif current_sub == 'activity':
        st.title("📈 Recent Activity")
        
        # Activity timeline with Antd components
        activities = [
            "User john_doe logged in",
            "Report 'Q1 Sales' generated",
            "New product 'Widget Pro' added",
            "System backup completed",
            "5 new user registrations"
        ]
        
        for i, activity in enumerate(activities):
            st.write(f"{i+1}. {activity}")
            st.write(sac.Tag(f"Activity {i+1}", color='blue'))
            st.write("")
    
    else:
        st.title("📧 Notifications")
        st.write("Notification management interface would go here.")

def render_analytics_content():
    current_sub = st.session_state.sub_navigation
    
    if current_sub == 'overview':
        st.title("📊 Analytics Overview")
        
        # Antd Segmented control for time periods
        time_period = sac.segmented(
            items=['Last 7 days', 'Last 30 days', 'Last 90 days'],
            index=1,
            key='time_period'
        )
        
        st.write(f"Showing data for: {time_period}")
        
        # Sample analytics chart
        analytics_data = pd.DataFrame({
            'Date': pd.date_range('2024-01-01', periods=30, freq='D'),
            'Page Views': np.random.randint(1000, 5000, 30),
            'Unique Visitors': np.random.randint(500, 2000, 30)
        })
        
        st.line_chart(analytics_data.set_index('Date'))
    
    elif current_sub == 'users':
        st.title("👥 User Analytics")
        
        # Antd Pagination for user data
        st.subheader("User List")
        page = sac.pagination(total=200, page_size=10, key='user_pagination')
        st.write(f"Page {page} of user data")
        
        # Sample user data
        user_data = pd.DataFrame({
            'User ID': range((page-1)*10 + 1, page*10 + 1),
            'Name': [f'User {i}' for i in range((page-1)*10 + 1, page*10 + 1)],
            'Email': [f'user{i}@example.com' for i in range((page-1)*10 + 1, page*10 + 1)],
            'Status': np.random.choice(['Active', 'Inactive'], 10)
        })
        
        st.dataframe(user_data, use_container_width=True)
    
    else:
        st.title(f"📊 {current_sub.title()} Analytics")
        st.write(f"Analytics content for {current_sub} would be displayed here.")

def render_products_content():
    current_sub = st.session_state.sub_navigation
    
    if current_sub == 'catalog':
        st.title("📦 Product Catalog")
        
        # Antd Transfer component for product selection
        st.subheader("Manage Product Visibility")
        transfer_result = sac.transfer(
            items=[f'Product {i}' for i in range(1, 21)],
            index=[0, 2, 4, 6],
            key='product_transfer'
        )
        
        st.write(f"Selected products: {len(transfer_result) if transfer_result else 0}")
    
    elif current_sub in ['electronics', 'clothing', 'books', 'home']:
        st.title(f"🏷️ {current_sub.title()} Category")
        
        # Antd Checkbox group for filtering
        filter_options = sac.checkbox(
            items=['In Stock', 'On Sale', 'Featured', 'New Arrivals'],
            index=[0],
            key=f'{current_sub}_filters'
        )
        
        st.write(f"Applied filters: {filter_options}")
        
        # Sample product grid
        cols = st.columns(3)
        for i in range(6):
            with cols[i % 3]:
                st.image("https://via.placeholder.com/150", width=150)
                st.write(f"{current_sub.title()} Product {i+1}")
                st.write(sac.Tag(f"${np.random.randint(10, 100)}", color='green'))
    
    else:
        st.title(f"📦 {current_sub.title()}")
        st.write(f"Product {current_sub} content would be displayed here.")

def render_reports_content():
    current_sub = st.session_state.sub_navigation
    
    if current_sub == 'generate':
        st.title("📊 Generate Report")
        
        # Antd Cascader for report selection
        cascader_options = [
            {'label': 'Sales Reports', 'value': 'sales', 'children': [
                {'label': 'Monthly Sales', 'value': 'monthly'},
                {'label': 'Product Performance', 'value': 'products'},
            ]},
            {'label': 'User Reports', 'value': 'users', 'children': [
                {'label': 'User Activity', 'value': 'activity'},
                {'label': 'Registration Trends', 'value': 'registration'},
            ]},
        ]
        
        selected_report = sac.cascader(
            items=cascader_options,
            index=[0, 0],
            key='report_cascader'
        )
        
        if selected_report:
            st.write(f"Selected report: {' > '.join(selected_report)}")
            
            if st.button("Generate Report", type="primary"):
                st.success("Report generated successfully!")
    
    else:
        st.title(f"📋 {current_sub.title()}")
        st.write(f"Report {current_sub} content would be displayed here.")

def render_settings_content():
    current_sub = st.session_state.sub_navigation
    
    if current_sub == 'profile':
        st.title("👤 Profile Settings")
        
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Full Name", value="John Doe")
            st.text_input("Email", value="john@example.com")
        
        with col2:
            # Antd Rate for skill level
            st.subheader("Experience Level")
            experience = sac.rate(label='Rate your experience with this app', value=4, key='experience_rate')
            
        # Antd Result component for profile status
        sac.result(
            label='Profile Complete',
            description='Your profile is 95% complete. Add a phone number to reach 100%.',
            status='success',
            key='profile_status'
        )
    
    elif current_sub == 'appearance':
        st.title("🎨 Appearance Settings")
        
        # Color theme selection
        theme_color = sac.segmented(
            items=['Blue', 'Green', 'Purple', 'Orange'],
            index=0,
            key='theme_color'
        )
        
        st.write(f"Selected theme: {theme_color}")
    
    else:
        st.title(f"⚙️ {current_sub.title()}")
        st.write(f"Settings for {current_sub} would be displayed here.")

# MAIN CONTENT ROUTING
if st.session_state.main_section == 'Dashboard':
    render_dashboard_content()
elif st.session_state.main_section == 'Analytics':
    render_analytics_content()
elif st.session_state.main_section == 'Products':
    render_products_content()
elif st.session_state.main_section == 'Reports':
    render_reports_content()
elif st.session_state.main_section == 'Settings':
    render_settings_content()

# FOOTER with status
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"**Main:** {st.session_state.main_section}")
with col2:
    st.markdown(f"**Sub:** {st.session_state.sub_navigation}")
with col3:
    st.markdown(f"**Dark Mode:** {'✅' if dark_mode else '❌'}")
with col4:
    st.markdown(f"**Auto Refresh:** {'✅' if auto_refresh else '❌'}")

if quick_action:
    st.info(f"Quick action triggered: {quick_action}")

st.markdown("*🎯 Hybrid Navigation: Best of Both Worlds*")
