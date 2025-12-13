import requests
import json
import pandas as pd
import joblib
from typing import Dict, List, Optional

class OllamaESGGenerator:
    """
    Integrates Ollama LLM with your ESG evaluation system
    """
    
    def __init__(self, model_name="gemma3:4b", ollama_url="http://localhost:11434"):
        self.model_name = model_name
        self.ollama_url = ollama_url
        self.esg_context = self._load_esg_context()
        
        # Try to load your trained ESG model
        try:
            self.esg_model = joblib.load("model/sustainbilty.pkl")
            print("✅ ESG evaluation model loaded")
        except:
            print("⚠️ ESG model not found - predictions will use basic rules")
            self.esg_model = None
    
    def _load_esg_context(self):
        """Load ESG context from your documents"""
        return """
        You are an ESG (Environmental, Social, Governance) expert helping evaluate business ideas.
        
        ENVIRONMENTAL criteria include: carbon emissions, renewable energy, waste management, 
        resource efficiency, biodiversity impact, circular economy principles, climate action.
        
        SOCIAL criteria include: job creation, community impact, health & safety, diversity & inclusion,
        fair labor practices, stakeholder engagement, social equity, human rights.
        
        GOVERNANCE criteria include: transparency, ethics, accountability, compliance, risk management,
        board diversity, anti-corruption, stakeholder rights.
        
        UN SDGs focus areas: No poverty, Zero hunger, Good health, Quality education, Gender equality,
        Clean water, Affordable clean energy, Decent work, Industry innovation, Reduced inequalities,
        Sustainable cities, Responsible consumption, Climate action, Life below water, Life on land,
        Peace & justice, Partnerships.
        """
    
    def _call_ollama(self, prompt: str, system_prompt: str = None) -> str:
        """Make API call to local Ollama instance"""
        try:
            # Format the full prompt with system context for Gemma
            full_prompt = f"{system_prompt or self.esg_context}\n\nUser: {prompt}\n\nAssistant:"
            
            payload = {
                "model": self.model_name,
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "num_predict": 500
                }
            }
            
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                return response.json()['response']
            else:
                return f"Error: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Connection error: {str(e)}"
    
    def generate_sustainable_business_ideas(self, industry: str = "", focus_area: str = "", num_ideas: int = 3) -> List[Dict]:
        """
        Generate sustainable business ideas using Ollama
        """
        prompt = f"""
        Generate {num_ideas} innovative and sustainable business ideas that strongly align with ESG principles.
        
        Industry focus: {industry if industry else "Any industry"}
        Special focus: {focus_area if focus_area else "General sustainability"}
        
        For each business idea, provide:
        1. Business Name & Concept (2-3 sentences)
        2. Environmental Impact (how it helps the environment)
        3. Social Impact (how it benefits society)
        4. Governance Approach (ethical business practices)
        5. UN SDG Alignment (which SDGs it addresses)
        
        Make the ideas specific, actionable, and commercially viable.
        
        Format each idea as:
        IDEA #: [Business Name]
        CONCEPT: [Brief description]
        ENVIRONMENTAL: [Environmental benefits]
        SOCIAL: [Social benefits] 
        GOVERNANCE: [Governance practices]
        SDGS: [Relevant SDG numbers and names]
        ---
        """
        
        response = self._call_ollama(prompt)
        
        # Parse the response into structured format
        ideas = []
        sections = response.split('---')
        
        for section in sections:
            if 'IDEA #' in section:
                lines = section.strip().split('\n')
                idea = {
                    'raw_text': section.strip(),
                    'concept': '',
                    'environmental': '',
                    'social': '',
                    'governance': '',
                    'sdgs': ''
                }
                
                for line in lines:
                    if 'CONCEPT:' in line:
                        idea['concept'] = line.split('CONCEPT:', 1)[1].strip()
                    elif 'ENVIRONMENTAL:' in line:
                        idea['environmental'] = line.split('ENVIRONMENTAL:', 1)[1].strip()
                    elif 'SOCIAL:' in line:
                        idea['social'] = line.split('SOCIAL:', 1)[1].strip()
                    elif 'GOVERNANCE:' in line:
                        idea['governance'] = line.split('GOVERNANCE:', 1)[1].strip()
                    elif 'SDGS:' in line:
                        idea['sdgs'] = line.split('SDGS:', 1)[1].strip()
                
                ideas.append(idea)
        
        return ideas
    
    def explain_esg_decision(self, business_idea: str, esg_scores: Dict, sustainability_rating: str) -> str:
        """
        Generate natural language explanation of ESG evaluation
        """
        prompt = f"""
        Explain in simple, clear language why this business idea received the following ESG evaluation:
        
        BUSINESS IDEA: {business_idea}
        
        ESG SCORES:
        - Environmental Score: {esg_scores.get('Environmental', 0)}
        - Social Score: {esg_scores.get('Social', 0)}
        - Governance Score: {esg_scores.get('Governance', 0)}
        
        SUSTAINABILITY RATING: {sustainability_rating}
        
        Provide:
        1. Overall assessment (2-3 sentences)
        2. Strengths in each ESG dimension
        3. Areas for improvement
        4. Specific recommendations to enhance sustainability
        
        Write in a helpful, constructive tone suitable for entrepreneurs and business students.
        """
        
        return self._call_ollama(prompt)
    
    def answer_esg_question(self, question: str) -> str:
        """
        Answer user questions about ESG and sustainability
        """
        prompt = f"""
        Answer this question about ESG (Environmental, Social, Governance) and sustainability:
        
        QUESTION: {question}
        
        Provide a clear, accurate, and educational response. Include practical examples where helpful.
        If the question relates to business sustainability, connect it to real-world applications.
        """
        
        return self._call_ollama(prompt)
    
    def improve_business_idea(self, original_idea: str, weak_areas: List[str]) -> str:
        """
        Generate improved version of business idea addressing weak ESG areas
        """
        prompt = f"""
        Improve this business idea to address the identified weak ESG areas:
        
        ORIGINAL IDEA: {original_idea}
        
        WEAK AREAS TO ADDRESS: {', '.join(weak_areas)}
        
        Provide:
        1. Enhanced business concept that addresses the weak areas
        2. Specific improvements for each weak ESG dimension
        3. New value propositions that emerge from these improvements
        4. Implementation suggestions
        
        Keep the core business concept but make it more sustainable and socially responsible.
        """
        
        return self._call_ollama(prompt)
    
    def create_esg_business_plan_outline(self, business_idea: str) -> str:
        """
        Create ESG-focused business plan outline
        """
        prompt = f"""
        Create a comprehensive business plan outline focused on ESG principles for this idea:
        
        BUSINESS IDEA: {business_idea}
        
        Provide a detailed outline covering:
        1. Executive Summary (ESG-focused)
        2. Market Analysis (sustainability trends)
        3. ESG Impact Strategy
           - Environmental initiatives
           - Social impact programs
           - Governance framework
        4. Financial Projections (including ESG ROI)
        5. Risk Management (ESG risks)
        6. Implementation Timeline
        7. Success Metrics (ESG KPIs)
        
        Make it practical and actionable for entrepreneurs.
        """
        
        return self._call_ollama(prompt)

# Example usage and testing functions
def test_ollama_integration():
    """Test the Ollama integration"""
    generator = OllamaESGGenerator()
    
    print("🧪 Testing Ollama Integration...")
    print("="*50)
    
    # Test 1: Generate business ideas
    print("\n📝 Test 1: Generating sustainable business ideas...")
    ideas = generator.generate_sustainable_business_ideas(
        industry="Technology", 
        focus_area="Climate action",
        num_ideas=2
    )
    
    for i, idea in enumerate(ideas, 1):
        print(f"\n💡 Idea {i}:")
        print(f"Concept: {idea['concept']}")
        print(f"Environmental: {idea['environmental']}")
        print(f"SDGs: {idea['sdgs']}")
    
    # Test 2: Answer ESG question
    print("\n❓ Test 2: Answering ESG question...")
    question = "What makes a business truly sustainable?"
    answer = generator.answer_esg_question(question)
    print(f"Q: {question}")
    print(f"A: {answer}")
    
    # Test 3: Explain ESG decision
    print("\n📊 Test 3: Explaining ESG evaluation...")
    sample_business = "Solar panel recycling company with local job training programs"
    sample_scores = {'Environmental': 85, 'Social': 70, 'Governance': 45}
    explanation = generator.explain_esg_decision(sample_business, sample_scores, "High")
    print(f"Business: {sample_business}")
    print(f"Explanation: {explanation}")

if __name__ == "__main__":
    test_ollama_integration()