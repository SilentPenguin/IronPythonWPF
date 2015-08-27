import wpf
from Model import ViewModel
from System.Windows import Application, Window

class MyWindow(Window):

    def __init__(self):
        wpf.LoadComponent(self, 'Temperature_Converter.xaml')
        self.DataContext = ViewModel()

if __name__ == '__main__':
    Application().Run(MyWindow())
