#! coding:utf-8
"""
LiteListView


(2016/03/23) ver0.0 たたき台を作成

Created by fifi  (2016/03/23 22:01)
"""
__version__ = '0.0'
import os
import re

from PySide.QtCore import Qt, Signal
from PySide.QtGui import QListView, QStringListModel


# # :: FileListView
# self.listView = QListView()
# # self.listView.setModel(self.model)
# self.model = QStringListModel(self.listView)
# self.model.setStringList(["abc", "def", "ghi", "jkl"])
# self.listView.clicked.connect(self.flush_listitem)
# self.listView.dragDropMode()

class LiteListView(QListView):
    fileDropped = Signal(list)

    def __init__(self, parent=None):
        super(LiteListView, self).__init__(parent)
        # モデルの作成
        self.model = QStringListModel()
        self.setModel(self.model)
        # D&D処理を許可
        self.setAcceptDrops(True)

    def clearItems(self):
        self.model.setStringList([])

    def addItems(self, itemlist):
        self.model.setStringList(itemlist)

    def getItems(self):
        return self.model.stringList()

    # ***************************************
    # ドラッグアンドドロップのイベント処理
    # ***************************************
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)  # おまじない
            event.accept()  # おまじない

            # ファイルの読み込み
            files = [unicode(u.toLocalFile()) for u in event.mimeData().urls()]
            self.clearItems()  # Itemをクリア

            wav_files = []
            # 各ファイルをアイテムに保存
            for fname in files:
                root, ext = os.path.splitext(fname)
                # wavファイルを取得し、Itemを生成
                if re.match(r"^\.(wav|WAV)$", ext, re.IGNORECASE):
                    wav_files.append(fname)

            self.addItems(wav_files)
            # ドロップ処理終了のイベント発行
            self.fileDropped.emit(wav_files)

        else:
            # おまじない
            event.ignore()
