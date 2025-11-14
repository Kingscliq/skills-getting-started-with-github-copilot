"""
Tests for the Mergington High School Activities API endpoints.
"""
import pytest


class TestRootEndpoint:
    """Tests for the root endpoint."""
    
    def test_root_redirects_to_static(self, client):
        """Test that root endpoint redirects to static/index.html."""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"


class TestGetActivities:
    """Tests for GET /activities endpoint."""
    
    def test_get_activities_returns_all_activities(self, client, reset_activities):
        """Test that GET /activities returns all activities."""
        response = client.get("/activities")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) == 9
        assert "Chess Club" in data
        assert "Programming Class" in data
    
    def test_get_activities_structure(self, client, reset_activities):
        """Test that activities have the correct structure."""
        response = client.get("/activities")
        data = response.json()
        
        # Check Chess Club structure
        chess_club = data["Chess Club"]
        assert "description" in chess_club
        assert "schedule" in chess_club
        assert "max_participants" in chess_club
        assert "participants" in chess_club
        assert isinstance(chess_club["participants"], list)
        assert len(chess_club["participants"]) == 2


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint."""
    
    def test_signup_new_participant_success(self, client, reset_activities):
        """Test successful signup for an activity."""
        response = client.post(
            "/activities/Chess%20Club/signup?email=newstudent@mergington.edu"
        )
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "newstudent@mergington.edu" in data["message"]
        assert "Chess Club" in data["message"]
        
        # Verify participant was added
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert "newstudent@mergington.edu" in activities["Chess Club"]["participants"]
    
    def test_signup_duplicate_participant_fails(self, client, reset_activities):
        """Test that signing up twice with same email fails."""
        email = "michael@mergington.edu"  # Already in Chess Club
        
        response = client.post(
            f"/activities/Chess%20Club/signup?email={email}"
        )
        assert response.status_code == 400
        
        data = response.json()
        assert "detail" in data
        assert "already signed up" in data["detail"].lower()
    
    def test_signup_nonexistent_activity_fails(self, client, reset_activities):
        """Test that signing up for non-existent activity fails."""
        response = client.post(
            "/activities/Nonexistent%20Club/signup?email=test@mergington.edu"
        )
        assert response.status_code == 404
        
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()
    
    def test_signup_multiple_activities_same_student(self, client, reset_activities):
        """Test that a student can sign up for multiple activities."""
        email = "multisport@mergington.edu"
        
        # Sign up for Chess Club
        response1 = client.post(
            f"/activities/Chess%20Club/signup?email={email}"
        )
        assert response1.status_code == 200
        
        # Sign up for Drama Club
        response2 = client.post(
            f"/activities/Drama%20Club/signup?email={email}"
        )
        assert response2.status_code == 200
        
        # Verify participant in both
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities["Chess Club"]["participants"]
        assert email in activities["Drama Club"]["participants"]


class TestUnregisterFromActivity:
    """Tests for DELETE /activities/{activity_name}/unregister endpoint."""
    
    def test_unregister_existing_participant_success(self, client, reset_activities):
        """Test successful unregistration from an activity."""
        email = "michael@mergington.edu"  # Already in Chess Club
        
        response = client.delete(
            f"/activities/Chess%20Club/unregister?email={email}"
        )
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert "Unregistered" in data["message"]
        
        # Verify participant was removed
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email not in activities["Chess Club"]["participants"]
    
    def test_unregister_non_registered_participant_fails(self, client, reset_activities):
        """Test that unregistering a non-registered participant fails."""
        email = "notregistered@mergington.edu"
        
        response = client.delete(
            f"/activities/Chess%20Club/unregister?email={email}"
        )
        assert response.status_code == 400
        
        data = response.json()
        assert "detail" in data
        assert "not signed up" in data["detail"].lower()
    
    def test_unregister_nonexistent_activity_fails(self, client, reset_activities):
        """Test that unregistering from non-existent activity fails."""
        response = client.delete(
            "/activities/Nonexistent%20Club/unregister?email=test@mergington.edu"
        )
        assert response.status_code == 404
        
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()
    
    def test_unregister_then_register_again(self, client, reset_activities):
        """Test that a student can unregister and register again."""
        email = "michael@mergington.edu"
        
        # Unregister
        response1 = client.delete(
            f"/activities/Chess%20Club/unregister?email={email}"
        )
        assert response1.status_code == 200
        
        # Register again
        response2 = client.post(
            f"/activities/Chess%20Club/signup?email={email}"
        )
        assert response2.status_code == 200
        
        # Verify participant is back
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities["Chess Club"]["participants"]


class TestEdgeCases:
    """Tests for edge cases and special scenarios."""
    
    def test_special_characters_in_email(self, client, reset_activities):
        """Test handling of special characters in email."""
        from urllib.parse import quote
        
        email = "test+tag@mergington.edu"
        
        response = client.post(
            f"/activities/Chess%20Club/signup?email={quote(email)}"
        )
        assert response.status_code == 200
        
        # Verify participant was added
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities["Chess Club"]["participants"]
    
    def test_activity_name_with_spaces(self, client, reset_activities):
        """Test that activity names with spaces are properly handled."""
        # URL encoded space
        response = client.post(
            "/activities/Science%20Olympiad/signup?email=science@mergington.edu"
        )
        assert response.status_code == 200
        
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert "science@mergington.edu" in activities["Science Olympiad"]["participants"]
