# generate_half_key.py

## This is a script upon given numbers of student(integer) to the fuction half_key_generation(), it will auto-generate the 7 digit data448ID for that given number of student and store it in a csv file in one cloumn with header named Data448ID

## Structure
📜apps.py  
┣ Libaray imports
┣ Defined function: half_key_generation(int student)
┗ __name__ == "__main__"

## Structure of the Defined Function
    * half_key_generation(student)
        ┣ Declartion of dev_id(integer set), dev_key(String list) and is_full(boolean flag)
        ┣ Random generation of 7 digit id and store in set for duplication checking, when the length of dev_id the meet the required number of student, is_full wil be flagged
        ┣ Store integer set(dev_id) into String list(dev_key) for csv storage
        ┗ Open a csv file called HalfKey.csv in the /key folder and store the generated half keys into the csv in a single column with the header named Data448ID
