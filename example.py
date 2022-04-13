import grapp, story

# First wee need to open our text file 
with open('/Users/chizhikchi/NLP/Deshoras/text-files/Deshoras.txt', 'r') as file:
  text = file.read()
print(text[:150])

# now we define a list of characters of our story
pers_list = ['Sara', 'Doro', 'Felisa', 'Aníbal', 'la madre de Doro']

# initialize a `Story` object
s = story.Story(text, characters=pers_list, distance_threshold=15)

# get the matches of Story's relevant concepts 
c_dict = s.concept_matcher
p_dict = s.person_matcher

# get list of relevant concepts detected in the text
concept_list = s.concepts.values()

# extract connection between characters and concepts
pers_distances = s.get_distances(p_dict, p_dict)
cons_distances = s.get_distances(c_dict, c_dict)
pers_cons_distances = s.get_distances(c_dict, p_dict)

# define connection credential to store our graph in Neo4j
uri = "bolt://44.203.49.36:7687"
user= 'neo4j'
password = "feather-results-swap"

# initalize `Grapp` instance
app = grapp.Grapp(uri, user, password)

# store Person nodes
for p in pers_list:
  app.create_person(p)

# store Concept nodes
for c in concept_list:
  app.create_concept(c)
print(f'Created {len(concept_list)} concepts')

# create relations 
app.create_friendship(pers_distances)
app.create_relation(cons_distances)
app.create_pc_relation(pers_cons_distances)

app.close()