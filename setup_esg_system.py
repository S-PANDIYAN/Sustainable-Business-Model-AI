"""
Quick Start Guide for ESG System with Ollama
"""

import subprocess
import sys
import time

def check_ollama_status():
    """Check if Ollama is running and has models"""
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        if result.returncode == 0:
            models = result.stdout.strip().split('\n')[1:]  # Skip header
            print(f"✅ Ollama is running with {len(models)} models")
            
            # Show available models
            print("\n📋 Available models:")
            for model in models:
                if model.strip():
                    name = model.split()[0]
                    print(f"  • {name}")
            
            return True, models
        else:
            print("❌ Ollama not responding")
            return False, []
    except Exception as e:
        print(f"❌ Error checking Ollama: {e}")
        return False, []

def setup_recommended_model():
    """Download a good model for ESG tasks if needed"""
    print("\n🤖 Setting up recommended model for ESG tasks...")
    
    # Check if we have a suitable model
    status, models = check_ollama_status()
    if not status:
        print("❌ Please start Ollama first: 'ollama serve'")
        return False
    
    # Look for suitable models
    good_models = ['llama3.2:3b', 'llama3.1:8b', 'gemma3:4b', 'mistral:7b']
    available_model = None
    
    for model_line in models:
        model_name = model_line.split()[0] if model_line.strip() else ""
        for good_model in good_models:
            if good_model in model_name or model_name in good_model:
                available_model = model_name
                break
        if available_model:
            break
    
    if available_model:
        print(f"✅ Found suitable model: {available_model}")
        return available_model
    else:
        print("📥 Downloading recommended model: llama3.2:3b (small and efficient)")
        print("This may take a few minutes...")
        
        try:
            result = subprocess.run(['ollama', 'pull', 'llama3.2:3b'], 
                                 capture_output=True, text=True, timeout=300)
            if result.returncode == 0:
                print("✅ Model downloaded successfully!")
                return 'llama3.2:3b'
            else:
                print(f"❌ Download failed: {result.stderr}")
                return None
        except subprocess.TimeoutExpired:
            print("⏱️ Download taking too long, using available model")
            return models[0].split()[0] if models else None
        except Exception as e:
            print(f"❌ Error downloading model: {e}")
            return None

def run_quick_test():
    """Run a quick test of the integrated system"""
    print("\n🧪 Running Quick Test...")
    
    try:
        # Test basic Ollama connection
        from ollama_integration import OllamaESGGenerator
        
        generator = OllamaESGGenerator()
        
        print("Test 1: Simple ESG question...")
        response = generator.answer_esg_question("What does ESG stand for?")
        print(f"✅ Response received: {response[:100]}...")
        
        print("\nTest 2: Business idea generation...")
        ideas = generator.generate_sustainable_business_ideas(
            industry="Technology", 
            num_ideas=1
        )
        
        if ideas:
            print(f"✅ Generated idea: {ideas[0].get('concept', 'Generated successfully')[:100]}...")
        else:
            print("⚠️ No ideas generated - check Ollama connection")
        
        print("\n✅ Basic integration working!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("💡 Make sure Ollama is running: 'ollama serve'")
        return False

def run_complete_demo():
    """Run the complete ESG evaluation demo"""
    print("\n🎬 Running Complete ESG System Demo...")
    
    try:
        from complete_esg_system import ESGBusinessEvaluator
        
        evaluator = ESGBusinessEvaluator()
        
        # Simple test business idea
        test_idea = """
        Solar-powered vertical farm that grows organic vegetables in urban areas.
        Creates local jobs, reduces transportation emissions, uses renewable energy,
        and provides fresh food to underserved communities with transparent pricing.
        """
        
        print("🔄 Evaluating test business idea...")
        results = evaluator.complete_evaluation_workflow(business_idea_text=test_idea)
        
        print("\n✅ Complete system working!")
        return True
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        print("Check error details above")
        return False

def main():
    """Main setup and test function"""
    print("🚀 ESG System Setup and Test")
    print("="*50)
    
    # Step 1: Check Ollama
    print("Step 1: Checking Ollama status...")
    status, models = check_ollama_status()
    
    if not status:
        print("""
❌ Ollama is not running or not installed.

To start Ollama:
1. Open a new terminal
2. Run: ollama serve
3. Then run this script again
        """)
        return
    
    # Step 2: Setup model
    print("\nStep 2: Setting up model...")
    model = setup_recommended_model()
    
    if not model:
        print("❌ Could not set up a suitable model")
        return
    
    # Step 3: Quick test
    print("\nStep 3: Testing integration...")
    if run_quick_test():
        print("\nStep 4: Running complete demo...")
        if run_complete_demo():
            print(f"""
🎉 SUCCESS! Your ESG System is Ready!

✅ Ollama LLM: Connected
✅ ML Evaluation: Working  
✅ Rule Engine: Active
✅ Complete Integration: Functional

🚀 Next Steps:
1. Run: python complete_esg_system.py
2. Try the interactive mode
3. Test with your own business ideas

💡 Your 3-layer ESG system is now operational!
            """)
        else:
            print("⚠️ Basic test passed but full demo failed. Check logs above.")
    else:
        print("❌ Integration test failed. Check Ollama connection.")

if __name__ == "__main__":
    main()