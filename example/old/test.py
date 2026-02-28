from maskCanvas import AxidrawInterface
import dill

def main():

    with open('./canvas/falling_man.pkl', 'rb') as file:
        c = dill.load(file)

    c.show_bitmap(50)
    ai = AxidrawInterface(c)

if __name__ == "__main__":
    main()
