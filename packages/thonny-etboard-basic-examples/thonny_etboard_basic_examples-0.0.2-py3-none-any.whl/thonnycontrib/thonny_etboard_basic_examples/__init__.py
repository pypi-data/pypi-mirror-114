import tkinter as tk
import os
import time
from glob import glob
from thonny import get_workbench, workbench
from tkinter.messagebox import showinfo

class ETBoardMenu:
    def __init__(self):
        self.workbench = get_workbench()
        self.root_example_menu = tk.Menu(self.workbench, tearoff=False, postcommand = self.update_example_menu)
        
    def __del__(self):
        pass

    def hello(self):
        #핸들러 테스트 함수
        showinfo("Hello!", "Thonny rules!")

    def get_examples_list(self):
        examples_list = []
        target_path = os.path.abspath(__file__)
        target_path = os.path.dirname(target_path)
        for root, dirs_, files in os.walk(target_path):
            for file in files:
                name = file.split(os.path.sep)[-1]
                ext = file.split(".")[-1]
                full_path = os.path.join(root, file)
                dir = os.path.dirname(full_path).split(os.path.sep)[-1]
                if ext != "py" or name == "__init__.py" or dir == "lib":
                    continue
                
                examples_list.append(full_path)

        return examples_list

    def update_example_menu(self):
        #예제 파일 리스트를 가져옴, 풀 경로가 들어옴
        example_list = self.get_examples_list()

        #기존 리스트 초기화
        self.root_example_menu.delete(0, "end")

        dir_map = {}
        for path in example_list:
            name = path.split(os.path.sep)[-1]
            dir = os.path.dirname(path)

            def load(path=path):
                editor = self.workbench.get_editor_notebook()
                if editor.file_is_opened(path):
                    return

                editor.show_file(path)
            
            menu = None
            if dir in dir_map:
                menu = dir_map[dir]
            else:
                menu = tk.Menu(self.workbench, tearoff=False)
                dir_map[dir] = menu
            
            if menu is None:
                continue

            menu.add_command(label=name, command=load)
        
        for key, value in dir_map.items():
            name = key.split(os.path.sep)[-1]
            menu = value            
            self.root_example_menu.add_cascade(label=name, menu=menu)
        
    def load_plugin(self):
        self.workbench.add_command(command_id="et-examples",
                                menu_name="file",
                                command_label="ET-board 예제",
                                group=10,
                                submenu=self.root_example_menu)

        


if get_workbench() is not None:
    run = ETBoardMenu().load_plugin()
