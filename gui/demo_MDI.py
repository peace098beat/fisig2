#! coding:utf-8
"""
demo_MDI

Created by 0160929 on 2016/03/23 16:03
"""
import sys

from PySide.QtCore import Slot
from PySide.QtGui import QMainWindow, QApplication, QWorkspace, QVBoxLayout, QPushButton, QWidget, \
    QStatusBar, QProgressBar

from gui.guitools.FileListWidget import FileListView
from fisig import SignalData

class MyMDIApp(QMainWindow):
    def __init__(self):
        super(MyMDIApp, self).__init__()

        self.setGeometry(50, 40, 720, 480)
        # self.setAcceptDrops(True)

        # ====================================
        # UIの生成
        # ====================================
        # :: MDIワークスペースのインスタンス化
        workspace = QWorkspace()
        workspace.setWindowTitle("Simple WorkSpace Exmaple")

        # :: FileListView
        self.file_view = FileListView()
        self.file_view.resize(150, 300)
        self.file_view.setWindowTitle("File List")
        workspace.addWindow(self.file_view)

        # :: ボタンs
        layout = QVBoxLayout()
        self.btn_ana = QPushButton("Analysis")
        self.btn_plot = QPushButton("Plot")
        self.btn_save = QPushButton("Save")
        layout.addWidget(self.btn_ana)
        layout.addWidget(self.btn_plot)
        layout.addWidget(self.btn_save)
        btn_wid = QWidget()
        btn_wid.setWindowTitle("Btns")
        btn_wid.setLayout(layout)
        workspace.addWindow(btn_wid)

        # :: ステータスバー
        self.myStatusBar = QStatusBar()
        self.setStatusBar(self.myStatusBar)
        self.myStatusBar.showMessage('Ready', 1000)
        # ====================================
        # ステータスバーにプログラスバーを追加
        # ====================================
        self.progressBar = QProgressBar()
        self.myStatusBar.addPermanentWidget(self.progressBar)
        self.progressBar.reset()
        self.progressBar.setVisible(False)
        self.progressBar.setValue(0)

        # :: MainWidgetに追加
        # workspace.tile()
        self.setCentralWidget(workspace)
        self.setCSS()

        # ====================================
        # シグナルスロットのコネクト
        # ====================================
        # FileListViewの関数
        self.file_view.fileDropped.connect(self.set_filelist)
        self.file_view.clicked.connect(self.slot1)
        # Analysisボタンで解析実行
        self.btn_ana.clicked.connect(self.run_analysis)
        self.btn_plot.clicked.connect(self.run_plot)

    @Slot()
    def slot1(self, index):
        # print 'listslot', index.row(), index.data(Qt.DisplayRole)
        # print self.filelist[index.row()]
        s = "Clicked : " + self.filelist[index.row()]
        self.flush(s)
        pass

    @Slot()
    def set_filelist(self, file_list):
        self.filelist = file_list
        self.flush("Load File List")
        pass

    @Slot()
    def run_analysis(self):
        self.flush(">analysis")
        self.progressBar.setVisible(True)
        self.progressBar.reset()

        N = len(self.filelist)

        result=[]

        for i, wav_file in enumerate(self.filelist):

            # 解析
            gawa,katasa = demo_analysis(wav_file)
            result.append([gawa,katasa])
            # プログレスバー
            self.progressBar.setValue(float(i+1)/N*100)

        self.progressBar.setVisible(False)
        self.result = result

    @Slot()
    def run_plot(self):
        pass

    @Slot()
    def flush(self, s):
        self.myStatusBar.showMessage(s, 1 * 1000)

    def setCSS(self):
        """cssを読みこんでセット        """
        with open("./guimodule/style13.css", "r") as f:
            self.setStyleSheet("".join(f.readlines()))

def demo_analysis(wavfilepaht):
    # オーディオロード
    sig = SignalData().load_wav(wavfilepaht, 'M')
    # スペクトログラム
    spgram = sig.slice_time_ms(80, 120).gwt()
    # スペクトル(インパクト音)
    spec_impact = spgram.slice_time_ms(20, 23).time_average()  # .plot().show()

    # ガワ感
    from numpy import var as npvar
    g = spec_impact.liftering(lifter=5, mode="low").slice_freq_hz(1000, 4500).info().get_data()
    gawa = npvar(g)
    print gawa
    # 硬さ
    katasa = spec_impact.liftering(lifter=15, mode="low").slice_freq_khz(1, 4.5).cof()  # .plot().show()
    print katasa

    return gawa, katasa


def main():
    app = QApplication(sys.argv)
    # app.setStyle('plastique')
    win = MyMDIApp()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
