import sys
from pathlib import Path
from datetime import datetime
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow,QGridLayout, QFileDialog ,QListWidgetItem,QDialog ,QInputDialog,QComboBox,QWidget, QListWidget,QLabel, QPushButton, QFormLayout, QLineEdit, QMessageBox
from PyQt6.QtGui import QColor

# CLASE EQUIPO
class Equipo:
    def __init__ (self, nombre):
        self.nombre = nombre


# CLASE PARTIDO
class Partido:
    def __init__ (self, dia, equipo, resultado):
        self.dia = datetime.strptime(dia, '%Y/%m/%d')
        self.equipo = equipo
        self.resultado = resultado

    def verificar_fecha (self):
        return datetime.now() > self.dia


# FORMULARIO SECUNDARIO CON AÑADIR PARTIDO
class FormSec(QDialog):
    def __init__ (self, equipos):
        super().__init__()
        self.equipos = equipos
        self.correr_vent()

    def correr_vent(self):
        self.setWindowTitle("Añadir Datos")
        central_widget = QWidget(self)
        form_layout = QFormLayout(central_widget)

        self.resultado = QLineEdit()
        self.dia = QLineEdit()
        self.equipo_combo = QComboBox()
        for equipo in self.equipos:
            self.equipo_combo.addItem(equipo)
        
        self.boton_agregar = QPushButton("Añadir Datos")

        self.boton_agregar.clicked.connect(self.accept)
        
        form_layout.addRow("Resultado del partido",self.resultado)
        form_layout.addRow("Día del partido (aaaa/mm/dd)",self.dia)
        form_layout.addRow("Equipo",self.equipo_combo)
        form_layout.addRow(self.boton_agregar)

        self.setLayout(form_layout)
    
    def traer_datos(self):
        return {
            "Resultado" :self.resultado.text(),
            "Día" : self.dia.text(),
            "Equipo" : self.equipo_combo.currentText(),
        }


# VENTANA PRINCIPAL
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.equipos = [] 
        self.partidos = []
        self.setCentralWidget(self.correr_vent())
        self.show()  

    def correr_vent (self):
        self.setWindowTitle("Gestor de Partidos")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget(self)
        form_layout = QGridLayout(central_widget)

        self.Label = QLabel("Equipo: ")
        self.equipo_comb = QComboBox() #categoria boton de lista desplegable

        self.equipo_comb.currentIndexChanged.connect(self.mostrar_partidos)
        self.añadir_equipo = QPushButton("Añadir Equipo")
        self.añadir_equipo.clicked.connect (self.add_team)
        self.añadir_partido = QPushButton("Añadir Partido")
        self.añadir_partido.clicked.connect(self.agregar_partido)

        self.list_partidos = QListWidget()

        self.export_buton = QPushButton("Exportar a txt")
        self.export_buton.clicked.connect(self.export_txt)

        form_layout.addWidget(self.Label, 0,0)
        form_layout.addWidget(self.equipo_comb, 0,1)
        form_layout.addWidget(self.añadir_equipo,0,2)
        form_layout.addWidget(self.añadir_partido,0,3)
        form_layout.addWidget(self.list_partidos,1,0,1,4)
        form_layout.addWidget(self.export_buton,2,0,1,4)

        return central_widget
    
    def agregar_partido(self):
        form = FormSec(self.equipos)
        if form.exec() == QDialog.DialogCode.Accepted:
            data_partido = form.traer_datos()
            partido = Partido(
                    equipo = data_partido['Equipo'],
                    resultado = data_partido['Resultado'],
                    dia =  data_partido['Día'],
            ) 

            self.partidos.append(partido)
            self.update_team()
            self.mostrar_partidos()


    def mostrar_partidos(self):
        equipo_selec = self.equipo_comb.currentText()
        self.list_partidos.clear()
        for partido in self.partidos:
            if partido.equipo == equipo_selec:
                item_partido = QListWidgetItem(f"Resultado: {partido.resultado}, Día: {partido.dia}, Equipo: {partido.equipo}")
                if partido.verificar_fecha(): 
                    item_partido.setForeground(QColor(Qt.GlobalColor.red)) 
                self.list_partidos.addItem(item_partido)

    def add_team(self):
        equipo_name, ok  = QInputDialog.getText(self,"Añadir equipo","Ingresa el nombre del equipo: ")
        if ok and equipo_name:

            if equipo_name not in self.equipos:
                #añadir categoria
                print(equipo_name)
                self.equipos.append(equipo_name)
                self.actualizar_equipo_combo()
                self.equipo_comb.setCurrentText(equipo_name)
                self.agregar_partido() 
            else:
                QMessageBox.warning(self,"error de categoria","la categoria ya existe")
        
        elif ok and equipo_name == "":
            QMessageBox.warning(self,"Error de equipo","Ingresa un nombre en el campo de equipo")

    def actualizar_equipo_combo(self):
        self.equipo_comb.clear()
        for equipo in self.equipos:
            self.equipo_comb.addItem(equipo)

    def export_txt(self):
        file_path, _ = QFileDialog.getSaveFileName(self,"Exportar datos","Partidos Exportados", "TXT Files (*.txt);;All Files (*)")
        if file_path:
            with open(file_path, mode='w') as archivo:
                archivo.write("Equipo,Resultado,Día\n")
                for partido in self.partidos:
                    archivo.write(f"{partido.equipo},{partido.resultado},{partido.dia.strftime('%Y/%m/%d')}\n")
                QMessageBox.information(self,"Exito","Partidos guardados de manera exitosa")

    def update_team(self):
        with open(r"C:\Users\asier\Documentos\UP_lol\Proyectos_POO\Partidos Exportados.txt", mode="w", encoding="utf-8") as archivo:
                archivo.write("equipo,resultado,dia\n")
                for partido in self.partidos:
                    archivo.write(f"{partido.equipo},{partido.resultado},{partido.dia.strftime('%Y/%m/%d')}\n")

    def cargar_archivos(self, path):
        file_Path = Path(path)
        if file_Path.exists():
         with file_Path.open('r', encoding='utf-8') as archivo:
            encabezados = archivo.readline().strip().split(',')
            for linea in archivo:
                campos = linea.strip().split(',')
                datos = {}
                for i in range(len(encabezados)):
                    datos[encabezados[i]] = campos[i]

                partido = Partido(
                    equipo = datos['Equipo'],
                    resultado = datos['Resultado'],
                    dia =  datos['Día'],
                ) 
                self.partidos.append(partido)
                if datos["equipo"] not in self.equipos:
                    self.equipos.append(datos["equipo"])
            self.actualizar_equipo_combo()
            self.mostrar_partidos()
        else:
         print("El archivo no existe.")
        
            


app = QApplication(sys.argv)

window = MainWindow()



sys.exit(app.exec())

    