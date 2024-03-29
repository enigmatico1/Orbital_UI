#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# AÑO: 2024 CREADOR: Christian Yael Ramírez León

from PySide6.QtCore import QSize, Qt 
from PySide6.QtGui import QAction, QKeySequence, QResizeEvent, Qt
from PySide6.QtWidgets import QMainWindow, QToolBar, QComboBox, QLabel, QStatusBar, QFrame, QTabWidget, QVBoxLayout, QLineEdit 
from PySide6.QtWebEngineWidgets import QWebEngineView
from modules.tab_style import ColorTab
from modules.custom_widgets import *
import folium

class WidgetsIn(QMainWindow): 
    def IncluirWidgetsConfig(self): 

        #Ajustes app 
        # self.setWindowIcon()   #Falta agregar el ícono 
        self.setWindowTitle("Estación Terrena ORBITAL")
        self.setObjectName("Estación Terrena ORBITAL")
        self.setStyleSheet("background-color: black;"
                        "color: white;"
                        "selection-color: #DFDFDF;"
                        "selection-background-color: #242424")
        self.setFixedSize(int(1920*0.9), int(1080*0.9))

        #Menubar 
        self.menubar = self.menuBar()
        self.archivo_menu = self.menubar.addMenu("Archivo") 
        self.guardar_csv = self.archivo_menu.addAction("Guardar CSV")
        self.guardar_csv.setShortcut(QKeySequence("Ctrl+s"))
        self.salir_app = self.archivo_menu.addAction("Salir")
        self.salir_app.setShortcut(QKeySequence("Ctrl+q"))

        #Toolbar 
        self.toolbar = QToolBar("Herramientas") 
        self.toolbar.setIconSize(QSize(16,16))
        self.addToolBar(self.toolbar) 
        self.toolbar.setFloatable(False)
        self.toolbar.setMovable(False)

        #Combo box configuración serial. 
        label_baud = QLabel("Baudrate: ")
        self.baud_opts = QComboBox()
        self.baud_opts.addItems(['9600', '19200', '31250', '38400', '57600', '74880', '115200', '230400', '250000', '460800', '500000', '921600', '1000000', '2000000'])
        self.baud_opts.setCurrentIndex(-1)
        self.serial_opts = QComboBox() 
        label_serial = QLabel("Puertos Disponibles: ")
        
        #Agregar ubicación del objetivo
        label_pos = QLabel("Ubicación del objetivo: ")
        self.latitud = QLineEdit()
        self.longitud = QLineEdit()
        self.altura = QLineEdit()
        self.latitud.setFixedWidth(60)
        self.longitud.setFixedWidth(60)
        self.altura.setFixedWidth(60)
        self.latitud.setStyleSheet("background: #212121")
        self.longitud.setStyleSheet("background: #212121")
        self.altura.setStyleSheet("background: #212121")
        # Botones 
        self.boton_actualizar = QAction("Actualizar Puertos")
        self.boton_conec_ser = QAction("Conectar")
        self.boton_descon = QAction("Desconectar")
        self.boton_posicion = QAction("Actualizar")
        self.boton_calib_altura = QAction("Calibrar Altura")
        self.boton_conec_ser.setEnabled(False)
        self.boton_descon.setEnabled(False)
        
        #Widgets en el toolbar 
        self.toolbar.addWidget(label_baud)
        self.toolbar.addWidget(self.baud_opts)
        self.toolbar.addSeparator()
        self.toolbar.addWidget(label_serial) 
        self.toolbar.addWidget(self.serial_opts)
        self.toolbar.addAction(self.boton_actualizar)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.boton_conec_ser) 
        self.toolbar.addAction(self.boton_descon) 
        self.toolbar.addSeparator()
        self.toolbar.addWidget(label_pos)
        self.toolbar.addWidget(self.latitud)
        self.toolbar.addWidget(self.longitud)
        self.toolbar.addAction(self.boton_posicion)
        self.toolbar.addSeparator()
        self.toolbar.addWidget(self.altura)
        self.toolbar.addAction(self.boton_calib_altura)

        # Status Bar 
        self.setStatusBar(QStatusBar(self))
        
        # Cuadro con identificadores de la misión. 
        self.frame_data = CustomFrame(parent=self, background="#151515")
        self.hora_frame = CustomFrame(parent=self.frame_data, background="#00BDFF") 
        self.id_frame = CustomFrame(parent=self.frame_data, background="#00BDFF")
        self.launcht_frame = CustomFrame(parent=self.frame_data, background="#00BDFF")
        self.pack_frame = CustomFrame(parent=self.frame_data, background="#00BDFF")
        self.estado_frame = CustomFrame(parent=self.frame_data, background="#00BDFF")
        self.hora_label = CustomLabel("HORA", self.hora_frame)
        self.id_label = CustomLabel("ID", self.id_frame)
        self.launcht_label = CustomLabel("LAUNCH TIME", self.launcht_frame)
        self.pack_label = CustomLabel("PACKAGE COUNT", self.pack_frame) 
        self.estado_label = CustomLabel("ESTADO", self.estado_frame)

        self.hora = CustomLabel(parent=self.frame_data,fsize=20)
        self.id = CustomLabel(parent=self.frame_data,fsize=20)
        self.launcht = CustomLabel(parent=self.frame_data,fsize=20)
        self.pack = CustomLabel(parent=self.frame_data,fsize=20)
        self.estado = CustomLabel(parent=self.frame_data, fsize=20)

        #Sensores 
        self.frame_sensores = CustomFrame(parent=self, background="#151515")
        self.pitch_label = CustomLabel("PITCH:", self.frame_sensores, 20, "#151515", Qt.AlignLeft)
        self.roll_label = CustomLabel("ROLL:", self.frame_sensores, 20, "#151515", Qt.AlignLeft)
        self.rpm_label = CustomLabel("RPM:", self.frame_sensores, 20, "#151515", Qt.AlignLeft)
        self.velocidad_label = CustomLabel("VELOCIDAD:", self.frame_sensores, 20, "#151515", Qt.AlignLeft)

        self.pitch = CustomLabel(parent=self.frame_sensores)
        self.roll = CustomLabel(parent=self.frame_sensores)
        self.rpm = CustomLabel(parent=self.frame_sensores)
        self.velocidad = CustomLabel(parent=self.frame_sensores)
        
        #Tabs 
        self.tab_cont = QTabWidget(self) 
        self.tab_graphs = QFrame()
        self.tab_GPS = QFrame() 
        self.tab_cont.setStyleSheet(ColorTab())
        self.tab_cont.addTab(self.tab_graphs, "Sensores")
        self.tab_cont.addTab(self.tab_GPS,"GPS")

        #Tab Graficas
        self.tab_graphs.setStyleSheet("border-radius: 5px;")
        self.altura_cp = AltitudeWidget(parent=self.tab_graphs, label="ALTITUD CP")
        self.altura_cs = AltitudeWidget(parent=self.tab_graphs, label="ALTITUD CS")
        # self.altura_frame = CustomFrame(parent=self.tab_graphs, background="#151515")
        self.temp_frame = CustomFrame(parent=self.tab_graphs, background="#151515") 
        self.volt_frame = CustomFrame(parent=self.tab_graphs, background="#151515") 
        self.presion_frame = CustomFrame(parent=self.tab_graphs, background="#151515")
        self.volt_container = QVBoxLayout(self.volt_frame)
        self.temp_container = QVBoxLayout(self.temp_frame)
        self.presion_container = QVBoxLayout(self.presion_frame)

        self.volt = CustomGraph("Voltaje", "v")
        self.temp = CustomGraph("Temperatura", "°C")
        self.presion = CustomGraph("Presión", "Pa")
        self.volt_container.addWidget(self.volt)
        self.temp_container.addWidget(self.temp)
        self.presion_container.addWidget(self.presion)
        self.volt.setYRange(0,10)
        self.temp.setYRange(0,30)
        self.presion.setYRange(75000,80000)

        #Tab GPS
        self.tab_GPS.setStyleSheet("border-radius: 5px;")
        self.gps_frame = QFrame(self.tab_GPS)
        self.gps_w = QWebEngineView(self.gps_frame)
        self.maps = folium.Map(location = [19.4284, -99.1276], zoom_start=4)
        self.gps_w.setHtml(self.maps.get_root().render())

        self.gps_frame.setStyleSheet("background: #151515")

    def resizeEvent(self, event: QResizeEvent) -> None:
        width = self.geometry().width()
        height = self.geometry().height()

        #Tab
        self.tab_cont.setGeometry(int(width*0.018), int(height*0.28), width -int(width*0.22), int(height*0.67))
        width_f, height_f = self.tab_cont.geometry().width(), self.tab_cont.geometry().height()

        #GPS 
        self.gps_frame.setGeometry(int(0.01*width_f), int(0.01*height_f), int(0.6*width_f), int(0.9*height_f) - 31)
        self.gps_w.setGeometry(int(0.05*self.gps_frame.geometry().width()), int(0.05*self.gps_frame.geometry().height()), int(0.9*self.gps_frame.geometry().width()), int(0.9*self.gps_frame.geometry().height()))

        # Gráficas 
        # self.altura_frame.setGeometry(0, int(height_f*0.02), int(width*0.20), height_f - int(height_f*0.03) - 31)
        self.altura_cp.frame.setGeometry(0, int(height_f*0.02), int(width*0.09), height_f - int(height_f*0.03) - 31)
        self.altura_cs.frame.setGeometry(int(width*0.1), int(height_f*0.02), int(width*0.09), height_f - int(height_f*0.03) - 31)
        self.presion_frame.setGeometry(int(width_f*(0.158 + 0.105)), int(height_f*0.02), int(width_f*(0.46 - 0.05)), height_f - int(height_f*0.03) - 31) 
        self.temp_frame.setGeometry(int(width_f*(0.62 + 0.06)), int(height_f*0.02), int(width_f*(0.365 - 0.06)), height_f - int(height_f*0.52)) 
        self.volt_frame.setGeometry(int(width_f*(0.62 + 0.06)), int(height_f*0.51), int(width_f*(0.365 - 0.06)), height_f - int(height_f*0.52) - 31)
        
        self.altura_cp.Resize()
        self.altura_cs.Resize()
               
        # Identificadores: 
        self.frame_data.setGeometry(int(width*0.018), int(height*0.08), width - int(width*0.036), int(height*0.185))
        width_f, height_f = self.frame_data.geometry().width(), self.frame_data.geometry().height() 
        self.hora_frame.setGeometry(int(width_f*0.04), int(height_f*0.2), 200, 30) 
        self.launcht_frame.setGeometry(200 + int(width_f*0.06), int(height_f*0.2), 200, 30) 
        self.pack_frame.setGeometry(width_f - 400 - int(width_f*0.06), int(height_f*0.2), 200, 30) 
        self.id_frame.setGeometry(width_f- 200 - int(width_f*0.04), int(height_f*0.2), 200, 30) 
        self.estado_frame.setGeometry(width_f- 600 - int(width_f*0.08), int(height_f*0.2), 200, 30)
        self.hora.setGeometry(int(width_f*0.04), int(height_f*0.24) + 30, 200, 50)
        self.launcht.setGeometry(200 + int(width_f*0.06), int(height_f*0.24) + 30, 200, 50)
        self.pack.setGeometry(width_f - 400 - int(width_f*0.06), int(height_f*0.24) + 30, 200, 50)
        self.id.setGeometry(width_f- 200 - int(width_f*0.04), int(height_f*0.24) + 30, 200, 50)
        self.estado.setGeometry(width_f- 600 - int(width_f*0.08), int(height_f*0.24) + 30, 200, 50)

        # Datos de los sensores:  
        self.frame_sensores.setGeometry(int(width - width*0.2), int(height*0.3), width - int(width*0.818), int(height*0.65)) 
        width_f, height_f = self.frame_sensores.geometry().width(), self.frame_sensores.geometry().height() 
        self.velocidad_label.setGeometry(int(width_f*0.08), int(height_f/8) - 15, int(width_f*0.37), 30)
        self.rpm_label.setGeometry(int(width_f*0.08),  2*int(height_f/8) - 15, int(width_f*0.37), 30)
        self.pitch_label.setGeometry(int(width_f*0.08), 3*int(height_f/8) - 15, int(width_f*0.37), 30)
        self.roll_label.setGeometry(int(width_f*0.08), 4*int(height_f/8) - 15, int(width_f*0.37), 30)
        self.velocidad.setGeometry(int(width_f*0.55), 1*int(height_f/8) - 15, int(width_f*0.35), 30)
        self.rpm.setGeometry(int(width_f*0.55), 2*int(height_f/8) - 15, int(width_f*0.35), 30)
        self.pitch.setGeometry(int(width_f*0.55), 3*int(height_f/8) - 15, int(width_f*0.35), 30)
        self.roll.setGeometry(int(width_f*0.55), 4*int(height_f/8) - 15, int(width_f*0.35), 30)

