import glob, os
directory=input('Input Directory>>')
key=input('Input filename>>')   
os.chdir(directory)
for file in glob.glob("*.exe"):
    print(file)

