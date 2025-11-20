import requests
import random

# Generate synthetic data based on your research findings
def generate_synthetic_patients():
    base_url = "http://localhost:8000"
    
    # Demographics from your research
    age_groups = ["18-27", "28-37", "38-47", "48+"]
    age_weights = [0.09, 0.16, 0.26, 0.48]  # From your research
    
    genders = ["Male", "Female"] 
    gender_weights = [0.27, 0.73]  # 73% female from your research
    
    education_levels = ["Primary", "Secondary", "University"]
    education_weights = [0.34, 0.48, 0.09]  # From your research
    
    locations = ["Kiambu Town", "Limuru", "Kirigiti", "Thendigua", "Githiga", "Runda", "Other"]
    
    # Generate 20 synthetic patients
    for i in range(20):
        patient_data = {
            "age_group": random.choices(age_groups, weights=age_weights)[0],
            "gender": random.choices(genders, weights=gender_weights)[0],
            "education": random.choices(education_levels, weights=education_weights)[0],
            "income_level": random.choice(["<11,000", "11,000-20,999", "21,000-30,999"]),
            "location": random.choice(locations),
            # Satisfaction scores based on your research averages with some variation
            "physical_env_score": random.randint(55, 70),  # Around 61.8%
            "technical_quality_score": random.randint(60, 75),  # Around 64.8%
            "interpersonal_score": random.randint(75, 90),  # Around 81.9%
            "communication_score": random.randint(55, 70),  # Around 62.0%
            "accessibility_score": random.randint(55, 70),  # Around 61.4%
        }
        
        try:
            response = requests.post(f"{base_url}/patients/", json=patient_data)
            if response.status_code == 200:
                print(f"Created patient {i+1}")
            else:
                print(f"Failed to create patient {i+1}")
        except:
            print("Backend not running")
            break

if __name__ == "__main__":
    generate_synthetic_patients()