"""
Pytest configuration and fixtures for testing the FastAPI application.
"""
import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add the src directory to the path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from app import app, activities


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """Reset activities to initial state before each test."""
    # Store the original state
    original_state = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Soccer Team": {
            "description": "Join the varsity soccer team for practices and matches",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 6:00 PM",
            "max_participants": 25,
            "participants": ["alex@mergington.edu", "sarah@mergington.edu"]
        },
        "Swimming Club": {
            "description": "Improve swimming techniques and compete in swim meets",
            "schedule": "Mondays and Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 15,
            "participants": ["lucas@mergington.edu", "mia@mergington.edu"]
        },
        "Drama Club": {
            "description": "Perform in plays and develop acting skills",
            "schedule": "Wednesdays, 3:30 PM - 5:30 PM",
            "max_participants": 18,
            "participants": ["isabella@mergington.edu", "ethan@mergington.edu"]
        },
        "Art Studio": {
            "description": "Explore various art mediums including painting and sculpture",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 15,
            "participants": ["ava@mergington.edu", "james@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop critical thinking and public speaking through competitive debates",
            "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["noah@mergington.edu", "emily@mergington.edu"]
        },
        "Science Olympiad": {
            "description": "Compete in science and engineering challenges at regional competitions",
            "schedule": "Fridays, 3:30 PM - 5:30 PM",
            "max_participants": 20,
            "participants": ["liam@mergington.edu", "charlotte@mergington.edu"]
        }
    }
    
    # Clear and restore activities before each test
    activities.clear()
    activities.update(original_state)
    
    yield
    
    # Restore after test
    activities.clear()
    activities.update(original_state)
