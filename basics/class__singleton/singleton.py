#!/usr/bin/python3
##
## REFERENCES:
##     https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
##
## python2 and python3 compatible version
class Singleton_t(object):
  _instances = {}
  def __new__(class_, *args, **kwargs):
    if class_ not in class_._instances:
        class_._instances[class_] = super(Singleton_t, class_).__new__(class_, *args, **kwargs)
    return class_._instances[class_]

class Singleton(Singleton_t):
  pass



## usage
if __name__ == '__main__':

    s1=Singleton()
    s2=Singleton()

    if(id(s1)==id(s2)):
        print("Same")
    else:
        print("Different")
