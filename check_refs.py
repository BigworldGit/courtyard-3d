import cv2, os

ref_dir = '/Users/roy/Documents/workspace/courtyard_3d/ref_images'
for f in sorted(os.listdir(ref_dir)):
    if f.endswith('.jpg'):
        p = os.path.join(ref_dir, f)
        im = cv2.imread(p)
        if im is not None:
            print(f, im.shape)
