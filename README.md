## Description
A Minimalistic launch program for the much-loved Minecraft game.

## Required
Python >= 3.12

## Features
* **Customizable:** Configurations full of settings
* **Mod Support:** Fabric, Quilt, Forge

## Installation
1. **Download Python 3:** Get the latest version from the [python official website](https://www.python.org/downloads/).
   
3. **Clone the Repository:** Open your terminal and run:
   ```bash
   git clone https://github.com/kovadko/kovadko-minecraft-launcher.git
   ```
4. **Navigate to the created directory:**
   ```bash
   cd kovadko-minecraft-launcher
   ```
   
5. **Create a Virtual Environment:**
   ```python
   python3 -m venv .venv
   ```
  
6. **Activate the Virtual Environment:**
   * **Windows**
      ```bash
      .venv\bin\activate
      ```
      
   * **Linux/macOS**
      ```bash
      source .venv/bin/activate
      ```
    
7. **Install Dependencies:**
   ```python
   pip install -r requirements.txt
   ```
## Setting
**Open** the directory named: `configuration`.
> Make sure you are in the Launcher directory.

### command_args.json:
   * **Set** the value of the key: `“username”`
   > If not set, a random username will be generated.

   * **Set** the value of the key: `“gameDirectory”`
   > The destination directory should be named: .minecraft
      
## Run launcher
> Make sure you are in the Launcher directory and have the virtual environment enabled.

* **Run in terminal**
   ```bash
   python3 main.py
   ```
   
* **Click on the link**
http://127.0.0.1:5000

## Note
The first installation of minecraft will be noticeably long.