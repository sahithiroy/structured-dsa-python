import os
import py_compile

src_dir = "src"  # Change this if needed

for root, _, files in os.walk(src_dir):
    for file in files:
        if file.endswith(".py"):
            file_path = os.path.join(root, file)
            try:
                py_compile.compile(file_path, doraise=True)
                print(f"✅ {file_path} - No syntax errors")
            except py_compile.PyCompileError as e:
                print(f"❌ Syntax error in {file_path}:\n{e}")
