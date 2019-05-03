from importlib import import_module

#j将文件配置载入内存
class Settings:
    def __init__(self):
        self.attribute ={}  #存放配置数据
        self.setmodule('spiders.config')

    def get(self, name, default=None):
        return self.attribute[name] if self.attribute[name] is not None else default

    def getbool(self, name, default=False):
        got = self.attribute.get(name, default)
        try:
            return bool(int(got))
        except ValueError:
            if got in ("True", "true"):
                return True
            if got in ("False", "false"):
                return False
            raise ValueError("Supported values for boolean settings "
                             "are 0/1, True/False, '0'/'1', "
                             "'True'/'False' and 'true'/'false'")

    def getint(self, name, default=0):
        return int(self.attribute.get(name, default))

    def getlist(self,name,default =None):
        value = self.attribute.get(name, default or [])
        if isinstance(value,str):
            value = value.split(',')
        return list(value)

    def setmodule(self,module):
        # 检查modle的类型
        if isinstance(module,str):
            module = import_module(module)
        for key in dir(module):
            if key.isupper():
                self.attribute[key] = getattr(module,key)

    def getwithbase(self, name):
        """加一个后缀：_BASE"""
        return self.getlist(name+'_BASE')


if __name__ =='__main__':
    s =Settings()
    print(s.attribute)