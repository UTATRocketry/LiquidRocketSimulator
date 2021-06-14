'''
The Python 3D rendering engine is adapted from
https://github.com/hnhaefliger/pyEngine3D
'''
import graphics.engine
from graphics.item import Item

rocket = Item("Rocket")
plane = Item("Plane",len(rocket.points))

canvas = graphics.engine.Engine3D([rocket,plane], distance=100, title='Rocket', background='cyan')

def animation():
    canvas.clear()
    rocket.move("y",0.01)
    canvas.render()
    canvas.screen.after(1, animation)

animation()
canvas.screen.window.mainloop()