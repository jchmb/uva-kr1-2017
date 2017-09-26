import subprocess

p = subprocess.Popen(['minisat test test_out'], shell=True,
                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
r = p.communicate()

print(r[0].decode('ascii'))
