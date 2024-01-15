from tkinter import *

import sqlite3


root =Tk()

root.title('''Gestor de Tareas''')
root.geometry('500x500')

conn = sqlite3.connect('todo.bd')

c = conn.cursor()

c.execute("""
    CREATE TABLE if not exists todo(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        create_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        description TEXT NOT NULL,
        completed BOOLEAN NOT NULL
    );
""")

conn.commit()
#funcion que elimina la tarea despues que esta relizada
def remove(id):
    def _remove():
        c.execute('DELETE FROM todo WHERE id = ?', (id, ))
        conn.commit()
        mostrar_todo()

    return _remove
#funcion que marca como completado o no el Checkbutton
#tambien llamda currying retrasar la ejecucion de una funcion
def completado(id):
    def _completado():
        todo = c.execute('SELECT * from todo WHERE id = ?', (id, )).fetchone()
        c.execute('UPDATE todo SET completed = ? WHERE id = ?', (not todo[3], id))
        conn.commit()
        mostrar_todo()


    return _completado

#renderizar los todo, o traer nos todo
def mostrar_todo():
    #Esto de buelve una lista 
    rows = c.execute('SELECT * FROM todo').fetchall()
    for Widget in contenedorFrame.winfo_children():
        Widget.destroy()
    #iteramos o recoremos para optener los valores
    for i in range(0, len(rows)):
        id = rows[i][0]
        completed = rows[i][3]
        description = rows[i][2]
        color = 'red' if completed else 'cyan'
        check = Checkbutton(contenedorFrame, text=description, fg=color, width=42, anchor='w', command=completado(id))
        check.grid(row=i, column=0, sticky='w')
        botonRemove=Button(contenedorFrame, text='Eliminar',anchor='e', padx=30, border=2, command=remove(id))
        botonRemove.grid(row=i, column=1)
        check.select() if completed else check.deselect()






#funcion para agregar tareas
def addTodo():
    todo = campoDeTexto.get()
    if todo:
        c.execute('''
                INSERT INTO todo ( description, completed ) VALUES (?, ?)
                ''', (todo, False))
        conn.commit()
        campoDeTexto.delete(0, END)
        mostrar_todo()
    else:
        pass


tarea = Label(root, text='Tarea')
tarea.grid(row=0, column=0)


campoDeTexto = Entry(root, width=40)

campoDeTexto.grid(row=0, column=1)

botonAgregar=Button(root, text='agregar', command=addTodo)
botonAgregar.grid(row=0, column=2,)

contenedorFrame=LabelFrame(root, text='Mis Tareas')
contenedorFrame.grid(row=1, column=0, columnspan=3, sticky='nswe', padx=5)


campoDeTexto.focus()

root.bind('<Return>', lambda x:addTodo())

mostrar_todo()
root.mainloop()
