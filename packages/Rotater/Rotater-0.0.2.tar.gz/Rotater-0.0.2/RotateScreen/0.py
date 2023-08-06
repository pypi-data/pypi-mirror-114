import rotatescreen

def Rotate():
    screen = rotatescreen.get_primary_display()
    screen.rotate_to(0)
