import os


my_path =os.path.dirname(os.path.abspath(__file__))
folder_list = []
for file in os.listdir(my_path):
    if not "." in file:
        folder_list.append(file)
folder_list.remove("Image")
print (folder_list)

