import pickle

'''
emp = {1:"A"}
pickling_on = open("Emp.pickle","wb")
pickle.dump(emp, pickling_on)
pickling_on.close()
'''
pickle_off = open("3.pickle","rb")
emp = pickle.load(pickle_off)
print(emp)