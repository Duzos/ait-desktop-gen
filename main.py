import os, json, shutil
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog

WINDOW_TITLE = "duzo desktop generator :)"

OUTPUT_DIR = "./output/"
ASSETS_DIR = OUTPUT_DIR + "resourcepack/"
DATA_DIR = OUTPUT_DIR + "datapack/"

def CopyFile(source_path : str, target_path : str):
    try:
        shutil.copyfile(source_path, target_path)
        return True
    except Exception as e:
        print(e)
        return False

def CreateFolder(path : str):
    try:
        os.makedirs(path, 0o666, exist_ok=True)
        return True
    except Exception as e:
        print(e)
        return False

def CreateMcMeta(path : str, description: str = "Made with Duzos\'s generator"):
    meta = {
        "pack": {
            "pack_format": 15,
            "description": description
        }
    }

    with open(path + "pack.mcmeta", 'w', encoding='utf-8') as f:
        json.dump(meta, f, ensure_ascii=False, indent=4)

def CreateDesktopJson(namespace : str, id : str, data_path : str = DATA_DIR):
    data = {
        "id": namespace + ":" + id
    }

    with open(data_path + "/data/" + namespace + "/desktop/" + id + ".json", 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def CopyPreview(source_path : str, namespace : str, id : str, output_path : str = OUTPUT_DIR):
    CopyFile(source_path, output_path + "resourcepack/assets/" + namespace + "/textures/desktop/" + id + ".png")
    CopyFile(source_path, output_path + "resourcepack/pack.png")
    CopyFile(source_path, output_path + "datapack/pack.png")

def CopyStructure(source_path : str, namespace : str, id : str, output_path : str = OUTPUT_DIR):
    CopyFile(source_path, output_path + "datapack/data/" + namespace + "/structures/interiors/" + id + ".nbt")

def CreateRequiredPaths(output_path : str, namespace : str, desktop_id : str):
    # Resource pack folders
    CreateFolder(output_path + "resourcepack/assets/" + namespace + "/textures/desktop")

    # Generating datapack folders
    CreateFolder(output_path + "datapack/data/" + namespace + "/desktop")
    CreateFolder(output_path + "datapack/data/" + namespace + "/structures/interiors")
    
def CreatePack(namespace : str, id : str, preview_path : str, nbt_path : str, output_path : str = OUTPUT_DIR):
    CreateRequiredPaths(output_path, namespace, id)

    CreateMcMeta(output_path + "resourcepack/")
    CreateMcMeta(output_path + "datapack/")
    CreateDesktopJson(namespace, id)

    CopyPreview(preview_path, namespace, id)
    CopyStructure(nbt_path, namespace, id)

def main():
    root = tk.Tk()
    root.withdraw()

    namespace = simpledialog.askstring(WINDOW_TITLE, "Namespace")
    id = simpledialog.askstring(WINDOW_TITLE, "Desktop id")
    preview_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")], title="Select desktop preview")
    nbt_path = filedialog.askopenfilename(filetypes=[("NBT files", "*.nbt")], title="Select structure file")

    CreatePack(namespace, id, preview_path, nbt_path)

    # open file explorer at output
    os.startfile(os.getcwd() + "/output")

if (__name__ == '__main__'):
    main()