#!/usr/bin/env python3
"""
Script to view TSA API logs stored in Supabase
"""

from supabase import create_client, Client
from datetime import datetime
import json

# Supabase configuration
SUPABASE_URL = "https://kyudboffpfipzxlkzxam.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt5dWRib2ZmcGZpcHp4bGt6eGFtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDkzMTk3OTgsImV4cCI6MjA2NDg5NTc5OH0.BzJlk8x56I5IPg4S78aVlhm2-bWk3UYr4yh3AuM9vXc"

def view_tsa_logs():
    """Fetch and display TSA API logs from Supabase"""
    
    # Initialize Supabase client
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    try:
        # Fetch all logs ordered by creation time (most recent first)
        response = supabase.table("tsa_api_logs").select("*").order("created_at", desc=True).execute()
        
        logs = response.data
        
        if not logs:
            print("📭 No logs found in the database.")
            return
        
        print(f"📊 Found {len(logs)} API call logs:")
        print("=" * 80)
        
        for i, log in enumerate(logs, 1):
            created_at = datetime.fromisoformat(log['created_at'].replace('Z', '+00:00'))
            
            print(f"\n{i}. 🕐 {created_at.strftime('%Y-%m-%d %H:%M:%S UTC')}")
            print(f"   📦 Item: {log['item_name']}")
            print(f"   ✈️  Carry-on: {'✅ Yes' if log['carry_on'] else '❌ No'}")
            print(f"   🧳 Checked bag: {'✅ Yes' if log['checked_bag'] else '❌ No'}")
            print(f"   📝 Description: {log['description']}")
            print(f"   ⏱️  Response time: {log['response_time_ms']}ms")
            if log['user_agent']:
                print(f"   🖥️  User agent: {log['user_agent'][:50]}...")
            print("-" * 80)
            
    except Exception as e:
        print(f"❌ Error fetching logs: {str(e)}")

def get_stats():
    """Get some basic statistics about the API usage"""
    
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    try:
        # Get total count
        total_response = supabase.table("tsa_api_logs").select("id", count="exact").execute()
        total_calls = total_response.count
        
        # Get average response time
        avg_response = supabase.rpc("avg_response_time", {}).execute()
        
        # Get most searched items
        popular_items = supabase.table("tsa_api_logs").select("item_name").order("created_at", desc=True).limit(10).execute()
        
        print("\n📈 API Usage Statistics:")
        print("=" * 40)
        print(f"🔢 Total API calls: {total_calls}")
        
        if popular_items.data:
            print(f"🔥 Recent searches: {', '.join([item['item_name'] for item in popular_items.data[:5]])}")
        
    except Exception as e:
        print(f"❌ Error getting stats: {str(e)}")

if __name__ == "__main__":
    view_tsa_logs()
    get_stats() 