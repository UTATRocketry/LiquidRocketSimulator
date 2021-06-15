'''
The Python 3D rendering engine is adapted from
https://github.com/hnhaefliger/pyEngine3D
'''
import graphics.engine
from graphics.item import Item,LineItem

rocket = Item("Rocket")
plane = Item("Plane",prev_item=rocket,color="white",border='same')

trajectory = LineItem("Trajectory",[[0,0,0],[0,0,0]],prev_item=plane,color='red')

canvas = graphics.engine.Engine3D([rocket,plane,trajectory], distance=100, title='Rocket', background='cyan')


def animation():
    global p
    canvas.clear()
    rocket.move("y",0.01)
    rocket.move_to((0,0,0))
    canvas.render()
    canvas.screen.after(1, animation)

animation()
canvas.screen.window.mainloop()