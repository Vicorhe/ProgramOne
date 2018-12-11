import cv2 as cv
from matplotlib import pyplot as plt


def plot_image_set(image_set):
    set_size = len(image_set)
    for i, image in enumerate(image_set):
        rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)

        plt.subplot(set_size, 2, 2*i+1), plt.imshow(rgb)
        plt.title('img_' + str(i + 1)), plt.xticks([]), plt.yticks([])

        plt.subplot(set_size, 2, 2*i+2), plot_rgb_histogram(rgb)
        plt.title('hist_' + str(i + 1)), plt.xticks([]), plt.yticks([])

    plt.show()


def plot_rgb_histogram(image):
    color = ('r', 'g', 'b')
    for i, col in enumerate(color):
        histr = cv.calcHist([image], [i], None, [256], [0, 256])
        plt.plot(histr, color=col)
        plt.xlim([0, 256])


# iphone
'''
gal_1 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/iphone/glareAllLine/gal4/gample_1.jpeg')
gal_2 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/iphone/glareAllLine/gal4/gample_2.jpeg')
gal_3 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/iphone/glareAllLine/gal4/gample_3.jpeg')
gal_4 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/iphone/glareAllLine/gal4/gample_4.jpeg')
gal = [gal_1, gal_2, gal_3, gal_4]

gf1_1 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/iphone/glareFloor/gf1/gample_1.jpeg')
gf1_2 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/iphone/glareFloor/gf1/gample_2.jpeg')
gf1 = [gf1_1, gf1_2]

gf2_1 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/iphone/glareFloor/gf2/gample_1.jpeg')
gf2_2 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/iphone/glareFloor/gf2/gample_2.jpeg')
gf2_3 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/iphone/glareFloor/gf2/gample_3.jpeg')
gf2 = [gf2_1, gf2_2, gf2_3]


gf3_1 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/iphone/glareFloor/gf3/gample_2.jpeg')
gf3_2 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/iphone/glareFloor/gf3/gample_3.jpeg')
gf3 = [gf3_1, gf3_2]


ngf1_1 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/iphone/noGlareFloor/ngf1/gample_1.jpeg')
ngf1_2 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/iphone/noGlareFloor/ngf1/gample_2.jpeg')
ngf1 = [ngf1_1, ngf1_2]


ngf2_1 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/iphone/noGlareFloor/ngf2/gample_1.jpeg')
ngf2_2 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/iphone/noGlareFloor/ngf2/gample_2.jpeg')
ngf2_3 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/iphone/noGlareFloor/ngf2/gample_3.jpeg')
ngf2 = [ngf2_1, ngf2_2, ngf2_3]


ngf3_2 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/iphone/noGlareFloor/ngf3/gample_2.jpeg')
ngf3_3 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/iphone/noGlareFloor/ngf3/gample_3.jpeg')
ngf3 = [ngf3_2, ngf3_3]


a1_1 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/iphone/other/a/a1/fample_1.jpeg')
a1_2 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/iphone/other/a/a1/fample_2.jpeg')
a1 = [a1_1, a1_2]


b1_2 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/iphone/other/b/b1/sample_2.jpeg')
b1_3 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/iphone/other/b/b1/sample_3.jpeg')
b1_4 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/iphone/other/b/b1/sample_4.jpeg')
b1 = [b1_2, b1_2, b1_4]


b2_2 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/iphone/other/b/b2/sample_2.jpeg')
b2_3 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/iphone/other/b/b2/sample_3.jpeg')
b2_4 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/iphone/other/b/b2/sample_4.jpeg')
b2 = [b2_2, b2_2, b2_4]


c4_3 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/iphone/other/c/c4/sample_3.jpeg')
c4_4 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/iphone/other/c/c4/sample_4.jpeg')
c4 = [c4_3, c4_4]


d4_1 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/iphone/other/d/d4/sample_1.jpeg')
d4_2 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/iphone/other/d/d4/sample_2.jpeg')
d4_3 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/iphone/other/d/d4/sample_3.jpeg')
d4_4 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/iphone/other/d/d4/sample_4.jpeg')
d4 = [d4_1, d4_2, d4_3, d4_4]


e3_1 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/iphone/other/e/e3/sample_1.jpeg')
e3_2 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/iphone/other/e/e3/sample_2.jpeg')
e3_3 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/iphone/other/e/e3/sample_3.jpeg')
e3 = [e3_1, e3_2, e3_3]


t1a_1 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/iphone/soloTemplates/t1a/sample_1.jpeg')
t1a_2 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/iphone/soloTemplates/t1a/sample_2.jpeg')
t1a = [t1a_1, t1a_2]


t2a_1 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/iphone/soloTemplates/t2a/sample_1.jpeg')
t2a_2 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/iphone/soloTemplates/t2a/sample_2.jpeg')
t2a_3 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/iphone/soloTemplates/t2a/sample_3.jpeg')
t2a = [t2a_1, t2a_2, t2a_3]


t3b_2 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/iphone/soloTemplates/t3b/sample_2.jpeg')
t3b_3 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/iphone/soloTemplates/t3b/sample_3.jpeg')
t3b_4 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/iphone/soloTemplates/t3b/sample_4.jpeg')
t3b = [t3b_2, t3b_3, t3b_4]


v1_1 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/iphone/video2/sample1a.png')
v1_2 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/iphone/video2/sample1b.png')
v1_3 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/iphone/video2/sample1c.png')
v1_4 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/iphone/video2/sample1d.png')
v2_1 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/iphone/video2/sample2a.png')
v2_2 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/iphone/video2/sample2b.png')
v2_3 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/iphone/video2/sample2c.png')
v2_4 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/iphone/video2/sample2d.png')
v4_1 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/iphone/video2/sample4a.png')
v4_2 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/iphone/video2/sample4b.png')
v4_3 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/iphone/video2/sample4c.png')

v1 = [v1_1, v1_2, v1_3, v1_4]
v2 = [v2_1, v2_2, v2_3, v2_4]
v4 = [v4_1, v4_2, v4_3]

v = [v1_1, v1_2, v1_3, v1_4, v2_1, v2_2, v2_3, v2_4, v4_1, v4_2, v4_3]
'''


# oneplus
'''
t1_1 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/oneplus/templates1/sample_1.jpeg')
t1_2 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/oneplus/templates1/sample_2.jpeg')
t1_3 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/oneplus/templates1/sample_3.jpeg')
t1_4 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/oneplus/templates1/sample_4.jpeg')
t1 = [t1_1, t1_2, t1_3, t1_4]


t2_1 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/oneplus/templates2/sample_1.jpeg')
t2_2 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/oneplus/templates2/sample_2.jpeg')
t2_3 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/oneplus/templates2/sample_3.jpeg')
t2_4 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/oneplus/templates2/sample_4.jpeg')
t2 = [t2_1, t2_2, t2_3, t2_4]


t3_1 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/oneplus/templates3/sample_1.jpeg')
t3_2 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/oneplus/templates3/sample_2.jpeg')
t3_3 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/oneplus/templates3/sample_3.jpeg')
t3_4 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/oneplus/templates3/sample_4.jpeg')
t3 = [t3_1, t3_2, t3_3, t3_4]
'''


# partnerPhone1
'''
l1_3 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/partnerPhone1/line1/sample_3.jpg')
l1_4 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/partnerPhone1/line1/sample_4.jpg')
l1 = [l1_3, l1_4]


l2_2 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/partnerPhone1/line2/sample_2.jpg')
l2_3 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/partnerPhone1/line2/sample_3.jpg')
l2_4 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/partnerPhone1/line2/sample_4.jpg')
l2 = [l2_2, l2_3, l2_4]


l3af_1 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/partnerPhone1/line3/all4/sample_1.jpg')
l3af_2 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/partnerPhone1/line3/all4/sample_2.jpg')
l3af_3 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/partnerPhone1/line3/all4/sample_3.jpg')
l3af_4 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/partnerPhone1/line3/all4/sample_4.jpg')
l3af = [l3af_1, l3af_2, l3af_3, l3af_4]


l3l3_2 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/partnerPhone1/line3/last3/sample_1.jpg')
l3l3_3 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/partnerPhone1/line3/last3/sample_2.jpg')
l3l3_4 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/partnerPhone1/line3/last3/sample_3.jpg')
l3l3 = [l3l3_2, l3l3_3, l3af_4]


l4_1 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/partnerPhone1/line4/sample_1.jpg')
l4_2 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/partnerPhone1/line4/sample_2.jpg')
l4 = [l4_1, l4_2]


vl1_1 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/partnerPhone1/video2/l_1_a.png')
vl1_2 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/partnerPhone1/video2/l_1_b.png')
vl1_3 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/partnerPhone1/video2/l_1_c.png')
vl1_4 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/partnerPhone1/video2/l_1_d.png')
vl1 = [vl1_1, vl1_2, vl1_3, vl1_4]


vl2_1 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/partnerPhone1/video2/l_2_a.png')
vl2_2 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/partnerPhone1/video2/l_2_b.png')
vl2_3 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/partnerPhone1/video2/l_2_c.png')
vl2_4 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/partnerPhone1/video2/l_2_d.png')
vl2 = [vl2_1, vl2_2, vl2_3, vl2_4]


vl4_1 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/partnerPhone1/video2/l_4_a.png')
vl4_2 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/partnerPhone1/video2/l_4_b.png')
vl4 = [vl4_1, vl4_2]

vl = vl1 + vl2 + vl4
'''


# partnerPhone2

f1_1 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/partnerPhone2/floor1/fample_1.jpg')
f1_2 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/partnerPhone2/floor1/fample_2.jpg')
f1 = [f1_1, f1_2]

f2_1 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/partnerPhone2/floor2/fample_1.jpg')
f2_2 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/partnerPhone2/floor2/fample_2.jpg')
f2_3 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/partnerPhone2/floor2/fample_3.jpg')
f2 = [f2_1, f2_2, f2_3]

f3_2 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/partnerPhone2/floor3/fample_2.jpg')
f3_3 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/partnerPhone2/floor3/fample_3.jpg')
f3 = [f3_2, f3_3]

fh1_1 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/partnerPhone2/floorhigh1/fample_1.jpg')
fh1_2 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/partnerPhone2/floorhigh1/fample_2.jpg')
fh1 = [fh1_1, fh1_2]

fh2_1 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/partnerPhone2/floorhigh2/fample_1.jpg')
fh2_2 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/partnerPhone2/floorhigh2/fample_2.jpg')
fh2_3 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/partnerPhone2/floorhigh2/fample_3.jpg')
fh2 = [fh2_1, fh2_2, fh2_3]

fh3_2 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/partnerPhone2/floorhigh3/fample_2.jpg')
fh3_3 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/partnerPhone2/floorhigh3/fample_3.jpg')
fh3 = [fh3_2, fh3_3]

fl1_1 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/partnerPhone2/floorlow1/fample_1.jpg')
fl1_2 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/partnerPhone2/floorlow1/fample_2.jpg')
fl1 = [fl1_1, fl1_2]

fl2_2 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/partnerPhone2/floorlow2/fample_2.jpg')
fl2_3 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/partnerPhone2/floorlow2/fample_3.jpg')
fl2 = [fl2_2, fl2_3]

ll1_1 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/partnerPhone2/line1/sample_1.jpg')
ll1_2 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/partnerPhone2/line1/sample_2.jpg')
ll1 = [ll1_1, ll1_2]

ll2_2 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/partnerPhone2/line2/sample_2.jpg')
ll2_3 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/partnerPhone2/line2/sample_3.jpg')
ll2 = [ll2_2, ll2_3]

ll3_3 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/partnerPhone2/line3/sample_3.jpg')
ll3_4 = cv.imread('/Users/victorhe/Pictures/factorySampleCollection/partnerPhone2/line3/sample_4.jpg')
ll3 = [ll3_3, ll3_4]


plot_image_set(ll1)
plot_image_set(ll2)
plot_image_set(ll3)
