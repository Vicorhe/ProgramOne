from lucasKanadeTracker import lktrack
from matplotlib import pyplot as plt

imnames = ['/Users/victorhe/Desktop/f_1.png',
           '/Users/victorhe/Desktop/f_2.png',
           '/Users/victorhe/Desktop/f_3.png',
           '/Users/victorhe/Desktop/f_4.png',
           '/Users/victorhe/Desktop/f_5.png',
           '/Users/victorhe/Desktop/f_6.png']

lkt = lktrack.LKTracker(imnames)

for im, ft in lkt.track():
    print('tracking %d features' % len(ft))

    plt.figure()
    plt.imshow(im)
    for p in ft:
        plt.plot(p[0], p[1], 'bo')
    for t in lkt.tracks:
        plt.plot([p[0] for p in t], [p[1] for p in t])
    plt.axis('off')
    plt.show()
