# Datapack to Fabric Mod Converter

A simple yet powerful desktop tool for converting Minecraft datapacks into complete, working Fabric mods. This tool provides a clean user interface to automate the process of packaging your datapack into a distributable `.jar` mod file.

## Features

- **Modern GUI:** A clean and user-friendly interface built with CustomTkinter.
- **Direct `.jar` Export:** Packages your project directly into a mod `.jar` file, ready to be used.
- **Metadata Automation:** Automatically detects and uses the description from `pack.mcmeta` and the icon from `pack.png`.
- **Full Customization:** Easily edit the Mod ID, Mod Name, Version, Author, and other metadata before converting.
- **Correct File Structure:** Builds the JAR with the correct file paths (`data/`, `assets/`, `fabric.mod.json`, `pack.mcmeta`) for compatibility with the Fabric mod loader.
- **License Dropdown:** Includes a pre-populated list of common open-source software licenses to choose from.

## Installation

To run this tool, you need Python 3 installed on your system.

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2.  **Install the required dependencies:**
    This project uses `customtkinter`. You can install it easily using the `requirements.txt` file.
    ```sh
    pip install -r requirements.txt
    ```

## How to Use

1.  **Run the script:**
    ```sh
    python main.py
    ```

2.  Click **Browse...** to select your datapack's main folder. The tool will auto-fill the Mod Name, Mod ID, Description, and Icon.

3.  Review and edit the metadata in the input fields as needed.

4.  Select a license for your project from the dropdown menu.

5.  Click **Convert to Mod**.

6.  Your new mod `.jar` file will be saved in the `output` folder (or your chosen output directory). You can now drop this file into your Minecraft mods folder!

## Why Fabric Only?

This tool is designed specifically for Fabric because Fabric's mod-loading structure is flexible enough to load a datapack's contents directly from a JAR's resources without requiring any Java code. Converting a datapack for Forge is a more complex process and is not supported by this tool.

## License

The code for this tool is licensed under the MIT License. See the `LICENSE` file for details.
