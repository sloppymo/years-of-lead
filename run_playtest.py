#!/usr/bin/env python3
"""
Years of Lead - Playtest Launcher

Quick launcher for testing mission failures and cascading effects
"""

import subprocess
import sys
import os


def print_menu():
    print("\n" + "🎮" * 25)
    print("YEARS OF LEAD - PLAYTEST LAUNCHER")
    print("🎮" * 25)
    print("\n🎯 Choose your testing approach:")
    print()
    print("1. 🎮 Manual CLI Playthrough")
    print("   Interactive testing using the CLI interface")
    print("   Follow the detailed guide in CLI_PLAYTEST_GUIDE.md")
    print()
    print("2. 🤖 Enhanced Automated Testing")
    print("   Comprehensive automated testing with real game systems")
    print("   Tests missions, emotions, cascading effects, multi-agent scenarios")
    print()
    print("3. 📊 Legacy Automated Analysis")
    print("   Original automated simulation (basic version)")
    print("   Generates statistical analysis and patterns")
    print()
    print("4. 📋 View Playtest Guide")
    print("   Display the comprehensive testing guide")
    print()
    print("5. 🔄 Run All Tests")
    print("   Enhanced automated testing followed by manual testing")
    print()
    print("6. ❌ Exit")


def run_manual_cli():
    """Launch the manual CLI playthrough"""
    print("\n🎮 Launching Manual CLI Playthrough...")
    print("=" * 50)
    print("Follow the guide in CLI_PLAYTEST_GUIDE.md for systematic testing")
    print("Key focus areas:")
    print("  • Mission failure scenarios")
    print("  • Emotional impact on agents")
    print("  • Cascading effects across network")
    print("  • Dynamic narrative generation")
    print()
    
    try:
        # Try to launch the main CLI
        subprocess.run([sys.executable, "main.py", "--mode", "cli"])
    except FileNotFoundError:
        print("❌ Could not find main.py")
        print("Make sure you're in the Years of Lead root directory")
    except Exception as e:
        print(f"❌ Error launching CLI: {e}")


def run_enhanced_automated_testing():
    """Launch the enhanced automated testing system"""
    print("\n🤖 Launching Enhanced Automated Testing...")
    print("=" * 60)
    print("This will run comprehensive tests including:")
    print("• Mission failure scenarios with real game systems")
    print("• Emotional state impact tracking")
    print("• Multi-agent interaction testing")
    print("• Cascading effects analysis")
    print("• System stability and performance testing")
    print("=" * 60)
    
    try:
        subprocess.run([sys.executable, "automated_failure_analysis.py"])
    except FileNotFoundError:
        print("❌ Could not find automated_failure_analysis.py")
    except Exception as e:
        print(f"❌ Error running enhanced testing: {e}")

def run_legacy_automated_analysis():
    """Launch the legacy automated failure analysis"""
    print("\n📊 Launching Legacy Automated Analysis...")
    print("=" * 50)
    print("Running basic simulation-based testing...")
    
    try:
        # Create a simple legacy analyzer for backwards compatibility
        import json
        import random
        from datetime import datetime
        
        print("🔄 Running legacy simulation...")
        results = {"missions": [], "analysis": {}}
        
        for i in range(5):
            outcome = "FAILURE" if random.random() < 0.4 else "SUCCESS"
            results["missions"].append({
                "mission_id": i,
                "outcome": outcome,
                "stress_impact": random.randint(10, 30) if outcome == "FAILURE" else random.randint(-5, 5),
                "timestamp": datetime.now().isoformat()
            })
            print(f"  Mission {i+1}: {outcome}")
        
        # Basic analysis
        failures = [m for m in results["missions"] if m["outcome"] == "FAILURE"]
        results["analysis"] = {
            "failure_rate": len(failures) / len(results["missions"]),
            "total_stress_impact": sum(m["stress_impact"] for m in results["missions"]),
            "cascade_detected": len(failures) >= 3
        }
        
        print(f"\n📊 Legacy Analysis Results:")
        print(f"   Failure Rate: {results['analysis']['failure_rate']:.1%}")
        print(f"   Total Stress Impact: {results['analysis']['total_stress_impact']}")
        print(f"   Cascade Detected: {results['analysis']['cascade_detected']}")
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"legacy_analysis_{timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n💾 Results saved to {filename}")
        
    except Exception as e:
        print(f"❌ Error running legacy analysis: {e}")


def view_guide():
    """Display the playtest guide"""
    print("\n📋 PLAYTEST GUIDE OVERVIEW")
    print("=" * 50)
    
    guide_file = "CLI_PLAYTEST_GUIDE.md"
    if os.path.exists(guide_file):
        print(f"📖 Full guide available in: {guide_file}")
        print("\n🎯 Quick Summary:")
        print("Phase 1: Baseline Assessment (10-15 min)")
        print("  • Check initial agent status and emotional states")
        print("  • Note faction resources and network stress")
        print()
        print("Phase 2: Mission Failure Testing (20-30 min)")
        print("  • Create high-risk sabotage missions")
        print("  • Assign stressed/traumatized agents")
        print("  • Document failure consequences")
        print()
        print("Phase 3: Psychological Impact Analysis (15-20 min)")
        print("  • Track emotional state changes")
        print("  • Monitor stress progression")
        print("  • Document behavioral changes")
        print()
        print("Phase 4: Cascading Effects Documentation (15-25 min)")
        print("  • Track network-wide impacts")
        print("  • Test recovery scenarios")
        print("  • Analyze cascade amplification")
        print()
        print(f"📖 Read the full guide in {guide_file} for detailed instructions")
    else:
        print(f"❌ Guide file {guide_file} not found")


def run_all_tests():
    """Run enhanced automated testing followed by manual testing"""
    print("\n🔄 Running Complete Testing Suite...")
    print("=" * 60)
    print("Step 1: Enhanced automated testing for comprehensive analysis")
    print("Step 2: Manual CLI testing for detailed observation")
    print()
    
    input("Press Enter to start enhanced automated testing...")
    run_enhanced_automated_testing()
    
    print("\n" + "=" * 60)
    print("Enhanced automated testing complete!")
    print("Now switching to manual CLI testing for hands-on verification...")
    input("Press Enter to launch CLI interface...")
    
    run_manual_cli()


def main():
    """Main launcher interface"""
    
    while True:
        print_menu()
        
        choice = input("\nSelect option (1-6): ").strip()
        
        if choice == "1":
            run_manual_cli()
        elif choice == "2":
            run_enhanced_automated_testing()
        elif choice == "3":
            run_legacy_automated_analysis()
        elif choice == "4":
            view_guide()
        elif choice == "5":
            run_all_tests()
        elif choice == "6":
            print("\n👋 Happy testing! May your failures be educational and your bugs be squashed!")
            break
        else:
            print("❌ Invalid choice. Please select 1-6.")
        
        if choice in ["1", "2", "3", "5"]:
            input("\nPress Enter to return to menu...")


if __name__ == "__main__":
    main() 