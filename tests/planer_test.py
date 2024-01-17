import unittest
from src.config_class import Planner

class test_config_class(unittest.TestCase):        
    def setUp(self) -> None:
        self.params = Planner()


    def test_simple_variable(self):
        self.params.simple = "some_var"
        self.assertEqual(self.params.simple, "some_var")

    def test_simple_redefinition(self):
        self.params.simple = "some_var"
        self.params.simple = "redefined"
        self.assertEqual(self.params.simple, "redefined")

    # lets pass some dict to config class to see, how it will handle it
    def test_init(self):
        test_dict = {
            "one": 1,
            "two": 2
        }
        self.params.set_atributes(self.params, test_dict)
        self.assertEqual(self.params.one, 1)


    # lets test, how lazy is our config:
    # in this test we see, that variable can be used before declaration
    def test_future_int(self):
        test_dict = {
            "one": 1
        }
        self.params.set_atributes(self.params, test_dict)
        self.params.three = self.params.two + self.params.one
        self.params.four = self.params.one + self.params.two
        self.params.two = 2
        self.assertEqual(self.params.three, 3)
        self.assertEqual(self.params.four, 3)
        

    def test_future_string(self):
        test_dict = {
            "one": "world"
        }
        self.params.set_atributes(self.params, test_dict)
        self.params.four = self.params.one + self.params.two
        self.params.three = self.params.two + self.params.one
        self.params.two = "Hello "
        self.assertEqual(self.params.three, "Hello world")
        self.assertEqual(self.params.four, "worldHello ")


    # lets check, how we can create nested variables
    def test_nested(self):
        test_dict = {
            "nested_arg":{
                "nested_one": 1,
                "deeper_nested": {
                    "very_deep": 2
                }
            }
        }
        self.params.set_atributes(self.params, test_dict)
        self.assertEqual(self.params.nested_arg.nested_one, 1)
        self.assertEqual(self.params.nested_arg.deeper_nested.very_deep, 2)


    # lets check redefinition of basic params
    def test_redefinition(self):
        test_dict = {
            "two": bin(2)
        }
        self.params.set_atributes(self.params, test_dict)
        self.assertEqual(self.params.two, bin(2))        


    # lets check redefinition of nested params
    def test_redefinition_nested(self):
        test_dict = {
            "nested_arg": {
                "nested_one": bin(1)
            }
        }
        self.params.set_atributes(self.params, test_dict)    
        self.assertEqual(self.params.nested_arg.nested_one, bin(1))

    def test_class_to_dict(self):
        self.params.simple = "some_var"
        self.assertEqual(type(self.params.to_dict()), dict)

    def test_add_future(self):
        self.params.one = 1
        self.params.tree = self.params.one + self.params.two
        self.params.final = self.params.tree + self.params.four
        self.params.four = self.params.two + self.params.two
        self.params.two = 2
        self.assertEqual(self.params.final, 7)



if __name__ == "__main__":
    unittest.main()