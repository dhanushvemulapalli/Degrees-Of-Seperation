import csv
import sys

from util import Node, QueueFrontier

# Initialize a dictionary that keeps track of names
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    # The people.csv file has four columns: id, name, birth, and movies.
    # The id column contains a unique integer identifier for each person.
    # The name column contains the name of each person.
    # The birth column contains the year in which each person was born.
    # The movies column contains a comma-separated list of the IDs of all the movies in which that person has starred.
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    # The movies.csv file has three columns: id, title, and year.
    # The id column contains a unique integer identifier for each movie.
    # The title column contains the title of each movie.
    # The year column contains the year in which each movie was released.
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    # The stars.csv file has two columns: person_id and movie_id.
    # Each row contains one pair of identifiers.
    # Each pair identifies one actor and one movie in which that actor starred.
    # Each person_id in this file corresponds to an id value from the people.csv file.
    # Each movie_id in this file corresponds to an id value from the movies.csv file.
    # If Row 1 of stars.csv has the value 102 in the person_id column and the value 1045 in the movie_id column,
    # then Row 1 indicates that actor 102 starred in movie 1045.
    
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass
# Main Function

def main():    
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    #Taking the input of the source actor and the target actor
    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    #Calculating the shortest path using bfs algorithm

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """
    # Create a set to keep track of visited nodes
    visited = set()
    # Initialize the frontier queue with the source node
    frontier = QueueFrontier()
    start_node = Node(state=source, parent=None, action=None)
    frontier.add(start_node)

    while not frontier.empty():
        # Remove the node from the frontier
        current_node = frontier.remove()

        # Check if the current node is the target
        if current_node.state == target:
            # Build the path by traversing from target to source
            path = []
            while current_node.parent is not None:
                path.append((current_node.action, current_node.state))
                current_node = current_node.parent
            path.reverse()  # Reverse the path to start from source
            return path

        # Mark the current node as visited
        visited.add(current_node.state)

        # Explore the neighbors of the current node
        for movie_id, person_id in neighbors_for_person(current_node.state):
            #if the node is not visited and doesnt contain state then add the new node to frontier
            if person_id not in visited and not frontier.contains_state(person_id):
                new_node = Node(state=person_id, parent=current_node, action=movie_id)
                frontier.add(new_node)

    # If no path is found, return None
    return None



def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
    
