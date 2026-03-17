import re

from typing import List, Dict, Union, Any

# Predefined skills mapping for extraction
AVAILABLE_SKILLS: List[str] = [
    'Python', 'Java', 'C++', 'JavaScript', 'HTML', 'CSS', 'React', 'Angular', 
    'Vue', 'Node.js', 'Express', 'Django', 'Flask', 'Spring Boot', 'SQL', 
    'MySQL', 'PostgreSQL', 'MongoDB', 'Docker', 'Kubernetes', 'AWS', 'Azure', 
    'GCP', 'Git', 'Machine Learning', 'Data Science', 'Pandas', 'NumPy', 'TensorFlow'
]

# Rule-based recommendations
RECOMMENDATION_RULES: List[Dict[str, Any]] = [
    {
        'role': 'Backend Developer Intern',
        'required_skills': ['Python', 'Flask', 'Django', 'Java', 'Spring Boot', 'Node.js', 'SQL', 'MongoDB'],
        'threshold': 2 # Minimum matched skills to suggest role
    },
    {
        'role': 'Frontend Developer Intern',
        'required_skills': ['HTML', 'CSS', 'JavaScript', 'React', 'Angular', 'Vue'],
        'threshold': 2
    },
    {
        'role': 'Full Stack Developer Intern',
        'required_skills': ['HTML', 'CSS', 'JavaScript', 'Python', 'Java', 'Node.js', 'SQL', 'MongoDB', 'React'],
        'threshold': 4
    },
    {
        'role': 'AI/ML Intern',
        'required_skills': ['Python', 'Machine Learning', 'Data Science', 'Pandas', 'NumPy', 'TensorFlow'],
        'threshold': 2
    },
    {
        'role': 'DevOps Intern',
        'required_skills': ['Docker', 'Kubernetes', 'AWS', 'Azure', 'GCP', 'Git', 'Python'],
        'threshold': 2
    }
]

import pdfplumber

def extract_text_from_pdf(file_stream):
    """Extract text from a PDF file stream using pdfplumber."""
    try:
        text = ""
        with pdfplumber.open(file_stream) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        return text
    except Exception as e:
        print(f"Error extracting PDF: {e}")
        return ""

def extract_skills_from_jd(description):
    """Extract skills from a job description based on the predefined list."""
    detected_skills = []
    # Use word boundary and ignore case for matching
    for skill in AVAILABLE_SKILLS:
        # Escape special characters in skill names like C++
        escaped_skill = re.escape(skill)
        if re.search(rf'\b{escaped_skill}\b', description, re.IGNORECASE):
            detected_skills.append(skill)
    return list(set(detected_skills))

def get_recommendations(user_skills: List[str]) -> List[Dict[str, Any]]:
    """Return recommended roles based on user skills."""
    user_skills_lower = [s.lower() for s in user_skills]
    recommendations = []
    
    for rule in RECOMMENDATION_RULES:
        rule_skills = rule.get('required_skills', []) # Ensure list typing
        rule_skills_lower = [str(s).lower() for s in rule_skills]
        # Count overlaps
        matches = len(set(user_skills_lower).intersection(set(rule_skills_lower)))
        threshold = int(rule.get('threshold', 0))
        
        if matches >= threshold:
            # Calculate match percentage
            score = int((matches / len(rule_skills)) * 100) if len(rule_skills) > 0 else 0
            
            # Identify missing skills for this role
            missing = [str(s) for s in rule_skills if str(s).lower() not in user_skills_lower]
            top_missing = missing[:3] if len(missing) >= 3 else missing
            
            recommendations.append({
                'role': str(rule.get('role', '')),
                'matches': matches,
                'score': score,
                'missing_skills': top_missing # Suggest top 3 missing skills
            })
            
    # Sort by score descending
    return sorted(recommendations, key=lambda x: int(x.get('score', 0)), reverse=True)


def calculate_match_score(user_skills: List[str], required_skills: List[str]) -> float:
    if not required_skills:
        return 0.0

    user_skills_lower = [s.lower() for s in user_skills]
    required_skills_lower = [s.lower() for s in required_skills]
    
    matched = set(user_skills_lower).intersection(set(required_skills_lower))
    score = (len(matched) / len(required_skills)) * 100.0
    return round(score, 2)

def generate_learning_path(missing_skills: List[str]) -> List[str]:
    """Generate a step-by-step learning path based on missing skills."""
    if not missing_skills:
        return []
        
    path = []
    
    # Generic mapping logic for common skills
    skill_paths = {
        'sql': [
            "Learn basic SQL CRUD operations (SELECT, INSERT, UPDATE, DELETE).",
            "Understand relational database concepts and Practice SQL Joins."
        ],
        'docker': [
            "Learn what containers are and basic Docker commands.",
            "Build a small containerized project (write a Dockerfile)."
        ],
        'python': [
            "Learn basic Python syntax and data structures.",
            "Practice Object-Oriented Programming in Python."
        ],
        'react': [
            "Understand React components and JSX.",
            "Learn React component state and effect hooks."
        ],
        'git': [
            "Learn basic version control concepts.",
            "Practice Git commit, push, pull, and branching workflows."
        ]
    }
    
    for skill in missing_skills:
        skill_lower = str(skill).lower()
        if skill_lower in skill_paths:
            for step in skill_paths[skill_lower]:
                path.append(step)
        else:
            path.append(f"Research and learn the fundamentals of {skill}.")
            path.append(f"Build a small introductory project using {skill}.")
            
    # Deduplicate but preserve order if a step somehow duplicates
    seen = set()
    unique_path = []
    
    current_step = 1
    for step in path:
        if step not in seen:
            seen.add(step)
            unique_path.append(f"Step {current_step}: {step}")
            current_step = current_step + 1
            
    return unique_path
