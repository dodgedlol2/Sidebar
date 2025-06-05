import yaml
import streamlit_authenticator as stauth
from datetime import datetime
import os

class KaspaConfigManager:
    """Configuration manager for Kaspa Analytics authentication"""
    
    def __init__(self, config_path='config.yaml'):
        self.config_path = config_path
        self.config = self.load_config()
    
    def load_config(self):
        """Load configuration from YAML file"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as file:
                    config = yaml.safe_load(file)
                print(f"✅ Configuration loaded from {self.config_path}")
                return config
            else:
                print(f"⚠️ Config file {self.config_path} not found. Creating default config.")
                return self.create_default_config()
        except Exception as e:
            print(f"❌ Error loading config: {e}")
            return self.create_default_config()
    
    def save_config(self):
        """Save configuration to YAML file"""
        try:
            with open(self.config_path, 'w') as file:
                yaml.dump(self.config, file, default_flow_style=False, allow_unicode=True)
            print(f"✅ Configuration saved to {self.config_path}")
            return True
        except Exception as e:
            print(f"❌ Error saving config: {e}")
            return False
    
    def create_default_config(self):
        """Create default configuration"""
        return {
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
                    }
                }
            },
            'cookie': {
                'name': 'kaspa_analytics_auth',
                'key': 'kaspa_secret_key_12345_change_in_production',
                'expiry_days': 30
            },
            'preauthorized': ['admin@kaspalytics.com'],
            'api_key': 'a9fz9gh0zq7io3zpjnya1vmx8et9b3pd'
        }
    
    def hash_passwords(self):
        """Hash all plain text passwords in the configuration"""
        try:
            passwords_to_hash = []
            usernames = []
            
            for username, user_info in self.config['credentials']['usernames'].items():
                password = user_info.get('password')
                if password and not self.is_password_hashed(password):
                    passwords_to_hash.append(password)
                    usernames.append(username)
            
            if passwords_to_hash:
                hashed_passwords = stauth.Hasher(passwords_to_hash).generate()
                
                for i, username in enumerate(usernames):
                    self.config['credentials']['usernames'][username]['password'] = hashed_passwords[i]
                    print(f"✅ Password hashed for user: {username}")
                
                self.save_config()
                print("✅ All passwords have been hashed and saved")
            else:
                print("ℹ️ All passwords are already hashed")
                
        except Exception as e:
            print(f"❌ Error hashing passwords: {e}")
    
    def is_password_hashed(self, password):
        """Check if a password is already hashed"""
        return password.startswith('$2b$') or password.startswith('$2a$')
    
    def add_user(self, username, email, first_name, last_name, password, subscription='free'):
        """Add a new user to the configuration"""
        try:
            if username in self.config['credentials']['usernames']:
                print(f"⚠️ User {username} already exists")
                return False
            
            self.config['credentials']['usernames'][username] = {
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'password': password,  # Will be hashed later
                'subscription': subscription,
                'failed_login_attempts': 0,
                'logged_in': False,
                'created_at': datetime.now().isoformat()
            }
            
            print(f"✅ User {username} added successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error adding user: {e}")
            return False
    
    def update_user_subscription(self, username, new_subscription):
        """Update user subscription level"""
        try:
            if username not in self.config['credentials']['usernames']:
                print(f"⚠️ User {username} not found")
                return False
            
            old_subscription = self.config['credentials']['usernames'][username].get('subscription', 'free')
            self.config['credentials']['usernames'][username]['subscription'] = new_subscription
            
            print(f"✅ User {username} subscription updated: {old_subscription} → {new_subscription}")
            return True
            
        except Exception as e:
            print(f"❌ Error updating subscription: {e}")
            return False
    
    def add_preauthorized_email(self, email):
        """Add email to preauthorized list"""
        try:
            if email not in self.config['preauthorized']:
                self.config['preauthorized'].append(email)
                print(f"✅ Email {email} added to preauthorized list")
                return True
            else:
                print(f"ℹ️ Email {email} already in preauthorized list")
                return False
        except Exception as e:
            print(f"❌ Error adding preauthorized email: {e}")
            return False
    
    def remove_user(self, username):
        """Remove a user from the configuration"""
        try:
            if username in self.config['credentials']['usernames']:
                del self.config['credentials']['usernames'][username]
                print(f"✅ User {username} removed successfully")
                return True
            else:
                print(f"⚠️ User {username} not found")
                return False
        except Exception as e:
            print(f"❌ Error removing user: {e}")
            return False
    
    def list_users(self):
        """List all users with their subscription levels"""
        print("\n📋 Current Users:")
        print("-" * 60)
        for username, user_info in self.config['credentials']['usernames'].items():
            subscription = user_info.get('subscription', 'free')
            email = user_info.get('email', 'No email')
            name = f"{user_info.get('first_name', '')} {user_info.get('last_name', '')}".strip()
            failed_attempts = user_info.get('failed_login_attempts', 0)
            
            print(f"👤 {username:<15} | {name:<20} | {subscription:<10} | {email}")
            if failed_attempts > 0:
                print(f"   ⚠️ Failed login attempts: {failed_attempts}")
        print("-" * 60)
    
    def reset_failed_attempts(self, username):
        """Reset failed login attempts for a user"""
        try:
            if username in self.config['credentials']['usernames']:
                self.config['credentials']['usernames'][username]['failed_login_attempts'] = 0
                print(f"✅ Failed login attempts reset for {username}")
                return True
            else:
                print(f"⚠️ User {username} not found")
                return False
        except Exception as e:
            print(f"❌ Error resetting failed attempts: {e}")
            return False
    
    def backup_config(self, backup_path=None):
        """Create a backup of the current configuration"""
        try:
            if not backup_path:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_path = f"config_backup_{timestamp}.yaml"
            
            with open(backup_path, 'w') as file:
                yaml.dump(self.config, file, default_flow_style=False, allow_unicode=True)
            
            print(f"✅ Configuration backed up to {backup_path}")
            return backup_path
            
        except Exception as e:
            print(f"❌ Error creating backup: {e}")
            return None

def main():
    """Demo usage of the configuration manager"""
    print("🚀 Kaspa Analytics Configuration Manager")
    print("=" * 50)
    
    # Initialize config manager
    config_manager = KaspaConfigManager()
    
    # List current users
    config_manager.list_users()
    
    # Example: Add a new user
    print("\n➕ Adding new demo user...")
    config_manager.add_user(
        username='newuser',
        email='newuser@example.com',
        first_name='New',
        last_name='User',
        password='newuser123',
        subscription='free'
    )
    
    # Hash all passwords
    print("\n🔒 Hashing passwords...")
    config_manager.hash_passwords()
    
    # Add preauthorized email
    print("\n📧 Adding preauthorized email...")
    config_manager.add_preauthorized_email('vip@kaspalytics.com')
    
    # Save configuration
    print("\n💾 Saving configuration...")
    config_manager.save_config()
    
    # Create backup
    print("\n🗂️ Creating backup...")
    backup_file = config_manager.backup_config()
    
    print(f"\n✅ Configuration management complete!")
    print(f"📁 Config file: {config_manager.config_path}")
    if backup_file:
        print(f"🗂️ Backup file: {backup_file}")

if __name__ == "__main__":
    main()
