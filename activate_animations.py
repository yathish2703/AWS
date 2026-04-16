#!/usr/bin/env python3
"""
AWS Learning Platform - Switch to Animated Design
Run this script to activate the new animated templates
"""

import os
import shutil
from datetime import datetime

def backup_file(filepath):
    """Create backup of original file"""
    if os.path.exists(filepath):
        backup_path = f"{filepath}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copy2(filepath, backup_path)
        print(f"✅ Backed up: {filepath} → {backup_path}")
        return True
    return False

def activate_animated_design():
    """Switch to animated design templates"""
    print("\n" + "="*60)
    print("🎨 AWS LEARNING PLATFORM - ANIMATED DESIGN ACTIVATION")
    print("="*60 + "\n")

    templates_dir = "templates"

    files_to_replace = [
        {
            'original': os.path.join(templates_dir, 'index.html'),
            'animated': os.path.join(templates_dir, 'index_animated.html')
        },
        {
            'original': os.path.join(templates_dir, 'lesson.html'),
            'animated': os.path.join(templates_dir, 'lesson_animated.html')
        }
    ]

    print("📦 Backing up original files...\n")
    for file_pair in files_to_replace:
        backup_file(file_pair['original'])

    print("\n🎨 Activating animated design...\n")
    for file_pair in files_to_replace:
        if os.path.exists(file_pair['animated']):
            shutil.copy2(file_pair['animated'], file_pair['original'])
            print(f"✅ Activated: {file_pair['animated']} → {file_pair['original']}")
        else:
            print(f"⚠️  Warning: {file_pair['animated']} not found")

    print("\n" + "="*60)
    print("🎉 ANIMATED DESIGN ACTIVATED!")
    print("="*60)
    print("\n✨ Your platform now includes:")
    print("  • Floating animations and particles")
    print("  • 3D card hover effects")
    print("  • Interactive AWS diagrams")
    print("  • Celebration effects (confetti, level up)")
    print("  • Smooth transitions and fades")
    print("  • Animated progress bars")
    print("  • Sound effects (optional)")
    print("\n🚀 Restart your Flask app to see the changes:")
    print("   python app.py")
    print("\n📖 Read ANIMATION_GUIDE.md for full documentation")
    print("\n💡 To restore original design, rename .backup files back\n")

def restore_original_design():
    """Restore original design from backups"""
    print("\n" + "="*60)
    print("🔄 RESTORING ORIGINAL DESIGN")
    print("="*60 + "\n")

    templates_dir = "templates"
    backup_files = [f for f in os.listdir(templates_dir) if f.endswith('.backup')]

    if not backup_files:
        print("⚠️  No backup files found")
        return

    for backup_file in backup_files:
        original_name = backup_file.split('.backup')[0]
        backup_path = os.path.join(templates_dir, backup_file)
        original_path = os.path.join(templates_dir, original_name)

        shutil.copy2(backup_path, original_path)
        print(f"✅ Restored: {backup_file} → {original_name}")

    print("\n✅ Original design restored!")
    print("🚀 Restart your Flask app to see the changes\n")

def show_menu():
    """Show interactive menu"""
    print("\n" + "="*60)
    print("🎨 AWS Learning Platform - Design Manager")
    print("="*60)
    print("\n1. Activate Animated Design (Recommended)")
    print("2. Restore Original Design")
    print("3. Show File Status")
    print("4. Exit")
    print("\n" + "="*60)

    choice = input("\nEnter your choice (1-4): ").strip()
    return choice

def show_file_status():
    """Show status of template files"""
    print("\n" + "="*60)
    print("📁 TEMPLATE FILES STATUS")
    print("="*60 + "\n")

    templates_dir = "templates"
    files_to_check = [
        'index.html',
        'index_animated.html',
        'lesson.html',
        'lesson_animated.html'
    ]

    for filename in files_to_check:
        filepath = os.path.join(templates_dir, filename)
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            modified = datetime.fromtimestamp(os.path.getmtime(filepath))
            print(f"✅ {filename}")
            print(f"   Size: {size:,} bytes")
            print(f"   Modified: {modified.strftime('%Y-%m-%d %H:%M:%S')}\n")
        else:
            print(f"❌ {filename} - NOT FOUND\n")

    # Check backup files
    backup_files = [f for f in os.listdir(templates_dir) if '.backup.' in f]
    if backup_files:
        print(f"\n📦 Found {len(backup_files)} backup file(s):")
        for backup in backup_files:
            print(f"   • {backup}")
    else:
        print("\n📦 No backup files found")

    print("\n" + "="*60 + "\n")

def main():
    """Main function"""
    if not os.path.exists("templates"):
        print("❌ Error: templates directory not found")
        print("💡 Please run this script from the project root directory")
        return

    while True:
        choice = show_menu()

        if choice == '1':
            activate_animated_design()
            break
        elif choice == '2':
            restore_original_design()
            break
        elif choice == '3':
            show_file_status()
        elif choice == '4':
            print("\n👋 Goodbye!\n")
            break
        else:
            print("\n⚠️  Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
