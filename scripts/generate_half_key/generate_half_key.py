from random import randint
import csv

def half_key_generation(num_students):
    is_full = False

    dev_id = set()
    dev_key = list()
    dev_key.append("Data448ID")

    while is_full == False:
        random_id = randint(1000000, 9999999)

        dev_id.add(random_id)

        if len(dev_id) == num_students:
            is_full = True

    for id in dev_id:
        dev_key.append(str(id))

    with open("../../keys/HalfKey.csv", "w") as f: 
        writer = csv.writer(f, lineterminator='\n')
        for id in dev_key:
            writer.writerow([id])
    f.close()

if __name__ == "__main__":
    half_key_generation(161) 
