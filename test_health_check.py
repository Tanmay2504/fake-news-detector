"""
Quick test to verify the health check system works
"""

def test_health_check():
    """Test the health check function"""
    print("Testing Health Check System...\n")
    
    # Import and run the check
    import sys
    import os
    sys.path.insert(0, os.path.dirname(__file__))
    
    # Try to import colorama
    try:
        from colorama import init
        init(autoreset=True)
        print("✓ Colorama installed")
    except ImportError:
        print("✗ Colorama not installed - installing now...")
        import subprocess
        subprocess.run([sys.executable, "-m", "pip", "install", "colorama"])
        from colorama import init
        init(autoreset=True)
    
    # Import main.py health check
    from main import check_system_health
    
    print("\nRunning comprehensive health check...\n")
    health = check_system_health()
    
    print("\n" + "="*70)
    print("Health Check Test Complete!")
    print("="*70)
    
    if health["overall"]:
        print("✓ System is operational")
    else:
        print("⚠ System has issues that need attention")
    
    print(f"\nComponents checked: {len(health['components'])}")
    print(f"Components OK: {sum(1 for v in health['components'].values() if v)}")

if __name__ == "__main__":
    test_health_check()
