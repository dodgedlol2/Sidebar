import streamlit as st
import streamlit_antd_components as sac

# Configure page settings
st.set_page_config(
    page_title="My App with Antd Menu",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for navigation
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'

# Sidebar with Antd Menu
with st.sidebar:
    st.title("Navigation")
    
    # Create the menu
    selected = sac.menu([
        sac.MenuItem('home', icon='house-fill', tag=[
            sac.Tag('New', color='green'), 
            sac.Tag('Hot', color='red')
        ]),
        sac.MenuItem('products', icon='box-fill', children=[
            sac.MenuItem('apple', icon='apple'),
            sac.MenuItem('other', icon='git', description='other items', children=[
                sac.MenuItem('google', icon='google', description='Search engine'),
                sac.MenuItem('gitlab', icon='gitlab', description='Git repository'),
                sac.MenuItem('wechat', icon='wechat', description='Messaging app'),
            ]),
        ]),
        sac.MenuItem('analytics', icon='bar-chart-fill', children=[
            sac.MenuItem('dashboard', icon='speedometer2'),
            sac.MenuItem('reports', icon='file-earmark-text'),
            sac.MenuItem('charts', icon='graph-up'),
        ]),
        sac.MenuItem('settings', icon='gear-fill'),
        sac.MenuItem(type='divider'),
        sac.MenuItem('help', type='group', children=[
            sac.MenuItem('documentation', icon='book-fill', href='https://streamlit.io/'),
            sac.MenuItem('support', icon='question-circle-fill'),
        ]),
    ], open_all=True, key='main_menu')
    
    # Update session state based on menu selection
    if selected:
        st.session_state.current_page = selected

# Main content area
def render_home():
    st.title("🏠 Welcome to the Home Page")
    st.write("This is the main dashboard of your application.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Users", "1,234", "12%")
    with col2:
        st.metric("Revenue", "$45,678", "8%")
    with col3:
        st.metric("Orders", "567", "-2%")
    
    st.subheader("Recent Activity")
    st.write("Here you can display recent activities, notifications, or quick actions.")

def render_apple():
    st.title("🍎 Apple Products")
    st.write("Information about Apple products and services.")
    
    products = ["iPhone", "iPad", "MacBook", "Apple Watch", "AirPods"]
    selected_product = st.selectbox("Select a product:", products)
    st.write(f"You selected: {selected_product}")

def render_google():
    st.title("🔍 Google Services")
    st.write("Information about Google services and tools.")
    st.info("This page demonstrates navigation to a nested menu item.")

def render_gitlab():
    st.title("🦊 GitLab")
    st.write("GitLab repository management and CI/CD information.")
    st.code("""
    git clone https://gitlab.com/username/repository.git
    cd repository
    git add .
    git commit -m "Initial commit"
    git push origin main
    """)

def render_wechat():
    st.title("💬 WeChat")
    st.write("WeChat messaging and social features.")
    st.warning("This is a demo page for WeChat integration.")

def render_dashboard():
    st.title("📊 Analytics Dashboard")
    st.write("Your main analytics dashboard with key metrics and visualizations.")
    
    # Sample data visualization
    import pandas as pd
    import numpy as np
    
    # Generate sample data
    dates = pd.date_range('2024-01-01', periods=30, freq='D')
    data = pd.DataFrame({
        'Date': dates,
        'Sales': np.random.randint(100, 1000, 30),
        'Users': np.random.randint(50, 500, 30)
    })
    
    st.line_chart(data.set_index('Date'))

def render_reports():
    st.title("📄 Reports")
    st.write("Generate and view various reports.")
    
    report_type = st.selectbox("Select report type:", 
                              ["Sales Report", "User Activity", "Performance Metrics"])
    
    if st.button("Generate Report"):
        st.success(f"{report_type} generated successfully!")
        st.download_button("Download Report", "Sample report data", "report.csv")

def render_charts():
    st.title("📈 Charts")
    st.write("Various data visualizations and charts.")
    
    chart_type = st.radio("Select chart type:", ["Bar Chart", "Line Chart", "Pie Chart"])
    
    # Sample chart data
    import pandas as pd
    import numpy as np
    
    if chart_type == "Bar Chart":
        data = pd.DataFrame({
            'Category': ['A', 'B', 'C', 'D', 'E'],
            'Values': np.random.randint(10, 100, 5)
        })
        st.bar_chart(data.set_index('Category'))
    elif chart_type == "Line Chart":
        data = pd.DataFrame(np.random.randn(20, 3), columns=['X', 'Y', 'Z'])
        st.line_chart(data)
    else:  # Pie Chart
        st.write("Pie chart functionality would be implemented here with a plotting library like Plotly.")

def render_settings():
    st.title("⚙️ Settings")
    st.write("Application settings and preferences.")
    
    with st.expander("User Preferences"):
        theme = st.selectbox("Theme", ["Light", "Dark", "Auto"])
        language = st.selectbox("Language", ["English", "Spanish", "French", "German"])
        notifications = st.checkbox("Enable notifications", value=True)
    
    with st.expander("Account Settings"):
        st.text_input("Username", value="user@example.com")
        st.text_input("Full Name", value="John Doe")
        change_password = st.checkbox("Change Password")
        if change_password:
            st.text_input("New Password", type="password")
            st.text_input("Confirm Password", type="password")
    
    if st.button("Save Settings"):
        st.success("Settings saved successfully!")

def render_support():
    st.title("❓ Support")
    st.write("Get help and support for using the application.")
    
    st.subheader("Frequently Asked Questions")
    with st.expander("How do I navigate the menu?"):
        st.write("Use the sidebar menu to navigate between different sections of the application.")
    
    with st.expander("How do I generate reports?"):
        st.write("Go to Analytics > Reports and select the type of report you want to generate.")
    
    st.subheader("Contact Support")
    contact_method = st.radio("How would you like to contact us?", 
                             ["Email", "Phone", "Live Chat"])
    
    if contact_method == "Email":
        st.write("📧 support@example.com")
    elif contact_method == "Phone":
        st.write("📞 +1 (555) 123-4567")
    else:
        st.write("💬 Click the chat icon in the bottom right corner")

def render_other():
    st.title("🔧 Other Items")
    st.write("This is a general page for other miscellaneous items and tools.")
    
    st.subheader("Available Tools")
    tools = st.multiselect("Select tools to use:", 
                          ["Data Export", "Backup", "System Health Check", "Log Viewer"])
    
    for tool in tools:
        st.write(f"✅ {tool} - Ready to use")

# Main content routing
current_page = st.session_state.current_page

# Page routing
if current_page == 'home':
    render_home()
elif current_page == 'apple':
    render_apple()
elif current_page == 'google':
    render_google()
elif current_page == 'gitlab':
    render_gitlab()
elif current_page == 'wechat':
    render_wechat()
elif current_page == 'dashboard':
    render_dashboard()
elif current_page == 'reports':
    render_reports()
elif current_page == 'charts':
    render_charts()
elif current_page == 'settings':
    render_settings()
elif current_page == 'support':
    render_support()
elif current_page == 'other':
    render_other()
else:
    # Default fallback
    render_home()

# Footer
st.markdown("---")
st.markdown("**Current Page:** " + current_page.title())
st.markdown("*Built with Streamlit and Antd Components*")
