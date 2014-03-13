
import gtk

import appconsts
import edit
from editorstate import current_sequence
import tlinewidgets
import updater

MAX_DELTA = 100000000
        
edit_data = None
mouse_disabled = True

class MultimoveData:
    """
    This class collects and saves data that enables a "Multi" tool edit to be performed.
    """
    def __init__(self, pressed_track, first_moved_frame, move_all_tracks):
        
        self.first_moved_frame = first_moved_frame
        self.pressed_track_id = pressed_track.id
        self.max_backwards = 0
        self.move_all_tracks = move_all_tracks
        self.trim_blank_indexes = []
        self.track_edit_ops = []
        self.track_affected = []
        self.legal_edit = True
        self._build_move_data()

    def _build_move_data(self):
        # Look at all tracks exept
        tracks = current_sequence().tracks

        # Get per track:
        # - maximum length edit can be done backwards before an overwrite happens
        # - indexes of blanks that are trimmed and/or added/removed, -1 when no blanks are trimmed on that track
        track_max_deltas = []
        trim_blank_indexes = []
        for i in range(1, len(tracks) - 1):
            track = tracks[i]
            if len(track.clips) == 0:
                track_max_deltas.append(MAX_DELTA)
                trim_blank_indexes.append(-1)
                print "empty"
            else:
                clip_index = current_sequence().get_clip_index(track, self.first_moved_frame)
                print "clip_index", clip_index
                # Case: frame after track last clip, no clips are moved
                if clip_index == -1:
                    track_max_deltas.append(MAX_DELTA)
                    trim_blank_indexes.append(-1)
                    continue
                first_frame_clip = track.clips[clip_index]
                # case: frame on clip 
                if not first_frame_clip.is_blanck_clip:
                    # last clip on track, no clips are moved
                    if clip_index == len(track.clips) - 1:
                        print "eeee"
                        track_max_deltas.append(MAX_DELTA)
                        trim_blank_indexes.append(-1)
                    else:
                        # not last clip on track
                        next_clip = track.clips[clip_index + 1]
                        if not next_clip.is_blanck_clip:
                            # first clip to be moved is tight after clip on first move frame
                            track_max_deltas.append(0)
                            trim_blank_indexes.append(clip_index + 1)
                            print "d"
                        else:
                            print "f2"
                            blank_clip_start_frame = track.clip_start(clip_index + 1)
                            moved_clip_start_frame = track.clip_start(clip_index + 2)
                            track_max_deltas.append(moved_clip_start_frame - blank_clip_start_frame)
                            trim_blank_indexes.append(clip_index + 1) 
                # case: frame on blank
                else:
                    print "2"
                    track_max_deltas.append(track.clips[clip_index].clip_length())
                    trim_blank_indexes.append(clip_index)

        self.trim_blank_indexes = trim_blank_indexes

        # Pressed track max delta trim blank index is calculated differently (because on pressed track to the hit clip is moved)
        # and existing values overwritten
        track = tracks[self.pressed_track_id]
        clip_index = current_sequence().get_clip_index(track, self.first_moved_frame)
        first_frame_clip = track.clips[clip_index]
        
        if first_frame_clip.is_blanck_clip:
            self.legal_edit = False
            return

        if clip_index == 0:
            max_d = 0
            trim_index = -1
        else:
            prev_clip = track.clips[clip_index - 1]
            if prev_clip.is_blanck_clip == True:
                max_d = prev_clip.clip_length()
                trim_index = clip_index - 1
            else:
                max_d = 0
                trim_index = clip_index
        
        track_max_deltas[self.pressed_track_id - 1] = max_d
        self.trim_blank_indexes[self.pressed_track_id - 1] = trim_index

        print track_max_deltas
        
        # Smallest track delta is the max number of frames the edit can be done backwards 
        smallest_max_delta = MAX_DELTA
        for i in range(1, len(tracks) - 1):
            d = track_max_deltas[i - 1]
            if d < smallest_max_delta:
                smallest_max_delta = d
        self.max_backwards = smallest_max_delta
        print self.max_backwards
        
        # Track have different ways the edit will need to be applied
        # make a list of those
        track_edit_ops = []
        for i in range(1, len(tracks) - 1):
            track = tracks[i]
            track_delta = track_max_deltas[i - 1]
            if track_delta == 0:
                track_edit_ops.append(appconsts.MULTI_ADD_TRIM)
            elif track_delta == MAX_DELTA:
                track_edit_ops.append(appconsts.MULTI_NOOP)
            elif self.max_backwards > 0 and track_delta == self.max_backwards:
                track_edit_ops.append(appconsts.MULTI_TRIM_REMOVE)
            else:
                track_edit_ops.append(appconsts.MULTI_TRIM)
        self.track_edit_ops = track_edit_ops

        # Make list of boolean values of tracks affected by the edit
        if self.move_all_tracks:
            for i in range(1, len(tracks) - 1):
                self.track_affected.append(True)
        else:
            for i in range(1, len(tracks) - 1):
                self.track_affected.append(False)
            self.track_affected[self.pressed_track_id - 1] = True
                
def mouse_press(event, frame):
    x = event.x
    y = event.y

    global edit_data, mouse_disabled

    # Clear edit data in gui module
    edit_data = None
    mouse_disabled = False
    tlinewidgets.set_edit_mode_data(edit_data)

    # Get pressed track
    track = tlinewidgets.get_track(y)  
    if track == None:
        mouse_disabled = True
        return

    # Get pressed clip index
    clip_index = current_sequence().get_clip_index(track, frame)

    # Selecting empty or blank clip does not define edit
    if clip_index == -1:
        mouse_disabled = True
        return
    pressed_clip = track.clips[clip_index]
    if pressed_clip.is_blanck_clip:
        mouse_disabled = True
        return

    if (event.state & gtk.gdk.CONTROL_MASK):
        move_all = False
    else:
        move_all = True

    first_moved_frame = track.clip_start(clip_index)
    multi_data = MultimoveData(track, first_moved_frame, move_all)
    
    edit_data = {"track_id":track.id,
                 "press_frame":frame,
                 "current_frame":frame,
                 "first_moved_frame":first_moved_frame,
                 "mouse_start_x":x,
                 "mouse_start_y":y,
                 "multi_data":multi_data}

    tlinewidgets.set_edit_mode_data(edit_data)
    updater.repaint_tline()

def mouse_move(x, y, frame, state):
    if mouse_disabled:
        return

    global edit_data
    edit_data["current_frame"] = frame


    updater.repaint_tline()
    
def mouse_release(x, y, frame, state):
    if mouse_disabled:
        return

    global edit_data

    press_frame = edit_data["press_frame"]
    #current_frame = edit_data["current_frame"]
    min_allowed_delta = - edit_data["multi_data"].max_backwards
    #first_moved_frame = edit_data["first_moved_frame"]
    
    delta = frame - press_frame
    if delta < min_allowed_delta:
        delta = min_allowed_delta
    
    if delta != 0:
        data = {"edit_delta":delta,
                "multi_data":edit_data["multi_data"]}
        action = edit.multi_move_action(data)
        action.do_edit()
    
    edit_data = None
    tlinewidgets.set_edit_mode_data(edit_data)
    
    updater.repaint_tline()

