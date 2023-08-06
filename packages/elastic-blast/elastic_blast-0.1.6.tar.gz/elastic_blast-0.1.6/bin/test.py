import os
import subprocess

cmd = os.path.join(os.path.dirname(__file__), 'test.sh')
print(cmd)

subprocess.run(['bash', cmd])
