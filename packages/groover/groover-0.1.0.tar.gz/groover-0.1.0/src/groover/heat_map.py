import numpy as np


def pitch_weight(pitch):
    return -pitch / 128 + 1


def velocity_weight(velocity):
    return velocity / 128


def notes_weight(notes):
    pitches = np.array([note.pitch for note in notes])
    velocities = np.array([note.velocity for note in notes])

    return pitch_weight(pitches) + velocity_weight(velocities)


def get_heat_map(notes, n_bins=24, beat_resolution=480, is_drum=False, pitches=range(0, 128)):
    bin_resolution = np.ceil(beat_resolution / n_bins).astype(int)
    notes = [note for note in notes if note.pitch in pitches and note.instrument.is_drum == is_drum]
    heat_map = np.zeros(n_bins)
    weights = notes_weight(notes)
    if is_drum:
        weights = np.clip(np.ceil(weights), 0., 1.)
    for note, weight in zip(notes, weights):
        heat_map[(note.start % beat_resolution) // bin_resolution] += weight

    return heat_map
