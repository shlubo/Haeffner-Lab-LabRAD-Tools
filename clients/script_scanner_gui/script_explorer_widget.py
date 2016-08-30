from PyQt4 import QtGui, QtCore
from experiment_selector_widget import experiment_selector_widget
from script_explorer.ParameterImporter import ParameterImportWidget

class script_explorer_widget(QtGui.QWidget):

    def __init__(self, parent, font = None):
        super(script_explorer_widget, self).__init__(parent)
        self.font = font
        self.parent = parent
        self.experiments = []
        if self.font is None:
            self.font = QtGui.QFont('MS Shell Dlg 2', pointSize=12)
        # dictionary containing Parent items for the tree model
        self.parameters = {}
        self.setupLayout()
        self.connect_layout()

    def setupLayout(self):

        layout = QtGui.QGridLayout()
        label = QtGui.QLabel('Experiment', font = self.font)
        self.dropdown = QtGui.QComboBox()
        self.dropdown.setMaxVisibleItems(30)
        self.dropdown.addItem('')#add empty item for no selection state    
        #enable sorting
        sorting_model = QtGui.QSortFilterProxyModel(self.dropdown)
        sorting_model.setSortCaseSensitivity(QtCore.Qt.CaseInsensitive)
        sorting_model.setSourceModel(self.dropdown.model())
        self.dropdown.model().setParent(sorting_model)

        self.tree_view = QtGui.QTreeView()
        self.tree_model = QtGui.QStandardItemModel()
        self.tree_view.setModel(self.tree_model)

        self.parameter_importer = ParameterImportWidget(self)

        self.tree_view.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tree_view.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)

        layout.addWidget(label, 0, 0, 1, 1)
        layout.addWidget(self.dropdown, 0, 1, 1, 1)
        layout.addWidget(self.tree_view, 1, 0, 2, 1)
        layout.addWidget(self.parameter_importer, 3, 0, 2, 1)
        self.setLayout(layout)

    def connect_layout(self):
        self.tree_view.selectionModel().currentChanged.connect(self.currentChanged)
    def currentChanged(self, current, old):
        row = current.row()
        item = self.tree_model.item(row)
        collection, parameter = item.text().split(', ')
        self.parameter_importer.new_parameter(collection, parameter)

    def addExperiment(self, experiment):
        self.dropdown.addItem(experiment)
        self.dropdown.model().sort(0)
        self.experiments.append(experiment)

    def add_parameter(self, collection, parameter):
        p = QtGui.QStandardItem(collection + ", " + parameter)
        self.tree_model.appendRow(p)

    def clear(self):
        '''
        Remove all data from the model
        '''
        self.tree_model.removeRows( 0, self.tree_model.rowCount() )
        self.parameters = {}
