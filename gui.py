import PySimpleGUI as sg

layout = [
    [sg.Text("Welcome to MLB Pitching Coach! Upload baseball savant data here:"), sg.Input(key="-IN-"), sg.FileBrowse()],
    [sg.Exit(), sg.OK()]
]

window = sg.Window("MLB Pitching Coach", layout)

while True:
    event, values = window.read()
    print(event, values)
    if event in (sg.WINDOW_CLOSED, "Exit"):
      break
    