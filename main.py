







import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk, ImageSequence
import io

# Track the animation job
animation_job = None
frames = []

def get_pokemon_data(pokemon_name_or_id):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name_or_id.lower()}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return {
            'name': data['name'].capitalize(),
            'id': data['id'],
            'height': data['height'],
            'weight': data['weight'],
            'types': ', '.join([t['type']['name'] for t in data['types']]),
            'abilities': ', '.join([a['ability']['name'] for a in data['abilities']]),
            'animated_url': f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/{data['id']}.gif"
        }
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def fetch_and_display():
    global animation_job, frames

    pokemon_name_or_id = entry.get()
    if not pokemon_name_or_id:
        messagebox.showwarning("Input Error", "Please enter a Pokémon name or ID.")
        return

    # Cancel previous animation if any
    if animation_job is not None:
        root.after_cancel(animation_job)
        animation_job = None

    result = get_pokemon_data(pokemon_name_or_id)
    if result is None:
        messagebox.showerror("Error", "Pokémon not found.")
        output_label.config(text="")
        sprite_label.config(image='')
        sprite_label.image = None
        return

    output_text = (
        f"Name: {result['name']}\n"
        f"ID: {result['id']}\n"
        f"Height: {result['height']}\n"
        f"Weight: {result['weight']}\n"
        f"Types: {result['types']}\n"
        f"Abilities: {result['abilities']}"
    )
    output_label.config(text=output_text)

    try:
        response = requests.get(result['animated_url'], stream=True)
        response.raise_for_status()
        image = Image.open(io.BytesIO(response.content))

        frames = [ImageTk.PhotoImage(frame.copy().resize((120, 120)))
                  for frame in ImageSequence.Iterator(image)]

        def animate(counter=0):
            global animation_job
            sprite_label.config(image=frames[counter])
            sprite_label.image = frames[counter]
            animation_job = root.after(100, animate, (counter + 1) % len(frames))

        animate()

    except Exception as e:
        print(f"Failed to load animated sprite: {e}")
        sprite_label.config(image='')
        sprite_label.image = None

# GUI setup
root = tk.Tk()
root.title("Pokémon Data Fetcher")

label = tk.Label(root, text="Enter Pokémon name or ID:")
label.pack(pady=5)

entry = tk.Entry(root)
entry.pack(pady=5)

button = tk.Button(root, text="Fetch Data", command=fetch_and_display)
button.pack(pady=5)

output_label = tk.Label(root, text="", justify=tk.LEFT, font=("Arial", 12))
output_label.pack(pady=10)

sprite_label = tk.Label(root)
sprite_label.pack(pady=5)

root.mainloop()
