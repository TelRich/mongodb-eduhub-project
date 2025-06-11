"""
Eduhub MongoDB Project - Complete Implementation
AltSchool of Data Engineering Tinyuka 2024 Second Semester Project Exam

This module contains all MongoDB operations for the EduHub e-learning platform.
Author: Goodrich Okoro
Date: June 2025
"""

from pymongo import MongoClient
from datetime import datetime, timedelta
import pandas as pd
import json
import random
from faker import Faker
import re 

# Initialize Faker for generating sample data
fake = Faker()

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
        """Set up all colections with validation rules"""
        
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