from . import File_encryption as ENC
import os

def NewDir(path):
    new=f"os.makedirs({path})"
    return new

def packs(mes):
    e=ENC.ENC()
    e.enc(fr'{mes}')

class Pack:
    def __init__(self):
        self.cd={}
    def main(self, pathfile):
        p,f=os.path.split(pathfile)
        PakeName=f
        p,f=os.path.split(pathfile)
        if os.path.exists(pathfile) == True:
            with open(fr"{f}.py", 'w+', encoding="utf-8") as f:
                dirss=NewDir(f"'{PakeName}'")
                f.write(f"import os\n{dirss}")
                for path,dirs,file in os.walk(pathfile):
                    print(dirs)
                    print(file)
                    if dirs:
                        print("不支持打包子文件夹 Package subfolders are not supported")
                        break
                    else:
                        for fi in file:
                            with open(rf"{pathfile}\{fi}", 'r', encoding="utf-8")as i:
                                reads=i.read()
                                newfile=f"""
\nwith open(r'{PakeName}\{fi}', 'w')as w:
    w.write('''{reads}''')"""
                                f.write(f"{newfile}")
            print(fr'{os.getcwd()}\{PakeName}.py')
            packs(fr'{os.getcwd()}\{PakeName}.py')
        else:
            print(f"ErrorPath:This {pathfile} path does not exist!")
