import numpy as np
from miditoolkit.midi import containers
from .data import get_heat_maps, get_drum_maps
from .metrics import rhythm_similarity
from .timepoints import get_rhythm_markers_by_beat


class RhythmKMeans:
    def __init__(self, cluster_centers=None):
        if cluster_centers is None:
            self.cluster_centers_ = np.zeros((0, 24))
        else:
            if type(cluster_centers) != np.ndarray:
                raise TypeError("K-means cluster centers has to be in the form of numpy.ndarray")
            elif len(cluster_centers.shape) != 2:
                raise AssertionError("K-means cluster centers has to be a 2D array")
            elif cluster_centers.shape[1] != 24:
                raise AssertionError("K-means cluster centers has to have 24 columns")
            self.cluster_centers_ = cluster_centers.copy()

    def fit(self, dataset, k, max_iter=1000, epsilon=1e-6):
        N, n_features = dataset.shape
        if n_features != 24:
            raise AssertionError("dataset has to have 24 columns")
        elif N < k:
            raise AssertionError("")
        init_indices = np.random.choice(N, size=k, replace=False)
        cluster_centers = dataset[init_indices]
        for i in range(max_iter):
            new_centers = cluster_centers.copy()
            n_points = np.ones((k, 1))

            for data in dataset:
                cluster = np.argmax(rhythm_similarity(data, cluster_centers))
                new_centers[cluster] += data
                n_points[cluster, 0] += 1

            new_centers = new_centers / n_points

            if np.mean(rhythm_similarity(new_centers, cluster_centers)) > 1 - epsilon:
                self.cluster_centers_ = new_centers
                return
            else:
                cluster_centers = new_centers

        self.cluster_centers_ = cluster_centers
        return

    def load_cluster_centers(self, cluster_centers):
        if type(cluster_centers) != np.ndarray:
            raise TypeError("K-means cluster centers has to be in the form of numpy.ndarray")
        elif len(cluster_centers.shape) != 2:
            raise AssertionError("K-means cluster centers has to be a 2D array")
        elif cluster_centers.shape[1] != 24:
            raise AssertionError("K-means cluster centers has to have 24 columns")
        self.cluster_centers_ = cluster_centers.copy()

    def k(self):
        return self.cluster_centers_.shape[0]

    def is_empty(self):
        return self.k() == 0

    def add_beat_clusters(self, midi_obj, beat_resolution=480, preprocessing='default', pitches=range(0, 128)):
        if self.is_empty():
            raise AssertionError('K-means classifier is empty. Use fit() to generate cluster centers')

        heat_maps = get_heat_maps(midi_obj, beat_resolution=beat_resolution, pitches=pitches)
        if preprocessing == 'binary':
            heat_maps = np.clip(np.ceil(heat_maps), 0., 1.)
        elif preprocessing == 'quantized':
            bins = [0, 0.5, 1.5, 2.5, 4, 5.5, 6.5, 8.5, 11]
            for i, l, r in zip(range(len(bins)), bins[:-1], bins[1:]):
                heat_maps[(heat_maps >= l) & (heat_maps < r)] = i

        for beat, heat_map in enumerate(heat_maps):
            rhythm_type = np.argmax(rhythm_similarity(heat_map, self.cluster_centers_))
            marker = containers.Marker(text=f'{preprocessing} rhythm {int(rhythm_type)}',
                                       time=beat * beat_resolution)
            midi_obj.markers.append(marker)

    def get_rhythm_scores(self, midi_obj, beat_resolution=480, pitches=range(0, 128)):
        if self.is_empty():
            raise AssertionError('K-means classifier is empty. Use fit() to generate cluster centers')

        heat_maps = get_heat_maps(midi_obj, beat_resolution=beat_resolution, pitches=pitches)
        types = np.zeros(heat_maps.shape[0])
        centers_by_beats = np.zeros((heat_maps.shape[0], 24))

        rhythm_markers_by_beat = get_rhythm_markers_by_beat(midi_obj, heat_maps.shape[0], resolution=beat_resolution)
        for i, marker in enumerate(rhythm_markers_by_beat):
            if marker is None:
                continue
            rhythm_type = int(marker.text.split(' ')[1])
            types[i] = rhythm_type
            try:
                centers_by_beats[i] = self.cluster_centers_[rhythm_type]
            except IndexError:
                pass

        return types.astype(int), rhythm_similarity(heat_maps, centers_by_beats)


class DrumRawClassifier:
    def __init__(self):
        self.rhythms = np.zeros((0, 96))

    def fit(self, dataset, k=64, indices=None, quantize=True):
        dataset_temp = dataset.copy()

        if indices is None:
            indices = np.arange(dataset_temp.shape[1])

        if quantize:
            for i in np.arange(16):
                dataset_temp[:, :, (i * 6 + 1):(i * 6 + 6)] = 0

        rhythm_count = dict()
        for data in dataset_temp[:, indices].reshape(dataset_temp.shape[0], len(indices) * dataset_temp.shape[2]):
            rhythm_tuple = tuple(data)
            if rhythm_tuple in rhythm_count.keys():
                rhythm_count[rhythm_tuple] += 1
            else:
                rhythm_count[rhythm_tuple] = 1

        pairs = sorted(list(rhythm_count.items()), key=lambda x: -x[1])
        self.rhythms = np.array([pair[0] for pair in pairs])[:k]

    def add_bar_class(self, midi_obj, bar_resolution=1920, indices=None):
        drum_maps = get_drum_maps(midi_obj, bar_resolution=bar_resolution)
        if indices is None:
            indices = np.arange(drum_maps.shape[1])

        for bar, drum_map in enumerate(drum_maps.reshape(drum_maps.shape[0], len(indices) * drum_maps.shape[2])):
            rhythm_type = np.argmax(rhythm_similarity(drum_map, self.rhythms))
            marker = containers.Marker(text=f'drum rhythm {int(rhythm_type)}',
                                       time=bar * bar_resolution)
            midi_obj.markers.append(marker)
