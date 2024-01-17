from typing import Any
import inspect
import sys
import traceback

def flatten(S):
    if S == []:
        return S
    if isinstance(S[0], list):
        return flatten(S[0]) + flatten(S[1:])
    return S[:1] + flatten(S[1:])

class future_list():
    future = []
    def __init__(self, *lis):
        self.future = flatten([*lis])
    def __add__(self, other):
        return future_list(flatten(self.future + [other]))
    def __radd__(self, other):
        return future_list(flatten([other] + self.future))


class future_var():
    def __init__(self, var=None):
        self.future = var
    def __repr__(self):
        return self.future
    def __str__(self) -> str:
        return str(self.future)
    def __add__(self, other):
        return future_list(self, other)
    def __radd__(self, other):
        return future_list(other, self)
    
class blank():
    pass

class Planner(object):
    def __init__(self, args: dict = None) -> None:
        self.set_atributes(self, args)

    def __getattribute__(self, __name: str) -> Any:
        if type(object.__getattribute__(self, __name)) == future_var or type(object.__getattribute__(self, __name)) == future_list:
            return self.__getattr__(__name)
        else:
            return object.__getattribute__(self, __name)
    def __getattr__ (self, __name: str) -> Any:
        if __name in self.__dict__:
            if type(object.__getattribute__(self, __name)) == future_var:
                if object.__getattribute__(self, __name).future in self.__dict__:
                    self.__setattr__(__name, object.__getattribute__(self, __name).future)
                    
                    return object.__getattribute__(self, __name)
                else: 
                    return 0 #TODO
            elif type(object.__getattribute__(self, __name)) == future_list:
                present_list = []
                for key_2 in object.__getattribute__(self, __name).future:
                    if type(key_2) == future_var:
                        if key_2.future in self.__dict__:
                            
                            present_list.append(self.__getattr__(key_2.future))
                        else:
                            return object.__getattribute__(self, __name)
                    else:
                        present_list.append(key_2)
                for i in range(1, len(present_list)):
                    present_list[0] += present_list[i]
                self.__setattr__(__name, present_list[0])

                return object.__getattribute__(self, __name)

            else:
                return object.__getattribute__(self, __name)
        else:
            return future_var(__name)
    
    # function for reading comand line arguments 
    def parse_comand_args(self):
        for arg in sys.argv[1:]:
            setattr(self, arg.split(":"))

    @staticmethod
    def set_atributes(exemplar, atributes: dict):
        if type(atributes) != dict:
            return exemplar
        try:
            for key in atributes:
                if type(atributes[key]) == dict:
                    if hasattr(exemplar, key) and not type(getattr(exemplar, key)) in [future_var, future_list]:
                        Planner.set_atributes(getattr(exemplar, key), atributes[key])
                    else:     
                        setattr(exemplar, key, Planner())
                        Planner.set_atributes(getattr(exemplar, key), atributes[key])
                else:
                    setattr(exemplar, key, atributes[key])
            return True
        except Exception as ex: 
            print(traceback.format_exc())
            return ex
    # TODO: check!!
    # TODO: list not resolved objcts
    
    @staticmethod    
    def check_resolve(exemplar: object):
        for key in exemplar.__dict__:
            attribute = getattr(exemplar, key)
            if type(attribute) == future_list or type(attribute) == future_var:
                return False
            else:
                if inspect.isclass(attribute):
                    if not Planner.check_resolve(attribute):
                        return False
        return True

    @staticmethod
    def get_attributes(obj):
        attribute_values = []

        # Get all attributes of the object
        attributes = dir(obj)
        attributes = [attr for attr in attributes if not attr.startswith('__')]

        for attr in attributes:
            value = getattr(obj, attr)
            
            # If the value is an object, recursively get its attribute values
            if hasattr(value, '__dict__'):
                attribute_values.extend(Planner.get_attributes(value))
            else:
                attribute_values.append(value)
        return attribute_values
    
    @staticmethod
    def dict_collector(obj):
        res_dict = {}
        for key in obj.__dict__:
            if type(getattr(obj, key)) in [int, str, dict, list]:
                res_dict[key] = getattr(obj, key)
            elif getattr(obj, key) == None:
                pass
            else:
                res_dict[key] = Planner.to_dict(getattr(obj, key))

        return res_dict

    def to_dict(self):
        return Planner.dict_collector(self)
    
    def hasattr(self, attr):
        return type(self.__getattr__(attr)) != future_var
    