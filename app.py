import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import Label, Button, Entry
from analise_matricial import *

class Demo1:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        master.title("APS 2 - Transferência de Calor e Mecânica dos sólidos")

        self.titulogrande = Label(master, text = "Analise de estruturas")
        self.titulogrande.config(font = ("Arial", 30))
        self.titulogrande.grid(row = 0)

        self.labelOpcoes = Label(self.master, text = "Insira manualmente os dados ou o arquivo .txt")
        self.labelOpcoes.config(font = ("Arial bold", 18))
        self.labelOpcoes.grid(row = 1, column = 0)

        self.insertTxt_button = Button(self.master, text = "Inserir arquivo .txt", command = self.OpenFile)  #Inserir comando de entrada
        self.insertTxt_button.grid(row = 2, column = 0)
        self.UploadedFile = ""

        self.filename = ""
        if(self.filename != ""):
            self.master.destroy()

        self.nos_entry_label = Label(self.master, text = "Número de nós da estrutura:")
        self.nos_entry_label.grid(row = 3, column = 0)

        self.elementos_entry_label = Label(self.master, text = "Número de elementos da estrutura:")
        self.elementos_entry_label.grid(row = 4, column = 0)

        self.cargas_entry_label = Label(self.master, text = "Número de cargas aplicadas:")
        self.cargas_entry_label.grid(row = 5, column = 0)

        self.nos_entry = Entry(self.master)
        self.nos_entry.grid(row = 3, column = 1)

        self.elementos_entry = Entry(self.master)
        self.elementos_entry.grid(row = 4, column = 1)

        self.cargas_entry = Entry(self.master)
        self.cargas_entry.grid(row = 5, column = 1)

        self.greet_button = Button(self.master, text = "Next", command = self.new_window)
        self.greet_button.grid(row = 6, column = 1)    


    def new_window(self):
        self.n_cargas = int(self.cargas_entry.get())
        self.n_nos = int(self.nos_entry.get())
        self.n_elementos = int(self.elementos_entry.get())
        self.newWindow = tk.Toplevel(self.master)
        self.app = Insira_nos(self.newWindow, self.n_nos, self.n_elementos, self.n_cargas)
        # self.master.destroy()

    def OpenFile(self):
        self.filename = askopenfilename(initialdir="./",
                           filetypes =(("Text File", "*.txt"),("All Files","*.*")),
                           title = "Choose a file."
                           )
        self.master.destroy()
        #Using try in case user types in unknown file or closes without choosing a file.
        # try:
        #     with open(self.filename,'r') as UseFile:
        #         print(UseFile.read())
        #         # f = UseFile
        #         # self.UploadedFile = f
        # except:
        #     print("No file exists")

class Insira_nos:
    def __init__(self, master, n_nos, n_elementos, n_cargas):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.n_nos = n_nos
        self.n_elementos = n_elementos
        self.n_cargas = n_cargas

        self.lista_nos = []
        self.lista_elementos = []
        self.lista_materiais = []
        self.lista_area = []
        self.lista_gdlX = []
        self.lista_gdlY = []
        self.lista_nos_carga = []
        self.lista_forca_aplicada = []
        self.lista_direcao = []

        self.f_nos = []
        self.f_elementos = []
        self.f_materiais = []
        self.f_area = []
        self.f_gdlX = []
        self.f_gdlY = []
        self.f_carga_nos = []
        self.f_forca_aplicada = []
        self.f_direcao = []

        self.coordenadas_label = Label(self.master, text = "Coordenadas")
        self.coordenadas_label.config(font = ("Arial bold", 18))
        self.coordenadas_label.grid(row = 0, column = 1)
        
        self.title_lable = Label(self.master, text = "Exemplo:")
        self.title_lable.grid(row = 1, column = 0)

        self.exemplo_no = Label(self.master, text = "x,y")
        self.exemplo_no.grid(row = 1, column = 1)

        for i in range(n_nos):
            nos_label = Label(self.master, text = "Nó {0}:".format(i + 1))
            nos_label.grid(row = i + 2, column = 0)
            en = Entry(self.master)
            en.grid(row = i + 2, column = 1)
            self.lista_nos.append(en)

        
        self.exemplo_elemento = Label(self.master, text = "Exemplo:")
        self.exemplo_elemento.grid(row = 1, column = 2)
        
        self.incidencia_label = Label(self.master, text = "Incidência")
        self.incidencia_label.config(font = ("Arial bold", 18))
        self.incidencia_label.grid(row = 0, column = 3)
        self.incidencia_exemplo = Label(self.master, text = "Nó1, Nó2")
        self.incidencia_exemplo.grid(row = 1, column = 3)

        self.materiais_label = Label(self.master, text = "Materiais")
        self.materiais_label.config(font = ("Arial bold", 18))
        self.materiais_label.grid(row = 0, column = 4)
        self.materiais_exemplo = Label(self.master, text = "Elasticidade, Tração, Compressão")
        self.materiais_exemplo.grid(row = 1, column = 4)

        self.area_label = Label(self.master, text = "Área Seção transversal")
        self.area_label.config(font = ("Arial bold", 18))
        self.area_label.grid(row = 0, column = 5)
        self.area_exemplo = Label(self.master, text = "Área")
        self.area_exemplo.grid(row = 1, column = 5)

        self.gdlx_label = Label(self.master, text = "Grau de Liberade X")
        self.gdlx_label.config(font = ("Arial bold", 18))
        self.gdlx_label.grid(row = 0, column = 6)
        self.gdlx_exemplo = Label(self.master, text = "0: Sem restrição, 1: Restrito")
        self.gdlx_exemplo.grid(row = 1, column = 6)

        self.gdly_label = Label(self.master, text = "Grau de Liberdade Y")
        self.gdly_label.config(font = ("Arial bold", 18))
        self.gdly_label.grid(row = 0, column = 7)
        self.gdly_exemplo = Label(self.master, text = "0: Sem restrição, 1: Restrito")
        self.gdly_exemplo.grid(row = 1, column = 7)
        
        self.filename = ""



        for x in range(n_elementos):
            elementos_label = Label(self.master, text = "Elemento {0}:".format(x + 1))
            elementos_label.grid(row = x + 2, column = 2)
            entry_elementos = Entry(self.master)
            entry_elementos.grid(row = x + 2, column = 3)
            self.lista_elementos.append(entry_elementos)

            entry_materiais = Entry(self.master)
            entry_materiais.grid(row = x + 2, column = 4)
            self.lista_materiais.append(entry_materiais)

            entry_area = Entry(self.master)
            entry_area.grid(row = x + 2, column = 5)
            self.lista_area.append(entry_area)

            entry_gdlx = Entry(self.master)
            entry_gdlx.grid(row = x + 2, column = 6)
            self.lista_gdlX.append(entry_gdlx)

            entry_gdly = Entry(self.master)
            entry_gdly.grid(row = x + 2, column = 7)
            self.lista_gdlY.append(entry_gdly) 


        if n_nos >= n_elementos:
            self.titulo_cargas = Label(self.master, text = "Nó Aplicado")
            self.titulo_cargas.config(font = ("Arial bold", 18))
            self.titulo_cargas.grid(row = n_nos + 5, column = 1)

            self.direcao = Label(self.master, text = "Direção da carga(1:X | 2:Y)")
            self.direcao.config(font = ("Arial bold", 18))
            self.direcao.grid(row = n_nos + 5, column = 3)   

            self.exemplo_valor = Label(self.master, text = "Valor em Newtons")
            self.exemplo_valor.config(font = ("Arial bold", 18))
            self.exemplo_valor.grid(row = n_nos + 5, column = 2)
        else:
            self.titulo_cargas = Label(self.master, text = "Nó Aplicado")
            self.titulo_cargas.config(font = ("Arial bold", 18))
            self.titulo_cargas.grid(row = n_elementos + 5, column = 1)

            self.direcao = Label(self.master, text = "Direção da carga(1:X | 2:Y)")
            self.direcao.config(font = ("Arial bold", 18))
            self.direcao.grid(row = n_elementos + 5, column = 3) 

            self.exemplo_valor = Label(self.master, text = "Valor em Newtons")
            self.exemplo_valor.config(font = ("Arial bold", 18))
            self.exemplo_valor.grid(row = n_elementos + 5, column = 2)


        for z in range(n_cargas):
            if n_nos >= n_elementos:
                cargas_label = Label(self.master, text = "Carga Aplicada {0}".format(z + 1))
                cargas_label.grid(row = n_nos + 6 + z, column = 0)

                entry_no_carga = Entry(self.master)
                entry_no_carga.grid(row = n_nos + 6 + z, column = 1)
                self.lista_nos_carga.append(entry_no_carga)

                entry_valor = Entry(self.master)
                entry_valor.grid(row = n_nos + 6 + z, column = 2)
                self.lista_forca_aplicada.append(entry_valor)

                entry_direcao = Entry(self.master)
                entry_direcao.grid(row = n_nos + 6 + z, column = 3)
                self.lista_direcao.append(entry_direcao)

            else:
                cargas_label = Label(self.master, text = "Carga Aplicada {0}".format(z + 1))
                cargas_label.grid(row = n_elementos + 6 + z, column = 0)

                entry_no_carga = Entry(self.master)
                entry_no_carga.grid(row = n_elementos + 6 + z, column = 1)
                self.lista_nos_carga.append(entry_no_carga)

                entry_valor = Entry(self.master)
                entry_valor.grid(row = n_elementos + 6 + z, column = 2)
                self.lista_forca_aplicada.append(entry_valor)

                entry_direcao = Entry(self.master)
                entry_direcao.grid(row = n_elementos + 6 + z, column = 3)
                self.lista_direcao.append(entry_direcao)


                

        self.greet_button = Button(self.master, text="Next", command = self.get_entradas)
        self.greet_button.grid(row = n_nos + n_cargas + 6, column = 6)

    def get_entradas(self):

        for entry in self.lista_nos:
            coordenadas = entry.get()
            coordenadas = coordenadas.split(',')
            self.f_nos.append(coordenadas)
        
        for entry in self.lista_elementos:
            elemento = entry.get()
            elemento = elemento.split(',')
            self.f_elementos.append(elemento)

        for entry in self.lista_materiais:
            materiais = entry.get()
            materiais = materiais.split(',')
            self.f_materiais.append(materiais)

        for entry in self.lista_area:
            area = entry.get()
            self.f_area.append(area)

        for entry in self.lista_gdlX:
            gdlX = entry.get()
            self.f_gdlX.append(gdlX)

        for entry in self.lista_gdlY:
            gdlY = entry.get()
            self.f_gdlY.append(gdlY)
        
        for entry in self.lista_nos_carga:
            no = entry.get()
            self.f_carga_nos.append(no)

        for entry in self.lista_forca_aplicada:
            forca = entry.get()
            self.f_forca_aplicada.append(forca)

        for entry in self.lista_direcao:
            direcao = entry.get()
            self.f_direcao.append(direcao)
        
        self.gera_arquivo()

    def gera_arquivo(self):
        txt_entradas = open("entradas.txt", "w")
        txt_entradas.write("*COORDINATES\n{0}\n".format(self.n_nos))
        i = 1
        for no in self.f_nos:
            txt_entradas.write("{0} {1} {2}\n".format(i, no[0], no[1]))
            i += 1

        txt_entradas.write("*INCIDENCES\n")
        i = 1
        for elemento in self.f_elementos:
            txt_entradas.write("{0} {1} {2}\n".format(i, elemento[0], elemento[1]))
            i += 1
        
        txt_entradas.write("*MATERIALS\n{0}\n".format(len(self.f_materiais)))
        for materiais in self.f_materiais:
            txt_entradas.write("{0} {1} {2}\n".format(materiais[0], materiais[1], materiais[2]))

        txt_entradas.write("*GEOMETRIC_PROPERTIES\n{0}\n".format(len(self.f_area)))
        for area in self.f_area:
            txt_entradas.write("{0}\n".format(area))

        txt_entradas.write("*BCNODES\n{0}\n".format(len(self.f_gdlX) + len(self.f_gdlY)))
        i = 0
        while i < len(self.f_gdlY) or i < len(self.f_gdlX):
            if self.f_gdlX[i] != 0:
                txt_entradas.write("{0} {1}\n".format(i + 1, self.f_gdlX[i]))
            if self.f_gdlY[i] != 0:
                txt_entradas.write("{0} {1}\n".format(i + 1, int(self.f_gdlY[i]) + 1))
            i += 1

        txt_entradas.write("*LOADS\n{0}\n".format(len(self.f_carga_nos)))
        i = 0
        while i < len(self.f_carga_nos):
            txt_entradas.write("{0} {1} {2}\n".format(self.f_carga_nos[i], self.f_direcao[i], self.f_forca_aplicada[i]))
            i += 1
        self.filename = "entradas.txt"
        self.master.destroy()




        

        

            

def main(): 
    root = tk.Tk()
    app = Demo1(root)
    # texto_manual = Insira_nos()
    root.mainloop()
    if (app.filename != ""):
        print("Foi")
        truss_calc(app.filename)
    # elif(app.filename != ""):
    #     truss_calc(app.)


if __name__ == '__main__':
    main() 