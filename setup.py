"""
EduHub MongoDB Project Setup Script
Installs required dependencies and sets up the environment
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ Successfully installed {package}")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Failed to install {package}")
        return False

def main():
    print("🚀 EduHub MongoDB Project Setup")
    print("=" * 50)
    
    # Required packages
    packages = [
        "pymongo>=4.0.0",
        "pandas>=1.3.0",
        "faker>=13.0.0",
        "jupyter>=1.0.0",
        "notebook>=6.0.0"
    ]
    
    print("\n📦 Installing required packages...")
    
    success_count = 0
    for package in packages:
        if install_package(package):
            success_count += 1
    
    print(f"\n📊 Installation Summary:")
    print(f"   • Successfully installed: {success_count}/{len(packages)} packages")
    
    if success_count == len(packages):
        print("\n✅ All packages installed successfully!")
        print("\n🎯 Next steps:")
        print("   1. Update the MongoDB connection string in the notebook")
        print("   2. Ensure MongoDB is running")
        print("   3. Run: jupyter notebook notebooks/eduhub_mongodb_project.ipynb")
        print("   4. Execute all cells to see the complete implementation")
        
        print("\n📝 Connection String Examples:")
        print("   • Local MongoDB: 'mongodb://localhost:27017/'")
        print("   • MongoDB Atlas: 'mongodb+srv://username:password@cluster.mongodb.net/'")
        
    else:
        print("\n⚠️ Some packages failed to install. Please install them manually:")
        print("   pip install pymongo pandas faker jupyter notebook")
    
    print(f"\n📂 Project structure created in: {os.getcwd()}")
    print("🎉 Setup complete! Happy coding!")

if __name__ == "__main__":
    main()
