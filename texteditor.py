import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

class MainWindow(qtw.QMainWindow):

    def __init__(self):
        """MainWindow constructor"""
        super().__init__()
        # Main UI code
        # Setting central widget
        self.textedit = qtw.QTextEdit()
        self.setCentralWidget(self.textedit)

        # Creating status bar
        self.statusBar().showMessage('This is a text editor')

        charcount_label = qtw.QLabel('Chars: 0')
        self.textedit.textChanged.connect(
            lambda: charcount_label.setText(
                "chars: " +
                str(len(self.textedit.toPlainText()))
            )
        )
        self.statusBar().addPermanentWidget(charcount_label)

        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')
        edit_menu = menubar.addMenu('Edit')
        help_menu = menubar.addMenu('Help')

        open_action = file_menu.addAction('Open')
        save_action = file_menu.addAction('Save')
        quit_action = file_menu.addAction('Quit', self.destroy)
        edit_menu.addAction('Undo', self.textedit.undo)

        redo_action = qtw.QAction('Redo', self)  # Add parent widget to QAction
        redo_action.triggered.connect(self.textedit.redo)
        edit_menu.addAction(redo_action)

        toolbar = self.addToolBar('File')
        toolbar.addAction(open_action)
        toolbar.addAction('Save')
        # toolbar.setMovable(False)
        toolbar.setFloatable(False)
        toolbar.setAllowedAreas(
            qtc.Qt.TopToolBarArea |
            qtc.Qt.BottomToolBarArea
        )

        # icons
        open_icon = self.style().standardIcon(qtw.QStyle.SP_DirOpenIcon)
        save_icon = self.style().standardIcon(qtw.QStyle.SP_DriveHDIcon)

        open_action.setIcon(open_icon)
        toolbar.addAction(open_action)

        save_action.setIcon(save_icon)
        toolbar.addAction(
            save_icon, 'Save',
            lambda: self.statusBar().showMessage('File Saved!')
        )

        help_action = qtw.QAction(
            self.style().standardIcon(qtw.QStyle.SP_DialogHelpButton),
                                      'Help',
                                      self, #VERY IMPORTANT TO PASS THE PARENT!!
                                      triggered=lambda: self.statusBar().showMessage(
                                          'Sorry!')
                                      )

        toolbar.addAction(help_action)

        toolbar2 = qtw.QToolBar('Edit')
        toolbar2.addAction('Copy', self.textedit.copy)
        toolbar2.addAction('Cut', self.textedit.cut)
        toolbar2.addAction('Paste', self.textedit.paste)
        self.addToolBar(qtc.Qt.RightToolBarArea, toolbar2)

        # Dock widgets
        dock = qtw.QDockWidget('Replace')
        self.addDockWidget(qtc.Qt.LeftDockWidgetArea, dock)

        dock.setFeatures(
            qtw.QDockWidget.DockWidgetMovable |
            qtw.QDockWidget.DockWidgetFloatable
        )

        replace_widget = qtw.QWidget()
        replace_widget.setLayout(qtw.QVBoxLayout())
        dock.setWidget(replace_widget)

        self.search_text_inp = qtw.QLineEdit(placeholderText='search')
        self.replace_text_inp = qtw.QLineEdit(placeholderText='replace')
        search_and_replace_btn = qtw.QPushButton(
            'Search and Replace',
            clicked=self.search_and_replace
        )
        replace_widget.layout().addWidget(self.search_text_inp)
        replace_widget.layout().addWidget(self.replace_text_inp)
        replace_widget.layout().addWidget(search_and_replace_btn)
        replace_widget.layout().addStretch()



        # End main UI code
        self.show()

    def search_and_replace(self):
        s_text = self.search_text_inp.text()
        r_text = self.replace_text_inp.text()

        if s_text:
            self.textedit.setText(
                self.textedit.toPlainText().replace(s_text, r_text)
            )

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())