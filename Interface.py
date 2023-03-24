from PySimpleGUI import PySimpleGUI as sg
from AuditoriaST import Read_xml as db

sg.theme('Light Grey')
layout = [
    [sg.Text('Pasta de origem'), sg.Input(key='orig')],
    [sg.Button('Executar'),sg.Button('Cancelar'), sg.Text('Desenvolvido por Bruno Luiel')]
]

janela = sg.Window('Copiador de Arquivos', layout)

sg.Popup('Este é um programa de auditoria onde será feito um cruzamento dos dados do XML com o banco de dados.\n No primeiro campo selecione onde está a pasta que contem todos os XMLS\n Na mesma pasta constarão os arquivos "TXT" com o resultado da auditoria')
while True:
    evento, valores = janela.read()#eventos é click e valores é os dados inseridos
    if evento == sg.WIN_CLOSED:
        break
    if evento == 'Cancelar':
        break
    if evento == 'Executar':
        x = db(valores['orig'])   
        sg.Popup(f'Auditoria finalizada!')



janela.close()