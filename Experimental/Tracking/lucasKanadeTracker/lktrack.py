import cv2 as cv
import numpy as np

lk_params = dict(winSize=(15, 15), maxLevel=2,
                 criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))

subpix_params = dict(zeroZone=(-1, -1), winSize=(10, 10),
                     criteria=(cv.TERM_CRITERIA_COUNT | cv.TERM_CRITERIA_EPS, 20, 0.03))

feature_params = dict(maxCorners=500, qualityLevel=0.01, minDistance=10)


class LKTracker(object):
    def __init__(self, imnames):
        self.imnames = imnames
        self.features = []
        self.tracks = []
        self.current_frame = 0

    def detect_points(self):
        self.image = cv.imread(self.imnames[self.current_frame])
        self.gray = cv.cvtColor(self.image, cv.COLOR_BGR2GRAY)

        features = cv.goodFeaturesToTrack(self.gray, **feature_params)

        cv.cornerSubPix(self.gray, features, **subpix_params)

        self.features = features
        self.tracks = [[p] for p in features.reshape((-1, 2))]

        self.pre_gray = self.gray

    def track_points(self):
        if self.features != []:
            self.step()

            self.image = cv.imread(self.imnames[self.current_frame])
            self.gray = cv.cvtColor(self.image, cv.COLOR_BGR2GRAY)

            tmp = np.float32(self.features).reshape(-1, 1, 2)

            features, status, track_error = cv.calcOpticalFlowPyrLK(self.pre_gray,
                                                                    self.gray, tmp, None, **lk_params)

            self.features = [p for (st, p) in zip(status, features) if st]

            features = np.array(features).reshape((-1, 2))
            for i, f in enumerate(features):
                self.tracks[i].append(f)

            ndx = [i for (i, st) in enumerate(status) if not st]
            ndx.reverse()
            for i in ndx:
                self.tracks.pop(i)

            self.prev_gray = self.gray

    def step(self, framebr=None):
        if framebr is None:
            self.current_frame = (self.current_frame + 1) % len(self.imnames)
        else:
            self.current_frame = framebr % len(self.imnames)

    def draw(self):
        for point in self.features:
            cv.circle(self.image, (int(point[0][0]), int(point[0][1])), 3, (0, 255, 0), -1)

        cv.imshow('LKtrack', self.image)
        cv.waitKey()

    def track(self):
        for i in range(len(self.imnames)):
            if self.features == []:
                self.detect_points()
            else:
                self.track_points()

        f = np.array(self.features).reshape(-1, 2)
        im = cv.cvtColor(self.image, cv.COLOR_BGR2RGB)
        yield im, f
