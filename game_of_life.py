import itertools

from ursina import *
app = Ursina()

# --- Camera settings
camera.position = Vec3(15, 15, -100)

# --- Const
CANVAS_SIZE = 30

UPDATE_RATE = 0
def change_update_rate_value(value):
    global UPDATE_RATE
    UPDATE_RATE = value

# --- Variables
isGamePaused = True
update_timer = UPDATE_RATE

# --- GUI
update_rate_slider = ThinSlider(
    text="Update rate",
    max=100,
    dynamic=True,
    on_value_changed=lambda: change_update_rate_value(update_rate_slider.value/100)
)

generate_pattern_button = Button(
    text="Generate pattern",
    on_click=lambda: generate_random_pattern()
)

reset_canvas_button = Button(
    text="Reset canvas",
    on_click=lambda: reset_canvas()
)

info_text = Text(text="Press C to hide/show this widget\nPress SPACE to start/stop the game\nLeft Click to paint\nRight click to erease")

control_pannel = WindowPanel(
    title="Control Panel",
    content=(
        update_rate_slider,
        generate_pattern_button,
        reset_canvas_button,
        info_text
    )
)

# --- Generate a blank canvas
cells = []
for x in range(CANVAS_SIZE):
    row = []
    for y in range(CANVAS_SIZE):
        cell = Entity(model="quad", collider="box", position=Vec2(x, y))
        row.append(cell)
    cells.append(row)

# --- Customs functions
def reset_canvas():
    for row in cells:
        for cell in row:
            cell.color = color.white

def generate_random_pattern():
    reset_canvas()
    
    for row in cells:
        for cell in row:
            if random.randint(0, 100) >= random.randint(0, 100):
                continue
            cell.color = color.black

def paint():
    if (hovered_cell := mouse.hovered_entity):
        if mouse.right:
            hovered_cell.color = color.white
        if mouse.left:
            hovered_cell.color = color.black

def update_cells():
    for x, y in itertools.product(range(CANVAS_SIZE), repeat=2):
        cell : Entity = cells[x][y]

        neighbors = []
        for neighboring_x, neighboring_y in itertools.product(range(x - 1, x + 2), range(y - 1, y + 2)):
            if 0 < neighboring_x >= CANVAS_SIZE: continue
            if 0 < neighboring_y >= CANVAS_SIZE: continue
            
            neighboring_cell : Entity = cells[neighboring_x][neighboring_y]
            if neighboring_cell.position == cell.position: continue
            
            isNeighborBlack = neighboring_cell.color == color.black
            neighbors.append(isNeighborBlack)
            
        neighbors = sum(neighbors)

        if cell.color == color.black:
            if neighbors < 2 or neighbors > 3:
                cell.color = color.white
        elif cell.color == color.white:
            if neighbors == 3:
                cell.color = color.black

# --- Ursina functions
def update():
    global isGamePaused, update_timer
    
    paint()
    
    if isGamePaused: return
    
    if update_timer > 0:
        update_timer -= time.dt
    else:
        update_timer = UPDATE_RATE
        update_cells()

def input(key):
    global isGamePaused
    
    match(key):
        case "space":
            isGamePaused = not isGamePaused
        case "c":
            control_pannel.enabled = not control_pannel.enabled

app.run()
