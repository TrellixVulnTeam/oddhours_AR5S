import grapp, story
import os 
os.chdir('/Users/chizhikchi/NLP/Deshoras')
# First wee need to open our text file 
with open('text-files/Deshoras.txt', 'r') as file:
  text = file.read()
print(text[:150])

# now we define a list of characters of our story
pers_list = ['Sara', 'Doro', 'Felisa', 'Aníbal', 'la madre de Doro']

# initialize a `Story` object
s = story.Story(text, characters=pers_list, distance_threshold=15)
concept_list = s.concepts.values()
print(len(concept_list))
for s in concept_list:
    print(s)