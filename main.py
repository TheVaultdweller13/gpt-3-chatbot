import sys
from PyQt5.QtCore import Qt
import openai
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QVBoxLayout, QScrollArea
from PyQt5.QtGui import QFont

openai.api_key = "YOUR_OPENAI_API_KEY"
length = 2000  # Controla la máxima longitud del prompt
temperature = 0.5  # Controla el nivel de aletoriedad del texto generado (0-1)
prompts = []


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'OpenAI Chatbot'
        self.left = 10
        self.top = 10
        self.width = 1280
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.input_box = QLineEdit(self)
        self.input_box.resize(560, 40)

        self.button = QPushButton('Enviar', self)
        self.button.resize(560, 40)

        self.input_layout = QVBoxLayout()
        self.input_layout.addWidget(self.input_box)
        self.input_layout.addSpacing(10)
        self.input_layout.addWidget(self.button)

        self.scroll = QScrollArea(self)
        self.scroll.resize(640, 360)

        self.scroll.setMinimumSize(640, 360)

        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.label = QLabel(self.scroll)
        self.label.setFixedSize(1260, 360)
        self.label.setWordWrap(True)

        self.label.setStyleSheet('background-color: white;')
        self.label.setContentsMargins(10, 0, 10, 0)
        self.scroll.setWidget(self.label)

        self.output_layout = QVBoxLayout()
        self.output_layout.addWidget(self.scroll)

        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.input_layout)
        self.main_layout.addLayout(self.output_layout)

        self.setLayout(self.main_layout)

        self.button.clicked.connect(self.on_click)
        self.show()

    def on_click(self):
        prompt = self.input_box.text()
        prompts.append(prompt)
        full_prompt = " ".join(prompts)

        while len(full_prompt) >= length:
            prompts.pop(0)

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"{full_prompt}. Genera e inventa lo que no conozcas.",
            max_tokens=length,
            temperature=temperature
        )

        text = str(response["choices"][0].get("text"))
        prompts.append(text.strip())

        current_text = self.label.text()

        # Establece el color del texto del prompt en verde
        prompt_html = "<font color='green'><b>" + prompt + "</b></font>"

        # Establece el color del texto de la respuesta en azul
        response_html = "<font color='blue'>" + text + "</font>"

        self.label.setStyleSheet("color: blue;")

        full_text = current_text + "<br>" + prompt_html + "<br>" + response_html

        self.label.setText(full_text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
