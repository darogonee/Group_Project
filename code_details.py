import os


def list_files(extention=None):
    listed_files=[]
    for directory, paths, files in os.walk("."):
        for file in files:
            # no extention specified
            if extention is None:
                listed_files.append(os.path.join(directory, file))
            # is expected extention
            elif file.split(os.path.extsep)[-1]==extention:
                listed_files.append(os.path.join(directory, file))
    return listed_files

def count_chars(files):
    chars=0
    for file in files:
        with open(file, "rb") as reading:
            chars+=len(reading.read())
    return chars
            
def count_lines(files):
    chars=0
    for file in files:
        with open(file, "rb") as reading:
            chars+=len(reading.readlines())
    return chars
            
def sort_by_size(files):
    sorting_list=[]
    for file in files:
        with open(file, "rb") as reading:
            sorting_list.append((file, len(reading.read())))
    return sorted(sorting_list, key=lambda x:x[1])



def main_loop():
    while inp:=input("> "):
        command, *args = inp.split()
        if command == "list":
            files=[]
            if len(args)>0:
                files=list_files(args[0])
            else:
                files=list_files()
            print("\n".join(files))
            print(f"{len(files)} files retrieved")
        elif command == "bytes":
            files=[]
            if len(args)>0:
                files=list_files(args[0])
            else:
                files=list_files()
            total=count_chars(files)
            print(f"{total} bytes total")
        elif command == "sort":
            files=[]
            if len(args)>0:
                files=list_files(args[0])
            else:
                files=list_files()
            sorted_files=sort_by_size(files)
            print("\n".join(file+": "+str(size)+" bytes" for file, size in sorted_files))
        elif command == "lines":
            files=[]
            if len(args)>0:
                files=list_files(args[0])
            else:
                files=list_files()
            total=count_lines(files)
            print(f"{total} lines total")

main_loop()
