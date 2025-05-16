import pickle

ratings = {"Turkey BLT": {5:13, 4:12, 3:11, 2:10, 1:9},
        "Cheese Pizza" : {5:23, 4:22, 3:21, 2:20, 1:19},
        "Sausage Pizza" : {5:33, 4:32, 3:31, 2:30, 1:29},
        "Cheeseburger" : {5:43, 4:42, 3:41, 2:40, 1:39},
        }

def store_data(ratings_dict: dict[str, dict[int, int]]):


    ratings_file = open('example_ratings', 'wb')
    pickle.dump(ratings_dict, ratings_file)
    ratings_file.close()

store_data(ratings)