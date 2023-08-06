from .heat_map import get_heat_map
from .melody_extraction import extract_accompaniment
from .timepoints import get_notes_by_period
import numpy as np

drum_names_to_pitches = {
    'bass_drum': [35, 36],
    'closed_hihat': [42],
    'crash': [49, 57],
    'floor_tom': [41, 43],
    'open_hihat': [46],
    'pedal_hihat': [44],
    'ride': [51, 59],
    'snare': [38, 39, 40],
    'tambourine': [54],
    'tom': [45, 47, 48, 50]
}


def add_instrument_back_pointer(midi_obj):
    for instrument in midi_obj.instruments:
        for note in instrument.notes:
            note.instrument = instrument


def get_heat_maps(midi_obj, n_bins=24, beat_resolution=480, rid_melody=False, is_drum=False, pitches=range(0, 128)):
    add_instrument_back_pointer(midi_obj)
    notes = []
    for instrument in midi_obj.instruments:
        notes += instrument.notes
    if rid_melody:
        notes = extract_accompaniment(notes)
    notes_by_beats = get_notes_by_period(notes, resolution=beat_resolution)

    return np.stack([
        get_heat_map(
            notes=note_set,
            n_bins=n_bins,
            beat_resolution=beat_resolution,
            is_drum=is_drum,
            pitches=pitches
        )
        for note_set in notes_by_beats])


def get_drum_maps(midi_obj, n_bins=96, bar_resolution=1920, drums=None):
    if drums is None:
        drums = ['bass_drum', 'closed_hihat', 'snare']

    return np.stack([get_heat_maps(
        midi_obj=midi_obj,
        n_bins=n_bins,
        beat_resolution=bar_resolution,
        is_drum=True,
        pitches=drum_names_to_pitches[drum]
    ) for drum in drums], axis=1)


def get_dataset(midi_objs, n_bins=24, beat_resolution=480, rid_melody=False, is_drum=False, pitches=range(0, 128)):
    dataset = np.zeros((0, n_bins))
    for midi_obj in midi_objs:
        heat_maps = get_heat_maps(
            midi_obj=midi_obj,
            n_bins=n_bins,
            beat_resolution=beat_resolution,
            rid_melody=rid_melody,
            is_drum=is_drum,
            pitches=pitches)
        dataset = np.concatenate((dataset, heat_maps))

    return dataset


def get_drum_dataset(midi_objs, n_bins=96, drums=None):
    if drums is None:
        drums = ['bass_drum', 'closed_hihat', 'snare']

    dataset = np.zeros((0, len(drums), n_bins))
    for midi_obj in midi_objs:
        time_signatures = midi_obj.time_signature_changes
        if len(time_signatures) > 1:
            continue
        num = time_signatures[0].numerator
        while num % 2 == 0:
            num /= 2
        if num != 1:
            continue

        drum_maps = get_drum_maps(
            midi_obj=midi_obj,
            n_bins=n_bins,
            bar_resolution=midi_obj.ticks_per_beat * 4,
            drums=drums
        )
        dataset = np.concatenate((dataset, drum_maps))

    return dataset
