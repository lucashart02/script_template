from dotenv import load_dotenv
import sys
import os
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QFileDialog, QComboBox, QLineEdit, QMessageBox, QLabel, QDialog
from PyQt5.QtGui import QMovie, QIcon

def main():
    load_dotenv()

    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle('Script Runner')
    window.setFixedWidth(700)
    layout = QVBoxLayout()
    window.setWindowIcon(QIcon('./assets/logo.png'))

    show_input = True
    input_is_file = True
    show_output = True
    output_is_file = False
    show_run_mode = True

    if show_input:
        if input_is_file:
            input_label = QLabel('Input File')
            input_field = QLineEdit()
            input_button = QPushButton('Browse')
            input_button.clicked.connect(lambda: input_field.setText(QFileDialog.getOpenFileName()[0]))
            layout.addWidget(input_label)
            layout.addWidget(input_field)
            layout.addWidget(input_button)
        else:
            input_label = QLabel('Input Directory')
            input_field = QLineEdit()
            input_button = QPushButton('Browse')
            input_button.clicked.connect(lambda: input_field.setText(QFileDialog.getExistingDirectory()))
            layout.addWidget(input_label)
            layout.addWidget(input_field)
            layout.addWidget(input_button)

    if show_output:
        if output_is_file:
            output_label = QLabel('Output File')
            output_field = QLineEdit()
            output_button = QPushButton('Browse')
            output_button.clicked.connect(lambda: output_field.setText(QFileDialog.getOpenFileName()[0]))
            layout.addWidget(output_label)
            layout.addWidget(output_field)
            layout.addWidget(output_button)
        else:
            output_label = QLabel('Output Directory')
            output_field = QLineEdit()
            output_button = QPushButton('Browse')
            output_button.clicked.connect(lambda: output_field.setText(QFileDialog.getExistingDirectory()))
            layout.addWidget(output_label)
            layout.addWidget(output_field)
            layout.addWidget(output_button)

    if show_run_mode:
        mode_label = QLabel('Run Mode')
        mode_combo = QComboBox()
        mode_combo.addItems(['Production', 'SB', 'Authorization'])
        layout.addWidget(mode_label)
        layout.addWidget(mode_combo)

    run_button = QPushButton('Run')
    exit_button = QPushButton('Exit')
    layout.addWidget(run_button)
    layout.addWidget(exit_button)

    loading_gif = QMovie("./assets/pacman-loading.gif")
    loading_dialog = QDialog(window)
    loading_label = QLabel(loading_dialog)
    loading_label.setMovie(loading_gif)
    loading_dialog.setLayout(QVBoxLayout())
    loading_dialog.layout().addWidget(loading_label)

    central_widget = QWidget()
    central_widget.setLayout(layout)
    window.setCentralWidget(central_widget)

    def run_script():
        input_path, output_path, mode = None, None, None
        if show_input:
            input_path = input_field.text()
        if show_output:
            output_path = output_field.text()
        if show_run_mode:
            mode = mode_combo.currentText()

        if (show_input and not input_path) or (show_output and not output_path) or (show_run_mode and not mode):
            QMessageBox.warning(window, "Warning", "Please provide all required fields.")
            return

        with open("../.env", 'w') as env:
            if show_input:
                if input_is_file:
                    env.write(f"INPUT_FILE={input_path}\n")
                else:
                    env.write(f"INPUT_DIR={input_path}\n")
            if show_output:
                if output_is_file:
                    env.write(f"OUTPUT_FILE={output_path}\n")
                else:
                    env.write(f"OUTPUT_DIR={output_path}\n")
            if show_run_mode:
                env.write(f"RUN_MODE={mode}\n")

        if mode == "Production":
            script_path = "src/prod/script.py"
        elif mode == "SB":
            script_path = "src/sb/script.py"
        elif mode == "Authorization":
            script_path = "src/auth.py"
        else:
            QMessageBox.warning(window, "Warning", "Please select a valid run mode.")
            return

        run_button.setEnabled(False)
        loading_dialog.show()
        loading_gif.start()
        process = subprocess.Popen(["python", script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        loading_gif.stop()
        loading_dialog.close()
        run_button.setEnabled(True)
        QMessageBox.information(window, "Information", "Script finished running")

    run_button.clicked.connect(run_script)
    exit_button.clicked.connect(lambda: window.close())

    window.show()
    app.exec()

if __name__ == "__main__":
    main()
