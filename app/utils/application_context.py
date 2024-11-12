




class ApplicationContext:

    _container={}

    @staticmethod
    def getContainer(cls,*args,**keywords):
        if cls not in ApplicationContext._container:
            ApplicationContext._container[cls]=cls(*args,**keywords)
        return ApplicationContext._container[cls]
    @staticmethod
    def hashContainer(cls)->bool:
        return cls in ApplicationContext._container