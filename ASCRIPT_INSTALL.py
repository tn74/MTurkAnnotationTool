def subprocess_cmd(command):
    process = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    print (proc_stdout)
print('Deploying Site... This may take a few minutes')
subprocess_cmd ('cd toWeb')
subprocess_cmd ('firebase init hosting') # Puts toWeb folder online at firebase