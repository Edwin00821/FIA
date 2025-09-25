import sys

from src.app.application import Application


def main():

    try:
        app = Application()
        app.run()
        return 0
    except Exception as e:
        print(f"Error inesperado: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
