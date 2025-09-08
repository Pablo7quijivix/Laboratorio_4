import tkinter as tk
#clase principal con atributos nombre e institucion para ir heredadndo cunado estas lo requieran
class Participante:
    def __init__(self, nombre, institucion):
        self.nombre = nombre
        self.institucion = institucion

# metodo mostrar para mostrar la informacion concatenada del "Nombre-institucion ejemplo: Shekina-Academia Musical"
    def mostrar_info(self):
        return f"{self.nombre} - {self.institucion}"

#Clase BandaESscolar que hereda los atrinutos de la clase participantes
class BandaEscolar(Participante):
    categorias_validas = ["Primaria", "Basico", "Diversificado"]
    criterios_validos = ["ritmo", "uniformidad", "coreografia", "alineacion", "puntualidad"]

    def __init__(self, nombre, institucion, categoria):
        super().__init__(nombre, institucion)
        self._categoria = None
        self._puntajes = {}
        self.set_categoria(categoria)

    def set_categoria(self, categoria):
        if categoria in BandaEscolar.categorias_validas:
            self._categoria = categoria
        else:
            raise ValueError("--Categoria Invalida, Intente de nuevo--")

    def registrar_puntajes(self, puntajes):
        if set(puntajes.keys()) != set(BandaEscolar.criterios_validos):
            raise ValueError("Criterios incompletos o incorrectos")
        for criterio, valor in puntajes.items():
            if not (0 <= valor <= 10):
                raise ValueError("Puntajes deben estar entre 0 y 10")
        self._puntajes = puntajes

    @property
    def total(self):
        return sum(self._puntajes.values()) if self._puntajes else 0

    def mostrar_info(self):
        base = super().mostrar_info()
        if self._puntajes:
            return f"{base} | {self._categoria} | Total: {self.total}"
        return f"{base} | {self._categoria} | Sin evaluar"

class Concurso:
    def __init__(self, nombre, fecha):
        self.nombre = nombre
        self.fecha = fecha
        self.bandas = {}

    def inscribir_banda(self, banda):
        if banda.nombre in self.bandas:
            raise ValueError("Ya existe una banda con ese nombre")
        self.bandas[banda.nombre] = banda

    def registrar_evaluacion(self, nombre_banda, puntajes):
        if nombre_banda not in self.bandas:
            raise ValueError("Banda no inscrita")
        self.bandas[nombre_banda].registrar_puntajes(puntajes)

    def listar_bandas(self):
        return [b.mostrar_info() for b in self.bandas.values()]

    def ranking(self):
        return sorted(
            self.bandas.values(),
            key=lambda b: (b.total),
            reverse=True
        )
# inicio de la logica de nuestro programa
#mensaje inicial que se muestra en pantalla cuando se corre el programa
concurso = Concurso("Concurso de Bandas - 15 de Septiembre", "2025-09-15")
tk.messagebox = __import__("tkinter.messagebox")

# -----------primeras funciones de la interfaz--------------------------
# se creo una funcion en donde se crearon cada uno de los votones para ser llamadas a traves de su comando
def abrir_menu():
    menu = tk.Toplevel(ventana)
    menu.title("Opciones")
    menu.geometry("300x300")
    tk.Button(menu, text="Inscribir banda", width=25, command=inscribir_banda).pack(pady=5)
    tk.Button(menu, text= "Registrar Evaluacion", width=25, command=registrar_evaluacion).pack(pady=5)
    tk.Button(menu, text= "Listar Bandas", width=25, command= listar_bandas).pack(pady=5)
    tk.Button(menu, text= "Ver Ranking", width=25, cammand= ver_ranking).pack(pady=5)
    tk.Button(menu, text="Regresar", width=25, command= menu.destroy).pack(pady=5)



# ventana "inscribir_banda" la renombramos como "win" de window
def inscribir_banda():
    print("Se abrió la ventana: Inscribir Banda")
    win= tk.Toplevel(ventana)
    win.title("Inscribir Banda")
    win.geometry("400x300")


    tk.Label(win, text="Nombre de la Banda:").pack()
    entry_nombre = tk.Entry(win)
    entry_nombre.pack()

    tk.Label(win, texto="Nommbre de la Institucion:").pack()
    entry_institucion = tk.Entry(win)
    entry_institucion.pack()

    tk.Label(win, text="Categoria (Primaria, Basico, Diversificado").pack()
    entry_categoria = tk.Entry(win)
    entry_categoria.pack()

    mensaje= tk.Label(win, text= "", fg="red")
    mensaje.pack()

    def guardar(): #programando funcion para guardar los datos de nombre, institucion, categoria de cada banda
        nombre = entry_nombre.get().strip()
        institucion = entry_institucion.get().strip()
        categoria = entry_categoria.get().strip().capitalize()
        try:
            banda =BandaEscolar(nombre, institucion, categoria)
            concurso.inscribir_banda(banda)
            mensaje.config(text="informacion guardada correctamente.", fg="green")
        except Exception as e:
            mensaje.config(text=f" {str(e)}", fg="red")

    def limpiar(): # funcion para borrar los datos de las casillas e ingreasr nuevos datos
        entry_nombre.delete(0, tk.END)
        entry_institucion.delete(0, tk.END)
        entry_categoria.delete(0, tk.END)
        mensaje.config(text="")

    # programando el funcionamiento de los botones de la ventana
    tk.Button(win, text="Guardar", command=guardar).pack(pady=5)
    tk.Button(win, text="Limpiar", command=limpiar).pack(pady=5)
    tk.Button(win, text="Regresar", command=win.destroy).pack(pady=5)



def registrar_evaluacion():
    print("Se abrió la ventana: Registrar Evaluación")
    win = tk.Toplevel(ventana)
    win.title("Registrar Evaluación")
    win.geometry("400x300")

    tk.Label(win, text= "Nombre de la banda:").pack()
    entry_nombre= tk.Entry(win)
    entry_nombre.pack()

    entradas ={}
    for crit in BandaEscolar.criterios_validos:
        tk.Label(win, text=crit.capitalize()).pack()
        entradas[crit] =tk.Entry(win)
        entradas[crit].pack()

    mensaje =tk.Label(win, text="", fg= "red")
    mensaje.pack()

    def guardar():
        nombre = entry_nombre.get().strip()
        try:
            puntajes = {c:int(e.get()) for c, e in entradas.items()}
            concurso.registrar_evaluacion(nombre, puntajes)
            mensaje.config(text=f"{str(e)}", fg= "red")



def listar_bandas():
    print("Se abrió la ventana: Listado de Bandas")
    ventana_listado = tk.Toplevel(ventana)
    ventana_listado.title("Listado de Bandas")
    ventana_listado.geometry("400x300")

def ver_ranking():
    print("Se abrió la ventana: Ranking Final")
    ventana_ranking = tk.Toplevel(ventana)
    ventana_ranking.title("Ranking Final")
    ventana_ranking.geometry("400x300")

def salir():
    print("Aplicación cerrada")
    ventana.quit()

ventana = tk.Tk()
ventana.title("Concurso de Bandas - Quetzaltenango")
ventana.geometry("500x300")

etiqueta = tk.Label(ventana, text= "Eliga una accion del menu")
etiqueta.pack(pady=5)
barra_menu = tk.Menu(ventana)

menu_opciones = tk.Menu(barra_menu, tearoff=0)
menu_opciones.add_command(label="Inscribir Banda", command=inscribir_banda)
menu_opciones.add_command(label="Registrar Evaluación", command=registrar_evaluacion)
menu_opciones.add_command(label="Listar Bandas", command=listar_bandas)
menu_opciones.add_command(label="Ver Ranking", command=ver_ranking)
menu_opciones.add_separator()
menu_opciones.add_command(label="Salir", command=salir)

barra_menu.add_cascade(label="Opciones", menu=menu_opciones)

ventana.config(menu=barra_menu)

etiqueta = tk.Label(
    ventana,
    text="Sistema de Inscripción y Evaluación de Bandas Escolares\nDesfile 15 de Septiembre - Quetzaltenango",
    font=("Arial", 12, "bold"),
    justify="center"
)
etiqueta.pack(pady=50)

ventana.mainloop()
