import tkinter as tk
from tkinter import messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import date
from persona import Persona

class VentanaVentas:

    def __init__(self, ventana):
        # Crea la ventana principal
        self.ventana = ventana
        self.ventana.title("Programa de la veterinaria")
        self.ventana.config(bg="#37CC8F")
        self.ventana.iconbitmap("veterinaria.ico")
        
        # Crear el campo de entrada para el DNI
        self.label_dni = tk.Label(ventana, text="DNI:")
        self.label_dni.config(bg="#FE9901", fg="white")
        self.label_dni.pack()
        self.entry_dni = tk.Entry(ventana)
        self.entry_dni.config(bg="#FE9901", fg="white")
        self.entry_dni.pack()
        
        # Crear el botón para buscar productos
        self.btn_buscar_productos = tk.Button(ventana, text="Buscar Productos", command=self.mostrar_productos)
        self.btn_buscar_productos.config(bg="#FE9901", fg="white")
        self.btn_buscar_productos.pack()
        
        # Crear una lista para mostrar los productos
        self.lista_productos = tk.Listbox(ventana, width=50)
        self.lista_productos.config(bg="#FE9901", fg="white")
        self.lista_productos.pack()
        
        # Crear un botón para agregar productos al carrito
        self.btn_agregar_carrito = tk.Button(ventana, text="Agregar al Carrito", command=self.agregar_carrito)
        self.btn_agregar_carrito.config(bg="#FE9901", fg="white")
        self.btn_agregar_carrito.pack()
        
        # Crear una lista para mostrar los productos seleccionados
        self.lista_carrito = tk.Listbox(ventana, width=50)
        self.lista_carrito.config(bg="#FE9901", fg="white")
        self.lista_carrito.pack()
        
        # Crear el botón para imprimir la boleta en PDF
        self.btn_imprimir = tk.Button(ventana, text="Imprimir Boleta", command=self.imprimir_boleta)
        self.btn_imprimir.config(bg="#FE9901", fg="white")
        self.btn_imprimir.pack()
        
        # Datos de la veterinaria
        self.nombre_veterinaria = "Huellitas"
        
        # Variable para almacenar los productos y sus precios
        self.productos = {}
    
    def mostrar_productos(self):
        # Lógica para mostrar los productos disponibles en la lista de productos (self.lista_productos)
        # Aquí puedes ajustar y agregar más productos según tus necesidades
        self.productos = {
            "Vacuna contra el Parvovirosis": 10.0,
            "Vacuna contra el Moquillo": 8.0,
            "Vacuna-Hepatitis": 12.0,
            "Vacuna-Parainfluenza": 10.0,
            "Vacuna-Leptospirosis": 15.0,
            "Vacuna-Rabia": 10.0,
            "Vacuna-Parasitos": 15.0,
            "Vacuna-Refuerzo": 15.0,
            "Collar de piedrina": 25.0,
            "Collar Coirtmini": 15.0,
            "Correa de cuero con sujetador": 45.0,
            "Cat-Nip": 28.0,
            "Kugurumy de perro": 30.0,
            "Cama de perro": 55.0,
            "Cama de gato": 15.0,
            "Pelota de hule": 8.0,
            "Rasgador de gatos": 35.0,
            "Placas": 5.0
        }
        
        self.lista_productos.delete(0, tk.END)  # Limpiar la lista de productos
        
        for producto, precio in self.productos.items():
            self.lista_productos.insert(tk.END, f"{producto} - ${precio:.2f}")
    
    def agregar_carrito(self):
        # Obtener el producto seleccionado
        producto_seleccionado = self.lista_productos.get(tk.ACTIVE)
        
        # Agregar el producto al carrito (self.lista_carrito)
        self.lista_carrito.insert(tk.END, producto_seleccionado)

    datos_inicial:list=[{"dni":"47259697",
                     "nombres":"Noe Wilber",
                     "apellidos":"Tipo Mamani"},

                     {"dni":"72042723",
                     "nombres":"Carlos Santiago",
                     "apellidos":"Bustamante Carpio"},

                     {"dni":"72042723",
                     "nombres":"Fer",
                     "apellidos":"Blanco H"},

                     {"dni":"472596972",
                     "nombres":"Noe Wilber2",
                     "apellidos":"Tipo Mamani2"}
                     ]
    lista_personas:Persona=[]

    def imprimir_boleta(self):
        # Obtener el DNI ingresado
        dni = self.entry_dni.get()
        
        # Obtener los productos seleccionados
        productos_seleccionados = self.lista_carrito.get(0, tk.END)
        
        # Validar que haya al menos un producto seleccionado
        if not productos_seleccionados:
            messagebox.showerror("Error", "No hay productos en el carrito.")
            return
        
        # Obtener la fecha actual
        fecha_actual = date.today().strftime("%d/%m/%Y")
        
        # Generar el archivo PDF de la boleta
        nombre_archivo = f"boleta_{dni}.pdf"
        c = canvas.Canvas(nombre_archivo, pagesize=letter)
        
        # Agregar contenido a la boleta
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, 750, self.nombre_veterinaria)
        c.setFont("Helvetica", 12)
        c.drawString(50, 730, f"Fecha de Compra: {fecha_actual}")
        c.drawString(50, 710, f"DNI: {dni}")
        c.drawString(50, 690, "Productos:")
        
        y = 670
        subtotal = 0.0
        
        for producto in productos_seleccionados:
            nombre_producto, precio = self.obtener_nombre_precio(producto)
            cantidad = productos_seleccionados.count(producto)
            subtotal_producto = precio * cantidad
            subtotal += subtotal_producto
            
            c.drawString(70, y, f"{nombre_producto} x {cantidad} - ${precio:.2f}")
            y -= 20
        
        total = subtotal
        
        c.drawString(50, y-40, f"Subtotal: ${subtotal:.2f}")
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y-60, f"Total: ${total:.2f}")
        
        # Guardar y cerrar el archivo PDF
        c.save()
        
        messagebox.showinfo("Éxito", f"Se ha generado la boleta en el archivo {nombre_archivo}.")
        
        # Limpiar la lista de productos seleccionados
        self.lista_carrito.delete(0, tk.END)
    
    def obtener_nombre_precio(self, producto):
        # Función auxiliar para obtener el nombre y precio de un producto seleccionado
        nombre_producto, precio_str = producto.split(" - ")
        precio = float(precio_str[1:])
        
        return nombre_producto, precio


ventana = tk.Tk()
app = VentanaVentas(ventana)
ventana.mainloop()
