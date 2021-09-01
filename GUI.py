import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msg
import tkinter.filedialog as fdialog
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import time
import smbus
from random import gauss
from matplotlib import animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Mainframe(ttk.Frame):
    def __init__(self,master,*args,**kwargs):
        # *args junta os argumentos posicionais na tupla args
        #  **kwargs junta os argumentos de palavras chave no dicionário kwargs
        
        super(Mainframe,self).__init__(master,*args,**kwargs)
        # using super means if you change the base class 
        # you do not have to change this line
        # in this case the * and ** operators unpack the parameters
        
class App(tk.Tk):
    def __init__(self):
        super(App,self).__init__()
               
        # Título da Janela, dimensão e ícone do aplicativo
        self.title('ConFoSol')
        self.geometry("")
        #self.iconbitmap(r'solda.ico')
        
        # Criar a barra de ferramentas
        mainMenu = tk.Menu(self)
        self.config(menu=mainMenu)
        
        # Cria um menu de Arquivos na barra de ferramentas
        fileMenu = tk.Menu(mainMenu, tearoff = 0)
        mainMenu.add_cascade(label='Arquivos',menu=fileMenu)
        fileMenu.add_command(label='Salvar', command = self.saveFile)
        fileMenu.add_command(label='Salvar como...', command = self.saveAsFile)
        fileMenu.add_command(label='Abrir', command = self.browseFile)
        
        # Menu de ajuda
        helpMenu = tk.Menu(mainMenu, tearoff = 0)
        mainMenu.add_cascade(label = 'Ajuda',menu = helpMenu)
        helpMenu.add_command(label = 'Sobre',command = self.showAbout)
        
        # Widgets
        self.connectBtn = ttk.Button(self,text = 'Conectar',width = 20, command=self.connect)
        self.analyzeBtn = ttk.Button(self,text = 'Analisar',width = 20, command=self.analyzeGraph)
        self.graphBtn = ttk.Button(self,text = 'Transmitir',width = 20, command = self.graph)
        self.resetBtn = ttk.Button(self,text = 'Resetar',width = 20, command=self.resetSetting)
        self.quitBtn = ttk.Button(self,text = 'Fechar',width = 20,command = self.quit)

        self.connectBtn.grid(row=1, column=1, ipady = 5)
        self.analyzeBtn.grid(row=2, column=1, ipady = 5)
        self.resetBtn.grid(row=3, column=1, ipady = 5)
        self.graphBtn.grid(row=4, column=1, ipady = 5)
        self.quitBtn.grid(row=6, column=1, ipady = 5)


        # Labels em branco para formatar os espaços entre widgets
        ttk.Label(self, text = "").grid(row=0, column=0, ipadx=10, ipady = 10)
        ttk.Label(self, text = "").grid(row=0, column=2, ipadx=20, ipady = 10)
        ttk.Label(self, text = "").grid(row=0, column=5, ipadx=10, ipady = 10)
        ttk.Label(self, text = "").grid(row=0, column=7, ipadx=10, ipady = 10)

        ttk.Label(self, text = "").grid(row=5, column=0, ipadx=10, ipady = 10)
        ttk.Label(self, text = "").grid(row=7, column=0, ipadx=10, ipady = 10)
        ttk.Label(self, text = "").grid(row=8, column=0, ipadx=10, ipady = 10)
        ttk.Label(self, text = "").grid(row=9, column=0, ipadx=10, ipady = 10)
        ttk.Label(self, text = "").grid(row=12, column=0, ipadx=10, ipady = 10)

        # Corrente máxima      
        ttk.Label(self, text = "Corrente máxima (A)").grid(row=1, column=3)
        self.maxCurrentEntry = ttk.Entry(self, width = 10)
        self.maxCurrentEntry.grid(row=1, column=4)

        # Término do aumento da transmissão/recepção de corrente em segundos       
        ttk.Label(self, text = "Início de estabilidade (s)").grid(row=2, column=3)
        self.increaseTimeEntry = ttk.Entry(self, width = 10)
        self.increaseTimeEntry.grid(row=2, column=4)

        # Início da diminuição transmissão/recepção de corrente em segundos       
        ttk.Label(self, text = "Início do decremento (s)").grid(row=3, column=3)
        self.decreaseTimeEntry = ttk.Entry(self, width = 10)
        self.decreaseTimeEntry.grid(row=3, column=4)

        # Corrente estável      
        ttk.Label(self, text = "Segunda corrente (A)").grid(row=4, column=3)
        self.secondCurrentEntry = ttk.Entry(self, width = 10)
        self.secondCurrentEntry.grid(row=4, column=4)

        # Início da estabilidade        
        ttk.Label(self, text = "Segunda estabilidade (s)").grid(row=5, column=3)
        self.stableTimeEntry = ttk.Entry(self, width = 10)
        self.stableTimeEntry.grid(row=5, column=4)

        # Início da segunda diminuição de corrente       
        ttk.Label(self, text = "Ultimo decremento (s)").grid(row=6, column=3)
        self.lastDecreaseTimeEntry = ttk.Entry(self, width = 10)
        self.lastDecreaseTimeEntry.grid(row=6, column=4)

        # Término da transmissão/recepção em milisegundos       
        ttk.Label(self, text = "Tempo máximo (s)").grid(row=7, column=3)
        self.endTimeEntry = ttk.Entry(self, width = 10)
        self.endTimeEntry.grid(row=7, column=4)

        # Amostras por segundo
        ttk.Label(self, text = "Amostras por segundo").grid(row=8, column=3)
        self.samplesPerSecEntry = ttk.Entry(self, width = 10)
        self.samplesPerSecEntry.insert(0,"5")
        self.samplesPerSecEntry.grid(row=8, column=4)

        #Botão para atualizar as listas de tempo, corrente e tensão
        self.writeBtn = ttk.Button(self,text = 'Alterar',width = 25, command=self.initialParameters)
        self.writeBtn.grid(row=10, column=4)


        ################Deletar
        self.maxCurrentEntry.insert(0,"100")
        self.increaseTimeEntry.insert(0,"10")
        self.decreaseTimeEntry.insert(0,"20")
        self.stableTimeEntry.insert(0,"30")
        self.secondCurrentEntry.insert(0,"50")
        self.lastDecreaseTimeEntry.insert(0,"50")
        self.endTimeEntry.insert(0,"70")
        ##################

        self.bus = smbus.SMBus(1)

        # Cria a janela Mainframe
        Mainframe(self)

    def browseFile(self):
        self.filePathOpen = fdialog.askopenfilename()
        data = pd.read_csv(self.filePathOpen)
        try:
            self.xValue = data['xValue']
            self.currentTx = data['currentTx']
            self.currentRx = data['currentRx']
            self.voltageRx = data['voltageRx']
            self.potTx = data['powerTx']
            self.potRx = data['powerRx']
        except:
            msg.showerror('Erro de leitura', 'Algum dos parâmetros não foi encontrado')
            return

    def updateValues(self):
        try:
            self.maxCurrent = float(self.maxCurrentEntry.get())   
            self.secondCurrent = float(self.secondCurrentEntry.get())    
            self.increaseTime = float(self.increaseTimeEntry.get())
            self.decreaseTime = float(self.decreaseTimeEntry.get())
            self.stableTime = float(self.stableTimeEntry.get())
            self.lastDecreaseTime = float(self.lastDecreaseTimeEntry.get())
            self.endTime = float(self.endTimeEntry.get())
            self.samplesPerSec = int(self.samplesPerSecEntry.get())
            if ((self.endTime < self.lastDecreaseTime or self.lastDecreaseTime < self.stableTime or self.stableTime < self.decreaseTime or self.decreaseTime < self.increaseTime)):
                msg.showerror('Parâmetros', 'O tempo máximo deve ser maior do que o início do decremento e término do incremento!')
            else:
                return
        except:
            msg.showerror('Parâmetros', 'Algum dos parâmetros não foi alterado corretamente (separador de decimal deve ser um ponto ".")')
        return

    def initialParameters(self):
        self.updateValues()
        self.stepSize = 1/self.samplesPerSec
        self.xValue = [0]
        self.currentTx = []
        self.currentRx = []
        self.voltageRx = []
        self.j=0

        # Salva os valores de tempo na lista xValue
        while self.xValue[-1] < self.endTime:
                self.xValue.append(round((len(self.xValue)*self.stepSize),4))
        if self.xValue[-1] > self.endTime:
                self.xValue[-1:] = self.endTime    
        
        # Valores de corrente na lista currentTx 
        # Incremento de corrente
        while self.xValue[self.j] < (self.increaseTime):
            self.currentTx.append(round(self.xValue[self.j]*self.maxCurrent/self.increaseTime, 2))
            self.j = self.j +1

        # Corrente máxima constante
        while self.xValue[self.j] < self.decreaseTime:
            self.currentTx.append(round(self.maxCurrent, 2))
            self.j = self.j +1

        # Primeiro decremento de corrente
        while self.xValue[self.j] < self.stableTime:
            current = (self.xValue[self.j]*(self.maxCurrent - self.secondCurrent) + (self.secondCurrent*self.decreaseTime - self.maxCurrent*self.stableTime))/(self.decreaseTime - self.stableTime)
            self.currentTx.append(round(current))
            self.j = self.j +1

        # Segunda corrente estável
        while self.xValue[self.j] < self.lastDecreaseTime:
            self.currentTx.append(round(self.secondCurrent, 2))
            self.j = self.j +1

        # Último decremento de corrente
        while self.xValue[self.j] < self.endTime:
            self.currentTx.append(round(self.secondCurrent*(self.xValue[self.j]-self.endTime) / (self.lastDecreaseTime-self.endTime), 2))
            self.j = self.j +1

        # Garante que a última amostra é igual a zero
        if len(self.xValue) > len(self.currentTx):
                self.currentTx.append(int(0))
        
        fig, ax = plt.subplots()
        ax.cla()
        ax.plot(self.xValue, self.currentTx, label='Transmissao da corrente')
        ax.legend()
        ax.set_title('Controle da corrente')
        ax.set_xlabel('Tempo(s)')
        ax.set_ylabel('Corrente(A)')
        fig.tight_layout()
        plt.grid()
        plt.show()


    def graph(self):
        plt.style.use('tableau-colorblind10')
        self.updateValues()            
        figs, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, sharex=True)

        self.x = []
        self.y1 = []
        self.index=0
        self.startTime = time.perf_counter()
        def animate(i):                    
            self.i2cTransfer()
            
            ax1.cla()
            ax2.cla()
            ax1.set_title('Comunicação I2C')
            ax1.set_ylabel('Corrente(A)')
            ax2.set_ylabel('Tensão(V)')
            ax2.set_xlabel('Tempo(s)')
            ax1.plot(self.x, self.y1, label='Corrente transmitida')
            ax1.plot(self.x, self.currentRx, label='Corrente medida')
            ax2.plot(self.x, self.voltageRx, label='Tensao medida')
            ax1.legend()
            ax2.legend()
            ax1.grid()
            ax2.grid()
            figs.tight_layout()

            if self.index == len(self.currentTx):
                ani.event_source.stop()
                ax1.fill_between(self.xValue, self.currentRx, self.currentTx, facecolor = 'green', interpolate = True, alpha = 0.25)
                self.powerW()
                figure, (pax1, pax2) = plt.subplots(nrows=2, ncols=1, sharex=True)
                pax1.set_title('Potência em Quilowatts')
                pax1.set_ylabel('Potência(kW)')
                pax2.set_ylabel('Potência(kW)')
                pax2.set_xlabel('Tempo(s)')
                pax1.plot(self.xValue, self.potTx, label='Potência enviada')
                pax1.plot(self.xValue, self.potRx, label='Potência medida')
                pax1.fill_between(self.xValue, self.potTx, self.potRx, facecolor = 'green', interpolate = True, alpha = 0.25)
                pax2.plot(self.xValue, self.potDif, label='Diferença da potência medida e enviada')
                pax2.fill_between(self.xValue, 0, self.potDif, where = np.array(self.potDif)>=0, facecolor = 'green', interpolate = True, alpha = 0.25)
                pax2.fill_between(self.xValue, self.potDif, 0, where = np.array(self.potDif)<=0, facecolor = 'red', interpolate = True, alpha = 0.25)
                pax1.legend()
                pax2.legend()
            
                pax1.grid()
                pax2.grid()
                figure.tight_layout()
                plt.show()
                
        ani = animation.FuncAnimation(plt.gcf(), animate, interval = 1, repeat=False)
        plt.show()

    # Função para fazer o envio e recebimento dos dados
    def i2cTransfer(self):
        for i in range(self.samplesPerSec):
            if self.index == len(self.currentTx):
                break
            nowTime = time.perf_counter() - self.startTime
            while nowTime < self.xValue[self.index]:
                nowTime = time.perf_counter() - self.startTime
            try:
                # Enviar o valor da corrente a ser alterada
                MSBTx = (int(self.currentTx[self.index]*100)) >> 8
                LSBTx = (int(self.currentTx[self.index]*100)) & 255
                self.bus.write_byte(0x10, LSBTx)
                self.bus.write_byte(0x10, MSBTx)
            except:
                print('Problema na transferência')
            try:
                # Receber a corrente medida
                LSBRx = self.bus.read_byte(0x10)
                MSBRx = self.bus.read_byte(0x10)
                val = ((MSBRx << 8) + LSBRx)
                val=val*0.001*gauss(10,1)
                self.currentRx.append(round(val,2))
            except:
                print('Problema na recepção da corrente')
            try:
                # Receber a tensão medida
                LSBRx = self.bus.read_byte(0x10)
                MSBRx = self.bus.read_byte(0x10)
                val = ((MSBRx << 8) + LSBRx)
                val=val*0.01
                self.voltageRx.append(round(val,2))
            except:
                print('Problema na recepção da tensão')
            self.x.append(self.xValue[self.index])
            self.y1.append(self.currentTx[self.index])
            self.index = self.index + 1
        return
            
    def analyzeGraph(self):
        self.browseFile()
        figures, (ax01, ax02, ax03) = plt.subplots(nrows=3, ncols=1, sharex=True)
        ax01.cla()
        ax02.cla()
        ax03.cla()
        ax01.set_title(self.filePathOpen)
        ax01.set_ylabel('Corrente(A)')
        ax02.set_ylabel('Tensao(V)')
        ax03.set_ylabel('Potência(kW)')
        ax02.set_xlabel('Tempo(s)')
        ax01.plot(self.xValue, self.currentTx, label='Corrente enviada')
        ax01.plot(self.xValue, self.currentRx, label='Corrente medida')
        ax02.plot(self.xValue, self.voltageRx, label='Tensao medida')
        ax03.plot(self.xValue, self.potTx, label='Potência enviada')
        ax03.plot(self.xValue, self.potRx, label='Potência medida')
        ax01.legend()
        ax02.legend()
        ax03.legend()
        ax01.grid()
        ax02.grid()
        ax03.grid()

        figures.tight_layout()
        plt.show()


    def connect(self):
        try:
            self.bus.write_quick(0x10)
            msg.showinfo('Conexão', 'Conectado com escravo no endereço: 0x10.')
        
        except:
            msg.showerror('Conexão', 'Escravo não conectado.')
            return
       
    def powerW(self):
        self.potTx = []
        self.potRx = []
        self.potDif = []
        for i in range(len(self.currentRx)):
            pot = self.currentTx[i]*self.voltageRx[i]
            self.potTx.append(round(pot/1000,2))
            pot = self.currentRx[i]*self.voltageRx[i]
            self.potRx.append(round(pot/1000,2))   
            self.potDif.append(self.potRx[i] - self.potTx[i])     
        
    def resetSetting(self):
        self.maxCurrentEntry.delete(0,'end')
        self.increaseTimeEntry.delete(0,'end')
        self.decreaseTimeEntry.delete(0,'end')
        self.stableTimeEntry.delete(0,'end')
        self.lastDecreaseTimeEntry.delete(0,'end')
        self.secondCurrentEntry.delete(0,'end')
        self.endTimeEntry.delete(0,'end')
        self.samplesPerSecEntry.delete(0,'end')

    def saveAsFile(self):
        self.filePathSave = fdialog.asksaveasfilename(initialdir="/<file_name>", initialfile="({}-{}-{}-{})_{}s__({}_{})A__{}SampPerSec".format(round(self.increaseTime),round(self.decreaseTime),round(self.stableTime),round(self.lastDecreaseTime),round(self.endTime),round(self.maxCurrent),round(self.secondCurrent),self.samplesPerSec), defaultextension='.csv', filetypes=[("Comma Separated Values",".csv"),("All files",".*")])
        pd.DataFrame({'xValue':self.xValue,'currentTx':self.currentTx, 'currentRx':self.currentRx, 'voltageRx':self.voltageRx, 'powerTx':self.potTx, 'powerRx':self.potRx}).to_csv(self.filePathSave, index=False)

    def saveFile(self):
        if self.filePathSave != "":
            pd.DataFrame({'xValue':self.xValue,'currentTx':self.currentTx, 'currentRx':self.currentRx, 'voltageRx':self.voltageRx, 'powerTx':self.potTx, 'powerRx':self.potRx}).to_csv(self.filePathSave, index=False)
        else:
            try:
                pd.DataFrame({'xValue':self.xValue,'currentTx':self.currentTx, 'currentRx':self.currentRx, 'voltageRx':self.voltageRx, 'powerTx':self.potTx, 'powerRx':self.potRx}).to_csv(self.filePathOpen, index=False)
            except:
                msg.showerror('')    


    def showAbout(self):
        # Ajuda sobre o programa
        msg.showinfo('Ajuda', 'Para iniciar o programa, aperte o botão "Conectar" para estabelecer a conexão I2C com o escravo'
        'Alterar as correntes e tempos desejados e clicar no botão "Alterar" para ver no gráfico as mudanças realizadas.'
        'Para transferir os dados, conferir se está conectado, e clicar no botão Transmitir.'
        'Em caso de dúvidas, entrar em contato com: Renan.Tomisaki@gmail.com')
            
# Cria e roda o objeto App
App().mainloop()
