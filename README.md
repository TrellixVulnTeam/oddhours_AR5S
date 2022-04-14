# 🪄⏱ Oddhours: cuantitative graph-based analysis of short stories

Oddhours is a resource for knowledge graph extraction from texts in order to create a cuantitative base for literature analysis. Oddhours brings the text to [Neo4j](https://neo4j.com) graph database in form of conceptual graph, where all characters and relevant ideas are linked.

## 🔧 Installation
To install and set up Oddhours run the following commands in your terminal:

```git clone https://github.com/chizhikchi/oddhours 
cd oddhours\npython -m venv .env
source .env/bin/activate
pip install -r requirements.txt
```

Now that the package is ready to use, make sure you have set up your Ne4j database. I suggest using Neo4j Sanbox because it is free and is compatible with many other useful intruments, such as [Bloom](https://neo4j.com/product/bloom/), a graph data visualization platform and [NEuler](https://neo4j.com/developer/graph-data-science/neuler-no-code-graph-algorithms/), a no-code graph data-science environment. 

## 📖 Let the *Story* begin: process your text
By converting the text into Oddhours' Story object, you can access to it's relevant ideas and perform relation extraction. To do so, prepare the tale, a list of its characters and think of the maximum distance between two concepts to consider them linked. In this example we suppose that entities found on the distance of less that 15 tokens are linked. 

```import story
with open('text-files/Deshoras.txt', 'r') as file:
  text = file.read()
# define a list of characters of our story
pers_list = ['Sara', 'Doro', 'Felisa', 'Aníbal']
s = story.Story(text, characters=pers_list, distance_threshold=15)
```

The next step is to perform matching and get the links that exist between the entities in the text:

```# get the matches of Story's relevant concepts 
c_dict = s.concept_matcher
p_dict = s.person_matcher

# get list of relevant concepts detected in the text
concept_list = s.concepts.values()

# extract connections between characters and concepts
pers_distances = s.get_distances(p_dict, p_dict)
cons_distances = s.get_distances(c_dict, c_dict)
pers_cons_distances = s.get_distances(c_dict, p_dict)
```

## 🖇 *Grapp* it up: log the data to Neo4j
Once you're done with text processing, you need to log the data to Neo4j. **Grapp** is a module that helps you to deal with it:
```# initalize `Grapp` instance
app = grapp.Grapp(uri, user, password)

# store Person nodes
for p in pers_list:
  app.create_person(p)

# store Concept nodes
for c in set(concept_list):
  app.create_concept(c)

# create relations 
app.create_friendship(pers_distances)
app.create_relation(cons_distances)
app.create_pc_relation(pers_cons_distances)

# close the session
app.close()```

## 📚🔬 Do not accept other chronology than the time of the oddhours: knowledge ghraphs for literature investigation.
This package introduces a method for literature investigation which aims to construct an objective fundament for futher critical analysis. Disruption of the cualitative **vs** cuantitative dichotomy opens new directions for the Humanities that are attuned to the modern-day worldview: broad, multimodal and stereotype agnostic.
Knowledge graph is a data structure that can bring together literature and graph theory allowing Digital Humanists to get a fresh sight at the artwork. 
Just some simple examples to illustrate the potential of conceptual graphs for literature investigation:
* You can find the most important ideas calculating *betwenness centrality* for the nodes.
* Node clustering algorithms can show you how the text is structured
* *Grapp* watches the frecuency of occurence for each relation: take a look at the weight of each link. 

## 🔍 An example: the relevance of night (noche) and dream (sueño) in Cortazar's **Deshoras**
Here is an extract from a knowleghe graph from the text of one of Julio Cortazar's short stories. The size of each node depends on its betweennes centrality value and the darkness of line denotes the weight of each relationship. Long story short (in fact, short story shorter) night and dream are fundamental for the story's global economy, because the main character sees his beloved in dreams that materialize many years after in an unexpected encounter which clarifies the mutuality of his child's enthusiastic love that seemed frustrated. Here we can see that the graph underlines the importance of two concepts, making it possible to spot even in distant-readig scenario. 
![Sueño-noche](https://user-images.githubusercontent.com/80167197/163492929-a4e4df56-6657-41c9-96c4-35155d71a264.png)
