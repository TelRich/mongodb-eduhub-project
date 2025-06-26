"""
Eduhub MongoDB Project - Complete Implementation
Data Engineering - AltSchool Tinyuka 2024 Second Semester Project Exam

This module contains all MongoDB operations for the EduHub e-learning platform.
Author: Goodrich Okoro
Date: June 2025
"""

from pymongo import MongoClient
from datetime import datetime, timedelta
import pandas as pd
import json
import random
import re 

# Real educational data generator class
class EduHubDataGenerator:
    """Generates realistic educational data for the EduHub platform"""
    
    def __init__(self):
        # Real instructor names and their specializations
        self.instructors_data = [
            {"firstName": "Sarah", "lastName": "Johnson", "email": "sarah.johnson@eduhub.com", "specialization": "Data Science", "bio": "PhD in Computer Science with 10+ years experience in machine learning and data analytics. Former Google AI researcher."},
            {"firstName": "Michael", "lastName": "Chen", "email": "michael.chen@eduhub.com", "specialization": "Web Development", "bio": "Full-stack developer and former Facebook engineer with expertise in React, Node.js, and modern web technologies."},
            {"firstName": "Emily", "lastName": "Rodriguez", "email": "emily.rodriguez@eduhub.com", "specialization": "AI/ML", "bio": "AI researcher and Stanford graduate specializing in deep learning, computer vision, and natural language processing."},
            {"firstName": "David", "lastName": "Kumar", "email": "david.kumar@eduhub.com", "specialization": "Cloud Computing", "bio": "AWS Solutions Architect with 8+ years experience in cloud infrastructure, DevOps, and distributed systems."},
            {"firstName": "Lisa", "lastName": "Thompson", "email": "lisa.thompson@eduhub.com", "specialization": "Cybersecurity", "bio": "Cybersecurity expert and ethical hacker with certifications in CISSP, CEH, and extensive experience in security auditing."}
        ]
        
        # Real student names
        self.students_data = [
            {"firstName": "Alex", "lastName": "Williams", "email": "alex.williams@student.com", "interests": ["Python", "Data Analysis", "Statistics"]},
            {"firstName": "Maria", "lastName": "Garcia", "email": "maria.garcia@student.com", "interests": ["JavaScript", "React", "UI/UX"]},
            {"firstName": "James", "lastName": "Brown", "email": "james.brown@student.com", "interests": ["Machine Learning", "Python", "TensorFlow"]},
            {"firstName": "Emma", "lastName": "Davis", "email": "emma.davis@student.com", "interests": ["Web Design", "CSS", "HTML"]},
            {"firstName": "Ryan", "lastName": "Miller", "email": "ryan.miller@student.com", "interests": ["Cloud Computing", "AWS", "Docker"]},
            {"firstName": "Sophia", "lastName": "Wilson", "email": "sophia.wilson@student.com", "interests": ["Data Science", "R", "Visualization"]},
            {"firstName": "Noah", "lastName": "Moore", "email": "noah.moore@student.com", "interests": ["Cybersecurity", "Networking", "Linux"]},
            {"firstName": "Olivia", "lastName": "Taylor", "email": "olivia.taylor@student.com", "interests": ["Mobile Dev", "Flutter", "Android"]},
            {"firstName": "Liam", "lastName": "Anderson", "email": "liam.anderson@student.com", "interests": ["Backend Dev", "APIs", "Databases"]},
            {"firstName": "Ava", "lastName": "Thomas", "email": "ava.thomas@student.com", "interests": ["AI", "Computer Vision", "OpenCV"]},
            {"firstName": "Ethan", "lastName": "Jackson", "email": "ethan.jackson@student.com", "interests": ["DevOps", "Kubernetes", "Jenkins"]},
            {"firstName": "Isabella", "lastName": "White", "email": "isabella.white@student.com", "interests": ["Data Mining", "SQL", "MongoDB"]},
            {"firstName": "Mason", "lastName": "Harris", "email": "mason.harris@student.com", "interests": ["Game Dev", "Unity", "C#"]},
            {"firstName": "Mia", "lastName": "Martin", "email": "mia.martin@student.com", "interests": ["Frontend", "Vue.js", "TypeScript"]},
            {"firstName": "Lucas", "lastName": "Clark", "email": "lucas.clark@student.com", "interests": ["Blockchain", "Ethereum", "Smart Contracts"]}
        ]
        
        # Real course data with proper educational content
        self.courses_data = [
            {
                "title": "Complete Python Programming Bootcamp",
                "description": "Master Python from basics to advanced topics including OOP, web scraping, data analysis, and automation. Build real-world projects and prepare for Python developer roles.",
                "category": "Programming",
                "level": "beginner",
                "duration": 40,
                "price": 199.99,
                "tags": ["python", "programming", "automation", "data-analysis", "web-scraping"]
            },
            {
                "title": "Data Science with Machine Learning",
                "description": "Comprehensive course covering statistics, data visualization, machine learning algorithms, and real-world data science projects using Python and R.",
                "category": "Data Science",
                "level": "intermediate",
                "duration": 60,
                "price": 299.99,
                "tags": ["data-science", "machine-learning", "statistics", "pandas", "scikit-learn"]
            },
            {
                "title": "Full Stack Web Development",
                "description": "Build modern web applications using React, Node.js, Express, and MongoDB. Learn front-end and back-end development with hands-on projects.",
                "category": "Web Development",
                "level": "intermediate",
                "duration": 50,
                "price": 249.99,
                "tags": ["react", "nodejs", "javascript", "mongodb", "full-stack"]
            },
            {
                "title": "Artificial Intelligence Fundamentals",
                "description": "Introduction to AI concepts, neural networks, deep learning, and practical applications. Includes projects in computer vision and natural language processing.",
                "category": "AI/ML",
                "level": "advanced",
                "duration": 45,
                "price": 349.99,
                "tags": ["artificial-intelligence", "deep-learning", "neural-networks", "tensorflow", "computer-vision"]
            },
            {
                "title": "Cloud Computing with AWS",
                "description": "Master Amazon Web Services including EC2, S3, RDS, Lambda, and deployment strategies. Prepare for AWS certification and cloud architect roles.",
                "category": "Cloud Computing",
                "level": "intermediate",
                "duration": 35,
                "price": 279.99,
                "tags": ["aws", "cloud-computing", "ec2", "s3", "lambda", "devops"]
            },
            {
                "title": "Cybersecurity Essentials",
                "description": "Learn network security, ethical hacking, penetration testing, and security best practices. Includes hands-on labs and real-world scenarios.",
                "category": "Cybersecurity",
                "level": "intermediate",
                "duration": 30,
                "price": 229.99,
                "tags": ["cybersecurity", "ethical-hacking", "penetration-testing", "network-security", "kali-linux"]
            },
            {
                "title": "MongoDB Database Mastery",
                "description": "Complete guide to MongoDB including document modeling, queries, aggregation pipelines, indexing, and performance optimization for modern applications.",
                "category": "Database",
                "level": "intermediate",
                "duration": 25,
                "price": 179.99,
                "tags": ["mongodb", "nosql", "database", "aggregation", "indexing"]
            },
            {
                "title": "Mobile App Development with Flutter",
                "description": "Build cross-platform mobile applications using Flutter and Dart. Create iOS and Android apps with a single codebase and deploy to app stores.",
                "category": "Mobile Development",
                "level": "beginner",
                "duration": 38,
                "price": 219.99,
                "tags": ["flutter", "dart", "mobile-development", "ios", "android", "cross-platform"]
            }
        ]
        
        # Real lesson content for different courses
        self.lessons_content = {
            "Programming": [
                "Introduction to Python syntax and variables",
                "Control structures: loops and conditionals",
                "Functions and modules in Python",
                "Object-oriented programming concepts",
                "File handling and exception management"
            ],
            "Data Science": [
                "Statistics fundamentals for data science",
                "Data visualization with matplotlib and seaborn",
                "Pandas for data manipulation and analysis",
                "Machine learning algorithms overview",
                "Model evaluation and validation techniques"
            ],
            "Web Development": [
                "HTML5 and CSS3 fundamentals",
                "JavaScript ES6+ features and syntax",
                "React components and state management",
                "Node.js and Express server development",
                "Database integration and API development"
            ],
            "AI/ML": [
                "Introduction to artificial intelligence",
                "Neural network architecture and training",
                "Deep learning with TensorFlow and Keras",
                "Computer vision and image processing",
                "Natural language processing techniques"
            ],
            "Cloud Computing": [
                "Cloud computing fundamentals and service models",
                "AWS EC2 instances and virtual machines",
                "Storage solutions: S3, EBS, and EFS",
                "Serverless computing with AWS Lambda",
                "DevOps practices and CI/CD pipelines"
            ],
            "Cybersecurity": [
                "Network security principles and protocols",
                "Vulnerability assessment and penetration testing",
                "Cryptography and secure communication",
                "Incident response and forensics",
                "Security policy development and compliance"
            ]
        }
        
        # Real assignment topics
        self.assignment_topics = {
            "Programming": [
                "Build a web scraper for e-commerce data",
                "Create a personal expense tracker application",
                "Develop a REST API for a library management system",
                "Implement data structures and algorithms"
            ],
            "Data Science": [
                "Analyze customer behavior using retail dataset",
                "Build a predictive model for stock prices",
                "Create data visualizations for COVID-19 trends",
                "Perform sentiment analysis on social media data"
            ],
            "Web Development": [
                "Build a responsive e-commerce website",
                "Create a real-time chat application",
                "Develop a task management web app",
                "Build a portfolio website with animations"
            ],
            "AI/ML": [
                "Train an image classification model",
                "Build a chatbot using natural language processing",
                "Create a recommendation system",
                "Develop a computer vision application"
            ]
        }
        
    def get_random_date(self, start_days_ago, end_days_ago=0):
        """Generate a random date between start_days_ago and end_days_ago
        
        Args:
            start_days_ago: Number of days ago for start date (positive for past, negative for future)
            end_days_ago: Number of days ago for end date (positive for past, negative for future)
        """
        start_date = datetime.now() - timedelta(days=start_days_ago)
        end_date = datetime.now() - timedelta(days=end_days_ago)
        time_between = end_date - start_date
        days_between = abs(time_between.days)
        random_days = random.randrange(days_between + 1)
        
        if start_date < end_date:
            return start_date + timedelta(days=random_days)
        else:
            return end_date + timedelta(days=random_days)
        
    def get_avatar_url(self, name):
        """Generate a realistic avatar URL"""
        return f"https://ui-avatars.com/api/?name={name.replace(' ', '+')}&background=random&size=200"
        
    def get_video_url(self, lesson_title):
        """Generate a realistic video URL"""
        return f"https://eduhub-videos.s3.amazonaws.com/{lesson_title.lower().replace(' ', '-')}.mp4"
        
    def get_material_urls(self, count=None):
        """Generate realistic material URLs"""
        if count is None:
            count = random.randint(1, 3)
        materials = [
            "https://eduhub-materials.s3.amazonaws.com/slides.pdf",
            "https://eduhub-materials.s3.amazonaws.com/exercises.pdf",
            "https://eduhub-materials.s3.amazonaws.com/code-examples.zip",
            "https://eduhub-materials.s3.amazonaws.com/reference-guide.pdf",
            "https://eduhub-materials.s3.amazonaws.com/dataset.csv"
        ]
        return random.sample(materials, min(count, len(materials)))

# Initialize the data generator
data_generator = EduHubDataGenerator()

class EduHubDatabase:
    def __init__(self, connection_string="mongodb://localhost:27017/"):
        """
        Initialize the EduHub database connection
        
        Args:
            connection_string (str): MongoDB connection string
        """
        self.client = MongoClient(connection_string)
        self.db = self.client['eduhub_db']
        self.setup_collections()
        
    def setup_collections(self):
        """Set up all collections with validation rules"""
        
        # Users collection validation - Complete schema
        user_validator = {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["userId", "email", "firstName", "lastName", "role"],
                "properties": {
                    "userId": {"bsonType": "string"},
                    "email": {
                        "bsonType": "string",
                        "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
                    },
                    "firstName": {"bsonType": "string"},
                    "lastName": {"bsonType": "string"},
                    "role": {
                        "bsonType": "string",
                        "enum": ["student", "instructor"]
                    },
                    "dateJoined": {"bsonType": "date"},
                    "profile": {
                        "bsonType": "object",
                        "properties": {
                            "bio": {"bsonType": "string"},
                            "avatar": {"bsonType": "string"},
                            "skills": {
                                "bsonType": "array",
                                "items": {"bsonType": "string"}
                            }
                        }
                    },
                    "isActive": {"bsonType": "bool"}
                }
            }
        }
        
        # Courses collection validation - Complete schema
        course_validator = {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["courseId", "title", "instructorId"],
                "properties": {
                    "courseId": {"bsonType": "string"},
                    "title": {"bsonType": "string"},
                    "description": {"bsonType": "string"},
                    "instructorId": {"bsonType": "string"},
                    "category": {"bsonType": "string"},
                    "level": {
                        "bsonType": "string",
                        "enum": ["beginner", "intermediate", "advanced"]
                    },
                    "duration": {"bsonType": "number"},
                    "price": {"bsonType": "number"},
                    "tags": {
                        "bsonType": "array",
                        "items": {"bsonType": "string"}
                    },
                    "createdAt": {"bsonType": "date"},
                    "updatedAt": {"bsonType": "date"},
                    "isPublished": {"bsonType": "bool"},
                    "rating": {"bsonType": "number"}
                }
            }
        }
        
        # Enrollments collection validation
        enrollment_validator = {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["enrollmentId", "studentId", "courseId", "enrollmentDate"],
                "properties": {
                    "enrollmentId": {"bsonType": "string"},
                    "studentId": {"bsonType": "string"},
                    "courseId": {"bsonType": "string"},
                    "enrollmentDate": {"bsonType": "date"},
                    "status": {
                        "bsonType": "string",
                        "enum": ["active", "completed", "dropped"]
                    },
                    "progress": {
                        "bsonType": "number",
                        "minimum": 0,
                        "maximum": 100
                    },
                    "completionDate": {"bsonType": ["date", "null"]}
                }
            }
        }
        
        # Lessons collection validation
        lesson_validator = {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["lessonId", "courseId", "title", "content"],
                "properties": {
                    "lessonId": {"bsonType": "string"},
                    "courseId": {"bsonType": "string"},
                    "title": {"bsonType": "string"},
                    "content": {"bsonType": "string"},
                    "duration": {"bsonType": "number"},
                    "order": {"bsonType": "number"},
                    "videoUrl": {"bsonType": "string"},
                    "materials": {
                        "bsonType": "array",
                        "items": {"bsonType": "string"}
                    },
                    "createdAt": {"bsonType": "date"}
                }
            }
        }
        
        # Assignments collection validation
        assignment_validator = {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["assignmentId", "courseId", "title", "description"],
                "properties": {
                    "assignmentId": {"bsonType": "string"},
                    "courseId": {"bsonType": "string"},
                    "title": {"bsonType": "string"},
                    "description": {"bsonType": "string"},
                    "dueDate": {"bsonType": "date"},
                    "maxPoints": {"bsonType": "number"},
                    "createdAt": {"bsonType": "date"},
                    "instructions": {"bsonType": "string"}
                }
            }
        }
        
        # Submissions collection validation
        submission_validator = {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["submissionId", "assignmentId", "studentId"],
                "properties": {
                    "submissionId": {"bsonType": "string"},
                    "assignmentId": {"bsonType": "string"},
                    "studentId": {"bsonType": "string"},
                    "submissionDate": {"bsonType": "date"},
                    "content": {"bsonType": "string"},
                    "attachments": {
                        "bsonType": "array",
                        "items": {"bsonType": "string"}
                    },
                    "grade": {"bsonType": ["number", "null"]},
                    "feedback": {"bsonType": ["string", "null"]},
                    "gradedDate": {"bsonType": ["date", "null"]}
                }
            }
        }
        
        # Create collections with validation
        validators = {
            "users": user_validator,
            "courses": course_validator,
            "enrollments": enrollment_validator,
            "lessons": lesson_validator,
            "assignments": assignment_validator,
            "submissions": submission_validator
        }
        for collection_name, validator in validators.items():
            try:
                self.db.create_collection(collection_name, validator=validator)
                print(f"✅ Created collection '{collection_name}' with validation")
            except Exception as e:
                if "already exists" in str(e).lower():
                    print(f"ℹ️ Collection '{collection_name}' already exists")
                else:
                    print(f"⚠️ Error creating collection '{collection_name}': {e}")
                pass  # Collection might already exist
        
        # Create indexes for performance
        self.create_indexes()
        
    def create_indexes(self):
        """Create indexes for performance optimization"""
        
        # Users collection indexes
        self.db.users.create_index("userId", unique=True)
        self.db.users.create_index("email", unique=True)
        self.db.users.create_index("role")
        
        # Courses collection indexes
        self.db.courses.create_index("courseId", unique=True)
        self.db.courses.create_index("title")
        self.db.courses.create_index("category")
        self.db.courses.create_index("instructorId")
        self.db.courses.create_index([("title", "text"), ("description", "text")])
        
        # Enrollments collection indexes
        self.db.enrollments.create_index("enrollmentId", unique=True)
        self.db.enrollments.create_index([("studentId", 1), ("courseId", 1)], unique=True)
        self.db.enrollments.create_index("studentId")
        self.db.enrollments.create_index("courseId")
        self.db.enrollments.create_index("enrollmentDate")
        
        # Lessons collection indexes
        self.db.lessons.create_index("lessonId", unique=True)
        self.db.lessons.create_index("courseId")
        self.db.lessons.create_index([("courseId", 1), ("order", 1)])
        
        # Assignments collection indexes
        self.db.assignments.create_index("assignmentId", unique=True)
        self.db.assignments.create_index("courseId")
        self.db.assignments.create_index("dueDate")
        
        # Submissions collection indexes
        self.db.submissions.create_index("submissionId", unique=True)
        self.db.submissions.create_index([("studentId", 1), ("assignmentId", 1)])
        self.db.submissions.create_index("assignmentId")
        self.db.submissions.create_index("studentId")
        
        print("✅ All Indexes created successfully")
        
    # PART 1: DATABASE SETUP AND DATA MODELING

    def get_database_info(self):
        """Get information about the database and collections"""
        info = {
            "database_name": self.db.name,
            "collections": self.db.list_collection_names(),
            "collection_stats": {}
        }
        
        for collection_name in info["collections"]:
            stats = self.db.command("collstats", collection_name)
            info["collection_stats"][collection_name] = {
                "count": stats.get("count", 0),
                "size": stats.get("size", 0),
                "avgObjSize": stats.get("avgObjSize", 0)
            }
            
        return info
    
    # PART 2: DATA POPULATION

    def populate_sample_data(self):
        """Populate the database with comprehensive sample data"""
        
        print("🔄 Starting data population...")
        
        # Clear existing data
        self.clear_all_data()
        
        # Generate users (20 users: 15 students + 5 instructors)
        users = self.generate_sample_users(20)
        self.db.users.insert_many(users)
        print(f"✅ Inserted {len(users)} users")
        
        # Generate courses (8 courses)
        courses = self.generate_sample_courses(8)
        self.db.courses.insert_many(courses)
        print(f"✅ Inserted {len(courses)} courses")
        
        # Generate lessons (25 lessons)
        lessons = self.generate_sample_lessons(25)
        self.db.lessons.insert_many(lessons)
        print(f"✅ Inserted {len(lessons)} lessons")
        
        # Generate assignments (10 assignments)
        assignments = self.generate_sample_assignments(10)
        self.db.assignments.insert_many(assignments)
        print(f"✅ Inserted {len(assignments)} assignments")
        
        # Generate enrollments (15 enrollments)
        enrollments = self.generate_sample_enrollments(15)
        self.db.enrollments.insert_many(enrollments)
        print(f"✅ Inserted {len(enrollments)} enrollments")
        
        # Generate submissions (12 submissions)
        submissions = self.generate_sample_submissions(12)
        self.db.submissions.insert_many(submissions)
        print(f"✅ Inserted {len(submissions)} submissions")
        
        print("🎉 Data population completed successfully!")

    def generate_sample_users(self, count):
        """Generate sample users (mix of students and instructors)"""
        users = []
        
        # Generate instructors using real data
        instructor_count = min(count // 4, len(data_generator.instructors_data))
        for i in range(instructor_count):
            instructor_data = data_generator.instructors_data[i]
            full_name = f"{instructor_data['firstName']} {instructor_data['lastName']}"
            user = {
                "userId": f"IN_{str(i+1).zfill(3)}",
                "email": instructor_data['email'],
                "firstName": instructor_data['firstName'],
                "lastName": instructor_data['lastName'],
                "role": "instructor",
                "dateJoined": data_generator.get_random_date(730, 365),  # 2 years to 1 year ago
                "profile": {
                    "bio": instructor_data['bio'],
                    "avatar": data_generator.get_avatar_url(full_name),
                    "skills": [instructor_data['specialization'], "Teaching", "Curriculum Design", "Mentoring"]
                },
                "isActive": True
            }
            users.append(user)
            
        # Generate students using real data
        student_count = count - instructor_count
        for i in range(student_count):
            if i < len(data_generator.students_data):
                student_data = data_generator.students_data[i]
                full_name = f"{student_data['firstName']} {student_data['lastName']}"
                bio = f"Passionate learner interested in {', '.join(student_data['interests'][:2])} and modern technology."
            else:
                # Generate additional students if needed
                first_names = ["Jordan", "Taylor", "Casey", "Riley", "Morgan", "Avery", "Jamie", "Quinn"]
                last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"]
                interests = ["Programming", "Data Science", "Web Development", "Mobile Development", "AI/ML"]
                
                first_name = random.choice(first_names)
                last_name = random.choice(last_names)
                full_name = f"{first_name} {last_name}"
                student_data = {
                    "firstName": first_name,
                    "lastName": last_name,
                    "email": f"{first_name.lower()}.{last_name.lower()}@student.com",
                    "interests": random.sample(interests, 3)
                }
                bio = f"Student exploring {', '.join(student_data['interests'][:2])} with a focus on practical applications."
            
            user = {
                "userId": f"ST_{str(i+1).zfill(3)}",
                "email": student_data['email'],
                "firstName": student_data['firstName'],
                "lastName": student_data['lastName'],
                "role": "student",
                "dateJoined": data_generator.get_random_date(365, 0),  # Within last year
                "profile": {
                    "bio": bio,
                    "avatar": data_generator.get_avatar_url(full_name),
                    "skills": student_data['interests']
                },
                "isActive": True
            }
            users.append(user)
        
        return users
    
    def generate_sample_courses(self, count):
        """Generate sample courses using realistic educational data"""
        instructors = list(self.db.users.find({"role": "instructor"}))
        
        courses = []
        for i in range(min(count, len(data_generator.courses_data))):
            course_data = data_generator.courses_data[i]
            
            # Match instructor specialization with course category when possible
            suitable_instructor = None
            for instructor in instructors:
                instructor_specialization = instructor.get("profile", {}).get("skills", [])[0] if instructor.get("profile", {}).get("skills") else ""
                if course_data["category"] in instructor_specialization or instructor_specialization in course_data["category"]:
                    suitable_instructor = instructor
                    break
            
            if not suitable_instructor:
                suitable_instructor = random.choice(instructors)
            
            course = {
                "courseId": f"CO_{str(i+1).zfill(3)}",
                "title": course_data["title"],
                "description": course_data["description"],
                "instructorId": suitable_instructor["userId"],
                "category": course_data["category"],
                "level": course_data["level"],
                "duration": course_data["duration"],
                "price": course_data["price"],
                "tags": course_data["tags"],
                "createdAt": data_generator.get_random_date(180, 30),  # 6 months to 1 month ago
                "updatedAt": data_generator.get_random_date(30, 0),    # Within last month
                "isPublished": random.choice([True, True, True, False]),  # 75% published
                "rating": round(random.uniform(3.5, 5.0), 1)  # Higher ratings for realistic courses
            }
            courses.append(course)
            
        return courses
    
    def generate_sample_lessons(self, count):
        """Generate sample lessons with realistic educational content"""
        courses = list(self.db.courses.find())
        lessons = []
        
        lessons_per_course = count // len(courses) if courses else 1
        lesson_counter = 0
        
        for course in courses:
            course_category = course.get("category", "Programming")
            
            # Get lesson content for this category
            category_lessons = data_generator.lessons_content.get(course_category, 
                                                                data_generator.lessons_content["Programming"])
            
            # Generate lessons for this course
            course_lessons_count = min(lessons_per_course, len(category_lessons))
            for i in range(course_lessons_count):
                if lesson_counter >= count:
                    break
                    
                lesson_title = category_lessons[i]
                lesson_content = self._generate_lesson_content(lesson_title, course_category)
                
                lesson = {
                    "lessonId": f"LE_{str(lesson_counter+1).zfill(3)}",
                    "courseId": course["courseId"],
                    "title": lesson_title,
                    "content": lesson_content,
                    "duration": random.randint(20, 45),  # Realistic lesson duration
                    "order": i + 1,
                    "videoUrl": data_generator.get_video_url(lesson_title),
                    "materials": data_generator.get_material_urls(random.randint(1, 3)),
                    "createdAt": data_generator.get_random_date(90, 0)  # Within last 3 months
                }
                lessons.append(lesson)
                lesson_counter += 1
        
        # Fill remaining lessons if needed
        while lesson_counter < count and courses:
            course = random.choice(courses)
            course_category = course.get("category", "Programming")
            category_lessons = data_generator.lessons_content.get(course_category, 
                                                                data_generator.lessons_content["Programming"])
            
            lesson_title = random.choice(category_lessons)
            lesson_content = self._generate_lesson_content(lesson_title, course_category)
            
            lesson = {
                "lessonId": f"LE_{str(lesson_counter+1).zfill(3)}",
                "courseId": course["courseId"],
                "title": lesson_title,
                "content": lesson_content,
                "duration": random.randint(20, 45),
                "order": random.randint(1, 10),
                "videoUrl": data_generator.get_video_url(lesson_title),
                "materials": data_generator.get_material_urls(random.randint(1, 3)),
                "createdAt": data_generator.get_random_date(90, 0)
            }
            lessons.append(lesson)
            lesson_counter += 1
        
        return lessons
    
    def _generate_lesson_content(self, title, category):
        """Generate detailed lesson content based on title and category"""
        content_templates = {
            "Programming": f"In this lesson, you'll learn about {title.lower()}. We'll cover the fundamental concepts, best practices, and provide hands-on examples to reinforce your understanding. By the end of this lesson, you'll be able to apply these concepts in real-world programming scenarios.",
            "Data Science": f"This lesson focuses on {title.lower()} in the context of data science. You'll explore practical applications, work with real datasets, and understand how this concept fits into the broader data science workflow. We'll use Python libraries and tools to demonstrate key concepts.",
            "Web Development": f"Learn {title.lower()} for modern web development. This lesson covers both theoretical concepts and practical implementation. You'll build interactive examples and understand how to integrate these concepts into full-stack applications.",
            "AI/ML": f"Explore {title.lower()} in artificial intelligence and machine learning. This lesson combines theoretical foundations with practical implementation using popular frameworks like TensorFlow and PyTorch. You'll work on real AI projects and understand the mathematical concepts behind the algorithms.",
            "Cloud Computing": f"Master {title.lower()} in cloud environments. This lesson covers AWS services, best practices for cloud architecture, and hands-on labs to reinforce learning. You'll understand how to implement scalable and cost-effective cloud solutions.",
            "Cybersecurity": f"Understand {title.lower()} from a cybersecurity perspective. This lesson covers threat assessment, security protocols, and practical defense strategies. You'll learn to identify vulnerabilities and implement security measures to protect systems and data."
        }
        
        return content_templates.get(category, content_templates["Programming"])
    
    def generate_sample_assignments(self, count):
        """Generate sample assignments with realistic educational content"""
        courses = list(self.db.courses.find())
        assignments = []
        
        for i in range(count):
            course = random.choice(courses)
            course_category = course.get("category", "Programming")
            
            # Get assignment topics for this category
            category_assignments = data_generator.assignment_topics.get(course_category, 
                                                                       data_generator.assignment_topics["Programming"])
            
            assignment_title = random.choice(category_assignments)
            assignment_description = self._generate_assignment_description(assignment_title, course_category)
            assignment_instructions = self._generate_assignment_instructions(assignment_title, course_category)
            
            assignment = {
                "assignmentId": f"AS_{str(i+1).zfill(3)}",
                "courseId": course["courseId"],
                "title": assignment_title,
                "description": assignment_description,
                "dueDate": data_generator.get_random_date(-7, -30),  # Due in 7-30 days (future dates)
                "maxPoints": random.choice([100, 100, 100, 80, 90]),  # Most assignments worth 100 points
                "createdAt": data_generator.get_random_date(60, 30),  # Created 30-60 days ago
                "instructions": assignment_instructions
            }
            assignments.append(assignment)
        
        return assignments
    
    def _generate_assignment_description(self, title, category):
        """Generate detailed assignment description based on title and category"""
        descriptions = {
            "Programming": f"Complete a {title.lower()} project that demonstrates your understanding of programming concepts covered in class. This assignment will test your ability to write clean, efficient code and implement best practices.",
            "Data Science": f"Your task is to {title.lower()} using the techniques and tools we've discussed. You'll need to clean data, perform analysis, create visualizations, and present your findings in a clear, professional manner.",
            "Web Development": f"Develop a {title.lower()} that showcases modern web development practices. Focus on responsive design, user experience, and clean code architecture. Include both frontend and backend components.",
            "AI/ML": f"Implement a {title.lower()} using machine learning techniques. Your solution should include data preprocessing, model selection, training, evaluation, and a clear explanation of your approach and results."
        }
        
        return descriptions.get(category, descriptions["Programming"])
    
    def _generate_assignment_instructions(self, title, category):
        """Generate detailed assignment instructions"""
        instructions = {
            "Programming": "Submit your code in a GitHub repository with a README file explaining your approach. Include unit tests and documentation. Code should follow PEP 8 style guidelines.",
            "Data Science": "Submit a Jupyter notebook with your analysis, along with a PDF report summarizing your findings. Include data visualizations and statistical analysis. Ensure your code is well-commented.",
            "Web Development": "Deploy your application and submit the live URL along with your source code. Include a README with setup instructions and a brief description of your architecture choices.",
            "AI/ML": "Submit your trained model, source code, and a technical report explaining your methodology. Include performance metrics and a discussion of potential improvements."
        }
        
        return instructions.get(category, instructions["Programming"])
    
    def generate_sample_enrollments(self, count):
        """Generate sample enrollments"""
        students = list(self.db.users.find({"role": "student"}))
        courses = list(self.db.courses.find())
        enrollments = []
        
        used_combinations = set()
        
        for i in range(count):
            while True:
                student = random.choice(students)
                course = random.choice(courses)
                combination = (student["userId"], course["courseId"])
                
                if combination not in used_combinations:
                    used_combinations.add(combination)
                    break
            
            enrollment = {
                "enrollmentId": f"EN_{str(i+1).zfill(3)}",
                "studentId": student["userId"],
                "courseId": course["courseId"],
                "enrollmentDate": data_generator.get_random_date(60, 0),  # Within last 2 months
                "status": random.choice(["active", "completed", "dropped"]),
                "progress": random.randint(0, 100),
                "completionDate": data_generator.get_random_date(30, 0) if random.choice([True, False]) else None
            }
            enrollments.append(enrollment)
        
        return enrollments
    
    def generate_sample_submissions(self, count):
        """Generate sample submissions with realistic content"""
        assignments = list(self.db.assignments.find())
        enrollments = list(self.db.enrollments.find())
        submissions = []
        
        # Realistic submission content templates
        submission_content_templates = [
            "Completed the assignment as requested. Implemented all required features and tested thoroughly. The solution follows best practices and includes proper documentation.",
            "This project demonstrates my understanding of the concepts covered in class. I've included extensive comments and examples to show my thought process.",
            "Successfully implemented the requirements with additional features for enhanced functionality. Spent extra time on optimization and user experience.",
            "Encountered some challenges during implementation but found creative solutions. The final result meets all specifications and includes error handling.",
            "Applied the techniques learned in lectures to solve this problem. The solution is scalable and well-structured with clean, readable code."
        ]
        
        # Realistic feedback templates
        feedback_templates = [
            "Excellent work! Your solution demonstrates strong understanding of the concepts. Code is clean and well-documented.",
            "Good effort. The implementation is correct but could benefit from better error handling and code organization.",
            "Well done! Creative approach to the problem. Consider optimizing the algorithm for better performance.",
            "Solid work. All requirements met. Nice use of design patterns and best practices.",
            "Great attention to detail. The documentation and testing are particularly impressive.",
            "Good solution overall. Some minor issues with edge cases, but the core logic is sound."
        ]
        
        # Realistic attachment URLs
        attachment_types = [
            "https://github.com/student/assignment-repo",
            "https://student-portfolio.herokuapp.com/project",
            "https://colab.research.google.com/drive/assignment-notebook",
            "https://eduhub-submissions.s3.amazonaws.com/project-demo.mp4",
            "https://eduhub-submissions.s3.amazonaws.com/source-code.zip",
            "https://eduhub-submissions.s3.amazonaws.com/report.pdf"
        ]
        
        for i in range(count):
            assignment = random.choice(assignments)
            # Find enrollments for the same course
            course_enrollments = [e for e in enrollments if e["courseId"] == assignment["courseId"]]
            
            if course_enrollments:
                enrollment = random.choice(course_enrollments)
                
                # Determine if submission is graded (80% chance)
                is_graded = random.random() < 0.8
                grade = None
                feedback = None
                graded_date = None
                
                if is_graded:
                    # Realistic grade distribution (mostly B+ to A)
                    grade = random.choices(
                        [95, 90, 85, 88, 92, 78, 82, 96, 87, 91],
                        weights=[10, 15, 12, 13, 14, 8, 10, 12, 8, 15]
                    )[0]
                    feedback = random.choice(feedback_templates)
                    graded_date = data_generator.get_random_date(14, 0)  # Graded within 2 weeks
                
                submission = {
                    "submissionId": f"SU_{str(i+1).zfill(3)}",
                    "assignmentId": assignment["assignmentId"],
                    "studentId": enrollment["studentId"],
                    "submissionDate": data_generator.get_random_date(30, 0),  # Within last month
                    "content": random.choice(submission_content_templates),
                    "attachments": random.sample(attachment_types, random.randint(1, 3)),
                    "grade": grade,
                    "feedback": feedback,
                    "gradedDate": graded_date
                }
                submissions.append(submission)
        
        return submissions      
    
    def clear_all_data(self):
        """Clear all data from collections"""
        collections = ["users", "courses", "lessons", "assignments", "enrollments", "submissions"]
        for collection_name in collections:
            self.db[collection_name].delete_many({})
        print("🗑️ All existing data cleared")

    # PART 3: BASIC CRUD OPERATIONS

    # CREATE Operations
    def add_new_student(self, email, first_name, last_name, bio="", skills=None):
        """Add a new student user"""
        if skills is None:
            skills = []
            
        # Generate unique userId
        last_student = self.db.users.find({"role": "student"}).sort("userId", -1).limit(1)
        next_id = 1
        for student in last_student:
            current_id = int(student["userId"].split("_")[1])
            next_id = current_id + 1
            break
        
        new_student = {
            "userId": f"ST_{str(next_id).zfill(3)}",
            "email": email,
            "firstName": first_name,
            "lastName": last_name,
            "role": "student",
            "dateJoined": datetime.now(),
            "profile": {
                "bio": bio,
                "avatar": data_generator.get_avatar_url(f"{first_name} {last_name}"),
                "skills": skills
            },
            "isActive": True
        }
        
        try:
            result = self.db.users.insert_one(new_student)
            print(f"✅ New student added with ID: {result.inserted_id}")
            return result.inserted_id
        except Exception as e:
            print(f"❌ Error adding student: {e}")
            return None
    
    def create_new_course(self, title, description, instructor_id, category, level, duration, price, tags=None):
        """Create a new course"""
        if tags is None:
            tags = []
            
        # Generate unique courseId
        last_course = self.db.courses.find().sort("courseId", -1).limit(1)
        next_id = 1
        for course in last_course:
            current_id = int(course["courseId"].split("_")[1])
            next_id = current_id + 1
            break
        
        new_course = {
            "courseId": f"CO_{str(next_id).zfill(3)}",
            "title": title,
            "description": description,
            "instructorId": instructor_id,
            "category": category,
            "level": level,
            "duration": duration,
            "price": price,
            "tags": tags,
            "createdAt": datetime.now(),
            "updatedAt": datetime.now(),
            "isPublished": False,
            "rating": 0.0
        }
        
        try:
            result = self.db.courses.insert_one(new_course)
            print(f"✅ New course created with ID: {result.inserted_id}")
            return result.inserted_id
        except Exception as e:
            print(f"❌ Error creating course: {e}")
            return None
    
    def enroll_student_in_course(self, student_id, course_id):
        """Enroll a student in a course"""
        
        # Check if enrollment already exists
        existing = self.db.enrollments.find_one({"studentId": student_id, "courseId": course_id})
        if existing:
            print("❌ Student is already enrolled in this course")
            return None
        
        # Generate unique enrollmentId
        last_enrollment = self.db.enrollments.find().sort("enrollmentId", -1).limit(1)
        next_id = 1
        for enrollment in last_enrollment:
            current_id = int(enrollment["enrollmentId"].split("_")[1])
            next_id = current_id + 1
            break
        
        new_enrollment = {
            "enrollmentId": f"EN_{str(next_id).zfill(3)}",
            "studentId": student_id,
            "courseId": course_id,
            "enrollmentDate": datetime.now(),
            "status": "active",
            "progress": 0,
            "completionDate": None
        }
        
        try:
            result = self.db.enrollments.insert_one(new_enrollment)
            print(f"✅ Student enrolled with enrollment ID: {result.inserted_id}")
            return result.inserted_id
        except Exception as e:
            print(f"❌ Error enrolling student: {e}")
            return None
    
    def add_lesson_to_course(self, course_id, title, content, duration, video_url="", materials=None):
        """Add a new lesson to an existing course"""
        if materials is None:
            materials = []
            
        # Generate unique lessonId
        last_lesson = self.db.lessons.find().sort("lessonId", -1).limit(1)
        next_id = 1
        for lesson in last_lesson:
            current_id = int(lesson["lessonId"].split("_")[1])
            next_id = current_id + 1
            break
        
        # Get the next order number for this course
        last_order = self.db.lessons.find({"courseId": course_id}).sort("order", -1).limit(1)
        next_order = 1
        for lesson in last_order:
            next_order = lesson["order"] + 1
            break
        
        new_lesson = {
            "lessonId": f"LE_{str(next_id).zfill(3)}",
            "courseId": course_id,
            "title": title,
            "content": content,
            "duration": duration,
            "order": next_order,
            "videoUrl": video_url,
            "materials": materials,
            "createdAt": datetime.now()
        }
        
        try:
            result = self.db.lessons.insert_one(new_lesson)
            print(f"✅ New lesson added with ID: {result.inserted_id}")
            return result.inserted_id
        except Exception as e:
            print(f"❌ Error adding lesson: {e}")
            return None
    
    # READ Operations
    def find_all_active_students(self):
        """Find all active students"""
        return list(self.db.users.find({"role": "student", "isActive": True}))
    
    def get_course_with_instructor_info(self, course_id):
        """Retrieve course details with instructor information"""
        pipeline = [
            {"$match": {"courseId": course_id}},
            {"$lookup": {
                "from": "users",
                "localField": "instructorId",
                "foreignField": "userId",
                "as": "instructor"
            }},
            {"$unwind": "$instructor"},
            {"$project": {
                "courseId": 1,
                "title": 1,
                "description": 1,
                "category": 1,
                "level": 1,
                "duration": 1,
                "price": 1,
                "tags": 1,
                "rating": 1,
                "instructor.firstName": 1,
                "instructor.lastName": 1,
                "instructor.email": 1,
                "instructor.profile.bio": 1
            }}
        ]
        return list(self.db.courses.aggregate(pipeline))
    
    def get_courses_by_category(self, category):
        """Get all courses in a specific category"""
        return list(self.db.courses.find({"category": category}))
    
    def find_students_in_course(self, course_id):
        """Find students enrolled in a particular course"""
        pipeline = [
            {"$match": {"courseId": course_id}},
            {"$lookup": {
                "from": "users",
                "localField": "studentId",
                "foreignField": "userId",
                "as": "student"
            }},
            {"$unwind": "$student"},
            {"$project": {
                "enrollmentId": 1,
                "enrollmentDate": 1,
                "status": 1,
                "progress": 1,
                "student.firstName": 1,
                "student.lastName": 1,
                "student.email": 1
            }}
        ]
        return list(self.db.enrollments.aggregate(pipeline))
    
    def search_courses_by_title(self, search_term):
        """Search courses by title (case-insensitive, partial match)"""
        regex_pattern = re.compile(search_term, re.IGNORECASE)
        return list(self.db.courses.find({"title": {"$regex": regex_pattern}}))
    
    # UPDATE Operations
    def update_user_profile(self, user_id, bio=None, skills=None, avatar=None):
        """Update a user's profile information"""
        update_data = {}
        if bio is not None:
            update_data["profile.bio"] = bio
        if skills is not None:
            update_data["profile.skills"] = skills
        if avatar is not None:
            update_data["profile.avatar"] = avatar
        
        if update_data:
            try:
                result = self.db.users.update_one(
                    {"userId": user_id},
                    {"$set": update_data}
                )
                print(f"✅ Profile updated for user {user_id}. Modified count: {result.modified_count}")
                return result.modified_count
            except Exception as e:
                print(f"❌ Error updating profile: {e}")
                return 0
        else:
            print("❌ No update data provided")
            return 0
    
    def mark_course_as_published(self, course_id):
        """Mark a course as published"""
        try:
            result = self.db.courses.update_one(
                {"courseId": course_id},
                {"$set": {"isPublished": True, "updatedAt": datetime.now()}}
            )
            print(f"✅ Course {course_id} marked as published. Modified count: {result.modified_count}")
            return result.modified_count
        except Exception as e:
            print(f"❌ Error updating course: {e}")
            return 0
    
    def update_assignment_grade(self, submission_id, grade, feedback=None):
        """Update assignment grades"""
        update_data = {
            "grade": grade,
            "gradedDate": datetime.now()
        }
        if feedback:
            update_data["feedback"] = feedback
        
        try:
            result = self.db.submissions.update_one(
                {"submissionId": submission_id},
                {"$set": update_data}
            )
            print(f"✅ Grade updated for submission {submission_id}. Modified count: {result.modified_count}")
            return result.modified_count
        except Exception as e:
            print(f"❌ Error updating grade: {e}")
            return 0
    
    def add_tags_to_course(self, course_id, new_tags):
        """Add tags to an existing course"""
        try:
            result = self.db.courses.update_one(
                {"courseId": course_id},
                {"$addToSet": {"tags": {"$each": new_tags}}, "$set": {"updatedAt": datetime.now()}}
            )
            print(f"✅ Tags added to course {course_id}. Modified count: {result.modified_count}")
            return result.modified_count
        except Exception as e:
            print(f"❌ Error adding tags: {e}")
            return 0
    
    # DELETE Operations
    def soft_delete_user(self, user_id):
        """Remove a user (soft delete by setting isActive to false)"""
        try:
            result = self.db.users.update_one(
                {"userId": user_id},
                {"$set": {"isActive": False}}
            )
            print(f"✅ User {user_id} soft deleted. Modified count: {result.modified_count}")
            return result.modified_count
        except Exception as e:
            print(f"❌ Error soft deleting user: {e}")
            return 0
    
    def delete_enrollment(self, enrollment_id):
        """Delete an enrollment"""
        try:
            result = self.db.enrollments.delete_one({"enrollmentId": enrollment_id})
            print(f"✅ Enrollment {enrollment_id} deleted. Deleted count: {result.deleted_count}")
            return result.deleted_count
        except Exception as e:
            print(f"❌ Error deleting enrollment: {e}")
            return 0
    
    def remove_lesson_from_course(self, lesson_id):
        """Remove a lesson from a course"""
        try:
            result = self.db.lessons.delete_one({"lessonId": lesson_id})
            print(f"✅ Lesson {lesson_id} removed. Deleted count: {result.deleted_count}")
            return result.deleted_count
        except Exception as e:
            print(f"❌ Error removing lesson: {e}")
            return 0
    
    # PART 4: ADVANCED QUERIES AND AGGREGATION
    
    # Complex Queries
    def find_courses_by_price_range(self, min_price, max_price):
        """Find courses with price between min_price and max_price"""
        return list(self.db.courses.find({"price": {"$gte": min_price, "$lte": max_price}}))
    
    def get_recent_users(self, months=6):
        """Get users who joined in the last N months"""
        cutoff_date = datetime.now() - timedelta(days=30 * months)
        return list(self.db.users.find({"dateJoined": {"$gte": cutoff_date}}))
    
    def find_courses_with_tags(self, tag_list):
        """Find courses that have specific tags using $in operator"""
        return list(self.db.courses.find({"tags": {"$in": tag_list}}))
    
    def get_assignments_due_next_week(self):
        """Retrieve assignments with due dates in the next week"""
        start_date = datetime.now()
        end_date = start_date + timedelta(weeks=1)
        return list(self.db.assignments.find({
            "dueDate": {"$gte": start_date, "$lte": end_date}
        }))
    
    # Aggregation Pipelines
    def get_course_enrollment_statistics(self):
        """Course Enrollment Statistics: Count total enrollments per course, calculate average course rating, group by course category"""
        pipeline = [
            # Join with enrollments to count enrollments per course
            {"$lookup": {
                "from": "enrollments",
                "localField": "courseId",
                "foreignField": "courseId",
                "as": "enrollments"
            }},
            # Group by category and calculate statistics
            {"$group": {
                "_id": "$category",
                "totalCourses": {"$sum": 1},
                "totalEnrollments": {"$sum": {"$size": "$enrollments"}},
                "averageRating": {"$avg": "$rating"},
                "averagePrice": {"$avg": "$price"},
                "courses": {
                    "$push": {
                        "courseId": "$courseId",
                        "title": "$title",
                        "enrollmentCount": {"$size": "$enrollments"},
                        "rating": "$rating"
                    }
                }
            }},
            # Sort by total enrollments descending
            {"$sort": {"totalEnrollments": -1}}
        ]
        return list(self.db.courses.aggregate(pipeline))
    
    def get_student_performance_analysis(self):
        """Student Performance Analysis: Average grade per student, completion rate by course, top-performing students"""
        pipeline = [
            # Join submissions with assignments to get course info
            {"$lookup": {
                "from": "assignments",
                "localField": "assignmentId",
                "foreignField": "assignmentId",
                "as": "assignment"
            }},
            {"$unwind": "$assignment"},
            # Join with users to get student info
            {"$lookup": {
                "from": "users",
                "localField": "studentId",
                "foreignField": "userId",
                "as": "student"
            }},
            {"$unwind": "$student"},
            # Group by student to calculate average grade
            {"$group": {
                "_id": "$studentId",
                "studentName": {"$first": {"$concat": ["$student.firstName", " ", "$student.lastName"]}},
                "averageGrade": {"$avg": "$grade"},
                "totalSubmissions": {"$sum": 1},
                "coursesParticipated": {"$addToSet": "$assignment.courseId"}
            }},
            # Add calculated fields
            {"$addFields": {
                "coursesCount": {"$size": "$coursesParticipated"}
            }},
            # Sort by average grade descending
            {"$sort": {"averageGrade": -1}}
        ]
        return list(self.db.submissions.aggregate(pipeline))
    
    def get_instructor_analytics(self):
        """Instructor Analytics: Total students taught by each instructor, average course rating per instructor, revenue generated per instructor"""
        pipeline = [
            # Join courses with users to get instructor info
            {"$lookup": {
                "from": "users",
                "localField": "instructorId",
                "foreignField": "userId",
                "as": "instructor"
            }},
            {"$unwind": "$instructor"},
            # Join with enrollments to count students
            {"$lookup": {
                "from": "enrollments",
                "localField": "courseId",
                "foreignField": "courseId",
                "as": "enrollments"
            }},
            # Group by instructor
            {"$group": {
                "_id": "$instructorId",
                "instructorName": {"$first": {"$concat": ["$instructor.firstName", " ", "$instructor.lastName"]}},
                "totalCourses": {"$sum": 1},
                "totalStudents": {"$sum": {"$size": "$enrollments"}},
                "averageRating": {"$avg": "$rating"},
                "totalRevenue": {"$sum": {"$multiply": ["$price", {"$size": "$enrollments"}]}},
                "courses": {
                    "$push": {
                        "title": "$title",
                        "enrollments": {"$size": "$enrollments"},
                        "rating": "$rating",
                        "revenue": {"$multiply": ["$price", {"$size": "$enrollments"}]}
                    }
                }
            }},
            # Sort by total revenue descending
            {"$sort": {"totalRevenue": -1}}
        ]
        return list(self.db.courses.aggregate(pipeline))
    
    def get_advanced_analytics(self):
        """Advanced Analytics: Monthly enrollment trends, most popular course categories, student engagement metrics"""
        
        # Monthly enrollment trends
        monthly_trends = list(self.db.enrollments.aggregate([
            {"$group": {
                "_id": {
                    "year": {"$year": "$enrollmentDate"},
                    "month": {"$month": "$enrollmentDate"}
                },
                "enrollmentCount": {"$sum": 1},
                "activeEnrollments": {"$sum": {"$cond": [{"$eq": ["$status", "active"]}, 1, 0]}},
                "completedEnrollments": {"$sum": {"$cond": [{"$eq": ["$status", "completed"]}, 1, 0]}}
            }},
            {"$sort": {"_id.year": 1, "_id.month": 1}}
        ]))
        
        # Most popular course categories
        popular_categories = list(self.db.courses.aggregate([
            {"$lookup": {
                "from": "enrollments",
                "localField": "courseId",
                "foreignField": "courseId",
                "as": "enrollments"
            }},
            {"$group": {
                "_id": "$category",
                "totalEnrollments": {"$sum": {"$size": "$enrollments"}},
                "averageRating": {"$avg": "$rating"},
                "courseCount": {"$sum": 1}
            }},
            {"$sort": {"totalEnrollments": -1}}
        ]))
        
        # Student engagement metrics
        engagement_metrics = list(self.db.enrollments.aggregate([
            {"$group": {
                "_id": "$status",
                "count": {"$sum": 1},
                "averageProgress": {"$avg": "$progress"}
            }}
        ]))
        
        return {
            "monthly_trends": monthly_trends,
            "popular_categories": popular_categories,
            "engagement_metrics": engagement_metrics
        }
    
    # PART 5: PERFORMANCE OPTIMIZATION
    
    def analyze_query_performance(self, collection_name, query, explain_type="executionStats"):
        """Analyze query performance using explain() method"""
        collection = self.db[collection_name]
        return collection.find(query).explain(explain_type)
    
    def optimize_slow_queries(self):
        """Optimize common slow queries and document performance improvements"""
        
        print("🔍 Analyzing and optimizing query performance...")
        
        # Query 1: Find courses by title (text search)
        print("\n1. Optimizing course title search...")
        start_time = datetime.now()
        courses = list(self.db.courses.find({"title": {"$regex": "Course", "$options": "i"}}))
        end_time = datetime.now()
        print(f"   Before optimization: {(end_time - start_time).total_seconds():.4f} seconds")
        
        # Create text index if not exists
        try:
            self.db.courses.create_index([("title", "text"), ("description", "text")])
            print("   ✅ Text index created for title and description")
        except Exception:
            print("   ℹ️ Text index already exists")
        
        # Query 2: Find enrollments by student and date range
        print("\n2. Optimizing enrollment queries...")
        start_time = datetime.now()
        recent_enrollments = list(self.db.enrollments.find({
            "enrollmentDate": {"$gte": datetime.now() - timedelta(days=30)}
        }))
        end_time = datetime.now()
        print(f"   Query time: {(end_time - start_time).total_seconds():.4f} seconds")
        
        # Query 3: Find assignments by due date
        print("\n3. Optimizing assignment due date queries...")
        start_time = datetime.now()
        upcoming_assignments = list(self.db.assignments.find({
            "dueDate": {"$gte": datetime.now(), "$lte": datetime.now() + timedelta(days=7)}
        }))
        end_time = datetime.now()
        print(f"   Query time: {(end_time - start_time).total_seconds():.4f} seconds")
        
        print("\n🎯 Performance optimization completed!")
    
    # PART 6: DATA VALIDATION AND ERROR HANDLING
    
    def validate_email_format(self, email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def handle_duplicate_key_error(self, collection_name, document):
        """Handle duplicate key errors"""
        try:
            result = self.db[collection_name].insert_one(document)
            print(f"✅ Document inserted successfully: {result.inserted_id}")
            return result.inserted_id
        except Exception as e:
            if "duplicate key" in str(e).lower():
                print(f"❌ Duplicate key error: {e}")
                print("💡 Suggestion: Check for existing records with the same unique field values")
            else:
                print(f"❌ Unexpected error: {e}")
            return None
    
    def validate_and_insert_user(self, user_data):
        """Validate user data before insertion"""
        errors = []
        
        # Check required fields
        required_fields = ["userId", "email", "firstName", "lastName", "role"]
        for field in required_fields:
            if field not in user_data or not user_data[field]:
                errors.append(f"Missing required field: {field}")
        
        # Validate email format
        if "email" in user_data and not self.validate_email_format(user_data["email"]):
            errors.append("Invalid email format")
        
        # Validate role enum
        if "role" in user_data and user_data["role"] not in ["student", "instructor"]:
            errors.append("Role must be 'student' or 'instructor'")
        
        if errors:
            print("❌ Validation errors:")
            for error in errors:
                print(f"   - {error}")
            return None
        
        # If validation passes, insert the user
        return self.handle_duplicate_key_error("users", user_data)
    
    # UTILITY METHODS
    
    def export_sample_data(self, output_file="sample_data.json"):
        """Export sample data to JSON file"""
        
        data = {}
        collections = ["users", "courses", "lessons", "assignments", "enrollments", "submissions"]
        
        for collection_name in collections:
            cursor = self.db[collection_name].find()
            documents = []
            for doc in cursor:
                # Convert ObjectId to string for JSON serialization
                doc["_id"] = str(doc["_id"])
                # Convert datetime objects to ISO format
                for key, value in doc.items():
                    if isinstance(value, datetime):
                        doc[key] = value.isoformat()
                documents.append(doc)
            data[collection_name] = documents
        
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        print(f"✅ Sample data exported to {output_file}")
    
    def get_collection_statistics(self):
        """Get statistics for all collections"""
        stats = {}
        for collection_name in self.db.list_collection_names():
            collection_stats = self.db.command("collstats", collection_name)
            stats[collection_name] = {
                "count": collection_stats.get("count", 0),
                "size": collection_stats.get("size", 0),
                "avgObjSize": collection_stats.get("avgObjSize", 0),
                "indexes": collection_stats.get("nindexes", 0)
            }
        return stats
    
    def close_connection(self):
        """Close the database connection"""
        self.client.close()
        print("📊 Database connection closed")

if __name__ == "__main__":
    # Initialize the database
    db = EduHubDatabase()
    
    # Populate sample data
    print("🚀 Starting EduHub Database Project...")
    db.populate_sample_data()
    
    # Display database info
    print("\n📊 Database Information:")
    info = db.get_database_info()
    for collection, stats in info["collection_stats"].items():
        print(f"   {collection}: {stats['count']} documents")
    
    # Export sample data
    db.export_sample_data()
    
    print("\n🎉 EduHub Database setup completed successfully!")
    