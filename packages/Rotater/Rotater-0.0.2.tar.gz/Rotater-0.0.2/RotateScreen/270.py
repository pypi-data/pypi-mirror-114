import rotatescreen

def Back():
    screen = rotatescreen.get_primary_display()
    screen.rotate_to(270)
