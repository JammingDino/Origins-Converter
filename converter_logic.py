# converter_logic.py

import os
import shutil
import json
import re
import zipfile
import tempfile

def sanitize_mod_id(name: str) -> str:
    """Sanitizes a string to be a valid mod ID."""
    s = name.lower().replace(" ", "_")
    s = re.sub(r'[^a-z0-9_\-]+', '', s)
    return s

def create_mod_jar(datapack_path: str, output_dir: str, metadata: dict, icon_path: str) -> str:
    """
    Creates a fully compliant Fabric mod JAR, including all necessary metadata files.
    """
    mod_id = metadata['id']
    mod_name = metadata['name']
    
    with tempfile.TemporaryDirectory() as build_dir:
        data_folder_in_jar = os.path.join(build_dir, "data")
        os.makedirs(data_folder_in_jar)

        source_data_folder = os.path.join(datapack_path, "data")
        if not os.path.isdir(source_data_folder):
            raise FileNotFoundError(f"Could not find a 'data' folder inside: {datapack_path}")
        
        for item_name in os.listdir(source_data_folder):
            source_item = os.path.join(source_data_folder, item_name)
            destination_item = os.path.join(data_folder_in_jar, item_name)
            if os.path.isdir(source_item):
                shutil.copytree(source_item, destination_item)
            else:
                shutil.copy2(source_item, destination_item)

        fabric_mod_json = {
            "schemaVersion": 1, "id": mod_id, "version": metadata['version'],
            "name": mod_name, "description": metadata['description'],
            "authors": [author.strip() for author in metadata['authors'].split(',')],
            "contact": {}, "license": metadata['license'], "environment": "*",
            "entrypoints": {"main": []}, "mixins": [],
            "depends": {
                "fabricloader": metadata['fabricloader_version'],
                "minecraft": metadata['minecraft_version']
            }
        }
        
        if icon_path and os.path.exists(icon_path):
            assets_folder = os.path.join(build_dir, "assets", mod_id)
            os.makedirs(assets_folder)
            shutil.copy2(icon_path, os.path.join(assets_folder, "icon.png"))
            fabric_mod_json["icon"] = f"assets/{mod_id}/icon.png"

        with open(os.path.join(build_dir, "fabric.mod.json"), "w") as f:
            json.dump(fabric_mod_json, f, indent=4)

        source_mcmeta = os.path.join(datapack_path, "pack.mcmeta")
        if os.path.exists(source_mcmeta):
            shutil.copy2(source_mcmeta, build_dir)

        meta_inf_dir = os.path.join(build_dir, "META-INF")
        os.makedirs(meta_inf_dir)
        with open(os.path.join(meta_inf_dir, "MANIFEST.MF"), "w") as f:
            f.write("Manifest-Version: 1.0\n")

        jar_filename = f"{sanitize_mod_id(mod_name)}-{metadata['version']}.jar"
        jar_path = os.path.join(output_dir, jar_filename)
        
        # --- THIS IS THE FIX ---
        with zipfile.ZipFile(jar_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(build_dir):
                # The missing inner loop is now here
                for file in files:
                    file_path = os.path.join(root, file)
                    archive_name = os.path.relpath(file_path, build_dir)
                    zipf.write(file_path, archive_name)

    return jar_path