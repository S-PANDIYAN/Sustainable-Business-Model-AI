"""
Master Test Runner for ESG Project
Executes all tests and performs complete cleanup
"""

import os
import sys
import shutil
import time
from pathlib import Path
import subprocess

class MasterTestRunner:
    """Coordinates all testing and cleanup operations"""
    
    def __init__(self):
        self.project_root = Path("d:/AI-BSM")
        self.test_dir = self.project_root / "tests"
        self.results = {}
        self.start_time = time.time()
        
    def run_individual_test(self, test_file, test_name):
        """Run a specific test file"""
        print(f"\n🎯 Running {test_name}...")
        print("-" * 40)
        
        test_path = self.test_dir / test_file
        
        if not test_path.exists():
            print(f"❌ Test file not found: {test_file}")
            return False
        
        try:
            # Run the test
            result = subprocess.run(
                [sys.executable, str(test_path)],
                cwd=str(self.project_root),
                capture_output=True,
                text=True,
                timeout=60
            )
            
            print(result.stdout)
            
            if result.stderr:
                print(f"⚠️ Warnings/Errors:")
                print(result.stderr)
            
            success = result.returncode == 0
            
            if success:
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED (Exit code: {result.returncode})")
            
            return success
            
        except subprocess.TimeoutExpired:
            print(f"⏰ {test_name} TIMED OUT")
            return False
        except Exception as e:
            print(f"❌ {test_name} ERROR: {e}")
            return False
    
    def run_all_tests(self):
        """Execute all available tests"""
        print("🚀 ESG PROJECT - MASTER TEST SUITE")
        print("=" * 60)
        
        # List of tests to run
        test_suite = [
            ("test_gemma.py", "Ollama Gemma Model Test"),
            ("test_manager.py", "Comprehensive Test Manager")
        ]
        
        print(f"📋 Found {len(test_suite)} test suites to execute")
        
        # Execute each test
        for test_file, test_name in test_suite:
            self.results[test_name] = self.run_individual_test(test_file, test_name)
        
        # Generate summary
        self.generate_final_report()
        
        # Cleanup
        self.perform_cleanup()
        
        return self.results
    
    def generate_final_report(self):
        """Generate comprehensive test report"""
        print("\n" + "=" * 60)
        print("📊 FINAL TEST EXECUTION REPORT")
        print("=" * 60)
        
        total_tests = len(self.results)
        passed_tests = sum(1 for result in self.results.values() if result)
        failed_tests = total_tests - passed_tests
        
        execution_time = time.time() - self.start_time
        
        print(f"⏱️  Total Execution Time: {execution_time:.2f} seconds")
        print(f"📊 Test Statistics:")
        print(f"   • Total Test Suites: {total_tests}")
        print(f"   • ✅ Passed: {passed_tests}")
        print(f"   • ❌ Failed: {failed_tests}")
        print(f"   • 🎯 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        print(f"\n📋 Detailed Results:")
        for test_name, result in self.results.items():
            status_icon = "✅" if result else "❌"
            status_text = "PASS" if result else "FAIL"
            print(f"   {status_icon} {test_name}: {status_text}")
        
        # Overall assessment
        if passed_tests == total_tests:
            print(f"\n🎉 EXCELLENT! All tests passed successfully!")
            print(f"✅ Your ESG system is fully functional and ready for production")
        elif passed_tests > 0:
            print(f"\n⚠️ Partial Success: {passed_tests}/{total_tests} tests passed")
            print(f"💡 Review failed tests and address any issues")
        else:
            print(f"\n❌ All tests failed - system needs attention")
            print(f"🔧 Check Ollama connection and dependencies")
    
    def perform_cleanup(self):
        """Clean up all temporary test files and artifacts"""
        print(f"\n🧹 PERFORMING CLEANUP...")
        print("-" * 40)
        
        cleanup_items = []
        
        # Find and remove temporary files in test directory
        if self.test_dir.exists():
            for item in self.test_dir.iterdir():
                if item.is_file():
                    # Keep only the main test files, remove temp files
                    if item.name.startswith('test_') and not item.name.endswith('.pyc'):
                        continue  # Keep main test files
                    elif item.name == '__pycache__':
                        continue  # Handle pycache separately
                    else:
                        cleanup_items.append(item)
        
        # Remove __pycache__ directories
        pycache_dirs = list(self.test_dir.rglob('__pycache__'))
        for pycache_dir in pycache_dirs:
            try:
                shutil.rmtree(pycache_dir)
                cleanup_items.append(pycache_dir)
                print(f"🗑️ Removed: {pycache_dir.name}/")
            except Exception as e:
                print(f"⚠️ Could not remove {pycache_dir}: {e}")
        
        # Remove temporary files
        for item in cleanup_items:
            try:
                if item.is_file():
                    item.unlink()
                    print(f"🗑️ Removed: {item.name}")
                elif item.is_dir():
                    shutil.rmtree(item)
                    print(f"🗑️ Removed: {item.name}/")
            except Exception as e:
                print(f"⚠️ Could not remove {item.name}: {e}")
        
        print(f"✅ Cleanup completed! Removed {len(cleanup_items)} items")
        print(f"📁 Test directory preserved with main test files")
    
    def quick_health_check(self):
        """Perform a quick system health check"""
        print("🏥 ESG System Health Check")
        print("-" * 30)
        
        checks = {
            "Ollama Service": self.check_ollama_service(),
            "ESG Data Files": self.check_data_files(),
            "Python Dependencies": self.check_dependencies(),
            "Model Files": self.check_model_files()
        }
        
        for check_name, result in checks.items():
            status = "✅" if result else "❌"
            print(f"{status} {check_name}")
        
        overall_health = sum(checks.values()) / len(checks) * 100
        print(f"\n🎯 Overall System Health: {overall_health:.0f}%")
        
        return checks
    
    def check_ollama_service(self):
        """Check if Ollama is running"""
        try:
            result = subprocess.run(['ollama', 'list'], capture_output=True, timeout=10)
            return result.returncode == 0
        except:
            return False
    
    def check_data_files(self):
        """Check if essential data files exist"""
        essential_files = [
            self.project_root / "data" / "esg_labeled.csv",
            self.project_root / "data" / "esg_features.csv"
        ]
        return all(file.exists() for file in essential_files)
    
    def check_dependencies(self):
        """Check if key Python packages are available"""
        try:
            import pandas
            import requests
            import sklearn
            return True
        except ImportError:
            return False
    
    def check_model_files(self):
        """Check if model files exist"""
        model_files = [
            self.project_root / "model" / "sustainbilty.pkl"
        ]
        return any(file.exists() for file in model_files)

def main():
    """Main execution function"""
    runner = MasterTestRunner()
    
    print("🎯 ESG Project Master Test Runner")
    print("This will execute all tests and perform automatic cleanup")
    
    # Quick health check first
    print("\n🔍 Performing initial health check...")
    health = runner.quick_health_check()
    
    # Ask user if they want to proceed
    proceed = input(f"\n🚀 Proceed with full test execution? (y/n): ").strip().lower()
    
    if proceed == 'y':
        results = runner.run_all_tests()
        
        print(f"\n🎉 Test execution completed!")
        print(f"📁 Test files remain in: {runner.test_dir}")
        print(f"🧹 All temporary artifacts have been cleaned up")
        
        return results
    else:
        print("👋 Test execution cancelled")
        return None

if __name__ == "__main__":
    main()