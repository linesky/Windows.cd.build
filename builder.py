import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
import subprocess
import shutil
import os



class BareboneBuilder:
    def __init__(self, root):
        self.root = root
        self.root.title("Barebone Builder")

        # Janela amarela
        self.root.configure(bg='red')

        # Área de texto
        self.text_area = tk.Text(self.root, height=10, width=50)
        self.text_area.pack(pady=10)

        # Botões
        self.build_button = tk.Button(self.root, text="Build", command=self.build_kernel)
        self.build_button.pack(pady=5)

        self.run_button = tk.Button(self.root, text="Run", command=self.run_kernel)
        self.run_button.pack(pady=5)

        self.copy_button = tk.Button(self.root, text="new file", command=self.copy_file)
        self.copy_button.pack(pady=5)

    def execute_command(self, command,show:bool):
        try:
            
            result = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True, text=True)
            self.text_area.insert(tk.END, result)
        except subprocess.CalledProcessError as e:
            if show:
                self.text_area.insert(tk.END,f"Error executing command:\n{e.output}")

    def build_kernel(self):
        filename = tk.filedialog.askopenfilename(title="Select file")
        self.text_area.delete(1.0, tk.END)
        self.execute_command("mkdir ./tmp",False)
        filename=filename.replace("/","\\")

        self.execute_command('cmd /c ""C:\\Program Files (x86)\\7-Zip\\7z.exe\" x -y ".\\file\\CD_root.zip" -o./tmp "',False)
        self.text_area.delete(1.0, tk.END)
        fff='cmd.exe /c "".\\file\\gcc.cmd" "$1""'.replace("$1",filename)
        self.execute_command(fff,True)
    
        filesn=True
        
        while filesn:
            nfilesn=filename.find("\\")
            nfilesn+=1
            if nfilesn>0:
                filename=filename[nfilesn:]
            else:

                filesn=False
        filename=filename.replace(".zip","")
        
        filename=filename.replace("/","\\")
        
       
        
        
        
        self.execute_command("copy .\\tmp\\hello.bin .\\tmp\\hello.c32",True)
        f3=open(".\\file\\head.o","rb")
        heads=f3.read()
        f3.close() 
        f4=open(".\\tmp\\hello.bin","rb+")
        f4.write(heads)
        f4.close()
        self.execute_command("copy  .\\tmp\\hello.bin .\\tmp\\CD_root\\isolinux\\hello.c32",True)     
       
       




        fff='.\\file\\mkisofs.exe -o .\\myos.iso -input-charset utf8 -b isolinux/isolinux.bin -no-emul-boot -boot-load-size 4  -boot-info-table .\\tmp\\CD_root'
        
        self.execute_command(fff,True)
    def run_kernel(self):
        self.text_area.delete(1.0, tk.END)
        self.execute_command("qemu-system-x86_64 -serial msmouse -cdrom myos.iso",True)


    def copy_file(self):
        self.text_area.delete(1.0, tk.END)
        filename = tk.filedialog.asksaveasfilename(title="Select file")
        if filename:
            shutil.copy( f".\file\new",filename+".c")
            self.text_area.insert(tk.END, f"File {filename} copied \n",True)


if __name__ == "__main__":
    root = tk.Tk()
    builder = BareboneBuilder(root)
    root.mainloop()
