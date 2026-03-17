import sys, os
from amr_to_mp3 import amr_to_mp3
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QFileDialog, QAction, QMessageBox, QPushButton, QLineEdit

def convert_files(file_list, outPath = None):
    success = []
    failed = []
    for file in file_list:
        print(f"\nConverting file: {file}")
        file_name = os.path.basename(file)
        try:
            amr_to_mp3(file, outPath = outPath, output = f"{file_name[:file_name.rfind('.')]}.mp3")
            success.append(file)
        except Exception as e:
            print(f"Error converting {file}: {e}")
            failed.append(file)
    return success, failed

class MainWindow(QMainWindow):

    amrFiles = []
    file_display = []
    file_delete_button = []
    output = f"{os.path.dirname(__file__)}"

    def __init__(self):
        print("\nloading GUI...")
        super().__init__()
        
        # 设置窗口标题和大小
        print("Loading window...")
        self.setWindowTitle("QQ音频缓存(ARM)还原(MP3)工具")
        self.setGeometry(500, 500, 1000, 500)  # x, y, width, height
        self.setWindowFlags(self.windowFlags() & ~0x00040000)  # 禁止最大化
        self.setFixedSize(1000, 500)  # 设置窗口为固定大小
        self.setStyleSheet('background-color: white;')
        self.create_actions()

        print("Loading menu...")
        menubar = self.menuBar()
        file_menu = menubar.addMenu('文件')
        file_menu.addAction(self.open_action)
        file_menu.addAction(self.reload_action)
        file_menu.addAction(self.output_action)
        menubar.setStyleSheet('border: 1px solid gray; color: black;')
        file_menu.setStyleSheet('border: None;')

        print("Loading output directory...")
        self.output_label = QLabel("输出目录:", self)
        self.output_label.setGeometry(20, 440, 150, 40)
        self.path_input = QLineEdit(self)
        self.path_input.setGeometry(120, 440, 500, 40)
        self.path_input.setText(self.output)
        self.path_input.textChanged.connect(self.set_output)

        print("Loading label and button...")
        self.label = QLabel("  已加载文件:\n", self)
        self.label.setGeometry(0, 40, 150, 40)  # x, y, width, height

        self.open_files_button = QPushButton('打开', self)
        self.open_files_button.clicked.connect(self.open_file)
        self.open_files_button.setStyleSheet('border: 0px solid black;')
        self.open_files_button.setGeometry(899, 33, 100, 34)  # x, y, width, height

        self.label1 = QLabel("", self)
        self.label1.setStyleSheet('border: 1px solid black; background-color: rgba(0, 0, 0, 50); color: black;')
        self.label1.setGeometry(0, 70, 1000, 350)  # x, y, width, height

        self.path_input_button = QPushButton('设置', self)
        self.path_input_button.clicked.connect(self.selete_output_file)
        self.path_input_button.setGeometry(640, 440, 100, 40)  # x, y, width, height

        self.clear_files_button = QPushButton('清除', self)
        self.clear_files_button.clicked.connect(self.clear_files)
        self.clear_files_button.setGeometry(760, 440, 100, 40)  # x, y, width, height


        self.button = QPushButton('转换', self)
        self.button.clicked.connect(self.convert_files)
        self.button.setGeometry(880, 440, 100, 40)  # x, y, width, height

        print("GUI loaded successfully!")
    
    def create_actions(self):
        print("\nCreating actions...")

        print("Creating open action...")
        self.open_action = QAction('打开文件夹', self)
        self.open_action.setShortcut('Ctrl+O')
        self.open_action.triggered.connect(self.open_file)

        print("creating output directory action...")
        self.output_action = QAction('设置输出目录', self)
        self.output_action.setShortcut('Ctrl+Shift+O')
        self.output_action.triggered.connect(self.selete_output_file)

        print("Creating reload action...")
        self.reload_action = QAction('清除已加载文件', self)
        self.reload_action.setShortcut('Ctrl+R')
        self.reload_action.triggered.connect(self.clear_files)
        
    def open_file(self):
        print("\nOpening file dialog...")
        folderName = QFileDialog.getExistingDirectory(self, '选择你的amr文件所处的文件夹')
        if folderName:
            print(f"Selected folder: {folderName}")
            files = os.listdir(folderName)
            print(f"Files in folder: {files}")
            i = 0
            for file in files:
                if len(self.amrFiles)>=10:
                    msg = QMessageBox()
                    msg.setWindowTitle('提示')
                    msg.setText(f'最多只能同时加载10个文件')
                    msg.setIcon(QMessageBox.Information)
                    msg.exec_()
                    break
                if (file[-4:] == ".amr" or file[-5:] == ".silk") and (f"{folderName}/{file}" not in self.amrFiles):
                    self.amrFiles.append(f"{folderName}/{file}")
                    i+=1
            print(f"Loaded files:")
            for i, file in enumerate(self.amrFiles, 1):
                print(f"    {i}. {file}")
            self.reload_file(self.amrFiles)

            msg = QMessageBox()
            msg.setWindowTitle('提示')
            msg.setText(f'已加载{i}个文件')
            msg.setIcon(QMessageBox.Information)
            msg.exec_()
            return
        print("No folder selected.")

    def selete_output_file(self):
        print("\nOpening output directory dialog...")
        folderName = QFileDialog.getExistingDirectory(self, '选择输出文件夹', directory=self.output)
        if folderName:
            print(f"Selected output folder: {folderName}")
            self.output = folderName
            self.path_input.setText(folderName)
            return
        print("No output folder selected.")

    def clear_files(self):
        print("\nClearing loaded files...")
        self.amrFiles = []
        self.reload_file(self.amrFiles)

    def reload_file(self, files = []):
        print("\nReloading file list...")
        while self.file_display:
            label = self.file_display.pop()
            label.deleteLater()
        while self.file_delete_button:
            button = self.file_delete_button.pop()
            button.deleteLater()
        self.amrFiles = files
        text = "\n"
        y = 70
        for i, file in enumerate(self.amrFiles, 1):
            label = QLabel(f"{i}.", self)
            label.setGeometry(0, y, 35, 35)  # x, y, width, height
            label.setStyleSheet('border: 1px solid black; background-color: rgba(0, 0, 0, 50); color: black;')
            self.file_display.append(label)
            label = QLabel(f"{file}", self)
            label.setGeometry(35, y, 885, 35)  # x, y, width, height
            label.setStyleSheet('border: 1px solid black; background-color: rgba(0, 0, 0, 50); color: black;')
            self.file_display.append(label)
            button = QPushButton('删除', self)
            button.setGeometry(920, y, 80, 35)  # x, y, width, height
            button.setStyleSheet('border: 1px solid black;')
            self.file_delete_button.append(button)
            button.clicked.connect(lambda checked, file=file: self.delete_file(file))
            y += 35
        for label in self.file_display:
            label.show()
        for button in self.file_delete_button:
            button.show()

    def set_output(self):
        print("\nSetting output directory...")
        text = self.path_input.text()
        if os.path.isdir(text):
            self.output = text
            print(f"Output directory set to: {self.output}")
            msg = QMessageBox()
            msg.setWindowTitle('提示')
            msg.setText(f'输出目录已设置为:\n{text}')
            msg.setIcon(QMessageBox.Information)
            msg.exec_()
        else:
            return

    def delete_file(self, file):
        print(f"\nDeleting file: {file}")
        if file in self.amrFiles:
            self.amrFiles.remove(file)
            print(f"File deleted: {file}")
            self.reload_file(self.amrFiles)
        else:
            print(f"File not found: {file}")

    def convert_files(self):
        print("\nConverting files...")
        if not self.amrFiles:
            print("No files to convert.")
            msg = QMessageBox()
            msg.setWindowTitle('提示')
            msg.setText(f'请先加载文件')
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
            return
        print("Calling convert_files function...")
        success, failed = convert_files(self.amrFiles, outPath = self.output)
        print(f"\nConversion results:")
        print(f"    Successfully converted: {len(success)}")
        for i, file in enumerate(success, 1):
            print(f"        {i}. {file}")
        print(f"    Failed to convert: {len(failed)}")
        for i, file in enumerate(failed, 1):
            print(f"        {i}. {file}")
        text = ""
        if success:
            text += "转换完成！\n\n成功转换的文件:\n"
            for i, file in enumerate(success, 1):
                text += f"{i}. {file}\n"
            files = [file for file in self.amrFiles if file not in success]
            self.reload_file(files)
        if failed:
            text += "\n转换失败的文件:\n"
            for i, file in enumerate(failed, 1):
                text += f"{i}. {file}\n"
        msg = QMessageBox()
        msg.setWindowTitle('转换结果')
        msg.setText(text)
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())