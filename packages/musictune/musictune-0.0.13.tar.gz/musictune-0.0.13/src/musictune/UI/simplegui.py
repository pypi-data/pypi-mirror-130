import PySimpleGUI as sg

# param = {}
# while True:
#     config_path = sg.popup_get_file('Please enter a file name', file_types=(('.json', '*.json'),), history=True)
#     if not os.path.isfile(config_path):
#         sg.popup('Invalid file path', f'{config_path} is not valid')
#         continue
#     else:
#         param['config_path'] = config_path
#         break

# layout the window

# ------ Column Definition ------ #
column1 = [[sg.Text('Column 1', background_color='lightblue', justification='center', size=(10, 1))],
           [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 1')],
           [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 2')],
           [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 3')]]

layout = [
    [sg.Text('Config filepath', size=(15, 1), auto_size_text=False, justification='right'),
     sg.InputText('e.g. /hpc/user/img.json'), sg.FileBrowse(file_types=(("json", "*.json"),)), sg.Button('Load', )],
    [sg.Text('_' * 80)],
    [sg.Frame('Processing range', [
        [sg.Text('Blocks range', justification='right'), sg.InputText('10-15')],
        [sg.Text('Lasers', justification='right'), sg.Checkbox('561', size=(10, 1)),
         sg.Checkbox('640', default=True)],
        [sg.Text('Z range', justification='right'), sg.InputText('100-250')]])]

    # [sg.Text('Here is some text.... and a place to enter text')],
    # [sg.InputText('This is my text')],
    # [sg.Frame(layout=[
    #     [sg.Checkbox('Checkbox', size=(10, 1)), sg.Checkbox('My second checkbox!', default=True)],
    #     [sg.Radio('My first Radio!     ', "RADIO1", default=True, size=(10, 1)),
    #      sg.Radio('My second Radio!', "RADIO1")]], title='Options', title_color='red', relief=sg.RELIEF_SUNKEN,
    #     tooltip='Use these to set flags')],
    # [sg.Multiline(default_text='This is the default Text should you decide not to type anything', size=(35, 3)),
    #  sg.Multiline(default_text='A second multi-line', size=(35, 3))],
    # [sg.InputCombo(('Combobox 1', 'Combobox 2'), size=(20, 1)),
    #  sg.Slider(range=(1, 100), orientation='h', size=(34, 20), default_value=85)],
    # [sg.InputOptionMenu(('Menu Option 1', 'Menu Option 2', 'Menu Option 3'))],
    # [sg.Listbox(values=('Listbox 1', 'Listbox 2', 'Listbox 3'), size=(30, 3)),
    #  sg.Frame('Labelled Group', [[
    #      sg.Slider(range=(1, 100), orientation='v', size=(5, 20), default_value=25, tick_interval=25),
    #      sg.Slider(range=(1, 100), orientation='v', size=(5, 20), default_value=75),
    #      sg.Slider(range=(1, 100), orientation='v', size=(5, 20), default_value=10),
    #      sg.Column(column1, background_color='lightblue')]])],
]

window = sg.Window('PZF2ZARR', layout, default_element_size=(40, 1), grab_anywhere=False)
event, values = window.read()
window.close()

# sg.Popup('Title',
#          'The results of the window.',
#          'The button clicked was "{}"'.format(event),
#          'The values are', values)
