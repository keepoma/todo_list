import functions as fu
import PySimpleGUI as sg
import time

sg.theme('Black')

clock = sg.Text('', key='clock')
label = sg.Text("To-do")
input_box = sg.Input(tooltip="Type here", key="todo")
add_button = sg.Button("Add")
list_box = sg.Listbox(values=fu.read_file(), key='todos',
                      enable_events=True, size=(45, 10))
edit_button = sg.Button("Edit")
complete_button = sg.Button("Complete")
exit_button = sg.Button("Exit", button_color="red")

window = sg.Window("My To-Do App",
                   layout=[[clock],
                           [label, input_box, add_button],
                           [list_box, edit_button],
                           [complete_button, exit_button]],
                   font=("Helvetica", 16))

while True:
    event, values = window.read(timeout=200)
    window['clock'].update(value=time.strftime("%Y, %b. %d  %H:%M:%S"))
    print("Event:", event)
    print("Values", values)
    print("---")
    match event:
        case 'Add':
            todos = fu.read_file()
            todos.append(values["todo"] + "\n")
            fu.write_file(todos)
            window['todos'].update(values=todos)
        case 'Edit':
            try:
                new_todo = values['todo']
                todo_to_edit = values['todos'][0]
                todos = fu.read_file()
                index = todos.index(todo_to_edit)
                todos[index] = new_todo
                fu.write_file(todos)
                window['todos'].update(values=todos)
            except IndexError:
                sg.popup("Select an item first", font=("Helvetica", 16))
        case 'todos':
            window['todo'].update(value=values['todos'][0])
        case 'Complete':
            try:
                to_pop = values["todos"][0]
                todos = fu.read_file()
                todos.remove(to_pop)
                #todos.pop(todos.index(to_pop))
                fu.write_file(todos)
                window['todos'].update(values=todos)
                window['todo'].update(value='')
            except IndexError:
                sg.popup("Select an item first", font=("Helvetica", 16))
        case sg.WIN_CLOSED:
            break
        case "Exit":
            break

window.close()
