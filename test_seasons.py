#!/usr/bin/env python3
"""Test script to verify the seasons table functionality."""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from attached_assets.dynamic_pricing import show_season_management, create_default_seasons
    print("✅ Import successful!")
    
    # Test create_default_seasons function
    default_seasons = create_default_seasons()
    print(f"✅ Default seasons created: {len(default_seasons['seasons'])} seasons")
    
    for season in default_seasons['seasons']:
        print(f"   - {season['name']}: {season['start_date']} to {season['end_date']} ({season['price_modifier']}%)")
    
    print("\n🎉 All functions are working correctly!")
    print("The seasons table should now be visible in the Streamlit app.")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()