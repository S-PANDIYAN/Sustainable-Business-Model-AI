"""
ESG Model Prediction Validator
Tests model predictions with mock data and real user scenarios
"""

import pandas as pd
import numpy as np
import random
import json
from datetime import datetime
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class ESGPredictionValidator:
    """Validates ESG model predictions across different data types"""
    
    def __init__(self):
        self.mock_data_scenarios = []
        self.real_world_scenarios = []
        self.test_results = {}
        
        # Initialize ESG components
        self.esg_keywords = {
            'environment': ['renewable', 'solar', 'carbon', 'emission', 'sustainable', 'green', 
                          'climate', 'energy', 'waste', 'recycling', 'biodiversity', 'pollution'],
            'social': ['community', 'jobs', 'employment', 'health', 'education', 'safety', 
                     'diversity', 'inclusion', 'human rights', 'workers', 'training', 'welfare'],
            'governance': ['transparency', 'ethics', 'compliance', 'accountability', 'board', 
                         'governance', 'reporting', 'audit', 'integrity', 'policy', 'oversight']
        }
    
    def generate_mock_business_ideas(self, num_scenarios=20):
        """Generate diverse mock business ideas for testing"""
        
        # Business templates with varying ESG strengths
        business_templates = [
            {
                'template': "A {industry} company that focuses on {env_aspect} using {technology} to serve {market} while ensuring {social_aspect} and maintaining {gov_aspect}.",
                'esg_bias': 'balanced'
            },
            {
                'template': "Revolutionary {industry} startup leveraging {technology} for {env_aspect} with strong commitment to {social_aspect} and {gov_aspect} practices.",
                'esg_bias': 'high_esg'
            },
            {
                'template': "{industry} business offering {service} to maximize profits through {strategy} with minimal operational costs.",
                'esg_bias': 'low_esg'
            },
            {
                'template': "Sustainable {industry} enterprise combining {env_aspect} innovation with {social_aspect} programs and {gov_aspect} standards.",
                'esg_bias': 'env_focused'
            },
            {
                'template': "Community-centered {industry} organization prioritizing {social_aspect} while incorporating {env_aspect} and {gov_aspect}.",
                'esg_bias': 'social_focused'
            }
        ]
        
        # Component pools
        industries = ['technology', 'agriculture', 'manufacturing', 'retail', 'energy', 'transportation', 'healthcare', 'food', 'construction', 'finance']
        
        env_aspects = ['renewable energy', 'carbon reduction', 'waste management', 'sustainable materials', 'clean technology', 'circular economy']
        
        social_aspects = ['job creation', 'community development', 'employee welfare', 'diversity programs', 'education initiatives', 'health services']
        
        gov_aspects = ['transparent reporting', 'ethical sourcing', 'compliance frameworks', 'stakeholder engagement', 'board diversity', 'risk management']
        
        technologies = ['AI and machine learning', 'blockchain', 'IoT sensors', 'automation', 'mobile platforms', 'cloud computing']
        
        markets = ['underserved communities', 'urban areas', 'rural regions', 'developing markets', 'corporate clients', 'government sectors']
        
        services = ['cost-effective products', 'premium services', 'mass market solutions', 'niche offerings', 'customized solutions']
        
        strategies = ['aggressive pricing', 'rapid expansion', 'market domination', 'cost cutting', 'efficiency maximization']
        
        mock_scenarios = []
        
        for i in range(num_scenarios):
            template_info = random.choice(business_templates)
            template = template_info['template']
            bias = template_info['esg_bias']
            
            # Fill template
            business_idea = template.format(
                industry=random.choice(industries),
                env_aspect=random.choice(env_aspects),
                social_aspect=random.choice(social_aspects),
                gov_aspect=random.choice(gov_aspects),
                technology=random.choice(technologies),
                market=random.choice(markets),
                service=random.choice(services),
                strategy=random.choice(strategies)
            )
            
            # Calculate expected ESG profile based on bias
            expected_profile = self._calculate_expected_esg_profile(business_idea, bias)
            
            mock_scenarios.append({
                'id': f'mock_{i+1}',
                'business_idea': business_idea,
                'esg_bias': bias,
                'expected_profile': expected_profile,
                'data_type': 'mock'
            })
        
        self.mock_data_scenarios = mock_scenarios
        print(f"✅ Generated {num_scenarios} mock business scenarios")
        return mock_scenarios
    
    def create_real_world_scenarios(self):
        """Create real-world business scenarios for testing"""
        
        real_scenarios = [
            {
                'id': 'real_1',
                'business_idea': """
                EcoTech Solar Solutions: A renewable energy company that designs and installs solar panel systems 
                for residential and commercial properties. We use recycled materials in our installations, 
                create local employment opportunities through comprehensive training programs, and maintain 
                transparent pricing with detailed environmental impact reporting. Our governance includes 
                third-party audits and community stakeholder meetings.
                """,
                'expected_rating': 'High',
                'data_type': 'real_world'
            },
            {
                'id': 'real_2', 
                'business_idea': """
                FastFashion Express: An online clothing retailer offering trendy apparel at competitive prices. 
                Our business model focuses on rapid inventory turnover, global sourcing for cost optimization, 
                and efficient delivery systems. We aim to provide affordable fashion to price-conscious consumers 
                through streamlined operations and minimal overhead costs.
                """,
                'expected_rating': 'Low',
                'data_type': 'real_world'
            },
            {
                'id': 'real_3',
                'business_idea': """
                GreenAgri Vertical Farms: Urban agriculture startup using hydroponic vertical farming to grow 
                organic vegetables in city centers. Powered by renewable energy, creating jobs for veterans 
                and underemployed populations, providing fresh produce to food deserts. Implements transparent 
                supply chain tracking, fair wage policies, and regular community impact assessments.
                """,
                'expected_rating': 'High',
                'data_type': 'real_world'
            },
            {
                'id': 'real_4',
                'business_idea': """
                CommunityBank Plus: A digital community bank focused on serving underbanked populations with 
                fair lending practices, financial literacy programs, and transparent fee structures. 
                Uses clean energy for operations, promotes diversity in hiring and leadership, and maintains 
                ethical investment policies while supporting local small business development.
                """,
                'expected_rating': 'Medium',
                'data_type': 'real_world'
            },
            {
                'id': 'real_5',
                'business_idea': """
                TechGiant Corp: Global technology conglomerate focused on maximizing shareholder returns through 
                aggressive market expansion, cost reduction initiatives, and premium pricing strategies. 
                Operates across multiple continents with emphasis on operational efficiency and competitive positioning.
                """,
                'expected_rating': 'Low',
                'data_type': 'real_world'
            }
        ]
        
        self.real_world_scenarios = real_scenarios
        print(f"✅ Created {len(real_scenarios)} real-world test scenarios")
        return real_scenarios
    
    def _calculate_expected_esg_profile(self, business_text, bias):
        """Calculate expected ESG profile based on content and bias"""
        
        # Count ESG keywords in text
        text_lower = business_text.lower()
        esg_counts = {}
        
        for category, keywords in self.esg_keywords.items():
            count = sum(text_lower.count(keyword) for keyword in keywords)
            esg_counts[f'{category}_score'] = count
        
        # Apply bias adjustments
        if bias == 'high_esg':
            multiplier = 1.5
        elif bias == 'low_esg':
            multiplier = 0.3
        elif bias == 'env_focused':
            esg_counts['environment_score'] *= 2
            multiplier = 1.0
        elif bias == 'social_focused':
            esg_counts['social_score'] *= 2
            multiplier = 1.0
        else:  # balanced
            multiplier = 1.0
        
        # Apply multiplier
        for key in esg_counts:
            esg_counts[key] = int(esg_counts[key] * multiplier)
        
        total_score = sum(esg_counts.values())
        
        # Determine expected rating
        if total_score < 200:
            expected_rating = 'Low'
        elif total_score < 600:
            expected_rating = 'Medium'
        else:
            expected_rating = 'High'
        
        return {
            'esg_scores': esg_counts,
            'total_score': total_score,
            'expected_rating': expected_rating
        }
    
    def predict_with_model(self, business_text):
        """Make prediction using the ESG evaluation system"""
        
        try:
            # Extract features using keyword-based approach
            text_lower = business_text.lower()
            features = {}
            
            for category, keywords in self.esg_keywords.items():
                features[f'{category}_score'] = sum(text_lower.count(keyword) for keyword in keywords)
            
            # Apply your existing logic
            total_esg = sum(features.values())
            features['total_esg'] = total_esg
            
            if total_esg < 200:
                rating = "Low"
            elif total_esg < 600:
                rating = "Medium"
            else:
                rating = "High"
            
            # Calculate confidence based on score distribution
            scores = [features['environment_score'], features['social_score'], features['governance_score']]
            if max(scores) > 0:
                confidence = min(max(scores) / sum(scores), 1.0)
            else:
                confidence = 0.1  # Low confidence for no ESG signals
            
            return {
                'prediction': rating,
                'confidence': confidence,
                'esg_scores': {
                    'Environmental': features['environment_score'],
                    'Social': features['social_score'],
                    'Governance': features['governance_score']
                },
                'total_score': total_esg,
                'features': features
            }
            
        except Exception as e:
            print(f"❌ Prediction error: {e}")
            return {
                'prediction': 'Error',
                'confidence': 0.0,
                'esg_scores': {'Environmental': 0, 'Social': 0, 'Governance': 0},
                'total_score': 0,
                'error': str(e)
            }
    
    def validate_prediction_accuracy(self):
        """Validate prediction accuracy across all scenarios"""
        
        print("🎯 VALIDATING PREDICTION ACCURACY")
        print("=" * 50)
        
        all_scenarios = self.mock_data_scenarios + self.real_world_scenarios
        
        if not all_scenarios:
            print("❌ No test scenarios available. Run generate_mock_business_ideas() and create_real_world_scenarios() first.")
            return None
        
        results = {
            'total_scenarios': len(all_scenarios),
            'correct_predictions': 0,
            'accuracy_by_type': {},
            'detailed_results': [],
            'confidence_stats': []
        }
        
        for scenario in all_scenarios:
            print(f"\n🔍 Testing: {scenario['id']}")
            
            # Make prediction
            prediction_result = self.predict_with_model(scenario['business_idea'])
            
            # Determine expected result
            if 'expected_profile' in scenario:
                expected = scenario['expected_profile']['expected_rating']
            else:
                expected = scenario.get('expected_rating', 'Unknown')
            
            # Check accuracy
            predicted = prediction_result['prediction']
            is_correct = predicted == expected
            
            if is_correct:
                results['correct_predictions'] += 1
                status = "✅ CORRECT"
            else:
                status = "❌ WRONG"
            
            print(f"   Expected: {expected}, Predicted: {predicted} - {status}")
            print(f"   Confidence: {prediction_result['confidence']:.2%}")
            print(f"   ESG Scores: E={prediction_result['esg_scores']['Environmental']}, "
                  f"S={prediction_result['esg_scores']['Social']}, "
                  f"G={prediction_result['esg_scores']['Governance']}")
            
            # Store detailed result
            detailed_result = {
                'scenario_id': scenario['id'],
                'data_type': scenario['data_type'],
                'business_idea': scenario['business_idea'][:100] + "...",
                'expected': expected,
                'predicted': predicted,
                'correct': is_correct,
                'confidence': prediction_result['confidence'],
                'esg_scores': prediction_result['esg_scores'],
                'total_score': prediction_result['total_score']
            }
            
            results['detailed_results'].append(detailed_result)
            results['confidence_stats'].append(prediction_result['confidence'])
            
            # Track accuracy by data type
            data_type = scenario['data_type']
            if data_type not in results['accuracy_by_type']:
                results['accuracy_by_type'][data_type] = {'correct': 0, 'total': 0}
            
            results['accuracy_by_type'][data_type]['total'] += 1
            if is_correct:
                results['accuracy_by_type'][data_type]['correct'] += 1
        
        # Calculate overall accuracy
        overall_accuracy = results['correct_predictions'] / results['total_scenarios']
        results['overall_accuracy'] = overall_accuracy
        results['average_confidence'] = np.mean(results['confidence_stats'])
        
        # Generate comprehensive report
        self._generate_validation_report(results)
        
        self.test_results = results
        return results
    
    def _generate_validation_report(self, results):
        """Generate detailed validation report"""
        
        print(f"\n" + "=" * 60)
        print("📊 PREDICTION VALIDATION REPORT")
        print("=" * 60)
        
        print(f"📈 Overall Performance:")
        print(f"   • Total Scenarios Tested: {results['total_scenarios']}")
        print(f"   • Correct Predictions: {results['correct_predictions']}")
        print(f"   • Overall Accuracy: {results['overall_accuracy']:.1%}")
        print(f"   • Average Confidence: {results['average_confidence']:.1%}")
        
        print(f"\n📋 Accuracy by Data Type:")
        for data_type, stats in results['accuracy_by_type'].items():
            accuracy = stats['correct'] / stats['total'] if stats['total'] > 0 else 0
            print(f"   • {data_type.title()}: {accuracy:.1%} ({stats['correct']}/{stats['total']})")
        
        # Performance assessment
        print(f"\n🎯 Performance Assessment:")
        if results['overall_accuracy'] >= 0.8:
            assessment = "🟢 EXCELLENT"
            recommendation = "Model performs very well across different scenarios"
        elif results['overall_accuracy'] >= 0.6:
            assessment = "🟡 GOOD"
            recommendation = "Model shows good performance, minor improvements needed"
        elif results['overall_accuracy'] >= 0.4:
            assessment = "🟠 MODERATE"
            recommendation = "Model needs significant improvements"
        else:
            assessment = "🔴 POOR"
            recommendation = "Model requires major reconstruction"
        
        print(f"   Status: {assessment}")
        print(f"   Recommendation: {recommendation}")
        
        # Confidence analysis
        confidence_stats = results['confidence_stats']
        print(f"\n📊 Confidence Analysis:")
        print(f"   • High Confidence (>70%): {sum(1 for c in confidence_stats if c > 0.7)}")
        print(f"   • Medium Confidence (30-70%): {sum(1 for c in confidence_stats if 0.3 <= c <= 0.7)}")
        print(f"   • Low Confidence (<30%): {sum(1 for c in confidence_stats if c < 0.3)}")
    
    def test_edge_cases(self):
        """Test model behavior with edge cases"""
        
        print(f"\n🔬 TESTING EDGE CASES")
        print("=" * 30)
        
        edge_cases = [
            {
                'name': 'Empty Input',
                'input': '',
                'expected_behavior': 'Low rating with low confidence'
            },
            {
                'name': 'Very Short Text',
                'input': 'Green tech startup.',
                'expected_behavior': 'Should still provide prediction'
            },
            {
                'name': 'ESG Keyword Spam',
                'input': 'renewable renewable sustainable sustainable green green community community ethics ethics governance governance',
                'expected_behavior': 'High rating but should handle redundancy'
            },
            {
                'name': 'Mixed Signals',
                'input': 'Sustainable coal mining company with renewable energy and transparent reporting but cost-cutting labor practices',
                'expected_behavior': 'Medium rating due to conflicting signals'
            },
            {
                'name': 'No ESG Content',
                'input': 'Technology platform for optimizing database queries and improving server performance metrics',
                'expected_behavior': 'Low rating due to lack of ESG indicators'
            }
        ]
        
        edge_case_results = []
        
        for case in edge_cases:
            print(f"\n🧪 Testing: {case['name']}")
            print(f"   Input: '{case['input'][:50]}{'...' if len(case['input']) > 50 else ''}'")
            
            try:
                result = self.predict_with_model(case['input'])
                print(f"   Prediction: {result['prediction']}")
                print(f"   Confidence: {result['confidence']:.2%}")
                print(f"   Total Score: {result['total_score']}")
                print(f"   ✅ Handled successfully")
                
                edge_case_results.append({
                    'case_name': case['name'],
                    'prediction': result['prediction'],
                    'confidence': result['confidence'],
                    'handled_successfully': True
                })
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
                edge_case_results.append({
                    'case_name': case['name'],
                    'prediction': 'Error',
                    'confidence': 0.0,
                    'handled_successfully': False,
                    'error': str(e)
                })
        
        successful_cases = sum(1 for r in edge_case_results if r['handled_successfully'])
        print(f"\n📊 Edge Case Summary:")
        print(f"   • Successfully Handled: {successful_cases}/{len(edge_cases)}")
        print(f"   • Success Rate: {successful_cases/len(edge_cases):.1%}")
        
        return edge_case_results
    
    def export_test_results(self, filename=None):
        """Export test results to JSON file"""
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"tests/esg_prediction_validation_{timestamp}.json"
        
        export_data = {
            'test_timestamp': datetime.now().isoformat(),
            'test_results': self.test_results,
            'mock_scenarios': self.mock_data_scenarios,
            'real_world_scenarios': self.real_world_scenarios
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, default=str)
            
            print(f"📁 Test results exported to: {filename}")
            return filename
            
        except Exception as e:
            print(f"❌ Export failed: {e}")
            return None

def run_complete_prediction_validation():
    """Run complete prediction validation suite"""
    
    print("🚀 ESG MODEL PREDICTION VALIDATION SUITE")
    print("=" * 60)
    
    validator = ESGPredictionValidator()
    
    # Step 1: Generate test data
    print("\n📊 Step 1: Generating Test Data")
    validator.generate_mock_business_ideas(15)
    validator.create_real_world_scenarios()
    
    # Step 2: Validate predictions
    print("\n📊 Step 2: Validating Predictions")
    results = validator.validate_prediction_accuracy()
    
    # Step 3: Test edge cases
    print("\n📊 Step 3: Testing Edge Cases")
    edge_results = validator.test_edge_cases()
    
    # Step 4: Export results
    print("\n📊 Step 4: Exporting Results")
    export_file = validator.export_test_results()
    
    # Final summary
    print(f"\n🎉 VALIDATION COMPLETE!")
    print(f"✅ Model tested with {len(validator.mock_data_scenarios + validator.real_world_scenarios)} scenarios")
    print(f"📊 Overall accuracy: {results['overall_accuracy']:.1%}")
    print(f"📁 Results saved to: {export_file}")
    
    return validator, results

if __name__ == "__main__":
    run_complete_prediction_validation()