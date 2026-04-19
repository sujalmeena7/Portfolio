#!/usr/bin/env python3
"""
Comprehensive backend API tests for Portfolio FastAPI backend.
Tests all endpoints with proper authentication and error handling.
"""

import asyncio
import json
import os
import tempfile
import time
from io import BytesIO
from pathlib import Path

import aiohttp
import aiofiles

# Base URL from frontend/.env
BASE_URL = "https://futuristic-dev-45.preview.emergentagent.com/api"

# Admin credentials (seeded)
ADMIN_EMAIL = "admin@portfolio.dev"
ADMIN_PASSWORD = "Admin@123"

class TestResults:
    def __init__(self):
        self.results = []
        self.auth_token = None
        
    def add_result(self, test_name: str, success: bool, details: str = ""):
        self.results.append({
            "test": test_name,
            "success": success,
            "details": details
        })
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name}")
        if details:
            print(f"   Details: {details}")
    
    def summary(self):
        passed = sum(1 for r in self.results if r["success"])
        total = len(self.results)
        print(f"\n=== TEST SUMMARY ===")
        print(f"Passed: {passed}/{total}")
        print(f"Failed: {total - passed}")
        
        if total - passed > 0:
            print("\nFailed tests:")
            for r in self.results:
                if not r["success"]:
                    print(f"  - {r['test']}: {r['details']}")

async def test_auth_endpoints(session: aiohttp.ClientSession, results: TestResults):
    """Test authentication endpoints"""
    print("\n=== Testing Authentication ===")
    
    # Test login with correct credentials
    try:
        login_data = {
            "email": ADMIN_EMAIL,
            "password": ADMIN_PASSWORD
        }
        async with session.post(f"{BASE_URL}/auth/login", json=login_data) as resp:
            if resp.status == 200:
                data = await resp.json()
                if "access_token" in data and data.get("token_type") == "bearer":
                    results.auth_token = data["access_token"]
                    user = data.get("user", {})
                    if user.get("email") == ADMIN_EMAIL and user.get("role") == "admin":
                        results.add_result("Auth login with correct credentials", True, 
                                         f"Token received, user: {user.get('email')}")
                    else:
                        results.add_result("Auth login with correct credentials", False, 
                                         f"Invalid user data: {user}")
                else:
                    results.add_result("Auth login with correct credentials", False, 
                                     f"Missing token or wrong type: {data}")
            else:
                text = await resp.text()
                results.add_result("Auth login with correct credentials", False, 
                                 f"Status {resp.status}: {text}")
    except Exception as e:
        results.add_result("Auth login with correct credentials", False, f"Exception: {e}")
    
    # Test login with wrong password
    try:
        wrong_login = {
            "email": ADMIN_EMAIL,
            "password": "WrongPassword123"
        }
        async with session.post(f"{BASE_URL}/auth/login", json=wrong_login) as resp:
            if resp.status == 401:
                results.add_result("Auth login with wrong password", True, "Correctly returned 401")
            else:
                text = await resp.text()
                results.add_result("Auth login with wrong password", False, 
                                 f"Expected 401, got {resp.status}: {text}")
    except Exception as e:
        results.add_result("Auth login with wrong password", False, f"Exception: {e}")
    
    # Test /auth/me with token
    if results.auth_token:
        try:
            headers = {"Authorization": f"Bearer {results.auth_token}"}
            async with session.get(f"{BASE_URL}/auth/me", headers=headers) as resp:
                if resp.status == 200:
                    user = await resp.json()
                    if user.get("email") == ADMIN_EMAIL:
                        results.add_result("Auth /me with token", True, f"User: {user.get('email')}")
                    else:
                        results.add_result("Auth /me with token", False, f"Wrong user: {user}")
                else:
                    text = await resp.text()
                    results.add_result("Auth /me with token", False, f"Status {resp.status}: {text}")
        except Exception as e:
            results.add_result("Auth /me with token", False, f"Exception: {e}")
    
    # Test /auth/me without token
    try:
        async with session.get(f"{BASE_URL}/auth/me") as resp:
            if resp.status == 401:
                results.add_result("Auth /me without token", True, "Correctly returned 401")
            else:
                text = await resp.text()
                results.add_result("Auth /me without token", False, 
                                 f"Expected 401, got {resp.status}: {text}")
    except Exception as e:
        results.add_result("Auth /me without token", False, f"Exception: {e}")

async def test_projects_endpoints(session: aiohttp.ClientSession, results: TestResults):
    """Test projects CRUD endpoints"""
    print("\n=== Testing Projects ===")
    
    # Test GET /projects (public)
    try:
        async with session.get(f"{BASE_URL}/projects") as resp:
            if resp.status == 200:
                projects = await resp.json()
                if isinstance(projects, list) and len(projects) >= 3:
                    results.add_result("Projects GET public", True, f"Found {len(projects)} projects")
                else:
                    results.add_result("Projects GET public", False, f"Expected list with >=3 items, got: {projects}")
            else:
                text = await resp.text()
                results.add_result("Projects GET public", False, f"Status {resp.status}: {text}")
    except Exception as e:
        results.add_result("Projects GET public", False, f"Exception: {e}")
    
    # Test POST /projects without auth (should fail)
    try:
        project_data = {
            "title": "Test Project",
            "description": "A test project for validation",
            "tags": ["test", "validation"]
        }
        async with session.post(f"{BASE_URL}/projects", json=project_data) as resp:
            if resp.status == 401:
                results.add_result("Projects POST without auth", True, "Correctly returned 401")
            else:
                text = await resp.text()
                results.add_result("Projects POST without auth", False, 
                                 f"Expected 401, got {resp.status}: {text}")
    except Exception as e:
        results.add_result("Projects POST without auth", False, f"Exception: {e}")
    
    created_project_id = None
    if results.auth_token:
        headers = {"Authorization": f"Bearer {results.auth_token}"}
        
        # Test POST /projects with auth
        try:
            project_data = {
                "title": "Test Project API",
                "description": "A comprehensive test project created via API testing",
                "tags": ["api", "testing", "fastapi"],
                "order": 999
            }
            async with session.post(f"{BASE_URL}/projects", json=project_data, headers=headers) as resp:
                if resp.status == 201:
                    project = await resp.json()
                    created_project_id = project.get("id")
                    if project.get("title") == project_data["title"]:
                        results.add_result("Projects POST with auth", True, f"Created project: {created_project_id}")
                    else:
                        results.add_result("Projects POST with auth", False, f"Title mismatch: {project}")
                else:
                    text = await resp.text()
                    results.add_result("Projects POST with auth", False, f"Status {resp.status}: {text}")
        except Exception as e:
            results.add_result("Projects POST with auth", False, f"Exception: {e}")
        
        # Test PUT /projects/{id} with auth
        if created_project_id:
            try:
                update_data = {
                    "title": "Updated Test Project",
                    "description": "Updated description for testing",
                    "tags": ["updated", "testing"]
                }
                async with session.put(f"{BASE_URL}/projects/{created_project_id}", 
                                     json=update_data, headers=headers) as resp:
                    if resp.status == 200:
                        project = await resp.json()
                        if project.get("title") == update_data["title"]:
                            results.add_result("Projects PUT with auth", True, "Project updated successfully")
                        else:
                            results.add_result("Projects PUT with auth", False, f"Update failed: {project}")
                    else:
                        text = await resp.text()
                        results.add_result("Projects PUT with auth", False, f"Status {resp.status}: {text}")
            except Exception as e:
                results.add_result("Projects PUT with auth", False, f"Exception: {e}")
        
        # Test DELETE /projects/{id} with auth
        if created_project_id:
            try:
                async with session.delete(f"{BASE_URL}/projects/{created_project_id}", headers=headers) as resp:
                    if resp.status == 200:
                        result = await resp.json()
                        if result.get("ok"):
                            results.add_result("Projects DELETE with auth", True, "Project deleted successfully")
                        else:
                            results.add_result("Projects DELETE with auth", False, f"Delete failed: {result}")
                    else:
                        text = await resp.text()
                        results.add_result("Projects DELETE with auth", False, f"Status {resp.status}: {text}")
            except Exception as e:
                results.add_result("Projects DELETE with auth", False, f"Exception: {e}")
    
    # Test GET /projects/{nonexistent-id}
    try:
        fake_id = "nonexistent-project-id-12345"
        async with session.get(f"{BASE_URL}/projects/{fake_id}") as resp:
            if resp.status == 404:
                results.add_result("Projects GET nonexistent", True, "Correctly returned 404")
            else:
                text = await resp.text()
                results.add_result("Projects GET nonexistent", False, 
                                 f"Expected 404, got {resp.status}: {text}")
    except Exception as e:
        results.add_result("Projects GET nonexistent", False, f"Exception: {e}")

async def test_skills_endpoints(session: aiohttp.ClientSession, results: TestResults):
    """Test skills CRUD endpoints"""
    print("\n=== Testing Skills ===")
    
    # Test GET /skills (public)
    try:
        async with session.get(f"{BASE_URL}/skills") as resp:
            if resp.status == 200:
                skills = await resp.json()
                if isinstance(skills, list) and len(skills) >= 8:
                    results.add_result("Skills GET public", True, f"Found {len(skills)} skills")
                else:
                    results.add_result("Skills GET public", False, f"Expected list with >=8 items, got: {skills}")
            else:
                text = await resp.text()
                results.add_result("Skills GET public", False, f"Status {resp.status}: {text}")
    except Exception as e:
        results.add_result("Skills GET public", False, f"Exception: {e}")
    
    created_skill_id = None
    if results.auth_token:
        headers = {"Authorization": f"Bearer {results.auth_token}"}
        
        # Test POST /skills with auth
        try:
            skill_data = {
                "name": "Rust",
                "level": 70,
                "icon": "Box",
                "order": 999
            }
            async with session.post(f"{BASE_URL}/skills", json=skill_data, headers=headers) as resp:
                if resp.status == 201:
                    skill = await resp.json()
                    created_skill_id = skill.get("id")
                    if skill.get("name") == skill_data["name"]:
                        results.add_result("Skills POST with auth", True, f"Created skill: {created_skill_id}")
                    else:
                        results.add_result("Skills POST with auth", False, f"Name mismatch: {skill}")
                else:
                    text = await resp.text()
                    results.add_result("Skills POST with auth", False, f"Status {resp.status}: {text}")
        except Exception as e:
            results.add_result("Skills POST with auth", False, f"Exception: {e}")
        
        # Test PUT /skills/{id} with auth
        if created_skill_id:
            try:
                update_data = {
                    "name": "Advanced Rust",
                    "level": 85,
                    "icon": "Zap"
                }
                async with session.put(f"{BASE_URL}/skills/{created_skill_id}", 
                                     json=update_data, headers=headers) as resp:
                    if resp.status == 200:
                        skill = await resp.json()
                        if skill.get("name") == update_data["name"]:
                            results.add_result("Skills PUT with auth", True, "Skill updated successfully")
                        else:
                            results.add_result("Skills PUT with auth", False, f"Update failed: {skill}")
                    else:
                        text = await resp.text()
                        results.add_result("Skills PUT with auth", False, f"Status {resp.status}: {text}")
            except Exception as e:
                results.add_result("Skills PUT with auth", False, f"Exception: {e}")
        
        # Test DELETE /skills/{id} with auth
        if created_skill_id:
            try:
                async with session.delete(f"{BASE_URL}/skills/{created_skill_id}", headers=headers) as resp:
                    if resp.status == 200:
                        result = await resp.json()
                        if result.get("ok"):
                            results.add_result("Skills DELETE with auth", True, "Skill deleted successfully")
                        else:
                            results.add_result("Skills DELETE with auth", False, f"Delete failed: {result}")
                    else:
                        text = await resp.text()
                        results.add_result("Skills DELETE with auth", False, f"Status {resp.status}: {text}")
            except Exception as e:
                results.add_result("Skills DELETE with auth", False, f"Exception: {e}")

async def test_about_endpoints(session: aiohttp.ClientSession, results: TestResults):
    """Test about endpoints"""
    print("\n=== Testing About ===")
    
    # Test GET /about (public)
    try:
        async with session.get(f"{BASE_URL}/about") as resp:
            if resp.status == 200:
                about = await resp.json()
                if about.get("name") and about.get("email"):
                    results.add_result("About GET public", True, f"About data: {about.get('name')}")
                else:
                    results.add_result("About GET public", False, f"Missing required fields: {about}")
            else:
                text = await resp.text()
                results.add_result("About GET public", False, f"Status {resp.status}: {text}")
    except Exception as e:
        results.add_result("About GET public", False, f"Exception: {e}")
    
    # Test PUT /about with auth
    if results.auth_token:
        headers = {"Authorization": f"Bearer {results.auth_token}"}
        try:
            about_data = {
                "name": "Alex Vantage",
                "role": "Full Stack Developer",
                "tagline": "Building the future with code",
                "bio": ["Passionate developer", "AI enthusiast"],
                "location": "San Francisco, CA",
                "email": "alex@portfolio.dev",
                "available": True,
                "stats": [
                    {"label": "Projects", "value": "50", "suffix": "+"},
                    {"label": "Experience", "value": "5", "suffix": " years"}
                ],
                "socials": {
                    "github": "https://github.com/alexvantage",
                    "linkedin": "https://linkedin.com/in/alexvantage"
                }
            }
            async with session.put(f"{BASE_URL}/about", json=about_data, headers=headers) as resp:
                if resp.status == 200:
                    about = await resp.json()
                    if about.get("name") == about_data["name"]:
                        results.add_result("About PUT with auth", True, "About updated successfully")
                    else:
                        results.add_result("About PUT with auth", False, f"Update failed: {about}")
                else:
                    text = await resp.text()
                    results.add_result("About PUT with auth", False, f"Status {resp.status}: {text}")
        except Exception as e:
            results.add_result("About PUT with auth", False, f"Exception: {e}")

async def test_contact_endpoints(session: aiohttp.ClientSession, results: TestResults):
    """Test contact and messages endpoints"""
    print("\n=== Testing Contact & Messages ===")
    
    created_message_id = None
    
    # Test POST /contact (public)
    try:
        contact_data = {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "subject": "Test Contact Form",
            "body": "This is a test message from the API testing suite."
        }
        async with session.post(f"{BASE_URL}/contact", json=contact_data) as resp:
            if resp.status == 201:
                message = await resp.json()
                created_message_id = message.get("id")
                if message.get("name") == contact_data["name"]:
                    results.add_result("Contact POST", True, f"Message created: {created_message_id}")
                else:
                    results.add_result("Contact POST", False, f"Data mismatch: {message}")
            else:
                text = await resp.text()
                results.add_result("Contact POST", False, f"Status {resp.status}: {text}")
    except Exception as e:
        results.add_result("Contact POST", False, f"Exception: {e}")
    
    if results.auth_token:
        headers = {"Authorization": f"Bearer {results.auth_token}"}
        
        # Test GET /messages (admin)
        try:
            async with session.get(f"{BASE_URL}/messages", headers=headers) as resp:
                if resp.status == 200:
                    messages = await resp.json()
                    if isinstance(messages, list) and len(messages) >= 1:
                        results.add_result("Messages GET admin", True, f"Found {len(messages)} messages")
                    else:
                        results.add_result("Messages GET admin", False, f"Expected list with >=1 items: {messages}")
                else:
                    text = await resp.text()
                    results.add_result("Messages GET admin", False, f"Status {resp.status}: {text}")
        except Exception as e:
            results.add_result("Messages GET admin", False, f"Exception: {e}")
        
        # Test PATCH /messages/{id}/read (admin)
        if created_message_id:
            try:
                async with session.patch(f"{BASE_URL}/messages/{created_message_id}/read", headers=headers) as resp:
                    if resp.status == 200:
                        message = await resp.json()
                        if message.get("read") is True:
                            results.add_result("Messages PATCH read", True, "Message marked as read")
                        else:
                            results.add_result("Messages PATCH read", False, f"Read status not updated: {message}")
                    else:
                        text = await resp.text()
                        results.add_result("Messages PATCH read", False, f"Status {resp.status}: {text}")
            except Exception as e:
                results.add_result("Messages PATCH read", False, f"Exception: {e}")
        
        # Test DELETE /messages/{id} (admin)
        if created_message_id:
            try:
                async with session.delete(f"{BASE_URL}/messages/{created_message_id}", headers=headers) as resp:
                    if resp.status == 200:
                        result = await resp.json()
                        if result.get("ok"):
                            results.add_result("Messages DELETE", True, "Message deleted successfully")
                        else:
                            results.add_result("Messages DELETE", False, f"Delete failed: {result}")
                    else:
                        text = await resp.text()
                        results.add_result("Messages DELETE", False, f"Status {resp.status}: {text}")
            except Exception as e:
                results.add_result("Messages DELETE", False, f"Exception: {e}")
    
    # Test rate limiting (5/minute)
    print("Testing rate limiting (this may take a moment)...")
    try:
        contact_data = {
            "name": "Rate Test",
            "email": "rate@test.com",
            "subject": "Rate Limit Test",
            "body": "Testing rate limiting"
        }
        
        rate_limit_hit = False
        for i in range(6):  # Try 6 requests quickly
            async with session.post(f"{BASE_URL}/contact", json=contact_data) as resp:
                if resp.status == 429:
                    rate_limit_hit = True
                    break
                elif resp.status != 201:
                    break
                # Small delay to avoid overwhelming
                await asyncio.sleep(0.1)
        
        if rate_limit_hit:
            results.add_result("Contact rate limiting", True, "Rate limit triggered after multiple requests")
        else:
            results.add_result("Contact rate limiting", False, "Rate limit not triggered")
    except Exception as e:
        results.add_result("Contact rate limiting", False, f"Exception: {e}")

async def test_ai_endpoints(session: aiohttp.ClientSession, results: TestResults):
    """Test AI chat endpoints - CRITICAL"""
    print("\n=== Testing AI Chat (CRITICAL) ===")
    
    session_id = "test-session-abc"
    
    # Test first AI chat message
    try:
        chat_data = {
            "session_id": session_id,
            "message": "Which of your projects uses Three.js?"
        }
        async with session.post(f"{BASE_URL}/ai/chat", json=chat_data) as resp:
            if resp.status == 200:
                response = await resp.json()
                reply = response.get("reply", "")
                if reply and len(reply.strip()) > 0:
                    # Check if reply mentions expected projects
                    if "Nebula Commerce" in reply or "Signal Garden" in reply or "Three.js" in reply:
                        results.add_result("AI Chat first turn", True, f"Reply mentions relevant projects: {reply[:100]}...")
                    else:
                        results.add_result("AI Chat first turn", True, f"Got non-empty reply: {reply[:100]}...")
                else:
                    results.add_result("AI Chat first turn", False, f"Empty or missing reply: {response}")
            elif resp.status == 502:
                text = await resp.text()
                results.add_result("AI Chat first turn", False, f"LLM error (502): {text}")
            else:
                text = await resp.text()
                results.add_result("AI Chat first turn", False, f"Status {resp.status}: {text}")
    except Exception as e:
        results.add_result("AI Chat first turn", False, f"Exception: {e}")
    
    # Test second AI chat message (same session)
    try:
        chat_data = {
            "session_id": session_id,
            "message": "Tell me more about the first one."
        }
        async with session.post(f"{BASE_URL}/ai/chat", json=chat_data) as resp:
            if resp.status == 200:
                response = await resp.json()
                reply = response.get("reply", "")
                if reply and len(reply.strip()) > 0:
                    results.add_result("AI Chat second turn", True, f"Got contextual reply: {reply[:100]}...")
                else:
                    results.add_result("AI Chat second turn", False, f"Empty or missing reply: {response}")
            elif resp.status == 502:
                text = await resp.text()
                results.add_result("AI Chat second turn", False, f"LLM error (502): {text}")
            else:
                text = await resp.text()
                results.add_result("AI Chat second turn", False, f"Status {resp.status}: {text}")
    except Exception as e:
        results.add_result("AI Chat second turn", False, f"Exception: {e}")
    
    # Test GET /ai/history/{session_id}
    try:
        async with session.get(f"{BASE_URL}/ai/history/{session_id}") as resp:
            if resp.status == 200:
                history = await resp.json()
                turns = history.get("history", [])
                if len(turns) >= 4:  # 2 user + 2 assistant
                    results.add_result("AI Chat history", True, f"Found {len(turns)} turns in history")
                else:
                    results.add_result("AI Chat history", False, f"Expected >=4 turns, got {len(turns)}: {turns}")
            else:
                text = await resp.text()
                results.add_result("AI Chat history", False, f"Status {resp.status}: {text}")
    except Exception as e:
        results.add_result("AI Chat history", False, f"Exception: {e}")

async def test_analytics_endpoints(session: aiohttp.ClientSession, results: TestResults):
    """Test analytics endpoints"""
    print("\n=== Testing Analytics ===")
    
    # Test POST /analytics/event (public)
    try:
        event_data = {
            "type": "page_view",
            "path": "/",
            "meta": {"test": True}
        }
        async with session.post(f"{BASE_URL}/analytics/event", json=event_data) as resp:
            if resp.status == 201:
                event = await resp.json()
                if event.get("type") == event_data["type"]:
                    results.add_result("Analytics POST event", True, f"Event created: {event.get('id')}")
                else:
                    results.add_result("Analytics POST event", False, f"Type mismatch: {event}")
            else:
                text = await resp.text()
                results.add_result("Analytics POST event", False, f"Status {resp.status}: {text}")
    except Exception as e:
        results.add_result("Analytics POST event", False, f"Exception: {e}")
    
    # Test GET /analytics without auth (should fail)
    try:
        async with session.get(f"{BASE_URL}/analytics") as resp:
            if resp.status == 401:
                results.add_result("Analytics GET without auth", True, "Correctly returned 401")
            else:
                text = await resp.text()
                results.add_result("Analytics GET without auth", False, 
                                 f"Expected 401, got {resp.status}: {text}")
    except Exception as e:
        results.add_result("Analytics GET without auth", False, f"Exception: {e}")
    
    # Test GET /analytics with admin auth
    if results.auth_token:
        headers = {"Authorization": f"Bearer {results.auth_token}"}
        try:
            async with session.get(f"{BASE_URL}/analytics", headers=headers) as resp:
                if resp.status == 200:
                    summary = await resp.json()
                    if (summary.get("total_events", 0) >= 1 and 
                        "by_type" in summary and 
                        "last_7_days" in summary and 
                        "recent" in summary):
                        page_views = summary["by_type"].get("page_view", 0)
                        results.add_result("Analytics GET admin", True, 
                                         f"Summary: {summary['total_events']} events, {page_views} page_views")
                    else:
                        results.add_result("Analytics GET admin", False, f"Missing fields: {summary}")
                else:
                    text = await resp.text()
                    results.add_result("Analytics GET admin", False, f"Status {resp.status}: {text}")
        except Exception as e:
            results.add_result("Analytics GET admin", False, f"Exception: {e}")

async def test_uploads_endpoints(session: aiohttp.ClientSession, results: TestResults):
    """Test file upload endpoints"""
    print("\n=== Testing Uploads ===")
    
    # Test POST /uploads without auth (should fail)
    try:
        # Create a tiny PNG file
        png_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\tpHYs\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00\x00\nIDATx\x9cc\xf8\x00\x00\x00\x01\x00\x01\x00\x00\x00\x00IEND\xaeB`\x82'
        
        data = aiohttp.FormData()
        data.add_field('file', BytesIO(png_data), filename='test.png', content_type='image/png')
        
        async with session.post(f"{BASE_URL}/uploads", data=data) as resp:
            if resp.status == 401:
                results.add_result("Uploads POST without auth", True, "Correctly returned 401")
            else:
                text = await resp.text()
                results.add_result("Uploads POST without auth", False, 
                                 f"Expected 401, got {resp.status}: {text}")
    except Exception as e:
        results.add_result("Uploads POST without auth", False, f"Exception: {e}")
    
    uploaded_filename = None
    uploaded_url = None
    
    if results.auth_token:
        headers = {"Authorization": f"Bearer {results.auth_token}"}
        
        # Test POST /uploads with auth and valid PNG
        try:
            png_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\tpHYs\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00\x00\nIDATx\x9cc\xf8\x00\x00\x00\x01\x00\x01\x00\x00\x00\x00IEND\xaeB`\x82'
            
            data = aiohttp.FormData()
            data.add_field('file', BytesIO(png_data), filename='test.png', content_type='image/png')
            
            async with session.post(f"{BASE_URL}/uploads", data=data, headers=headers) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    uploaded_filename = result.get("filename")
                    uploaded_url = result.get("url")
                    if uploaded_filename and uploaded_url:
                        results.add_result("Uploads POST with auth", True, 
                                         f"File uploaded: {uploaded_filename}")
                    else:
                        results.add_result("Uploads POST with auth", False, f"Missing fields: {result}")
                else:
                    text = await resp.text()
                    results.add_result("Uploads POST with auth", False, f"Status {resp.status}: {text}")
        except Exception as e:
            results.add_result("Uploads POST with auth", False, f"Exception: {e}")
        
        # Test POST /uploads with invalid extension
        try:
            data = aiohttp.FormData()
            data.add_field('file', BytesIO(b'fake exe content'), filename='malware.exe', content_type='application/octet-stream')
            
            async with session.post(f"{BASE_URL}/uploads", data=data, headers=headers) as resp:
                if resp.status == 400:
                    results.add_result("Uploads POST invalid extension", True, "Correctly rejected .exe file")
                else:
                    text = await resp.text()
                    results.add_result("Uploads POST invalid extension", False, 
                                     f"Expected 400, got {resp.status}: {text}")
        except Exception as e:
            results.add_result("Uploads POST invalid extension", False, f"Exception: {e}")
    
    # Test GET uploaded file
    if uploaded_filename:
        try:
            async with session.get(f"{BASE_URL}/uploads/{uploaded_filename}") as resp:
                if resp.status == 200:
                    content = await resp.read()
                    if len(content) > 0:
                        results.add_result("Uploads GET file", True, f"File served: {len(content)} bytes")
                    else:
                        results.add_result("Uploads GET file", False, "Empty file content")
                else:
                    text = await resp.text()
                    results.add_result("Uploads GET file", False, f"Status {resp.status}: {text}")
        except Exception as e:
            results.add_result("Uploads GET file", False, f"Exception: {e}")

async def main():
    """Run all backend tests"""
    print(f"Starting Portfolio Backend API Tests")
    print(f"Base URL: {BASE_URL}")
    print(f"Admin: {ADMIN_EMAIL}")
    
    results = TestResults()
    
    # Create session with timeout
    timeout = aiohttp.ClientTimeout(total=30)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        # Test all endpoints
        await test_auth_endpoints(session, results)
        await test_projects_endpoints(session, results)
        await test_skills_endpoints(session, results)
        await test_about_endpoints(session, results)
        await test_contact_endpoints(session, results)
        await test_ai_endpoints(session, results)
        await test_analytics_endpoints(session, results)
        await test_uploads_endpoints(session, results)
    
    # Print summary
    results.summary()
    
    # Return results for programmatic access
    return results

if __name__ == "__main__":
    asyncio.run(main())