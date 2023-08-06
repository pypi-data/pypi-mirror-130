from math import ceil

from PySide6.QtCore import QPoint, QRect, QSize
from PySide6.QtGui import (
    QBrush,
    QCloseEvent,
    QMouseEvent,
    QPainter,
    QPaintEvent,
    QResizeEvent,
)
from PySide6.QtWidgets import QComboBox, QLabel, QLayout, QStatusBar, QToolBar, QWidget

from foundry import icon
from foundry.game.File import ROM
from foundry.game.gfx.drawable.Block import Block
from foundry.game.gfx.GraphicsSet import GraphicsSet
from foundry.game.gfx.Palette import (
    PALETTE_GROUPS_PER_OBJECT_SET,
    bg_color_for_object_set,
    load_palette_group,
)
from foundry.gui.CustomChildWindow import CustomChildWindow
from foundry.gui.LevelSelector import OBJECT_SET_ITEMS
from foundry.gui.Spinner import Spinner


class BlockViewer(CustomChildWindow):
    def __init__(self, parent):
        super(BlockViewer, self).__init__(parent, "Block Viewer")

        self._object_set = 0
        self.sprite_bank = BlockBank(parent=self)

        self.setCentralWidget(self.sprite_bank)

        self.toolbar = QToolBar(self)

        self.prev_os_action = self.toolbar.addAction(icon("arrow-left.svg"), "Previous object set")
        self.prev_os_action.triggered.connect(self.prev_object_set)

        self.next_os_action = self.toolbar.addAction(icon("arrow-right.svg"), "Next object set")
        self.next_os_action.triggered.connect(self.next_object_set)

        self.zoom_out_action = self.toolbar.addAction(icon("zoom-out.svg"), "Zoom Out")
        self.zoom_out_action.triggered.connect(self.sprite_bank.zoom_out)

        self.zoom_in_action = self.toolbar.addAction(icon("zoom-in.svg"), "Zoom In")
        self.zoom_in_action.triggered.connect(self.sprite_bank.zoom_in)

        self.bank_dropdown = QComboBox(parent=self.toolbar)
        self.bank_dropdown.addItems(OBJECT_SET_ITEMS)
        self.bank_dropdown.setCurrentIndex(0)

        self.bank_dropdown.currentIndexChanged.connect(self.on_combo)

        self.palette_group_spinner = Spinner(self, maximum=PALETTE_GROUPS_PER_OBJECT_SET - 1, base=10)
        self.palette_group_spinner.valueChanged.connect(self.on_palette)

        self.toolbar.addWidget(self.bank_dropdown)
        self.toolbar.addWidget(QLabel(" Object Palette: "))
        self.toolbar.addWidget(self.palette_group_spinner)

        self.addToolBar(self.toolbar)

        self.layout().setSizeConstraint(QLayout.SetFixedSize)

        self.setStatusBar(QStatusBar(self))

        return

    def closeEvent(self, event: QCloseEvent):
        self.toolbar.close()
        super().closeEvent(event)

    @property
    def object_set(self):
        return self._object_set

    @object_set.setter
    def object_set(self, value):
        self._object_set = value

        self._after_object_set()

    @property
    def palette_group(self):
        return self.palette_group_spinner.value()

    @palette_group.setter
    def palette_group(self, value):
        self.palette_group_spinner.setValue(value)

    def prev_object_set(self):
        self.object_set = max(self.object_set - 1, 0)

    def next_object_set(self):
        self.object_set = min(self.object_set + 1, 0xE)

    def _after_object_set(self):
        self.sprite_bank.object_set = self.object_set

        self.bank_dropdown.setCurrentIndex(self.object_set)

        self.sprite_bank.update()

    def on_combo(self, _):
        self.object_set = self.bank_dropdown.currentIndex()

        self.sprite_bank.object_set = self.object_set

        self.sprite_bank.update()

    def on_palette(self, value):
        self.sprite_bank.palette_group = value
        self.sprite_bank.update()


class BlockBank(QWidget):
    def __init__(self, parent, object_set=0, palette_group=0, zoom=2):
        super(BlockBank, self).__init__(parent)
        self.setMouseTracking(True)

        self.sprites = 256
        self.zoom_step = 256
        self.sprites_horiz = 16
        self.sprites_vert = ceil(self.sprites / self.sprites_horiz)

        self.object_set = object_set
        self.palette_group = palette_group
        self.zoom = zoom

        self._size = QSize(self.sprites_horiz * Block.WIDTH * self.zoom, self.sprites_vert * Block.HEIGHT * self.zoom)

        self.setFixedSize(self._size)

    def resizeEvent(self, event: QResizeEvent):
        self.update()

    def zoom_in(self):
        self.zoom += 1
        self._after_zoom()

    def zoom_out(self):
        self.zoom = max(self.zoom - 1, 1)
        self._after_zoom()

    def _after_zoom(self):
        new_size = QSize(self.sprites_horiz * Block.WIDTH * self.zoom, self.sprites_vert * Block.HEIGHT * self.zoom)

        self.setFixedSize(new_size)

    def mouseMoveEvent(self, event: QMouseEvent):
        x, y = event.pos().toTuple()

        block_length = Block.WIDTH * self.zoom

        column = x // block_length
        row = y // block_length

        dec_index = row * self.sprites_horiz + column
        hex_index = hex(dec_index).upper().replace("X", "x")

        status_message = f"Row: {row}, Column: {column}, Index: {dec_index} / {hex_index}"

        self.parent().statusBar().showMessage(status_message)

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)

        bg_color = bg_color_for_object_set(self.object_set, 0)
        painter.setBrush(QBrush(bg_color))

        painter.drawRect(QRect(QPoint(0, 0), self.size()))

        graphics_set = GraphicsSet.from_tileset(self.object_set)
        palette = load_palette_group(self.object_set, self.palette_group)
        tsa_data = ROM.get_tsa_data(self.object_set)

        horizontal = self.sprites_horiz

        block_length = Block.WIDTH * self.zoom

        for i in range(self.sprites):
            block = Block(i, palette, graphics_set, tsa_data)

            x = (i % horizontal) * block_length
            y = (i // horizontal) * block_length

            block.draw(painter, x, y, block_length)

        return
