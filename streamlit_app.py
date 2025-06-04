import streamlit as st
import streamlit_antd_components as sac
import streamlit_authenticator as stauth
import pandas as pd
import numpy as np
import yaml
from yaml.loader import SafeLoader

# Configure page settings
st.set_page_config(
    page_title="Secure Professional Dashboard",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load authentication configuration
@st.cache_data
def load_config():
    """Load authentication configuration from YAML file"""
    # You can also define this directly in code for testing
    config = {
        'credentials': {
            'usernames': {
                'admin': {
                    'email': 'admin@company.com',
                    'first_name': 'Admin',
                    'last_name': 'User',
                    'password': '$2b$12$R9Ek8JIj3VJLv7Z1QHE.quGbQnTG8jC9Y8Kk1kV9FjI.KJHGFDS1e'  # 'admin123'
                },
                'jsmith': {
                    'email': 'john.smith@company.com',
                    'first_name': 'John',
                    'last_name': 'Smith',
                    'password': '$2b$12$3P4t7y8R9Ek8JIj3VJLv7Z1QHE.quGbQnTG8jC9Y8Kk1kV9FjI.KJ'  # 'user123'
                },
                'mwilson': {
                    'email': 'mary.wilson@company.com',
                    'first_name': 'Mary',
                    'last_name': 'Wilson',
                    'password': '$2b$12$7Z1QHE.quGbQnTG8jC9Y8Kk1kV9FjI.KJHGFDS1eR9Ek8JIj3VJLv'  # 'mary456'
                }
            }
        },
        'cookie': {
            'name': 'dashboard_auth_cookie',
            'key': 'your_secret_random_key_12345',  # Change this to a random secret key
            'expiry_days': 30
        },
        'preauthorized': [
            'admin@company.com',
            'new.user@company.com'
        ]
    }
    return config

# Initialize authenticator
config = load_config()
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

# Custom CSS for better styling
st.markdown("""
<style>
/* Main styling */
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

/* Auth styling */
.auth-container {
    max-width: 400px;
    margin: 0 auto;
    padding: 2rem;
    background: white;
    border-radius: 12px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    border: 1px solid #e9ecef;
}

.user-info {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 1rem;
    border-radius: 8px;
    margin: 0.5rem 0;
}
</style>
""", unsafe_allow_html=True)

# Login function
def show_login_page():
    """Display the login page with antd components"""
    
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    st.title("🔐 Secure Dashboard Login")
    st.markdown("*Please log in to access your professional dashboard*")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Login form in center
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        
        # Login widget - Use the correct modern syntax
        authenticator.login()
        
        # Get authentication status from session state
        name = st.session_state.get('name')
        authentication_status = st.session_state.get('authentication_status')
        username = st.session_state.get('username')
        
        if authentication_status == False:
            sac.alert(
                label='Authentication Failed',
                description='Username/password is incorrect. Please try again.',
                banner=True,
                icon=True,
                type='error',
                key='login_error'
            )
        elif authentication_status == None:
            sac.alert(
                label='Welcome!',
                description='Please enter your username and password to continue.',
                banner=True,
                icon=True,
                type='info',
                key='login_info'
            )
        
        # Demo credentials info
        st.markdown("---")
        st.markdown("**🔑 Demo Credentials:**")
        
        demo_creds = sac.tabs([
            sac.TabsItem(label='Admin', icon='person-gear'),
            sac.TabsItem(label='User 1', icon='person'),
            sac.TabsItem(label='User 2', icon='person'),
        ], index=0, key='demo_creds_tabs')
        
        if demo_creds == 'Admin':
            st.code("Username: admin\nPassword: admin123")
        elif demo_creds == 'User 1':
            st.code("Username: jsmith\nPassword: user123")
        else:
            st.code("Username: mwilson\nPassword: mary456")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    return name, authentication_status, username

def show_main_app(name, username):
    """Display the main authenticated application"""
    
    # Initialize session state for navigation
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'home'
    
    # Main header with user info
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.title("🚀 Professional Dashboard")
        st.markdown(f"*Welcome back, **{name}**! You're logged in as **{username}***")
    
    with col2:
        st.markdown('<div class="user-info">', unsafe_allow_html=True)
        st.markdown(f"**👤 {name}**")
        st.markdown(f"🏷️ @{username}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Sidebar with navigation and user controls
    with st.sidebar:
        # User info section
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown(f"**👋 Welcome, {name.split()[0]}!**")
        st.markdown(f"Logged in as: **{username}**")
        
        # Logout button
        if st.button("🚪 Logout", type="secondary", use_container_width=True):
            # Use authenticator logout
            authenticator.logout()
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.title("🎯 Navigation")
        
        # Role-based navigation (example)
        user_role = "admin" if username == "admin" else "user"
        
        if user_role == "admin":
            # Admin gets full access
            menu_items = [
                sac.MenuItem('home', icon='house-fill', tag=[
                    sac.Tag('Main', color='blue'),
                    sac.Tag('Admin', color='red')
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
                    sac.MenuItem('categories', icon='tags'),
                    sac.MenuItem('inventory', icon='boxes', description='Stock management'),
                    sac.MenuItem('suppliers', icon='truck', description='Supplier network'),
                ]),
                
                sac.MenuItem('customers', icon='people-fill', children=[
                    sac.MenuItem('customer_list', icon='person-lines-fill'),
                    sac.MenuItem('segments', icon='diagram-3'),
                    sac.MenuItem('support', icon='headset', tag=sac.Tag('24/7', color='red')),
                ]),
                
                sac.MenuItem('admin', icon='shield-check', children=[
                    sac.MenuItem('user_management', icon='people-fill', description='Manage users'),
                    sac.MenuItem('system_settings', icon='gear-fill', description='System configuration'),
                    sac.MenuItem('audit_logs', icon='journal-text', description='System logs'),
                    sac.MenuItem('backup', icon='cloud-arrow-up', description='Data backup'),
                ]),
                
                sac.MenuItem(type='divider'),
                
                sac.MenuItem('settings', icon='sliders'),
                sac.MenuItem('help', icon='question-circle-fill'),
            ]
        else:
            # Regular users get limited access
            menu_items = [
                sac.MenuItem('home', icon='house-fill', tag=sac.Tag('Main', color='blue')),
                
                sac.MenuItem('analytics', icon='bar-chart-fill', children=[
                    sac.MenuItem('overview', icon='speedometer2', description='Key metrics dashboard'),
                    sac.MenuItem('reports', icon='file-earmark-text', description='Your reports'),
                ]),
                
                sac.MenuItem('products', icon='box-fill', children=[
                    sac.MenuItem('catalog', icon='grid', description='View catalog'),
                    sac.MenuItem('categories', icon='tags', description='Browse categories'),
                ]),
                
                sac.MenuItem('profile', icon='person-circle', description='Your profile'),
                sac.MenuItem('help', icon='question-circle-fill'),
            ]
        
        # Main navigation menu
        selected = sac.menu(menu_items, open_all=True, key='main_menu')
        
        # Update session state
        if selected:
            st.session_state.current_page = selected
        
        # Quick actions section
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown("**⚡ Quick Actions**")
        
        quick_action = sac.buttons([
            sac.ButtonsItem(label='Export Data', icon='download'),
            sac.ButtonsItem(label='Refresh', icon='arrow-clockwise'),
            sac.ButtonsItem(label='Profile', icon='person'),
        ], index=None, format_func='title', align='center', key='quick_buttons')
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Preferences section
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown("**🎛️ Preferences**")
        
        dark_mode = sac.switch(label='Dark Mode', value=False, key='dark_mode_switch')
        auto_refresh = sac.switch(label='Auto Refresh', value=True, key='auto_refresh_switch')
        notifications = sac.switch(label='Notifications', value=True, key='notifications_switch')
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Status section
        st.markdown('<div class="status-bar">', unsafe_allow_html=True)
        st.markdown(f"**📊 Status: Online | Role: {user_role.title()}**")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Content rendering based on user role and selection
    current_page = st.session_state.current_page
    
    # Route to appropriate content with role checking
    if current_page == 'home':
        render_home(name, username, user_role)
    elif current_page == 'overview':
        render_analytics_overview(user_role)
    elif current_page == 'catalog':
        render_product_catalog(user_role)
    elif current_page == 'user_management' and user_role == 'admin':
        render_user_management()
    elif current_page == 'system_settings' and user_role == 'admin':
        render_system_settings()
    elif current_page == 'audit_logs' and user_role == 'admin':
        render_audit_logs()
    elif current_page == 'profile':
        render_user_profile(name, username)
    elif current_page in ['reports', 'users', 'sales', 'traffic', 'categories', 'inventory', 'suppliers', 'customer_list', 'segments', 'support', 'backup', 'settings', 'help']:
        render_generic_page(current_page, user_role)
    else:
        render_home(name, username, user_role)
    
    # Footer with user and system info
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"**👤 User:** {name}")
    with col2:
        st.markdown(f"**📍 Page:** {current_page.replace('_', ' ').title()}")
    with col3:
        st.markdown(f"**🛡️ Role:** {user_role.title()}")
    with col4:
        st.markdown(f"**🔔 Notifications:** {'✅' if notifications else '❌'}")
    
    # Show quick action feedback
    if quick_action:
        if quick_action == 'Profile':
            st.session_state.current_page = 'profile'
            st.rerun()
        else:
            st.success(f"✅ Quick action executed: **{quick_action}**")

# Content rendering functions
def render_home(name, username, user_role):
    """Render the home dashboard with user-specific content"""
    
    st.title("🏠 Dashboard Home")
    
    # Welcome section with user info
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader(f"Welcome back, {name.split()[0]}! 👋")
        st.write(f"You're logged in as **{username}** with **{user_role}** privileges.")
        
        # Role-specific welcome message
        if user_role == "admin":
            sac.alert(
                label='Admin Dashboard',
                description='You have full administrative access to all features and data.',
                banner=True,
                icon=True,
                type='success',
                key='admin_welcome'
            )
        else:
            sac.alert(
                label='User Dashboard',
                description='Welcome! You have access to your personalized dashboard and reports.',
                banner=True,
                icon=True,
                type='info',
                key='user_welcome'
            )
    
    with col2:
        st.subheader("Rate your experience")
        rating = sac.rate(label='Satisfaction', value=4, key='satisfaction_rating')
        if rating:
            st.write(f"Rating: {rating}/5 ⭐")
    
    # Key metrics (role-based)
    st.subheader("📊 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    if user_role == "admin":
        # Admin sees all metrics
        with col1:
            st.metric("Total Users", "12,345", "↗️ 234 (12%)")
            st.write(sac.Tag("All Users", color='green'))
        
        with col2:
            st.metric("System Revenue", "$98,765", "↗️ $8,765 (9%)")
            st.write(sac.Tag("Full Access", color='blue'))
        
        with col3:
            st.metric("All Orders", "8,901", "↘️ -123 (-1%)")
            st.write(sac.Tag("Monitor", color='orange'))
        
        with col4:
            st.metric("System Performance", "98.5%", "↗️ 0.2%")
            st.write(sac.Tag("Admin View", color='red'))
    else:
        # Regular users see limited metrics
        with col1:
            st.metric("My Reports", "23", "↗️ 3")
            st.write(sac.Tag("Personal", color='blue'))
        
        with col2:
            st.metric("My Activity", "156", "↗️ 12")
            st.write(sac.Tag("Active", color='green'))
        
        with col3:
            st.metric("Notifications", "7", "↗️ 2")
            st.write(sac.Tag("New", color='orange'))
        
        with col4:
            st.metric("Profile Score", "85%", "↗️ 5%")
            st.write(sac.Tag("Good", color='purple'))
    
    # Recent activity
    st.subheader("📈 Recent Activity")
    
    if user_role == "admin":
        activities = [
            "System backup completed successfully",
            "New user 'demo_user' registered",
            "Security audit passed",
            "Database optimization completed",
            "3 new support tickets created"
        ]
    else:
        activities = [
            f"Welcome back, {name}!",
            "Profile updated successfully",
            "New notification received",
            "Report generated successfully",
            "Dashboard preferences saved"
        ]
    
    for i, activity in enumerate(activities):
        st.write(f"• {activity}")

def render_user_management():
    """Admin-only user management page"""
    
    st.title("👥 User Management")
    st.write("Manage system users, roles, and permissions.")
    
    # User list with antd components
    st.subheader("📋 System Users")
    
    # Sample user data
    users_data = pd.DataFrame({
        'Username': ['admin', 'jsmith', 'mwilson', 'demo_user'],
        'Full Name': ['Admin User', 'John Smith', 'Mary Wilson', 'Demo User'],
        'Email': ['admin@company.com', 'john.smith@company.com', 'mary.wilson@company.com', 'demo@company.com'],
        'Role': ['Admin', 'User', 'User', 'User'],
        'Status': ['Active', 'Active', 'Active', 'Inactive']
    })
    
    st.dataframe(users_data, use_container_width=True)
    
    # User actions
    st.subheader("🔧 User Actions")
    
    user_action = sac.buttons([
        sac.ButtonsItem(label='Add User', icon='person-plus'),
        sac.ButtonsItem(label='Edit Roles', icon='pencil-square'),
        sac.ButtonsItem(label='Export Users', icon='download'),
    ], index=None, format_func='title', key='user_management_actions')
    
    if user_action:
        st.success(f"Action triggered: {user_action}")

def render_system_settings():
    """Admin-only system settings page"""
    
    st.title("⚙️ System Settings")
    st.write("Configure system-wide settings and preferences.")
    
    settings_tab = sac.tabs([
        sac.TabsItem(label='General', icon='gear'),
        sac.TabsItem(label='Security', icon='shield'),
        sac.TabsItem(label='Backup', icon='cloud'),
        sac.TabsItem(label='Integration', icon='puzzle'),
    ], index=0, key='system_settings_tabs')
    
    if settings_tab == 'General':
        st.subheader("🎛️ General System Settings")
        
        maintenance_mode = sac.switch(label='Maintenance Mode', value=False, key='maintenance_mode')
        debug_logging = sac.switch(label='Debug Logging', value=True, key='debug_logging')
        auto_backup = sac.switch(label='Automatic Backup', value=True, key='auto_backup')
        
    elif settings_tab == 'Security':
        st.subheader("🔒 Security Settings")
        
        two_factor = sac.switch(label='Require 2FA', value=False, key='two_factor')
        session_timeout = st.slider("Session Timeout (minutes)", 15, 480, 60)
        password_policy = sac.checkbox(['Uppercase required', 'Numbers required', 'Special chars required'], 
                                     index=[0, 1], key='password_policy')

def render_audit_logs():
    """Admin-only audit logs page"""
    
    st.title("📋 Audit Logs")
    st.write("View system activity and security logs.")
    
    # Sample audit data
    audit_data = pd.DataFrame({
        'Timestamp': pd.date_range('2024-06-04 08:00', periods=10, freq='H'),
        'User': ['admin', 'jsmith', 'mwilson', 'admin', 'jsmith'] * 2,
        'Action': ['Login', 'View Report', 'Update Profile', 'System Config', 'Export Data'] * 2,
        'IP Address': ['192.168.1.1', '192.168.1.2', '192.168.1.3', '192.168.1.1', '192.168.1.2'] * 2,
        'Status': ['Success'] * 10
    })
    
    st.dataframe(audit_data, use_container_width=True)

def render_user_profile(name, username):
    """User profile page"""
    
    st.title("👤 User Profile")
    st.write(f"Manage your profile settings, {name}.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📝 Personal Information")
        st.text_input("Full Name", value=name)
        st.text_input("Username", value=username, disabled=True)
        st.text_input("Email", value=f"{username}@company.com")
    
    with col2:
        st.subheader("🎛️ Preferences")
        
        email_notifications = sac.switch(label='Email Notifications', value=True, key='profile_email_notif')
        weekly_digest = sac.switch(label='Weekly Digest', value=False, key='profile_weekly_digest')
        
        language = st.selectbox("Language", ["English", "Spanish", "French"])
        timezone = st.selectbox("Timezone", ["UTC", "EST", "PST", "CET"])
    
    if st.button("💾 Save Profile", type="primary"):
        st.success("Profile updated successfully!")

def render_generic_page(page_name, user_role):
    """Generic page renderer for other pages"""
    
    st.title(f"🎯 {page_name.replace('_', ' ').title()}")
    
    # Role-based access control
    admin_only_pages = ['user_management', 'system_settings', 'audit_logs', 'backup']
    
    if page_name in admin_only_pages and user_role != 'admin':
        sac.alert(
            label='Access Denied',
            description='You do not have permission to access this page. Contact your administrator.',
            banner=True,
            icon=True,
            type='error',
            key=f'{page_name}_access_denied'
        )
        return
    
    st.write(f"This is the **{page_name.replace('_', ' ').title()}** section.")
    
    if user_role == 'admin':
        st.info("You have full administrative access to this section.")
    else:
        st.info("You have user-level access to this section.")
    
    # Show sample content based on page
    if 'report' in page_name:
        time_period = sac.segmented(['Daily', 'Weekly', 'Monthly'], index=1, key=f'{page_name}_period')
        st.write(f"Generating {time_period} {page_name.replace('_', ' ')} report...")

# Main application logic
def main():
    """Main application entry point"""
    
    # Check authentication status from session state
    authentication_status = st.session_state.get('authentication_status')
    name = st.session_state.get('name')
    username = st.session_state.get('username')
    
    # If not authenticated, show login page
    if authentication_status is not True:
        name, authentication_status, username = show_login_page()
        
        # If login successful, rerun to show main app
        if authentication_status is True:
            st.rerun()
    else:
        # User is authenticated, show main app
        show_main_app(name, username)

# Run the application
if __name__ == "__main__":
    main()
