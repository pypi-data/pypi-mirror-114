from qb_solver import *

def main():
    menu()
    # setting camera, lighting, and scene
    camera.setPos(16, 8, -25)
    camera.lookAt(cube)
    light = DirectionalLight(x=3, y=20, z=-10)
    light.lookAt(cube)  # making sure the cube is always well lit
    window.icon_filename = 'icon'  # not working yet :(
    window.title = 'QB'
    hintCube.reparent_to(cube)  # making the hints stay attached to cube
    app.run()  # opens window

if __name__ == '__main__':
    main()