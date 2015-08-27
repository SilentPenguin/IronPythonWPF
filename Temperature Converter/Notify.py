from System.ComponentModel import INotifyPropertyChanged, PropertyChangedEventArgs

class notify(property):
    '''
    Wraps a property, allowing it to be used with INotifyPropertyChanged
    '''
    def __init__(self, getter):
        def new_getter(this):
            try:
                return getter(this)
            except AttributeError:
                return None
        return super(notify, self).__init__(new_getter)

    def setter(self, setter):
        def new_setter(this, value):
            if self.fget(this) == value: return
            setter(this, value)
            this.OnPropertyChanged(setter.__name__)
        return super(notify, self).setter(new_setter)

class NotifyPropertyChangedBase(INotifyPropertyChanged):
    '''
    Acts as a base for the implementation of INotifyPropertyChanged
    '''
    PropertyChanged = None

    def __init__(self):
        self.PropertyChanged = EventHandler()

    def add_PropertyChanged(self, value):
        self.PropertyChanged += value

    def remove_PropertyChanged(self, value):
        self.PropertyChanged -= value

    def OnPropertyChanged(self, propertyName):
        if self.PropertyChanged is None: return
        self.PropertyChanged(self, PropertyChangedEventArgs(propertyName))

class EventHandler(object):
    '''
    CLR style Event Handler
    '''
    handlers = None

    def __init__(self):
        self.handlers = []

    def __iadd__(self, value):
        if callable(value): self.handlers.append(value)
        return self

    def __isub__(self, value):
        if value in self.handlers: self.handlers.remove(value)
        return self

    def __get__(self, instance, owner):
        return self if self.handlers else None

    def __call__(self, *args):
        for handler in self.handlers: handler(*args)