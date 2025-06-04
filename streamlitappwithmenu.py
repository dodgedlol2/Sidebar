import streamlit as st
import streamlit_antd_components as sac
import pandas as pd
import numpy as np

# Configure page settings
st.set_page_config(
    page_title="Professional Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'

# Custom CSS for better styling
st.markdown("""
<style>
.main-header {
    padding: 1rem 0 2rem 0;
    border-bottom: 2px solid #f0f2f6;
    margin-bottom: 2rem;
}

.content-section {
    padding: 1.5rem;
    border-radius: 12px;
    background: #f8f9fa;
    margin: 1rem 0;
    border: 1px solid #e9ecef;
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

.sidebar-section {
    background: #f8f9fa;
    padding: 1rem;
    border-radius: 8px;
    margin: 1rem 0;
    border-left: 4px solid #4CAF50;
}

.status-bar {
    background: linear-gradient(90deg, #4CAF50 0%, #45a049 100%);
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 6px;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown('<div class="main-header">', unsafe_allow_html=True)
st.title("🚀 Professional Dashboard")
st.markdown("*Built with Streamlit Antd Components - Clean, Fast, Professional*")
st.markdown('</div>', unsafe_allow_html=True)

# Sidebar with comprehensive Antd menu
with st.sidebar:
    st.title("🎯 Navigation")
    
    # Main navigation menu
    selected = sac.menu([
        sac.MenuItem('home', icon='house-fill', tag=[
            sac.Tag('Main', color='blue'),
            sac.Tag('Live', color='green')
        ]),
        
        sac.MenuItem('analytics', icon='bar-chart-fill', children=[
            sac.MenuItem('overview', icon='speedometer2', description='Key metrics dashboard'),
            sac.MenuItem('reports', icon='file-earmark-text', description='Detailed reports'),
            sac.MenuItem('users', icon='people', description='User analytics'),
            sac.MenuItem('sales', icon='currency-dollar', description='Sales data'),
            sac.MenuItem('traffic', icon='graph-up', description='Website traffic'),
        ]),
        
        sac.MenuItem('products', icon='box-fill', children=[
            sac.MenuItem('catalog', icon='grid', tag=sac.Tag('1.2k', color='orange')),
            sac.MenuItem('categories', icon='tags', children=[
                sac.MenuItem('electronics', icon='laptop', description='Tech products'),
                sac.MenuItem('clothing', icon='bag', description='Fashion items'),
                sac.MenuItem('books', icon='book', description='Literature'),
                sac.MenuItem('home_garden', icon='house', description='Home & Garden'),
            ]),
            sac.MenuItem('inventory', icon='boxes', description='Stock management'),
            sac.MenuItem('suppliers', icon='truck', description='Supplier network'),
        ]),
        
        sac.MenuItem('customers', icon='people-fill', children=[
            sac.MenuItem('customer_list', icon='person-lines-fill'),
            sac.MenuItem('segments', icon='diagram-3'),
            sac.MenuItem('support', icon='headset', tag=sac.Tag('24/7', color='red')),
            sac.MenuItem('feedback', icon='chat-square-text'),
        ]),
        
        sac.MenuItem('reports', icon='file-earmark-bar-graph', children=[
            sac.MenuItem('generate', icon='file-plus', tag=sac.Tag('Quick', color='cyan')),
            sac.MenuItem('templates', icon='files', children=[
                sac.MenuItem('sales_report', icon='graph-up-arrow'),
                sac.MenuItem('user_activity', icon='person-check'),
                sac.MenuItem('financial', icon='calculator'),
                sac.MenuItem('performance', icon='speedometer'),
            ]),
            sac.MenuItem('scheduled', icon='clock', description='Automated reports'),
            sac.MenuItem('exports', icon='download', description='Data exports'),
        ]),
        
        sac.MenuItem(type='divider'),
        
        sac.MenuItem('tools', icon='gear-fill', children=[
            sac.MenuItem('settings', icon='sliders'),
            sac.MenuItem('integrations', icon='puzzle'),
            sac.MenuItem('api', icon='code-square'),
            sac.MenuItem('backup', icon='cloud-arrow-up'),
        ]),
        
        sac.MenuItem('help', type='group', children=[
            sac.MenuItem('documentation', icon='book-fill', href='https://streamlit.io/'),
            sac.MenuItem('support', icon='question-circle-fill'),
            sac.MenuItem('community', icon='chat-dots'),
        ]),
        
    ], open_all=True, key='main_menu')
    
    # Update session state
    if selected:
        st.session_state.current_page = selected
    
    # Sidebar tools section
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("**⚡ Quick Actions**")
    
    # Quick action buttons
    quick_action = sac.buttons([
        sac.ButtonsItem(label='Export Data', icon='download'),
        sac.ButtonsItem(label='Refresh', icon='arrow-clockwise'),
        sac.ButtonsItem(label='Settings', icon='gear'),
    ], index=None, format_func='title', align='center', key='quick_buttons')
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Preferences section
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("**🎛️ Preferences**")
    
    # Theme and settings
    dark_mode = sac.switch(label='Dark Mode', value=False, key='dark_mode_switch')
    auto_refresh = sac.switch(label='Auto Refresh', value=True, key='auto_refresh_switch')
    notifications = sac.switch(label='Notifications', value=True, key='notifications_switch')
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Status section
    st.markdown('<div class="status-bar">', unsafe_allow_html=True)
    st.markdown("**📊 System Status: Online**")
    st.markdown('</div>', unsafe_allow_html=True)

# Content rendering functions
def render_home():
    st.title("🏠 Dashboard Home")
    
    # Welcome section with rating
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("Welcome back! 👋")
        st.write("Here's your business overview for today.")
    
    with col2:
        st.subheader("Rate your experience")
        rating = sac.rate(label='Satisfaction', value=4, key='satisfaction_rating')
        if rating:
            st.write(f"Rating: {rating}/5 ⭐")
    
    # Key metrics
    st.subheader("📊 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Users", "12,345", "↗️ 234 (12%)")
        st.write(sac.Tag("Growing", color='green'))
    
    with col2:
        st.metric("Revenue", "$98,765", "↗️ $8,765 (9%)")
        st.write(sac.Tag("Excellent", color='blue'))
    
    with col3:
        st.metric("Orders", "8,901", "↘️ -123 (-1%)")
        st.write(sac.Tag("Monitor", color='orange'))
    
    with col4:
        st.metric("Conversion", "3.4%", "↗️ 0.2% (6%)")
        st.write(sac.Tag("Optimizing", color='purple'))
    
    # Process pipeline
    st.subheader("🔄 Current Operations")
    sac.steps(
        items=[
            sac.StepsItem(title='Data Collection', description='Real-time data gathering', icon='database'),
            sac.StepsItem(title='Processing', description='AI analysis in progress', icon='cpu'),
            sac.StepsItem(title='Insights', description='Generating recommendations', icon='lightbulb'),
            sac.StepsItem(title='Reporting', description='Ready for review', icon='file-check'),
        ],
        index=2,
        key='operations_pipeline'
    )
    
    # Performance chart
    st.subheader("📈 Performance Trends")
    chart_data = pd.DataFrame({
        'Date': pd.date_range('2024-05-01', periods=30, freq='D'),
        'Sales': np.random.randint(50, 200, 30) + np.sin(np.arange(30)) * 20 + 100,
        'Users': np.random.randint(30, 150, 30) + np.cos(np.arange(30)) * 15 + 80,
        'Revenue': np.random.randint(1000, 5000, 30) + np.sin(np.arange(30)) * 500 + 2500
    })
    st.line_chart(chart_data.set_index('Date'))
    
    # Recent alerts
    st.subheader("🔔 Recent Alerts")
    sac.alert(
        label='New Feature Released!',
        description='Advanced analytics dashboard is now available in the Analytics section.',
        banner=True,
        icon=True,
        type='success',
        key='feature_alert'
    )
    
    sac.alert(
        label='High Traffic Detected',
        description='Your site is experiencing 150% more traffic than usual today.',
        banner=True,
        icon=True,
        type='info',
        key='traffic_alert'
    )

def render_analytics_overview():
    st.title("📊 Analytics Overview")
    
    # Time period selector
    time_period = sac.segmented(
        items=['Last 7 days', 'Last 30 days', 'Last 90 days', 'Custom Range'],
        index=1,
        key='analytics_time_period'
    )
    
    st.write(f"📅 Showing data for: **{time_period}**")
    
    # Analytics metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("👥 User Metrics")
        st.metric("Total Users", "45,678", "↗️ 12%")
        st.metric("Active Users", "23,456", "↗️ 8%")
        st.metric("New Users", "5,432", "↗️ 15%")
    
    with col2:
        st.subheader("💰 Revenue Metrics")
        st.metric("Total Revenue", "$234,567", "↗️ 18%")
        st.metric("Avg. Order Value", "$78.90", "↗️ 5%")
        st.metric("Monthly Recurring", "$12,345", "↗️ 22%")
    
    with col3:
        st.subheader("📈 Performance")
        st.metric("Page Views", "567,890", "↗️ 25%")
        st.metric("Bounce Rate", "32.1%", "↘️ -3%")
        st.metric("Session Duration", "4m 32s", "↗️ 12%")
    
    # Detailed analytics chart
    st.subheader("📈 Detailed Analytics")
    
    # Chart type selector
    chart_type = sac.tabs([
        sac.TabsItem(label='Traffic', icon='graph-up'),
        sac.TabsItem(label='Revenue', icon='currency-dollar'),
        sac.TabsItem(label='Users', icon='people'),
        sac.TabsItem(label='Conversion', icon='target'),
    ], index=0, key='analytics_chart_tabs')
    
    # Generate sample data based on selection
    dates = pd.date_range('2024-05-01', periods=30, freq='D')
    
    if chart_type == 'Traffic':
        data = pd.DataFrame({
            'Date': dates,
            'Page Views': np.random.randint(1000, 5000, 30),
            'Unique Visitors': np.random.randint(500, 2500, 30),
            'Sessions': np.random.randint(800, 3500, 30)
        })
    elif chart_type == 'Revenue':
        data = pd.DataFrame({
            'Date': dates,
            'Daily Revenue': np.random.randint(5000, 15000, 30),
            'Orders': np.random.randint(50, 200, 30)
        })
    elif chart_type == 'Users':
        data = pd.DataFrame({
            'Date': dates,
            'New Users': np.random.randint(100, 500, 30),
            'Returning Users': np.random.randint(200, 800, 30)
        })
    else:  # Conversion
        data = pd.DataFrame({
            'Date': dates,
            'Conversion Rate': np.random.uniform(2.0, 5.0, 30),
            'Click Rate': np.random.uniform(8.0, 15.0, 30)
        })
    
    st.line_chart(data.set_index('Date'))

def render_product_catalog():
    st.title("📦 Product Catalog")
    
    # Product management tools
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("🔍 Product Search & Filter")
        search_term = st.text_input("Search products...", placeholder="Enter product name or SKU")
    
    with col2:
        st.subheader("📊 Quick Stats")
        st.metric("Total Products", "1,234")
        st.metric("In Stock", "1,156")
        st.metric("Low Stock", "78")
    
    # Category filter using checkbox
    st.subheader("🏷️ Filter by Category")
    categories = sac.checkbox(
        items=['Electronics', 'Clothing', 'Books', 'Home & Garden', 'Sports', 'Toys'],
        index=[0, 1],
        key='category_filter'
    )
    
    # Product status filter using transfer
    st.subheader("📋 Product Status Selection")
    product_statuses = sac.transfer(
        items=['Active', 'Draft', 'Archived', 'Out of Stock', 'Discontinued'],
        index=[0, 1],
        key='status_transfer'
    )
    
    # Pagination for product list
    st.subheader("📄 Product List")
    page = sac.pagination(total=1234, page_size=20, key='product_pagination')
    
    # Sample product data
    products_data = pd.DataFrame({
        'SKU': [f'PRD-{1000 + i + (page-1)*20}' for i in range(20)],
        'Product Name': [f'Product {i + (page-1)*20}' for i in range(20)],
        'Category': np.random.choice(['Electronics', 'Clothing', 'Books'], 20),
        'Price': [f'${np.random.randint(10, 500)}' for _ in range(20)],
        'Stock': np.random.randint(0, 100, 20),
        'Status': np.random.choice(['Active', 'Low Stock', 'Out of Stock'], 20)
    })
    
    st.dataframe(products_data, use_container_width=True)

def render_customer_support():
    st.title("🎧 Customer Support")
    
    # Support metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Open Tickets", "234", "↗️ 12")
    with col2:
        st.metric("Avg Response Time", "2h 15m", "↘️ -15m")
    with col3:
        st.metric("Resolution Rate", "94.5%", "↗️ 2%")
    with col4:
        st.metric("Satisfaction Score", "4.7/5", "↗️ 0.1")
    
    # Support tools
    st.subheader("🛠️ Support Tools")
    
    support_tool = sac.segmented(
        items=['Live Chat', 'Ticket System', 'Knowledge Base', 'Call Center'],
        index=0,
        key='support_tools'
    )
    
    if support_tool == 'Live Chat':
        st.subheader("💬 Live Chat Dashboard")
        st.write("Monitor active chat sessions and agent performance.")
        
        # Chat status
        chat_status = sac.tag("12 Active Chats", color='green')
        st.write(chat_status)
        
    elif support_tool == 'Ticket System':
        st.subheader("🎫 Support Tickets")
        
        # Ticket priority distribution
        ticket_priorities = sac.checkbox(
            items=['High Priority', 'Medium Priority', 'Low Priority', 'Urgent'],
            index=[0, 1],
            key='ticket_priorities'
        )
        
        st.write(f"Showing tickets with priorities: {ticket_priorities}")
    
    # Support result summary
    sac.result(
        label='Support Performance',
        description='Your support team is performing excellently with 94.5% resolution rate.',
        status='success',
        key='support_performance'
    )

def render_settings():
    st.title("⚙️ Settings")
    
    # Settings categories using tabs
    settings_tab = sac.tabs([
        sac.TabsItem(label='General', icon='gear'),
        sac.TabsItem(label='Account', icon='person'),
        sac.TabsItem(label='Notifications', icon='bell'),
        sac.TabsItem(label='Security', icon='shield'),
        sac.TabsItem(label='Integrations', icon='puzzle'),
    ], index=0, key='settings_tabs')
    
    if settings_tab == 'General':
        st.subheader("🎨 General Settings")
        
        # Theme selection
        theme = sac.segmented(
            items=['Light', 'Dark', 'Auto'],
            index=0,
            key='theme_selection'
        )
        
        # Language and region
        col1, col2 = st.columns(2)
        with col1:
            language = st.selectbox("Language", ["English", "Spanish", "French", "German"])
        with col2:
            timezone = st.selectbox("Timezone", ["UTC", "EST", "PST", "CET"])
        
        # Performance settings
        st.subheader("⚡ Performance")
        auto_save = sac.switch(label='Auto-save changes', value=True, key='auto_save')
        lazy_loading = sac.switch(label='Enable lazy loading', value=True, key='lazy_loading')
        
    elif settings_tab == 'Account':
        st.subheader("👤 Account Information")
        
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Full Name", value="John Doe")
            st.text_input("Email", value="john.doe@company.com")
            st.text_input("Company", value="Tech Corp")
        
        with col2:
            # Account level rating
            account_level = sac.rate(label='Account Level', value=4, key='account_level')
            st.write(f"Account Level: {account_level}/5")
            
            # Account status
            sac.result(
                label='Account Active',
                description='Your account is in good standing.',
                status='success',
                key='account_status'
            )
    
    elif settings_tab == 'Notifications':
        st.subheader("🔔 Notification Preferences")
        
        # Notification types
        notification_types = sac.checkbox(
            items=[
                'Email notifications',
                'Push notifications', 
                'SMS alerts',
                'Weekly digest',
                'System updates',
                'Security alerts'
            ],
            index=[0, 1, 5],
            key='notification_types'
        )
        
        st.write(f"Enabled notifications: {notification_types}")

# Main content routing
current_page = st.session_state.current_page

# Route to appropriate content
if current_page == 'home':
    render_home()
elif current_page == 'overview':
    render_analytics_overview()
elif current_page == 'catalog':
    render_product_catalog()
elif current_page == 'support':
    render_customer_support()
elif current_page == 'settings':
    render_settings()
elif current_page in ['reports', 'users', 'sales', 'traffic', 'electronics', 'clothing', 'books', 'home_garden', 'customer_list', 'segments', 'feedback', 'generate', 'templates', 'scheduled', 'exports', 'integrations', 'api', 'backup']:
    st.title(f"🎯 {current_page.replace('_', ' ').title()}")
    st.write(f"This is the **{current_page.replace('_', ' ').title()}** section.")
    st.info("Content for this section would be implemented here based on your specific needs.")
    
    # Show some example content based on the page
    if 'report' in current_page:
        st.subheader("📊 Sample Report Interface")
        report_type = sac.segmented(['Daily', 'Weekly', 'Monthly'], index=1, key=f'{current_page}_period')
        st.write(f"Generating {report_type} {current_page.replace('_', ' ')} report...")
        
    elif current_page in ['users', 'customer_list']:
        st.subheader("👥 User Management")
        user_page = sac.pagination(total=500, page_size=25, key=f'{current_page}_pagination')
        st.write(f"Showing page {user_page} of users")
        
    elif current_page in ['electronics', 'clothing', 'books']:
        st.subheader(f"🏷️ {current_page.title()} Category")
        filter_options = sac.checkbox(['In Stock', 'On Sale', 'New'], index=[0], key=f'{current_page}_filters')
        st.write(f"Filters applied: {filter_options}")
else:
    render_home()  # Default fallback

# Footer status bar
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"**📍 Current Page:** {current_page.replace('_', ' ').title()}")
with col2:
    st.markdown(f"**🌙 Dark Mode:** {'✅' if dark_mode else '❌'}")
with col3:
    st.markdown(f"**🔄 Auto Refresh:** {'✅' if auto_refresh else '❌'}")
with col4:
    st.markdown(f"**🔔 Notifications:** {'✅' if notifications else '❌'}")

# Show quick action feedback
if quick_action:
    st.success(f"✅ Quick action executed: **{quick_action}**")

st.markdown("*🚀 Powered by Streamlit Antd Components - Professional, Reliable, Feature-Rich*")
