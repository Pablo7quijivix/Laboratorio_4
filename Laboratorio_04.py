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

    tk.Button(menu, text="Inscribir Banda", width=25, command=inscribir_banda).pack(pady=5)
    tk.Button(menu, text="Registrar Evaluación", width=25, command=registrar_evaluacion).pack(pady=5)
    tk.Button(menu, text="Listar Bandas", width=25, command=listar_bandas).pack(pady=5)
    tk.Button(menu, text="Ver Ranking", width=25, command=ver_ranking).pack(pady=5)
    tk.Button(menu, text="Regresar", width=25, command=menu.destroy).pack(pady=5)


# ---------- INSCRIPCIÓN ----------
def inscribir_banda():
    win = tk.Toplevel(ventana)
    win.title("Inscribir Banda")
    win.geometry("400x300")

    tk.Label(win, text="Nombre de la Banda:").pack()
    entry_nombre = tk.Entry(win)
    entry_nombre.pack()

    tk.Label(win, text="Institución:").pack()
    entry_institucion = tk.Entry(win)
    entry_institucion.pack()

    tk.Label(win, text="Categoría (Primaria, Básico, Diversificado):").pack()
    entry_categoria = tk.Entry(win)
    entry_categoria.pack()

    mensaje = tk.Label(win, text="", fg="red")
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

# ventana "registrar_evaluacion" la renombramos como "win" de window
def registrar_evaluacion():
    win = tk.Toplevel(ventana)
    win.title("Registrar Evaluación")
    win.geometry("400x400")

    tk.Label(win, text="Nombre de la Banda:").pack()
    entry_nombre = tk.Entry(win)
    entry_nombre.pack()

    # creando casillas de texto para ingresar cada criterio de la evaluación
    entradas = {}
    for crit in BandaEscolar.criterios_validos:
        tk.Label(win, text=crit.capitalize()).pack()
        entradas[crit] = tk.Entry(win)
        entradas[crit].pack()

    mensaje = tk.Label(win, text="", fg="red")
    mensaje.pack()

    def guardar(): # funcion para guardar los datos de nombre y puntajes de cada criterio
        nombre = entry_nombre.get().strip()
        try:
            puntajes = {c: int(e.get()) for c, e in entradas.items()}
            concurso.registrar_evaluacion(nombre, puntajes)
            mensaje.config(text=" Evaluación guardada correctamente.", fg="green")
        except Exception as e:
            mensaje.config(text=f" {str(e)}", fg="red")

    def limpiar(): # funcion para borrar los datos de las casillas e ingresar nuevos datos
        entry_nombre.delete(0, tk.END)
        for e in entradas.values():
            e.delete(0, tk.END)
        mensaje.config(text="")

    # programando el funcionamiento de los botones de la ventana
    tk.Button(win, text="Guardar", command=guardar).pack(pady=5)
    tk.Button(win, text="Limpiar", command=limpiar).pack(pady=5)
    tk.Button(win, text="Regresar", command=win.destroy).pack(pady=5)

def listar_bandas(): # ventana para mostrar todas las bandas inscritas
    win = tk.Toplevel(ventana)
    win.title("Listado de Bandas")
    win.geometry("400x300")

    bandas = concurso.listar_bandas()
    if not bandas:
        tk.Label(win, text="No hay bandas inscritas").pack()
    else:
        for b in bandas:
            tk.Label(win, text=b).pack()

    # boton para regresar y cerrar la ventana
    tk.Button(win, text="Regresar", command=win.destroy).pack(pady=10)

def ver_ranking(): # ventana para mostrar el ranking final de las bandas evaluadas
    win = tk.Toplevel(ventana)
    win.title("Ranking Final")
    win.geometry("400x300")

    ranking = concurso.ranking()
    if not ranking:
        tk.Label(win, text="No hay bandas evaluadas").pack()
    else:
        for i, b in enumerate(ranking, start=1):
            tk.Label(win, text=f"{i}. {b.nombre} | {b.institucion} | {b._categoria} | Total: {b.total}").pack()

    # boton para regresar y cerrar la ventana
    tk.Button(win, text="Regresar", command=win.destroy).pack(pady=10)

def salir(): # funcion para cerrar la aplicación
    ventana.quit()

#Interfaz principal
ventana = tk.Tk()
ventana.title("Concurso de Bandas - Quetzaltenango")
ventana.geometry("500x300")

# etiqueta con el título principal del sistema
tk.Label(
    ventana,
    text="Sistema de Inscripción y Evaluación de Bandas Escolares\nDesfile 15 de Septiembre - Quetzaltenango",
    font=("Arial", 12, "bold"),
    justify="center"
).pack(pady=30)

# botones principales de la ventana inicial
tk.Button(ventana, text="Abrir Opciones", width=30, command=abrir_menu).pack(pady=10)
tk.Button(ventana, text="Salir", width=30, command=salir).pack(pady=10)

ventana.mainloop()
