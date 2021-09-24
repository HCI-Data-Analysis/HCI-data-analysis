from scripts.generate_half_key.generate_half_key import half_key_generation

NUM_STUDENTS = 161
HALF_KEY_PATH = 'keys/HalfKey.csv'

if __name__ == '__main__':
    half_key_generation(NUM_STUDENTS, HALF_KEY_PATH)
