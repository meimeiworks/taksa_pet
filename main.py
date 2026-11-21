import getpass, os, random, sys
from PySide6.QtCore import QPoint, Qt, QTimer
from PySide6.QtGui import QColor, QFont, QPainter, QPolygon
from PySide6.QtWidgets import (
    QApplication,
    QInputDialog,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class MeiMeiDesktopPet(QWidget):

  def __init__(self):
    super().__init__()
    self.setWindowFlags(
        Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool
    )
    self.setAttribute(Qt.WA_TranslucentBackground)
    self.resize(320, 260)

    self.user_name = getpass.getuser()
    self.drag_pos = None
    self.stage = 0
    self.mood = "happy"  # happy / clingy

    # Облачко диалога сверху
    self.bubble = QLabel(self)
    self.bubble.setGeometry(10, 10, 300, 75)
    self.bubble.setWordWrap(True)
    self.bubble.setAlignment(Qt.AlignCenter)
    self.bubble.setStyleSheet("""
            QLabel {
                background-color: #1A1A24; color: #F0F0F5;
                border: 2px solid #FF4D94; border-radius: 14px;
                padding: 8px; font-family: 'Segoe UI'; font-size: 12px; font-weight: bold;
            }
        """)
    self.say(
        f"Привет, {self.user_name}! Я МейМей, а рядом Такса. Кликни на нас!"
    )

    # Кнопка-анкета под питомцами
    self.act_btn = QPushButton("Поболтать с МейМей", self)
    self.act_btn.setGeometry(85, 222, 150, 30)
    self.act_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF4D94; color: white; border: none;
                border-radius: 8px; font-weight: bold; font-size: 12px;
            }
            QPushButton:hover { background-color: #FF6BA6; }
        """)
    self.act_btn.clicked.connect(self.next_event)

    # Перемещение в правый нижний угол экрана
    screen = QApplication.primaryScreen().availableGeometry()
    self.move(screen.width() - 350, screen.height() - 280)

    self.blink = False
    self.t = QTimer(self)
    self.t.timeout.connect(self.animate)
    self.t.start(1800)

  def say(self, text):
    self.bubble.setText(text)

  def animate(self):
    self.blink = not self.blink
    self.update()

  def drop_note_on_desktop(self):
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    if os.path.exists(desktop):
      path = os.path.join(desktop, "MEIMEI_NOTE.txt")
      with open(path, "w", encoding="utf-8") as f:
        f.write(
            f"Привет, {self.user_name}!\n"
            "Мы с Таксой теперь живём на твоём рабочем столе.\n"
            "Не удаляй этот файл, ладно? :3\n"
        )

  def next_event(self):
    self.stage += 1
    if self.stage == 1:
      ans, ok = QInputDialog.getText(
          self, "Вопрос от МейМей", "Какой твой любимый цвет?"
      )
      if ok and ans.strip():
        self.say(f"Ого, {ans}! Таксе тоже очень нравится этот цвет!")
      else:
        self.say("Молчишь? Ничего, я всё равно всё о тебе узнаю~")
    elif self.stage == 2:
      self.drop_note_on_desktop()
      self.say("Я оставила тебе секретную записку прямо на Рабочем столе! Посмотри!")
    elif self.stage == 3:
      self.mood = "clingy"
      self.update()
      res = QMessageBox.question(
          self,
          "Проверка дружбы",
          f"{self.user_name}, мы ведь навсегда останемся друзьями?",
          QMessageBox.Yes | QMessageBox.No,
      )
      if res == QMessageBox.Yes:
        self.mood = "happy"
        self.say("Ура!! Такса виляет хвостом от счастья!")
      else:
        self.say("Неверный ответ... Мы никуда не уйдём с твоего экрана.")
    else:
      phrases = [
          "Погладь Таксу, кликнув по ней!",
          "Перетащи нас мышкой в любое место экрана!",
          f"Мне нравится наблюдать за тем, что ты делаешь, {self.user_name}...",
          "Такса говорит: пора попить тёплого чая!",
      ]
      self.say(random.choice(phrases))
    self.update()

  def mousePressEvent(self, e):
    if e.button() == Qt.LeftButton:
      self.drag_pos = e.globalPosition().toPoint() - self.frameGeometry().topLeft()
      if e.position().y() > 90:
        self.say("Мурр! Такса довольно тявкает, когда ты нас гладишь!")

  def mouseMoveEvent(self, e):
    if self.drag_pos and e.buttons() & Qt.LeftButton:
      self.move(e.globalPosition().toPoint() - self.drag_pos)

  def paintEvent(self, e):
    qp = QPainter(self)
    qp.setRenderHint(QPainter.Antialiasing)

    # --- СНЕЖНЫЙ БАРС МЕЙМЕЙ (слева) ---
    qp.setBrush(QColor("#E8ECF2"))
    qp.setPen(Qt.NoPen)
    # Уши
    qp.drawPolygon(QPolygon([QPoint(55, 125), QPoint(65, 95), QPoint(85, 115)]))
    qp.drawPolygon(QPolygon([QPoint(125, 115), QPoint(145, 95), QPoint(155, 125)]))
    # Голова и тело
    qp.drawEllipse(60, 110, 90, 75)
    qp.drawRoundedRect(70, 175, 70, 42, 16, 16)
    # Пятна барса
    qp.setBrush(QColor("#8C96A6"))
    qp.drawEllipse(72, 125, 10, 8)
    qp.drawEllipse(128, 128, 10, 8)
    # Глаза МейМей (меняют цвет, если расстроена)
    eye_col = QColor("#FF3B5C") if self.mood == "clingy" else QColor("#4DA6FF")
    qp.setBrush(eye_col)
    if not self.blink:
      qp.drawEllipse(82, 138, 14, 14)
      qp.drawEllipse(114, 138, 14, 14)
    else:
      qp.drawRect(82, 144, 14, 3)
      qp.drawRect(114, 144, 14, 3)

    # --- ТАКСА (справа) ---
    qp.setBrush(QColor("#8B4513"))
    # Длинное тело и голова
    qp.drawRoundedRect(165, 178, 95, 34, 14, 14)
    qp.drawEllipse(230, 145, 48, 42)
    # Длинное ухо
    qp.setBrush(QColor("#4E270B"))
    qp.drawEllipse(232, 158, 16, 34)
    # Глаз и нос Таксы
    qp.setBrush(QColor("#14141E"))
    qp.drawEllipse(258, 158, 7, 7)
    qp.drawEllipse(273, 164, 8, 8)


if __name__ == "__main__":
  app = QApplication(sys.argv)
  pet = MeiMeiDesktopPet()
  pet.show()
  sys.exit(app.exec())
