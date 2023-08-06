from .remi import REMIEncoding
from .structured import StructuredEncoding
from .midi_like import MIDILikeEncoding
from .cp_word import CPWordEncoding
from .mumidi import MuMIDIEncoding
from .octuple import OctupleEncoding
from .octuple_mono import OctupleMonoEncoding
from .midi_tokenizer_base import MIDITokenizer, get_midi_programs, detect_chords, merge_tracks, \
    merge_same_program_tracks
from .vocabulary import Vocabulary, Event
from .constants import MIDI_INSTRUMENTS, INSTRUMENT_CLASSES, INSTRUMENT_CLASSES_RANGES, CHORD_MAPS, DRUM_SETS,\
    CONTROL_CHANGES
