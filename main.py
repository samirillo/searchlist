from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition

import sqlite3
from kivymd.app import MDApp
from kivymd.uix.list import OneLineIconListItem

Builder.load_string(
    '''
#:import images_path kivymd.images_path
<CustomOneLineIconListItem>
    on_press:
        app.get_running_app().root.ids.screen_one.change_screen()
        app.get_running_app().root.ids.screen_one.clear_list()
    IconLeftWidget:
        icon: root.icon
<PreviousMDIcons>
    name:"'screen1"
    MDBoxLayout:
        orientation: 'vertical'
        spacing: dp(10)
        padding: dp(20)
        MDBoxLayout:
            adaptive_height: True
            MDIconButton:
                icon: 'magnify'
            MDTextField:
                id: search_field
                hint_text: 'Search icon'
                on_text: root.set_list_md_icons(self.text, True)
        RecycleView:
            id: rv
            key_viewclass: 'viewclass'
            key_size: 'height'
            RecycleBoxLayout:
                id:container
                padding: dp(10)
                default_size: None, dp(48)
                default_size_hint: 1, None
                size_hint_y: None
                height: self.minimum_height
                orientation: 'vertical'
<ScreenTwo>:        
    BoxLayout:
        orientation: "vertical"
        size: root.size
        spacing: 20
        padding: 20
        Label:
            id: label
            text: "health points: "
        Button:
            text:"go screen 1"
            on_press:root.change_screen()
<Manager>:
    id: screen_manager
    screen_one: screen_one
    screen_two: screen_two
    PreviousMDIcons:
        id: screen_one
        name: "screen1"
        manager: screen_manager
    ScreenTwo:
        id: screen_two
        name: "screen2"
        manager: screen_manager                
'''
)


class MySQlite:
    conn = None

    def create_connection(self, db_file):

        """ create a database connection to a SQLite database """

        try:
            self.conn = sqlite3.connect(db_file)
            return True
        except sqlite3.Error as e:
            print(e)
        return False

    def query(self, query, params="", return_rows=False):

        """Funcion que ejecuta la query
           query      = cadena sql
           params     = una tupla con los valores si son necesarios
           returnRows = determina si devuelve el resultado """

        if not self.conn:
            return False

        try:

            c = self.conn.cursor()

            c.execute(query, params) if params else c.execute(query)

            if return_rows:
                # devolvemos los registros devueltos por la consulta
                return c.fetchall()
            self.conn.commit()
            # devolvemos los registros afectados
            return c.rowcount
        except sqlite3.Error as e:
            print(e)
        return False

    def create_table(self, query):

        return self.query(query)

    def insert_row(self, query, params):

        return self.query(query, params)

    def update_row(self, query, params):

        return self.query(query, params)

    def delete_row(self, query, params):

        return self.query(query, params)

    def get_rows(self, query, params=""):

        return self.query(query, params, True)


class CustomOneLineIconListItem(OneLineIconListItem):
    icon = StringProperty()


class ScreenTwo(Screen):

    def __init__(self, **kwargs):
        super(ScreenTwo, self).__init__(**kwargs)

    def change_screen(self):
        self.manager.current = 'screen1'


class Manager(ScreenManager):
    pass


class PreviousMDIcons(Screen):
    c = []

    def on_enter(self, *args):
        self.c = []
        if len(self.c) == 0:
            self.c = self.get_articulos()

    def change_screen(self):
        self.manager.current = 'screen2'

    def set_list_md_icons(self, text="", search=False):
        """Builds a list of icons for the screen MDIcons."""
        print(self.c)
        def add_icon_item(name):
            self.ids.rv.data.append(
                {
                    "viewclass": "CustomOneLineIconListItem",
                    "icon": "android",
                    "text": name,
                    "callback": lambda x: x,

                }
            )

        if len(self.c) == 0:
            self.ids.search_field.text = ""
            self.ids.container.clear_widgets()
            self.ids.rv.data = []
            self.c = self.get_articulos()
        for name_icon in self.c:

           if search and len(self.c)!=0:
              if text in name_icon:
                    add_icon_item(name_icon)
           else:
              self.c.clear()
        self.c.clear()

    def clear_list(self):
        self.ids.search_field.text = ""
        self.ids.container.clear_widgets()
        self.ids.rv.data = []
        self.c.clear()

    @staticmethod
    def get_articulos():
        lista = []
        mysqlite = MySQlite()
        mysqlite.create_connection("data.db")
        query = "select * from usuarios"
        filas = mysqlite.get_rows(query)
        if filas:
            for fila in filas:
                lista.append(fila[1])
        else:
            print("No existen usuarios para mostrar.")

        return lista


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = PreviousMDIcons()
        self.init_conn()

    @staticmethod
    def init_conn():
        mysqlite = MySQlite()

        # conectamos con la base de datos

        if mysqlite.create_connection("data.db"):
            print("conectado con la base de datos")
        else:
            print("No se ha podido crear o conectar con la base de datos")

        # creamos la tabla si no existe

        if mysqlite.create_table("""CREATE TABLE IF NOT EXISTS usuarios (
                              codigo integer primary key,
                              name text );"""):
            print("Creada la tabla")

        else:
            print("No se ha podido crear la tabla")

        """"# insertamos un registro
        query="INSERT INTO usuarios (codigo,name) VALUES (?,?);"
        params=(3,"Maria")
        result=mysqlite.insert_row(query, params)
        if result:
             print(f"Insertado {result} registro")
        else:
             print("No se ha podido añadir un registro")"""

    def build(self):
        m = Manager(transition=NoTransition())
        return m


MainApp().run()
