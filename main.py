import getpass, os, random, sys
from PySide6.QtCore import QPoint, Qt, QTimer
from PySide6.QtGui import QColor, QPainter, QPolygon
from PySide6.QtWidgets import (
    QApplication,
    QInputDialog,
    QLabel,
    QMessageBox,
    QPushButton,
    QWidget,
)


class TaksaPetApp(QWidget):

  def __init__(self):
    super().__init__()
    # Убрали Qt.Tool, чтобы окно не пряталось после закрытия диалогов
    self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
    self.setAttribute(Qt.WA_TranslucentBackground)
    self.resize(330, 265)

    self.player_name = getpass.getuser()
    self.best_friend = ""
    self.meimei_here = False
    self.mood = "happy"
    self.step = 0
    self.drag_pos = None

    self.bubble = QLabel(self)
    self.bubble.setGeometry(10, 10, 310, 78)
    self.bubble.setWordWrap(True)
    self.bubble.setAlignment(Qt.AlignCenter)
    self.bubble.setStyleSheet("""
            QLabel {
                background-color: #1A1A24; color: #F0F0F5;
                border: 2px solid #FF4D94; border-radius: 14px;
                padding: 8px; font-family: 'Segoe UI'; font-size: 12px; font-weight: bold;
            }
        """)
    self.say("Гав-привет! Я Такса. Давай познакомимся — нажми кнопку ниже!")

    self.btn = QPushButton("Ответить Таксе", self)
    self.btn.setGeometry(85, 226, 160, 30)
    self.btn.setStyleSheet("""
            QPushButton {
                background-color: #FF4D94; color: white; border: none;
                border-radius: 8px; font-weight: bold; font-size: 12px;
            }
            QPushButton:hover { background-color: #FF6BA6; }
        """)
    self.btn.clicked.connect(self.next_step)

    scr = QApplication.primaryScreen().availableGeometry()
    self.move(scr.width() - 360, scr.height() - 285)

    self.blink = False
    self.t = QTimer(self)
    self.t.timeout.connect(self.toggle_blink)
    self.t.start(1900)

  def say(self, text):
    self.bubble.setText(text)

  def toggle_blink(self):
    self.blink = not self.blink
    self.update()

  def drop_note(self):
    desk = os.path.join(os.path.expanduser("~"), "Desktop")
    if os.path.exists(desk):
      with open(
          os.path.join(desk, "MEIMEI_AND_TAKSA.txt"), "w", encoding="utf-8"
      ) as f:
        f.write(
            f"Досье друга: {self.player_name}\n"
            f"Лучший друг: {self.best_friend}\n"
            "Теперь мы с Таксой и МейМей следим за твоим рабочим столом! :3\n"
        )

  def next_step(self):
    self.step += 1
    if self.step == 1:
      name, ok = QInputDialog.getText(
          self, "Вопрос 1 от Таксы", "Как тебя зовут?"
      )
      if ok and name.strip():
        self.player_name = name.strip()
      self.say(
          f"Приятно познакомиться, {self.player_name}! А теперь следующий вопрос..."
      )
      self.btn.setText("Дальше")

    elif self.step == 2:
      friend, ok = QInputDialog.getText(
          self, "Вопрос 2 от Таксы", "Кто твой лучший друг?"
      )
      self.best_friend = (
          friend.strip() if (ok and friend.strip()) else "секретный друг"
      )
      self.say(
          f"{self.best_friend}? Звучит круто! Кстати, я тут не одна... Познакомься!"
      )
      self.btn.setText("Кто там?")

    elif self.step == 3:
      self.meimei_here = True
      self.say(
          f"Мурр! Я снежный барс МейМей! Теперь я тоже твой лучший друг, {self.player_name}!"
      )
      self.btn.setText("Поболтать")

    elif self.step == 4:
      self.drop_note()
      self.say(
          f"Я записала тебя и {self.best_friend} в файл на Рабочем столе! Проверь!"
      )

    elif self.step == 5:
      self.mood = "clingy"
      self.update()
      ans = QMessageBox.question(
          self,
          "Проверка дружбы",
          f"{self.player_name}, мы ведь лучше, чем {self.best_friend}?",
          QMessageBox.Yes | QMessageBox.No,
      )
      if ans == QMessageBox.Yes:
        self.mood = "happy"
        self.say("Правильный ответ! Мы с Таксой очень рады!")
      else:
        self.say(
            f"Ничего страшного... Скоро {self.best_friend} тоже с нами познакомится."
        )

    else:
      lines = [
          f"{self.player_name}, погладь нас кликом мышки!",
          f"Интересно, чем сейчас занимается {self.best_friend}?",
          "Перетащи нас на любое окно, мы будем помогать!",
          "МейМей мурлычет, а Такса виляет хвостом!",
      ]
      self.say(random.choice(lines))

    # Гарантированно возвращаем окно поверх рабочего стола
    self.show()
    self.raise_()
    self.activateWindow()
    self.update()

  def mousePressEvent(self, e):
    if e.button() == Qt.LeftButton:
      self.drag_pos = e.globalPosition().toPoint() - self.frameGeometry().topLeft()
      if e.position().y() > 95:
        if self.meimei_here:
          self.say("Мурр! Мы с Таксой любим, когда нас гладят!")
        else:
          self.say("Гав! Такса довольна!")

  def mouseMoveEvent(self, e):
    if self.drag_pos and e.buttons() & Qt.LeftButton:
      self.move(e.globalPosition().toPoint() - self.drag_pos)

  def paintEvent(self, e):
    qp = QPainter(self)
    qp.setRenderHint(QPainter.Antialiasing)
    qp.setPen(Qt.NoPen)

    # --- СНЕЖНЫЙ БАРС МЕЙМЕЙ ---
    if self.meimei_here:
      qp.setBrush(QColor("#E8ECF2"))
      qp.drawPolygon(QPolygon([QPoint(55, 125), QPoint(65, 95), QPoint(85, 115)]))
      qp.drawPolygon(
          QPolygon([QPoint(125, 115), QPoint(145, 95), QPoint(155, 125)])
      )
      qp.drawEllipse(60, 110, 90, 75)
      qp.drawRoundedRect(70, 175, 70, 42, 16, 16)

      qp.setBrush(QColor("#8C96A6"))
      qp.drawEllipse(72, 125, 10, 8)
      qp.drawEllipse(128, 128, 10, 8)

      qp.setBrush(
          QColor("#FF3B5C") if self.mood == "clingy" else QColor("#4DA6FF")
      )
      if not self.blink:
        qp.drawEllipse(82, 138, 14, 14)
        qp.drawEllipse(114, 138, 14, 14)
      else:
        qp.drawRect(82, 144, 14, 3)
        qp.drawRect(114, 144, 14, 3)

    # --- ТАКСА ---
    tx = 165 if self.meimei_here else 105
    qp.setBrush(QColor("#8B4513"))
    qp.drawRoundedRect(tx, 178, 95, 34, 14, 14)
    qp.drawEllipse(tx + 65, 145, 48, 42)
    qp.setBrush(QColor("#4E270B"))
    qp.drawEllipse(tx + 67, 158, 16, 34)
    qp.setBrush(QColor("#14141E"))
    if not self.blink:
      qp.drawEllipse(tx + 93, 158, 7, 7)
    else:
      qp.drawRect(tx + 92, 160, 8, 2)
    qp.drawEllipse(tx + 108, 164, 8, 8)


if __name__ == "__main__":
  app = QApplication(sys.argv)
  pet = TaksaPetApp()
  pet.show()
  sys.exit(app.exec())
