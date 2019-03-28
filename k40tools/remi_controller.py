
# -*- coding: utf-8 -*-

from remi.gui import *
from remi import start, App
from k40nano import NanoPlotter, MockUsb

move_amount = 50
down = False
#plotter = NanoPlotter(usb=MockUsb())
plotter = NanoPlotter()

class CLASSinitialize_button( Button ):
    def __init__(self, *args):
        #DON'T MAKE CHANGES HERE, THIS METHOD GETS OVERWRITTEN WHEN SAVING IN THE EDITOR
        super( CLASSinitialize_button, self ).__init__(*args)
        self.onclick.connect(self.onclick_initialize_button)
        
    def onclick_initialize_button(self, emitter):
        plotter.open()


class CLASShome_button( Button ):
    def __init__(self, *args):
        #DON'T MAKE CHANGES HERE, THIS METHOD GETS OVERWRITTEN WHEN SAVING IN THE EDITOR
        super( CLASShome_button, self ).__init__(*args)
        self.onclick.connect(self.onclick_home_button)
        
    def onclick_home_button(self, emitter):
        plotter.home()


class CLASSunlock_rail_button( Button ):
    def __init__(self, *args):
        #DON'T MAKE CHANGES HERE, THIS METHOD GETS OVERWRITTEN WHEN SAVING IN THE EDITOR
        super( CLASSunlock_rail_button, self ).__init__(*args)
        self.onclick.connect(self.onclick_unlock_rail_button)
        
    def onclick_unlock_rail_button(self, emitter):
        plotter.unlock_rail()


class CLASSlock_rail_button( Button ):
    def __init__(self, *args):
        #DON'T MAKE CHANGES HERE, THIS METHOD GETS OVERWRITTEN WHEN SAVING IN THE EDITOR
        super( CLASSlock_rail_button, self ).__init__(*args)
        self.onclick.connect(self.onclick_lock_rail_button)
        
    def onclick_lock_rail_button(self, emitter):
        plotter.lock_rail()


class CLASSup_button( Button ):
    def __init__(self, *args):
        #DON'T MAKE CHANGES HERE, THIS METHOD GETS OVERWRITTEN WHEN SAVING IN THE EDITOR
        super( CLASSup_button, self ).__init__(*args)
        self.onclick.connect(self.onclick_up_button)
        
    def onclick_up_button(self, emitter):
        plotter.move(0, -move_amount)


class CLASSdown_button( Button ):
    def __init__(self, *args):
        #DON'T MAKE CHANGES HERE, THIS METHOD GETS OVERWRITTEN WHEN SAVING IN THE EDITOR
        super( CLASSdown_button, self ).__init__(*args)
        self.onclick.connect(self.onclick_down_button)
        
    def onclick_down_button(self, emitter):
        plotter.move(0, move_amount)


class CLASSright_button( Button ):
    def __init__(self, *args):
        #DON'T MAKE CHANGES HERE, THIS METHOD GETS OVERWRITTEN WHEN SAVING IN THE EDITOR
        super( CLASSright_button, self ).__init__(*args)
        self.onclick.connect(self.onclick_right_button)
        
    def onclick_right_button(self, emitter):
        plotter.move(move_amount, 0)


class CLASSleft_button( Button ):
    def __init__(self, *args):
        #DON'T MAKE CHANGES HERE, THIS METHOD GETS OVERWRITTEN WHEN SAVING IN THE EDITOR
        super( CLASSleft_button, self ).__init__(*args)
        self.onclick.connect(self.onclick_left_button)
        
    def onclick_left_button(self, emitter):
        plotter.move(-move_amount, 0)


class CLASSstop_button( Button ):
    def __init__(self, *args):
        #DON'T MAKE CHANGES HERE, THIS METHOD GETS OVERWRITTEN WHEN SAVING IN THE EDITOR
        super( CLASSstop_button, self ).__init__(*args)
        self.onclick.connect(self.onclick_stop_button)
        
    def onclick_stop_button(self, emitter):
        plotter.abort()


class BasicController(App):
    def __init__(self, *args, **kwargs):
        #DON'T MAKE CHANGES HERE, THIS METHOD GETS OVERWRITTEN WHEN SAVING IN THE EDITOR
        if not 'editing_mode' in kwargs.keys():
            super(BasicController, self).__init__(*args, static_file_path={'my_res':'./res/'})

    def idle(self):
        #idle function called every update cycle
        pass
    
    def main(self):
        return BasicController.construct_ui(self)
        
    @staticmethod
    def construct_ui(self):
        #DON'T MAKE CHANGES HERE, THIS METHOD GETS OVERWRITTEN WHEN SAVING IN THE EDITOR
        main_layout = Widget()
        main_layout.attributes.update({"class":"Widget","editor_constructor":"()","editor_varname":"main_layout","editor_tag_type":"widget","editor_newclass":"False","editor_baseclass":"Widget"})
        main_layout.style.update({"margin":"0px","width":"190.0px","height":"370.0px","top":"20px","left":"20px","position":"absolute","overflow":"auto"})
        initialize_button = CLASSinitialize_button('Initialize')
        initialize_button.attributes.update({"class":"Button","editor_constructor":"('Initialize')","editor_varname":"initialize_button","editor_tag_type":"widget","editor_newclass":"True","editor_baseclass":"Button"})
        initialize_button.style.update({"margin":"0px","width":"170.0px","height":"30.0px","top":"10.0px","left":"10.0px","position":"absolute","overflow":"auto","background-color":"#008040"})
        main_layout.append(initialize_button,'initialize_button')
        home_button = CLASShome_button('Home')
        home_button.attributes.update({"class":"Button","editor_constructor":"('Home')","editor_varname":"home_button","editor_tag_type":"widget","editor_newclass":"True","editor_baseclass":"Button"})
        home_button.style.update({"margin":"0px","width":"50.0px","height":"30.0px","top":"50.0px","left":"10.0px","position":"absolute","overflow":"auto"})
        main_layout.append(home_button,'home_button')
        unlock_rail_button = CLASSunlock_rail_button('Unlock Rail')
        unlock_rail_button.attributes.update({"class":"Button","editor_constructor":"('Unlock Rail')","editor_varname":"unlock_rail_button","editor_tag_type":"widget","editor_newclass":"True","editor_baseclass":"Button"})
        unlock_rail_button.style.update({"margin":"0px","width":"50.0px","height":"30.0px","top":"50.0px","left":"70.0px","position":"absolute","overflow":"auto"})
        main_layout.append(unlock_rail_button,'unlock_rail_button')
        lock_rail_button = CLASSlock_rail_button('Lock Rail')
        lock_rail_button.attributes.update({"class":"Button","editor_constructor":"('Lock Rail')","editor_varname":"lock_rail_button","editor_tag_type":"widget","editor_newclass":"True","editor_baseclass":"Button"})
        lock_rail_button.style.update({"margin":"0px","width":"50.0px","height":"30.0px","top":"50.0px","left":"130.0px","position":"absolute","overflow":"auto"})
        main_layout.append(lock_rail_button,'lock_rail_button')
        up_button = CLASSup_button('/\\')
        up_button.attributes.update({"class":"Button","editor_constructor":"('/\\')","editor_varname":"up_button","editor_tag_type":"widget","editor_newclass":"True","editor_baseclass":"Button"})
        up_button.style.update({"margin":"0px","width":"50px","height":"50px","top":"110.0px","left":"70.0px","position":"absolute","overflow":"auto"})
        main_layout.append(up_button,'up_button')
        down_button = CLASSdown_button('\\/')
        down_button.attributes.update({"class":"Button","editor_constructor":"('\\/')","editor_varname":"down_button","editor_tag_type":"widget","editor_newclass":"True","editor_baseclass":"Button"})
        down_button.style.update({"margin":"0px","width":"50px","height":"50px","top":"210.0px","left":"70.0px","position":"absolute","overflow":"auto"})
        main_layout.append(down_button,'down_button')
        right_button = CLASSright_button('>')
        right_button.attributes.update({"class":"Button","editor_constructor":"('>')","editor_varname":"right_button","editor_tag_type":"widget","editor_newclass":"True","editor_baseclass":"Button"})
        right_button.style.update({"margin":"0px","width":"50px","height":"50px","top":"160.0px","left":"120.0px","position":"absolute","overflow":"auto"})
        main_layout.append(right_button,'right_button')
        left_button = CLASSleft_button('<')
        left_button.attributes.update({"class":"Button","editor_constructor":"('<')","editor_varname":"left_button","editor_tag_type":"widget","editor_newclass":"True","editor_baseclass":"Button"})
        left_button.style.update({"margin":"0px","width":"50px","height":"50px","top":"160.0px","left":"20.0px","position":"absolute","overflow":"auto"})
        main_layout.append(left_button,'left_button')
        stop_button = CLASSstop_button('Stop')
        stop_button.attributes.update({"class":"Button","editor_constructor":"('Stop')","editor_varname":"stop_button","editor_tag_type":"widget","editor_newclass":"True","editor_baseclass":"Button"})
        stop_button.style.update({"margin":"0px","width":"150.0px","height":"50.0px","top":"310.0px","left":"20.0px","position":"absolute","overflow":"auto","background-color":"#ff0000"})
        main_layout.append(stop_button,'stop_button')
        

        self.main_layout = main_layout
        return self.main_layout
    


#Configuration
configuration = {'config_project_name': 'untitled', 'config_address': '0.0.0.0', 'config_port': 8081, 'config_multiple_instance': True, 'config_enable_file_cache': True, 'config_start_browser': True, 'config_resourcepath': './res/'}

if __name__ == "__main__":
    # start(MyApp,address='127.0.0.1', port=8081, multiple_instance=False,enable_file_cache=True, update_interval=0.1, start_browser=True)
    start(BasicController, address=configuration['config_address'], port=configuration['config_port'],
                        multiple_instance=configuration['config_multiple_instance'], 
                        enable_file_cache=configuration['config_enable_file_cache'],
                        start_browser=configuration['config_start_browser'])
