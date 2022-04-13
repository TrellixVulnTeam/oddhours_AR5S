"""
This module serves to log your data into Neo4j Database
"""

from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable

class Grapp:

    def __init__(self, uri, user, password):
        """ 
        To use the Grapp class you need to register on Neo4j platform and open a Database.
        """
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
    # Don't forget to close the driver connection when you're finished with it
        self.drive.close()

    @staticmethod
    def _create_and_return_concept(tx, concept):
        entity_query = """
        MERGE (c:Concept{name:$concept})
        RETURN c
        """
        result = tx.run(entity_query, concept=concept)
        return [{'c': row['c']['name'  ]} for row in result]

    def create_concept(self, concept):
        """
        This function creates Concept node

        Args:
            concept: str containing concept name
        """
        with self.driver.session() as session:
            result = session.write_transaction(
                self._create_and_return_concept, concept)
        #for row in result:
            #print('Created concept: {}'.format(row['c']))

    @staticmethod
    def _create_and_return_person(tx, person):
        person_query = """
        MERGE (p:Person{name:$person})
        ON CREATE SET p.count = 1
        ON MATCH SET p.count = p.count + 1
        RETURN p
        """
        result = tx.run(person_query, person=person)
        return [{'p': row['p']['name']} for row in result]

    def create_person(self, person):
        """
        This function creates Person node
        
        Args:
            person: str containing person name
        """
        with self.driver.session() as session:
            result = session.write_transaction(
                self._create_and_return_person, person)
        for row in result: 
            print('Created person: {}'.format(row['p']))
  

    @staticmethod
    def _create_and_return_relation(tx, data):
        data = [{'source': el[0], 'target': el[1], 'weight': data[el]} for el in data]
        query = ("""
        UNWIND $data as row
        MERGE (c1:Concept {name: row.source})
        ON CREATE SET c1.count = 1
        ON MATCH SET c1.count = c1.count + 1
        MERGE (c2:Concept {name: row.target})
        ON CREATE SET c2.count = 1
        ON MATCH SET c2.count = c2.count + 1
        MERGE (c1)-[l:LINKED]->(c2)
        SET l.weight = coalesce(l.weight, 0) + row.weight
        RETURN c1, c2""")
        result = tx.run(query, {'data': data})
        return [{'c1': row['c1']['name'], 'c2': row['c2']['name']} for row in result]

    def create_relation(self, data):
        """ This function creates relation between Concept nodes
        Args:
            data: Counter or dict where keys are tuples ex: (Concept1, Concept2) and values are weights of relationships.
        """
        with self.driver.session() as session:
            result = session.write_transaction(
                self._create_and_return_relation, data)
        print('Created {} relations'.format(len(result)))


    @staticmethod
    def _create_and_return_pc_relation(tx, data):
        data = [{'source': el[0], 'target': el[1], 'weight': data[el]} for el in data]
        query = ("""
        UNWIND $data as row
        MERGE (p:Person {name: row.source})
        MERGE (c:Concept {name: row.target})
        MERGE (p)-[l:LINKED]->(c)
        SET l.weight = coalesce(l.weight, 0) + row.weight
        RETURN p, c"""
        )
        result = tx.run(query, {'data': data})
        return [{'p': row['p']['name'], 'c': row['c']['name']} for row in result]

    def create_pc_relation(self, data):
        """ This function creates relation between Person and Concept nodes
        Args:
            data: Counter or dict where keys are tuples ex: (Person, Concept) and values are weights of relationships.
        """
        with self.driver.session() as session:
            result = session.write_transaction(
                self._create_and_return_pc_relation, data)
        print('Created {} Person - Concept relations'.format(len(result)))

  
    @staticmethod
    def _create_and_return_fiendship(tx, data):
        data = [{'source': el[0], 'target': el[1], 'weight': data[el]} for el in data]
        query = ("""
        UNWIND $data as row
        MERGE (p1:Person {name: row.source})
        ON CREATE SET p1.count = 1
        ON MATCH SET p1.count = p1.count + 1
        MERGE (p2:Person {name: row.target})
        ON CREATE SET p2.count = 1
        ON MATCH SET p2.count = p2.count + 1
        MERGE (p1)-[l:LINKED]->(p2)
        SET l.weight = coalesce(l.weight, 0) + row.weight
        RETURN p1, p2""")

        result = tx.run(query, {'data': data})
        return [{'p1': row['p1']['name'], 'p2': row['p2']['name']} for row in result]

    def create_friendship(self, data):
        """ This function creates relation between Person nodes
        Args:
            data: Counter or dict where keys are tuples ex: (Person1, Person2) and values are weights of relationships.
        """
        with self.driver.session() as session:
            result = session.write_transaction(
                self._create_and_return_fiendship, data)
        for row in result:
            print('Created relation between: {p1}, {p2}'.format(p1=row['p1'], p2=row['p2']))


    @staticmethod
    def _find_and_return_concept(tx, concept_name):
        query = (
            "MATCH (c:Concept) WHERE c.name = $concept_name RETURN c.name AS name"
            )
        result = tx.run(query, concept_name=concept_name)
        return [row['name'] for row in result]

    
    def find_concept(self, concept_name):
        """ This function is used for cheking the existance of concept
        Args:
            concept_name: a string with name of the concept to find 
        """
        with self.driver.session() as session:
            result = session.read_transaction(self._find_and_return_concept, concept_name)
        for row in result:
            print('Found concept: {}'.format(row))