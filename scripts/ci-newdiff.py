import subprocess
import os
import json

proc = subprocess.run(["git", "diff", "--diff-filter=d", "--name-only", "HEAD~", "HEAD"],
                      text=True,
                      capture_output=True,
                      check=True)

files = proc.stdout.splitlines()

file_data = {
    "include": [{
        "fname": filename,
        "fname_safe": filename.replace("/", "_"),
        "parent": os.path.dirname(filename),
    } for filename in files if filename.startswith("file")]
}

if len(file_data["include"]) == 0:
    raise Exception("No files were changed")

print(json.dumps(file_data))
