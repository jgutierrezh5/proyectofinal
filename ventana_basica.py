import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import webbrowser
import os

class MagicDustApp:
    def __init__(self, master):
        self.master = master
        self.ruta_archivo = None

        self.configurar_ventana()
        self.crear_area_texto()
        self.crear_barra_estado()
        self.crear_menus()
        self.actualizar_barra()


    def configurar_ventana(self):
        self.master.title("Magic Dust")
        self.master.geometry("800x550")
        self.master.configure(bg="#234e72")
        try:
            self.master.iconbitmap("icono.ico")
        except Exception:
            pass

 
    def crear_area_texto(self):
        self.area_texto = tk.Text(
            self.master,
            wrap="word",
            font=("Waltograph", 18),
            bg="#FDFEFE",
            fg="#212121",
            undo=True
        )
        self.area_texto.pack(expand=True, fill="both", padx=10, pady=10)
        self.area_texto.bind("<<Modified>>", self.actualizar_barra_event)


    def crear_barra_estado(self):
        self.barra_estado = tk.Label(
            self.master,
            text="0 caracteres",
            bg="#234e72",
            fg="white",
            anchor="w",
            padx=10
        )
        self.barra_estado.pack(side="bottom", fill="x")


    def crear_menus(self):
        menu_principal = tk.Menu(self.master)

        menu_archivo = tk.Menu(menu_principal, tearoff=0)
        menu_archivo.add_command(label="Abrir", command=self.abrir_archivo)
        menu_archivo.add_command(label="Guardar", command=self.guardar_archivo)
        menu_archivo.add_command(label="Guardar como", command=self.guardar_como)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Salir", command=self.master.quit)
        menu_principal.add_cascade(label="Archivo", menu=menu_archivo)

        menu_editar = tk.Menu(menu_principal, tearoff=0)
        menu_editar.add_command(label="Deshacer", command=self.area_texto.edit_undo)
        menu_editar.add_command(label="Rehacer", command=self.area_texto.edit_redo)
        menu_editar.add_separator()
        menu_editar.add_command(label="Buscar", command=self.buscar_palabra)
        menu_editar.add_separator()
        menu_editar.add_command(label="Copiar", command=lambda: self.master.focus_get().event_generate("<<Copy>>"))
        menu_editar.add_command(label="Cortar", command=lambda: self.master.focus_get().event_generate("<<Cut>>"))
        menu_editar.add_command(label="Pegar", command=lambda: self.master.focus_get().event_generate("<<Paste>>"))
        menu_principal.add_cascade(label="Editar", menu=menu_editar)

        menu_ayuda = tk.Menu(menu_principal, tearoff=0)
        menu_ayuda.add_command(label="Información", command=self.mostrar_informacion)
        menu_ayuda.add_command(label="Manual de usuario", command=self.abrir_manual)
        menu_ayuda.add_command(label="Integrantes", command=self.mostrar_integrantes)
        menu_principal.add_cascade(label="Ayuda", menu=menu_ayuda)

        self.master.config(menu=menu_principal)

        self.master.bind("<Control-o>", lambda e: self.abrir_archivo())
        self.master.bind("<Control-s>", lambda e: self.guardar_archivo())
        self.master.bind("<Control-f>", lambda e: self.buscar_palabra())


    def abrir_archivo(self):
        self.ruta_archivo = filedialog.askopenfilename(
            title="Abrir archivo",
            filetypes=[
                ("Archivos de texto", "*.txt"),
                ("Archivos Python", "*.py"),
                ("Archivos C++", "*.cpp"),
                ("Archivos C#", "*.cs"),
                ("Todos los archivos", "*.*")
            ]
        )
        if self.ruta_archivo:
            try:
                with open(self.ruta_archivo, "r", encoding="utf-8") as archivo:
                    contenido = archivo.read()
                    self.area_texto.delete(1.0, tk.END)
                    self.area_texto.insert(tk.END, contenido)
                self.actualizar_barra()
                self.master.title(f"Magic Dust - {os.path.basename(self.ruta_archivo)}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir el archivo:\n{e}")


    def guardar_archivo(self):
        if self.ruta_archivo:
            try:
                with open(self.ruta_archivo, "w", encoding="utf-8") as archivo:
                    contenido = self.area_texto.get(1.0, tk.END)
                    archivo.write(contenido)
                messagebox.showinfo("Guardado", "Archivo guardado correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{e}")
        else:
            self.guardar_como()

    def guardar_como(self):
        self.ruta_archivo = filedialog.asksaveasfilename(
            title="Guardar como",
            defaultextension=".txt",
            filetypes=[
                ("Archivos de texto", "*.txt"),
                ("Archivos Python", "*.py"),
                ("Archivos C++", "*.cpp"),
                ("Archivos C#", "*.cs"),
                ("Todos los archivos", "*.*")
            ]
        )
        if self.ruta_archivo:
            self.guardar_archivo()
            self.master.title(f"Magic Dust - {os.path.basename(self.ruta_archivo)}")


    def buscar_palabra(self):
        palabra = simpledialog.askstring("Buscar", "Introduce la palabra o frase a buscar:")
        if palabra:
            self.area_texto.tag_remove("resaltado", "1.0", tk.END)
            indice_inicio = "1.0"
            contador = 0
            while True:
                indice_inicio = self.area_texto.search(palabra, indice_inicio, stopindex=tk.END)
                if not indice_inicio:
                    break
                indice_fin = f"{indice_inicio}+{len(palabra)}c"
                self.area_texto.tag_add("resaltado", indice_inicio, indice_fin)
                indice_inicio = indice_fin
                contador += 1
            self.area_texto.tag_config("resaltado", background="yellow", foreground="black")
            messagebox.showinfo("Buscar", f"{contador} coincidencia(s) encontrada(s).")


    def mostrar_informacion(self):
        messagebox.showinfo(
            "Acerca de Magic Dust",
            "Magic Dust v1.0\n\n"
            "Editor de texto multiplataforma creado en Python con Tkinter.\n"
            "Permite abrir, editar, guardar y buscar texto.\n"
            "Licencia: MIT\n"
            "Desarrollado por Grupo 4, Curso de Algoritmos (2025)"
        )

    def abrir_manual(self):
        ruta_pdf = "manual_usuario.pdf"
        if os.path.exists(ruta_pdf):
            try:
                os.startfile(ruta_pdf) 
            except Exception:
                webbrowser.open_new_tab("file://" + os.path.abspath(ruta_pdf))
        else:
            webbrowser.open("https://github.com/jgutierrezh5/proyectofinal")

    def mostrar_integrantes(self):
        messagebox.showinfo(
            "Integrantes del grupo",
            "Proyecto Final - Grupo 4\n\n"
            "• Jorge Alejadro Gutierrez Hidalgo 7690-25-18368\n"
            "• Marco Tulio Marquez Abrego 7690-25-5247\n"
            "Algoritmos (2025)\n"
            "Universidad Mariano Galvez"
        )

    def actualizar_barra_event(self, event):
        self.area_texto.edit_modified(False)
        self.actualizar_barra()

    def actualizar_barra(self, event=None):
        contenido = self.area_texto.get("1.0", "end-1c")
        num_caracteres = len(contenido)
        self.barra_estado.config(text=f"{num_caracteres} caracteres")


if __name__ == "__main__":
    ventana = tk.Tk()
    app = MagicDustApp(ventana)
    ventana.mainloop()
