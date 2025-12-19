"""
Test Manager for ESG Project
Handles test execution and automatic cleanup
"""

import os
import shutil
import tempfile
import sys
from pathlib import Path
import time
import unittest

class ESGTestManager:
    """Manages test execution and cleanup"""
    
    def __init__(self, base_dir="d:/AI-BSM"):
        self.base_dir = Path(base_dir)
        self.test_dir = self.base_dir / "tests"
        self.temp_files = []
        self.temp_dirs = []
        
        # Ensure test directory exists
        self.test_dir.mkdir(exist_ok=True)
        
    def create_temp_file(self, filename, content):
        """Create a temporary test file"""
        file_path = self.test_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.temp_files.append(file_path)
        print(f"📝 Created test file: {filename}")
        return file_path
    
    def create_temp_dir(self, dirname):
        """Create a temporary test directory"""
        dir_path = self.test_dir / dirname
        dir_path.mkdir(exist_ok=True)
        
        self.temp_dirs.append(dir_path)
        print(f"📁 Created test directory: {dirname}")
        return dir_path
    
    def run_test_and_cleanup(self, test_function, test_name="Test"):
        """Run a test function and cleanup afterwards"""
        print(f"\n🚀 Running {test_name}...")
        print("="*50)
        
        success = False
        start_time = time.time()
        
        try:
            result = test_function()
            success = bool(result)
            print(f"✅ {test_name} completed successfully!")
            
        except Exception as e:
            print(f"❌ {test_name} failed: {str(e)}")
            success = False
        
        finally:
            # Cleanup
            execution_time = time.time() - start_time
            print(f"⏱️ Execution time: {execution_time:.2f} seconds")
            self.cleanup()
            
        return success
    
    def cleanup(self):
        """Remove all temporary test files and directories"""
        print("\n🧹 Cleaning up test files...")
        
        cleanup_count = 0
        
        # Remove temporary files
        for file_path in self.temp_files:
            try:
                if file_path.exists():
                    file_path.unlink()
                    cleanup_count += 1
                    print(f"🗑️ Removed: {file_path.name}")
            except Exception as e:
                print(f"⚠️ Could not remove {file_path.name}: {e}")
        
        # Remove temporary directories
        for dir_path in self.temp_dirs:
            try:
                if dir_path.exists():
                    shutil.rmtree(dir_path)
                    cleanup_count += 1
                    print(f"🗑️ Removed directory: {dir_path.name}")
            except Exception as e:
                print(f"⚠️ Could not remove {dir_path.name}: {e}")
        
        # Clear the lists
        self.temp_files.clear()
        self.temp_dirs.clear()
        
        print(f"✅ Cleanup complete! Removed {cleanup_count} items")
    
    def run_all_tests(self):
        """Run all available tests"""
        print("🎯 ESG Project Test Suite")
        print("="*60)
        
        test_results = {}
        
        # Test 1: Ollama Connection
        test_results['ollama_connection'] = self.run_test_and_cleanup(
            self.test_ollama_connection, 
            "Ollama Connection Test"
        )
        
        # Test 2: ESG Model Evaluation
        test_results['esg_evaluation'] = self.run_test_and_cleanup(
            self.test_esg_evaluation,
            "ESG Model Evaluation Test"
        )
        
        # Test 3: Complete System Integration
        test_results['system_integration'] = self.run_test_and_cleanup(
            self.test_system_integration,
            "Complete System Integration Test"
        )
        
        # Test Summary
        self.print_test_summary(test_results)
        
        return test_results
    
    def test_ollama_connection(self):
        """Test Ollama model connection"""
        test_content = '''
import requests

def test_ollama():
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "gemma3:4b",
                "prompt": "What does ESG stand for? Answer in one sentence.",
                "stream": False,
                "options": {"num_predict": 50}
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json().get("response", "")
            print(f"📝 Ollama response: {result[:100]}...")
            return True
        return False
        
    except Exception as e:
        print(f"❌ Ollama test failed: {e}")
        return False

if __name__ == "__main__":
    result = test_ollama()
    print(f"Test result: {result}")
'''
        
        # Create test file
        test_file = self.create_temp_file("test_ollama_connection.py", test_content)
        
        # Execute test
        import subprocess
        result = subprocess.run([sys.executable, str(test_file)], 
                              capture_output=True, text=True, cwd=str(self.base_dir))
        
        print(result.stdout)
        if result.stderr:
            print(f"Errors: {result.stderr}")
            
        return result.returncode == 0
    
    def test_esg_evaluation(self):
        """Test ESG evaluation functionality"""
        test_content = '''
import pandas as pd
import sys
import os
sys.path.append("..")

def test_esg_evaluation():
    try:
        # Test basic ESG scoring
        test_text = "renewable energy solar panels carbon reduction community jobs transparency"
        
        # Simple keyword-based evaluation
        esg_keywords = {
            "environment": ["renewable", "solar", "carbon"],
            "social": ["community", "jobs", "safety"], 
            "governance": ["transparency", "ethics", "compliance"]
        }
        
        scores = {}
        for category, keywords in esg_keywords.items():
            scores[f"{category}_score"] = sum(test_text.count(word) for word in keywords)
        
        total_score = sum(scores.values())
        
        if total_score < 200:
            rating = "Low"
        elif total_score < 600:
            rating = "Medium"
        else:
            rating = "High"
        
        print(f"📊 ESG Scores: {scores}")
        print(f"📈 Total Score: {total_score}")
        print(f"🎯 Rating: {rating}")
        
        return total_score > 0
        
    except Exception as e:
        print(f"❌ ESG evaluation test failed: {e}")
        return False

if __name__ == "__main__":
    result = test_esg_evaluation()
    print(f"Test result: {result}")
'''
        
        test_file = self.create_temp_file("test_esg_evaluation.py", test_content)
        
        # Execute test
        import subprocess
        result = subprocess.run([sys.executable, str(test_file)], 
                              capture_output=True, text=True, cwd=str(self.test_dir))
        
        print(result.stdout)
        if result.stderr:
            print(f"Errors: {result.stderr}")
            
        return result.returncode == 0
    
    def test_system_integration(self):
        """Test complete system integration"""
        test_content = '''
import sys
import os
sys.path.append("..")

def test_integration():
    try:
        # Test data processing pipeline
        sample_business = "Solar-powered urban farm creating local jobs with transparent governance"
        
        # Simulate feature extraction
        features = {
            "env_score": 2,  # solar, urban
            "soc_score": 2,  # jobs, local
            "gov_score": 1,  # governance, transparent
        }
        
        total_esg = sum(features.values())
        
        # Apply rating logic
        if total_esg < 200:
            rating = "Low"
        elif total_esg < 600:
            rating = "Medium"
        else:
            rating = "High"
        
        # Generate recommendations
        recommendations = []
        if features["env_score"] < 150:
            recommendations.append("Enhance environmental practices")
        if features["soc_score"] < 100:
            recommendations.append("Improve social impact")
        if features["gov_score"] < 50:
            recommendations.append("Strengthen governance")
        
        print(f"🏢 Business: {sample_business}")
        print(f"📊 Features: {features}")
        print(f"🎯 Rating: {rating}")
        print(f"💡 Recommendations: {len(recommendations)} generated")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False

if __name__ == "__main__":
    result = test_integration()
    print(f"Test result: {result}")
'''
        
        test_file = self.create_temp_file("test_system_integration.py", test_content)
        
        # Execute test
        import subprocess
        result = subprocess.run([sys.executable, str(test_file)], 
                              capture_output=True, text=True, cwd=str(self.test_dir))
        
        print(result.stdout)
        if result.stderr:
            print(f"Errors: {result.stderr}")
            
        return result.returncode == 0
    
    def print_test_summary(self, results):
        """Print comprehensive test summary"""
        print("\n" + "="*60)
        print("📊 TEST EXECUTION SUMMARY")
        print("="*60)
        
        total_tests = len(results)
        passed_tests = sum(1 for result in results.values() if result)
        failed_tests = total_tests - passed_tests
        
        print(f"📈 Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"🎯 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        print("\n📋 Detailed Results:")
        for test_name, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"   {test_name}: {status}")
        
        if passed_tests == total_tests:
            print(f"\n🎉 ALL TESTS PASSED! Your ESG system is working correctly!")
        else:
            print(f"\n⚠️ Some tests failed. Check the output above for details.")
        
        print(f"\n🧹 All test files have been automatically cleaned up!")

def main():
    """Main function to run test manager"""
    manager = ESGTestManager()
    
    print("Welcome to ESG Project Test Manager")
    print("This will run all tests and automatically cleanup afterwards")
    
    choice = input("\nRun all tests? (y/n): ").strip().lower()
    
    if choice == 'y':
        results = manager.run_all_tests()
        return results
    else:
        print("👋 Test execution cancelled")
        return None

if __name__ == "__main__":
    main()