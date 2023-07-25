import tkinter as tk
import tkinter.messagebox

#Globals
canvas = None
pixels = None

current_size_x=50
current_size_y=50
current_border_size = 5

last_pixel = None

# Create window
window = tk.Tk()
window.title("knitt")

# create a frame to contain the canvas and toolbar
frame = tk.Frame(window)
frame.pack()

# create a toolbar at the bottom
toolbar = tk.Frame(frame)
toolbar.pack(side=tk.BOTTOM, fill=tk.X)

# populate toolbar
# create spinboxes for the grid size
spinbox_x = tk.Spinbox(toolbar, from_=1, to=100, width=4)
spinbox_x.pack(side=tk.LEFT)
spinbox_x.delete(0, tk.END)
spinbox_x.insert(0, 50)

spinbox_y = tk.Spinbox(toolbar, from_=1, to=100, width=4)
spinbox_y.pack(side=tk.LEFT)

spinbox_y.delete(0, tk.END)
spinbox_y.insert(0, 50)

generate_button = tk.Button(toolbar, text="Generate Pattern", command=None) 
generate_button.pack(side=tk.LEFT, padx=2, pady=2)

redraw_button = tk.Button(toolbar, text="Redraw Canvas", command=None) 
redraw_button.pack(side=tk.LEFT, padx=2, pady=2)

add_border_button = tk.Button(toolbar, text="Add Border", command=None)
add_border_button.pack(side=tk.LEFT, padx=2, pady=2)
border_size_spinbox = tk.Spinbox(toolbar, from_=1, to=50, width=4)
border_size_spinbox.pack(side=tk.LEFT, padx=2, pady=2)

# canvas functions
def add_border(border_size):
    global current_size_x
    global current_size_y
    global current_border_size
    global pixels

    # remove the current border from the pixels array
    for i in range(current_border_size):
        for j in range(current_size_x):
            pixels[i][j] = 0
            pixels[current_size_y-1-i][j] = 0
    for i in range(current_size_y):
        for j in range(current_border_size):
            pixels[i][j] = 0
            pixels[i][current_size_x-1-j] = 0


    # add new pixel border
    for i in range(border_size):
        for j in range(current_size_x):
            pixels[i][j] = i % 2
            pixels[current_size_y-1-i][j] = (current_size_y-1-i) % 2
    for i in range(current_size_y):
        for j in range(border_size):
            pixels[i][j] = i % 2
            pixels[i][current_size_x-1-j] = i % 2
    current_border_size = border_size
    create_canvas(current_size_x, current_size_y)

def clear_last_pixel():
    global last_pixel
    last_pixel = None

def toggle_pixel(event, pixels, canvas, size_x, size_y, on):
    global last_pixel
    # calculate the pixel coordinates
    pixel_x = event.x // 10
    pixel_y = event.y // 10

    # set the pixel
    #pixels[pixel_y][pixel_x] = 1 if on else 0
    if last_pixel != (pixel_x, pixel_y):
        if on:
            pixels[pixel_y][pixel_x] = 1 - pixels[pixel_y][pixel_x]

    # redraw the pixel on the canvas
    color = "light gray" if pixels[pixel_y][pixel_x] == 1 else "white"
    canvas.create_rectangle(pixel_x*10, pixel_y*10, pixel_x*10+10, pixel_y*10+10, fill=color)

    last_pixel = (pixel_x, pixel_y)

def create_canvas(size_x, size_y):
    global canvas
    global pixels
    global current_size_y
    global current_size_x
    # delete the old canvas if it exists
    if canvas is not None:
        canvas.destroy()

    current_size_x=size_x
    current_size_y=size_y
    
    # create a new 2D array for the pixel data
    new_pixels = [[0 for _ in range(size_x)] for _ in range(size_y)]

    # copy the old pixel data into the new array
    if pixels is not None:
        for i in range(min(len(pixels), len(new_pixels))):
            for j in range(min(len(pixels[i]), len(new_pixels[i]))):
                new_pixels[i][j] = pixels[i][j]

    # update the pixels variable to refer to the new array
    pixels = new_pixels

    # create a canvas for our pixel grid
    canvas = tk.Canvas(frame, width=size_x*10, height=size_y*10)
    canvas.pack()

    # draw the pixels on the new canvas
    for i in range(size_y):
        for j in range(size_x):
            color = "light gray" if pixels[i][j] else "white"
            canvas.create_rectangle(j*10, i*10, j*10+10, i*10+10, fill=color)

    # bind the mouse click event to handler
    canvas.bind("<Button-1>", lambda event: toggle_pixel(event, pixels, canvas, size_x, size_y, on=True))
    canvas.bind("<B1-Motion>", lambda event: toggle_pixel(event, pixels, canvas, size_x, size_y, on=True ))
    canvas.bind("<ButtonRelease-1>", lambda event: clear_last_pixel())

    # draw grid lines
    for i in range(0, size_x*10, 10):
        canvas.create_line([(i, 0), (i, size_y*10)], fill='light gray')
    for i in range(0, size_y*10, 10):
        canvas.create_line([(0, i), (size_x*10, i)], fill='light gray')

    # resize the window to match the canvas
    window.geometry(f"{size_x*10}x{size_y*10+30}")  # add 30 to the height for the toolbar


def generate_pattern(pixels):
    print(current_size_y)
    # initialize an empty list for our pattern
    pattern = []

    # iterate over each row
    for row in range(current_size_y):
        # start with a knit or purl stitch depending on the row number
        stitch = 'K' if row % 2 == 0 else 'P'
        count = 0
        row_pattern = []  # stores the pattern for the current row

        # iterate over each pixel in the row
        for pixel in pixels[row]:
            # if the pixel matches the current stitch color, increase the count
            if (pixel == 0 and row % 2 == 0 and stitch == 'K') or (pixel == 1 and row % 2 == 0 and stitch == 'P') or \
               (pixel == 0 and row % 2 == 1 and stitch == 'P') or (pixel == 1 and row % 2 == 1 and stitch == 'K'):
                count += 1
            # if the pixel does not match the current stitch color, add the current stitch to the pattern and switch stitches
            else:
                if count > 0:  # only add the stitch if the count is greater than zero
                    row_pattern.append(f"{stitch}{count}")
                stitch = 'K' if stitch == 'P' else 'P'
                count = 1

        # add the final stitch to the pattern
        if count > 0:  # only add the stitch if the count is greater than zero
            row_pattern.append(f"{stitch}{count}")
        
        # append the row pattern to the main pattern, prepending the row number
        pattern.append(f"Row {row + 1}: " + ', '.join(row_pattern))

    # join the pattern into a string
    pattern_str = '\n'.join(pattern)
    # create a new top-level window
    new_window = tk.Toplevel(window)

    # create a text widget
    text = tk.Text(new_window)
    text.pack(fill='both', expand=True)

    # insert the pattern into the text widget
    text.insert('1.0', pattern_str)

    # disable editing of the text widget
    text.config(state='disabled')

    def copy_to_clipboard():
        # enable editing of the text widget
        text.config(state='normal')

        # copy the text to the clipboard
        text_content = text.get("1.0", 'end-1c')
        window.clipboard_clear()
        window.clipboard_append(text_content)

        # disable editing of the text widget
        text.config(state='disabled')

    copy_button = tk.Button(new_window, text="Copy to Clipboard", command=copy_to_clipboard)
    copy_button.pack()


# assign the commands to the buttons
generate_button.config(command=lambda: generate_pattern(pixels))
redraw_button.config(command=lambda: create_canvas(int(spinbox_x.get()), int(spinbox_y.get())))
add_border_button.config(command=lambda: add_border(int(border_size_spinbox.get())))

# create the canvas and pixel data when the window is opened
create_canvas(int(spinbox_x.get()), int(spinbox_y.get()))

# start the Tkinter event loop
window.mainloop()
