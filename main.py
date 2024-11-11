import json
import os
import shutil
import tkinter as tk
import tkinter.messagebox
from tkinter import filedialog
from tkinter import simpledialog

VERSION = "1.0.0" # dont forget to increment this
WINDOW_TITLE = "duzo desktop generator :)" + " v" + VERSION

OUTPUT_DIR = "./output/"
ASSETS_DIR = OUTPUT_DIR + "resourcepack/"
DATA_DIR = OUTPUT_DIR + "datapack/"

DEFAULT_ICON = "./assets/icon.png"

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
        "watermark": WINDOW_TITLE,
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

def CreateRequiredPaths(output_path : str, namespace : str):
    # Resource pack folders
    CreateFolder(output_path + "resourcepack/assets/" + namespace + "/textures/desktop")

    # Generating datapack folders
    CreateFolder(output_path + "datapack/data/" + namespace + "/desktop")
    CreateFolder(output_path + "datapack/data/" + namespace + "/structures/interiors")

def CreatePack(namespace : str, id : str, preview_path : str, nbt_path : str, output_path : str = OUTPUT_DIR):
    CreateRequiredPaths(output_path, namespace)

    CreateMcMeta(output_path + "resourcepack/")
    CreateMcMeta(output_path + "datapack/")
    CreateDesktopJson(namespace, id)

    CopyPreview(preview_path, namespace, id)
    CopyStructure(nbt_path, namespace, id)

def main():
    root = tk.Tk()
    root.withdraw()

    namespace = simpledialog.askstring(WINDOW_TITLE, "namespace")
    id = simpledialog.askstring(WINDOW_TITLE, "desktop id")
    nbt_path = filedialog.askopenfilename(filetypes=[("NBT files", "*.nbt")], title="Select structure file")
    preview_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")], title="Select desktop preview")

    if preview_path == "":
        tkinter.messagebox.showinfo(WINDOW_TITLE, "No preview selected, using default icon")
        preview_path = DEFAULT_ICON

        if not os.path.exists(preview_path):
            tkinter.messagebox.showerror(WINDOW_TITLE, "Default icon not found, does resources folder exist? (./assets/icon.png)")
            return

    if nbt_path == "":
        tkinter.messagebox.showerror(WINDOW_TITLE, "No structure file selected")
        return

    CreatePack(namespace, id, preview_path, nbt_path)

    # open file explorer at output
    os.startfile(os.getcwd() + "/output")

if __name__ == '__main__':
    main()