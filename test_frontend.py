#!/usr/bin/env python3
"""
Automated frontend test using Selenium
"""
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import subprocess
import threading
import requests
import os

class FrontendTester:
    def __init__(self):
        self.driver = None
        self.api_process = None
        self.frontend_process = None
    
    def setup_servers(self):
        """Start backend and frontend servers"""
        print("🚀 Starting backend server...")
        self.api_process = subprocess.Popen(['python', '-m', 'app.api'], 
                                          stdout=subprocess.PIPE, 
                                          stderr=subprocess.PIPE)
        time.sleep(3)  # Wait for server to start
        
        # Test if API is running
        try:
            response = requests.get('http://localhost:5001/health', timeout=5)
            if response.status_code == 200:
                print("✅ Backend server running")
            else:
                raise Exception("Backend not responding")
        except:
            print("❌ Backend server failed to start")
            return False
        
        print("🌐 Starting frontend server...")
        os.chdir('frontend')
        self.frontend_process = subprocess.Popen(['python', '-m', 'http.server', '8000'],
                                               stdout=subprocess.PIPE,
                                               stderr=subprocess.PIPE)
        os.chdir('..')
        time.sleep(2)
        
        return True
    
    def setup_browser(self):
        """Setup Chrome browser in headless mode"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            print("✅ Browser setup complete")
            return True
        except Exception as e:
            print(f"❌ Browser setup failed: {e}")
            print("💡 Install ChromeDriver: brew install chromedriver")
            return False
    
    def test_form_submission(self):
        """Test the main form submission flow"""
        print("\n📝 Testing form submission...")
        
        try:
            # Navigate to frontend
            self.driver.get('http://localhost:8000')
            
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "salary"))
            )
            print("✅ Page loaded successfully")
            
            # Fill salary
            salary_input = self.driver.find_element(By.ID, "salary")
            salary_input.clear()
            salary_input.send_keys("15000")
            
            # Fill spending amounts
            spending_data = {
                "groceries": "2000",
                "international_travel": "3000", 
                "fuel": "500",
                "online": "1000",
                "dining": "1500"
            }
            
            for field, value in spending_data.items():
                element = self.driver.find_element(By.NAME, field)
                element.clear()
                element.send_keys(value)
            
            print("✅ Form fields filled")
            
            # Select goals
            travel_goal = self.driver.find_element(By.CSS_SELECTOR, '[data-goal="travel"]')
            travel_goal.click()
            
            lounge_goal = self.driver.find_element(By.CSS_SELECTOR, '[data-goal="airport_lounge"]')
            lounge_goal.click()
            
            print("✅ Goals selected")
            
            # Submit form
            submit_btn = self.driver.find_element(By.ID, "submitBtn")
            submit_btn.click()
            
            # Wait for loading to appear
            WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.ID, "loading"))
            )
            print("✅ Loading state activated")
            
            # Wait for results to appear (max 30 seconds)
            WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located((By.ID, "results"))
            )
            print("✅ Results displayed")
            
            # Check if recommendations are present
            cards = self.driver.find_elements(By.CLASS_NAME, "card-result")
            if len(cards) > 0:
                print(f"✅ Found {len(cards)} card recommendations")
                
                # Get first card details
                first_card = cards[0]
                card_name = first_card.find_element(By.TAG_NAME, "h3").text
                print(f"✅ Top recommendation: {card_name}")
                
                return True
            else:
                print("❌ No card recommendations found")
                return False
                
        except Exception as e:
            print(f"❌ Form submission test failed: {e}")
            return False
    
    def test_chat_functionality(self):
        """Test the chat feature"""
        print("\n💬 Testing chat functionality...")
        
        try:
            # Find chat input
            chat_input = self.driver.find_element(By.ID, "chatInput")
            chat_input.clear()
            chat_input.send_keys("What cards have no annual fee?")
            
            # Send message
            send_btn = self.driver.find_element(By.CSS_SELECTOR, ".chat-input-group button")
            send_btn.click()
            
            # Wait for response (max 15 seconds)
            WebDriverWait(self.driver, 15).until(
                lambda driver: len(driver.find_elements(By.CSS_SELECTOR, ".chat-message.agent")) > 1
            )
            
            messages = self.driver.find_elements(By.CSS_SELECTOR, ".chat-message.agent")
            if len(messages) > 1:
                print("✅ Chat response received")
                return True
            else:
                print("❌ No chat response")
                return False
                
        except Exception as e:
            print(f"❌ Chat test failed: {e}")
            return False
    
    def test_ui_elements(self):
        """Test UI elements are present and functional"""
        print("\n🎨 Testing UI elements...")
        
        try:
            # Check main sections exist
            sections = ["profileForm", "loading", "results"]
            for section_id in sections:
                element = self.driver.find_element(By.ID, section_id)
                if element:
                    print(f"✅ {section_id} section found")
            
            # Check goal tags are clickable
            goal_tags = self.driver.find_elements(By.CLASS_NAME, "goal-tag")
            if len(goal_tags) >= 6:
                print(f"✅ Found {len(goal_tags)} goal options")
            
            # Check spending inputs
            spending_inputs = self.driver.find_elements(By.CSS_SELECTOR, ".spending-grid input")
            if len(spending_inputs) >= 10:
                print(f"✅ Found {len(spending_inputs)} spending categories")
            
            return True
            
        except Exception as e:
            print(f"❌ UI elements test failed: {e}")
            return False
    
    def run_all_tests(self):
        """Run all frontend tests"""
        print("🧪 Starting automated frontend tests...\n")
        
        if not self.setup_servers():
            return False
        
        if not self.setup_browser():
            return False
        
        try:
            results = {
                "ui_elements": self.test_ui_elements(),
                "form_submission": self.test_form_submission(), 
                "chat_functionality": self.test_chat_functionality()
            }
            
            print(f"\n📊 Test Results:")
            print(f"UI Elements: {'✅ PASS' if results['ui_elements'] else '❌ FAIL'}")
            print(f"Form Submission: {'✅ PASS' if results['form_submission'] else '❌ FAIL'}")
            print(f"Chat Functionality: {'✅ PASS' if results['chat_functionality'] else '❌ FAIL'}")
            
            all_passed = all(results.values())
            print(f"\n🎯 Overall Result: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")
            
            return all_passed
            
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        if self.driver:
            self.driver.quit()
        
        if self.api_process:
            self.api_process.terminate()
        
        if self.frontend_process:
            self.frontend_process.terminate()
        
        print("\n🧹 Cleanup completed")

def main():
    tester = FrontendTester()
    success = tester.run_all_tests()
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())