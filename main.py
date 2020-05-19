import _thread
import time
import tkinter as tk 
import datastorage as dsm
import downlink
import uplink
import fastreport
import socket
import PySimpleGUI as sg
import select
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

flightIP = 'localhost'
flightDoor = 10000
bufsize = 4812


def downlinkThread():
    server_address = (flightIP, flightDoor)
    print('starting up on {} port {}'.format(*server_address))
    sock.bind(server_address)
    while True:
      print(downlink.read(sock, bufsize))




command_list = ['']

def userInterface():
   server_address = (flightIP, flightDoor)
   sock.bind(server_address)
   sock.setblocking(0)
   #print = sg.Print
   title= "STRATOSPOLCA - Ground Support Unit"
   sg.theme('DarkAmber')	
   # All the stuff inside your window.
   menu_def = [
      ['Reconnect', ['Define IP', 'Reconnect']],
      ['Fast Report Module', ['Temperature', 'Events']],
      ['Quit']
         ]
   
   layout = [  [sg.Text('STRATOSPOLCA/SAAA-AAC')],
               [sg.MenuBar(menu_def,)],
               [sg.Text('Uplink:'), sg.Text(' '*78), sg.Text('Downlink:')],
               [sg.Multiline(size=(50,10), key='-UPLINK-'), sg.Multiline(size=(50,10), key='-DOWNLINK-')],
               [sg.Text('COMMAND:'), sg.OptionMenu(('SOE', 'MANUAL', 'AUTO', 'SAMPLE START', 'SAMPLE STOP', 'RESET', 'DC RESET', 'DC DISABLE', 'THERMAL RESET', 'THERMAL DISABLE'), key = '-COM-'), sg.Button('SEND')],
               [sg.Button('Ok'), sg.Button('Quit')]]

   # Create the Window
   window = sg.Window(title, layout)
   # Event Loop to process "events" and get the "values" of the inputs
   time.sleep(4)
   window.Finalize()
   window['-DOWNLINK-'].print('starting up on {} port {}'.format(*server_address))
   window['-DOWNLINK-'].print('waiting to receive message')
   while True:
      ready = select.select([sock], [], [], 1)
      if ready[0]:
         data_received = sock.recv(bufsize)
         #TODO Gravar em Documento
         window['-DOWNLINK-'].print(data_received)
         window.Refresh()
      event, values = window.Read(timeout=0)
      if event in ('Quit'):	# if user closes window or clicks cancel
         window.close()
         sock.close()
         break
      if event == 'SEND': 
         window['-UPLINK-'].print(time.ctime(), '>', values['-COM-'])
         print(event, values)

   window.close()
   sock.close()
   sys.exit()
   
userInterface()

# try:
#    #_thread.start_new_thread( userInterface , () )
#    #_thread.start_new_thread( downlinkThread, () )
#    userInterface()
# except:
#    print ("Error: unable to start thread")