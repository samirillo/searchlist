from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivymd.icon_definitions import md_icons
from kivymd.app import MDApp
from kivymd.uix.list import OneLineIconListItem

from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.properties import ObjectProperty
from functools import partial

Builder.load_string(
    '''
#:import images_path kivymd.images_path
<CustomOneLineIconListItem>
    on_press:app.get_running_app().root.ids.screen_one.changeScreen()
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
            on_press:root.changeScreen()
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


class CustomOneLineIconListItem(OneLineIconListItem):
    icon = StringProperty()

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.properties import ObjectProperty, NumericProperty


import sqlite3

conexion=sqlite3.connect("bd1.db")
try:
    conexion.execute("""create table articulos (
                              codigo integer primary key autoincrement,
                              descripcion text,
                              precio real
                        )""")
    print("se creo la tabla articulos")                        
except sqlite3.OperationalError:
    print("La tabla articulos ya existe")                    

"""conexion.execute("insert into articulos(descripcion,precio) values (?,?)", ("naranjas", 23.50))
conexion.execute("insert into articulos(descripcion,precio) values (?,?)", ("peras", 34))
conexion.execute("insert into articulos(descripcion,precio) values (?,?)", ("bananas", 25))
conexion.commit()
conexion.close()"""




class ScreenTwo(Screen):
    health_points = NumericProperty(100)

    def __init__(self, **kwargs):
        super(ScreenTwo, self).__init__(**kwargs)

    def changeScreen(self):
        self.manager.current = 'screen1'


class Manager(ScreenManager):

    screen_one = ObjectProperty(None)
    screen_two = ObjectProperty(None)

class PreviousMDIcons(Screen):
    myList=[]
    def changeScreen(self):
        self.manager.current = 'screen2'

    def set_list_md_icons(self, text="", search=False):
        '''Builds a list of icons for the screen MDIcons.'''
        self.ids.rv.data = []
        def add_icon_item(name_icon):
            self.ids.rv.data.append(
                {
                    "viewclass": "CustomOneLineIconListItem",
                    "icon": "android",
                    "text": name_icon,
                    "callback": lambda x: x,

                }
            )

        self.ids.rv.data = []
        c=self.articulos()
        conexion.close()            
        for name_icon in c:

            if search:
                if text in name_icon:
                    add_icon_item(name_icon)
            else:
                add_icon_item(name_icon)
    def articulos(self):
        conexion=sqlite3.connect("bd1.db")
        cursor=conexion.execute("select * from articulos ")
        filas=cursor.fetchall()
        if len(filas)>0:
            for fila in filas:
               self.myList.append(fila[1])
        else:
            print("No existen artículos con un precio menor al ingresado.")
        conexion.close()
        
        return self.myList
       
class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = PreviousMDIcons()

    def build(self):
        m = Manager(transition=NoTransition())
        return m




MainApp().run()
