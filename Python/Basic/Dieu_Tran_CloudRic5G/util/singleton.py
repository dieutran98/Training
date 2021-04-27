class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        if cls not in cls._instances: 
            cls._instances[cls] = instance
        return cls._instances[cls]       
    
if __name__ == "__main__":
    class Testing(metaclass = Singleton):
        pass
    
    t1 = Testing()
    t2 = Testing()
    print(t1)
    print(t2)