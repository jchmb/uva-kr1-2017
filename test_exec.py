import subprocess

p = subprocess.Popen(['./execminisat test'], shell=True)
r = p.communicate()

print(r)
print(r[0])
print(r[1])
