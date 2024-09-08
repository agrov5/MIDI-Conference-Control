import mido
import pyautogui as pg


toggle_mute_keys = {'keys': [96, 94], 'hotkey': []} # 'C6': 96, 'B6b': 94
toggle_video_keys = {'keys': [95, 94], 'hotkey': []} # 'B6': 95, 'B6b': 94

pressed_keys = set()

    
def confrence_platform():
    platform = input('Zoom or GMeet?').strip().lower()
    
    if platform == 'zoom':
        toggle_mute_keys['hotkey'] = ['alt', 'a']
        toggle_video_keys['hotkey'] = ['alt', 'v']
        print('Keys: ', toggle_mute_keys['hotkey'], toggle_video_keys['hotkey'])
        
    elif platform == 'gmeet':
        toggle_mute_keys['hotkey'] = ['ctrl', 'd']
        toggle_video_keys['hotkey'] = ['ctrl', 'e']
        print('Keys: ', toggle_mute_keys['hotkey'], toggle_video_keys['hotkey'])
        
    else:
        print('Invalid platform! Please enter either Zoom or GMeet')
        confrence_platform()

def handle_midi_message(message):
    if message.type == 'note_on' and message.velocity > 0:
        
        pressed_keys.add(message.note)
    elif message.type == 'note_off' or (message.type == 'note_on' and message.velocity == 0):
        
        pressed_keys.discard(message.note)

 
    if toggle_mute_keys['keys'][0] in pressed_keys and toggle_mute_keys['keys'][1] in pressed_keys:
        print("Mute toggle keys pressed!")
        pg.hotkey(*toggle_mute_keys['hotkey'])

    # Check if toggle_video_keys are pressed together
    if toggle_video_keys['keys'][0] in pressed_keys and toggle_video_keys['keys'][1] in pressed_keys:
        print("Video toggle keys pressed!")
        pg.hotkey(*toggle_video_keys['hotkey'])


# Open MIDI input and listen for messages
port_name = mido.get_input_names()[0]
confrence_platform()
with mido.open_input(port_name) as inport:
    print("Listening for MIDI input on", port_name)
    
    for message in inport:
        handle_midi_message(message)

