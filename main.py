import math
import fuerzaBruta
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import time

# Por el momento no necesitan intalar ninguna dependencia (Creo), si la van a utilizar avisan para que todos la puendan descargar
# Otra cosa mas documente lo mas importante para que vean como esta el codigo, aunque pues lo importante son las clases y lo algoritmos
# Pero documente la interfaz por si necesitan saber... Cuando hagan la funcion de su algorimo haganlo en diferentes ramas y despues hacen el merge a la rama principal
# Esto es para no tener ningun conflicto 

# Mas adelante colocare mas comentarios para que puedan entender el codigo

# Clases donde estructuramos los datos
class GrupoAgente:
    def __init__(self, n, op1, op2, rig):
        self.n = n
        self.op1 = op1
        self.op2 = op2
        self.rig = rig
    
    def __str__(self):
        return f"Agentes: {self.n}, Opinión 1: {self.op1}, Opinión 2: {self.op2}, Rigidez: {self.rig}"

class RedSocial:
    def __init__(self, grupos, R_max):
        self.grupos = grupos
        self.R_max = R_max 
    
    #cambiamos la funcincion de conflicto interno y  aplicar estrategia
    def calcular_conflicto_interno(self):
        if len(self.grupos) == 0:
            return 0
        numerador = sum(grupo.n * (grupo.op1 - grupo.op2)**2 for grupo in self.grupos)
        return numerador / len(self.grupos)
        
    def calcular_esfuerzo(self, estrategia):

        esfuerzo = 0
        for i, e in enumerate(estrategia):
            if e > 0:
                grupo = self.grupos[i]
                esfuerzo += math.ceil(abs(grupo.op1 - grupo.op2) * grupo.rig * e)
        return esfuerzo
    
    def aplicar_estrategia(self, estrategia):
        nuevos_grupos = []
        
        for i, grupo in enumerate(self.grupos):
            e = estrategia[i]
            nuevo_n = grupo.n - e
            # Aseguramos que nuevo_n no sea negativo (si se moderan todos, queda 0)
            nuevo_n = max(nuevo_n, 0)
            nuevos_grupos.append(GrupoAgente(nuevo_n, grupo.op1, grupo.op2, grupo.rig))
        
        return RedSocial(nuevos_grupos, self.R_max)


########### En enta parte coloquen lo algoritmos ##########

# Funcion Fuerza Bruta
fuerzaBruta = fuerzaBruta.modciFuerzaBruta

# Funcion Programacion Dinamica
#...

# Funcion Voraz
#...

###########################################################

# Funciones para manejar los archivos
def cargar_datos(ruta_archivo):
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(f"El archivo {ruta_archivo} no existe")
    
    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        lineas = archivo.readlines()
        
        n = int(lineas[0].strip())
        grupos = []
        
        for i in range(1, n+1):
            datos = lineas[i].strip().split(',')
            n_agentes = int(datos[0])
            op1 = int(datos[1])
            op2 = int(datos[2])
            rig = float(datos[3])
            grupos.append(GrupoAgente(n_agentes, op1, op2, rig))
        
        R_max = int(lineas[n+1].strip())
        
        return RedSocial(grupos, R_max)

def guardar_resultados(ruta_archivo, estrategia, esfuerzo, conflicto):

    with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
        archivo.write(f"{conflicto}\n")
        archivo.write(f"{esfuerzo}\n")
        for e in estrategia:
            archivo.write(f"{e}\n")

# Interfaz gráfica
def interfaz_grafica():
    ventana = tk.Tk()
    ventana.title("Moderación de Conflicto Interno en Red Social")
    ventana.geometry("800x600")
    
    # Variables
    entrada_var = tk.StringVar()
    salida_var = tk.StringVar()
    algoritmo_var = tk.StringVar(value="Fuerza Bruta")
    resultado_texto = tk.StringVar()
    
    # Función para ejecutar el algoritmo seleccionado
    def ejecutar_algoritmo():
        ruta_entrada = entrada_var.get()
        ruta_salida = salida_var.get()
        
        if not ruta_entrada or not ruta_salida:
            messagebox.showerror("Error", "Por favor, seleccione archivos de entrada y salida")
            return
        
        try:
            red_social = cargar_datos(ruta_entrada)
            algoritmo = algoritmo_var.get()
            
            tiempo_inicio = time.time()

            # Casi se me olvida, tienen guardar lo que les de el algoritmo con una variable llamada resultado
            # Ejemplo: resultado  =  fuerzaBruta()
            
            if algoritmo == "Fuerza Bruta":
                # Aca llama la funcion de fuerza bruta (Jean Paul)
                resultado = fuerzaBruta(red_social)
            elif algoritmo == "Voraz":
                # Aca llama a la funcion voraz (Miguel)
                return #Este retunr es solo para que no de error, lo quitan cuando hagan la funcion
            elif algoritmo == "Programación Dinámica":
                # Aca llama a la funcion programacio dinamica (Alejandro)
                return #Este retunr es solo para que no de error, lo quitan cuando hagan la funcion (Casi se me olvida)
            
            tiempo_fin = time.time()
            tiempo_ejecucion = tiempo_fin - tiempo_inicio
            
            estrategia, esfuerzo, conflicto = resultado
            guardar_resultados(ruta_salida, estrategia, esfuerzo, conflicto)
            
            # Mostramos los resultados
            texto_resultado = f"Algoritmo: {algoritmo}\n"
            texto_resultado += f"Tiempo de ejecución: {tiempo_ejecucion:.6f} segundos\n\n"
            texto_resultado += f"Conflicto Interno: {conflicto}\n"
            texto_resultado += f"Esfuerzo: {esfuerzo}\n\n"
            texto_resultado += "Estrategia de moderación:\n"
            
            for i, e in enumerate(estrategia):
                grupo = red_social.grupos[i]
                texto_resultado += f"Grupo {i+1} ({grupo.n} agentes): {e} agentes moderados\n"
            
            resultado_texto.set(texto_resultado)
            
            messagebox.showinfo("Éxito", f"El algoritmo {algoritmo} se ejecutó correctamente.\nResultados guardados en {ruta_salida}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al ejecutar el algoritmo: {str(e)}")
    
    # Función para seleccionar archivo de entrada
    def seleccionar_entrada():
        archivo = filedialog.askopenfilename(
            title="Selecciona el archivo de entrada",
            filetypes=(("Archivo de texto", "*.txt"), ("Todos los archivos", "*.*"))
        )
        if archivo:
            entrada_var.set(archivo)
    
    # Función para seleccionar archivo de salida
    def seleccionar_salida():
        archivo = filedialog.asksaveasfilename(
            title="Selecciona el archivo de salida",
            defaultextension=".txt",
            filetypes=(("Archivo de texto", "*.txt"), ("Todos los archivos", "*.*"))
        )
        if archivo:
            salida_var.set(archivo)
    
    # Sección de archivos
    frame_archivos = ttk.LabelFrame(ventana, text="Archivos")
    frame_archivos.pack(fill="x", padx=10, pady=10)
    
    # Archivo de entrada
    tk.Label(frame_archivos, text="Archivo de entrada:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    tk.Entry(frame_archivos, textvariable=entrada_var, width=50).grid(row=0, column=1, padx=5, pady=5)
    tk.Button(frame_archivos, text="Seleccionar", command=seleccionar_entrada).grid(row=0, column=2, padx=5, pady=5)
    
    # Archivo de salida
    tk.Label(frame_archivos, text="Archivo de salida:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    tk.Entry(frame_archivos, textvariable=salida_var, width=50).grid(row=1, column=1, padx=5, pady=5)
    tk.Button(frame_archivos, text="Seleccionar", command=seleccionar_salida).grid(row=1, column=2, padx=5, pady=5)
    
    # Sección de algoritmos
    frame_algoritmos = ttk.LabelFrame(ventana, text="Algoritmo a utilizar")
    frame_algoritmos.pack(fill="x", padx=10, pady=10)
    
    algoritmos = ["Fuerza Bruta", "Voraz", "Programación Dinámica"]
    for i, alg in enumerate(algoritmos):
        ttk.Radiobutton(frame_algoritmos, text=alg, variable=algoritmo_var, value=alg).pack(anchor="w", padx=20, pady=5)
    
    # Botón para ejecutar
    tk.Button(ventana, text="Ejecutar Algoritmo", font=("Arial", 12), command=ejecutar_algoritmo).pack(pady=10)
    
    # Sección de resultados
    frame_resultados = ttk.LabelFrame(ventana, text="Resultados")
    frame_resultados.pack(fill="both", expand=True, padx=10, pady=10)
    
    texto_resultado = tk.Text(frame_resultados, wrap="word", width=80, height=15)
    texto_resultado.pack(fill="both", expand=True, padx=5, pady=5)
    
    # Enlazar el Text widget con la variable StringVar
    def actualizar_texto(*args):
        texto_resultado.delete(1.0, tk.END)
        texto_resultado.insert(tk.END, resultado_texto.get())
    
    resultado_texto.trace_add("write", actualizar_texto)
    
    ventana.mainloop()

if __name__ == "__main__":
    interfaz_grafica()