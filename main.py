import GUI

infinity=99999

graph = [
    [0, 5, 6, 17],
    [6, 0, 3, 1],
    [6, 5, 0, 1],
    [7, 1, 1, 0]
]


def main():
    app = GUI.TrashCollectionApp_GUI()
    app.mainloop()


if __name__ == "__main__":
    main()
