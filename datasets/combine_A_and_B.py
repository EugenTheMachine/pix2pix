import os
import numpy as np
import cv2
import argparse
from multiprocessing import Pool
from skimage.io import imread, imsave

from multiprocessing import freeze_support


def image_write(path_A, path_B, path_AB):
    im_A = cv2.imread(path_A) # python2: cv2.CV_LOAD_IMAGE_COLOR; python3: cv2.IMREAD_COLOR
    im_B = cv2.imread(path_B) # python2: cv2.CV_LOAD_IMAGE_COLOR; python3: cv2.IMREAD_COLOR
    # im_B = imread(path_B) # python2: cv2.CV_LOAD_IMAGE_COLOR; python3: cv2.IMREAD_COLOR
    # im_B_rgb = np.stack((im_B,)*3, axis=-1)
    im_AB = np.concatenate([im_A, im_B], 1)
    cv2.imwrite(path_AB, im_AB)


parser = argparse.ArgumentParser('create image pairs')
parser.add_argument('--fold_A', dest='fold_A', help='input directory for image A', type=str, default='mydata/A')
parser.add_argument('--fold_B', dest='fold_B', help='input directory for image B', type=str, default='mydata/B')
parser.add_argument('--fold_AB', dest='fold_AB', help='output directory', type=str, default='mydata')
parser.add_argument('--num_imgs', dest='num_imgs', help='number of images', type=int, default=1000000)
parser.add_argument('--use_AB', dest='use_AB', help='if true: (0001_A, 0001_B) to (0001_AB)', action='store_true')
parser.add_argument('--no_multiprocessing', dest='no_multiprocessing', help='If used, chooses single CPU execution instead of parallel execution', action='store_true',default=False)
args = parser.parse_args()

for arg in vars(args):
    print('[%s] = ' % arg, getattr(args, arg))

splits = os.listdir(args.fold_A)

# if not args.no_multiprocessing:
#     # pool=Pool()
#     if __name__ == '__main__':
#         pool = Pool()

if __name__ == '__main__':
    freeze_support()
    if not args.no_multiprocessing:
        pool = Pool()

    for sp in splits:
        img_fold_A = os.path.join(args.fold_A, sp)
        img_fold_B = os.path.join(args.fold_B, sp)
        img_list = os.listdir(img_fold_A)
        if args.use_AB:
            img_list = [img_path for img_path in img_list if '_A.' in img_path]

        num_imgs = min(args.num_imgs, len(img_list))
        print('split = %s, use %d/%d images' % (sp, num_imgs, len(img_list)))
        img_fold_AB = os.path.join(args.fold_AB, sp)
        if not os.path.isdir(img_fold_AB):
            os.makedirs(img_fold_AB)
        print('split = %s, number of images = %d' % (sp, num_imgs))
        for n in range(num_imgs):
            name_A = img_list[n]
            path_A = os.path.join(img_fold_A, name_A)
            if args.use_AB:
                name_B = name_A.replace('_A.', '_B.')
            else:
                name_B = name_A
                name_B = name_B.replace('jpg', 'png')
            path_B = os.path.join(img_fold_B, name_B)
            if os.path.isfile(path_A) and os.path.isfile(path_B):
                # name_AB = name_A
                name_AB = name_B
                if args.use_AB:
                    name_AB = name_AB.replace('_A.', '.')  # remove _A
                path_AB = os.path.join(img_fold_AB, name_AB)
                if not args.no_multiprocessing:
                    pool.apply_async(image_write, args=(path_A, path_B, path_AB))
                else:
                    # im_A = cv2.imread(path_A, 1) # python2: cv2.CV_LOAD_IMAGE_COLOR; python3: cv2.IMREAD_COLOR
                    # im_B = cv2.imread(path_B, 1) # python2: cv2.CV_LOAD_IMAGE_COLOR; python3: cv2.IMREAD_COLOR
                    # im_AB = np.concatenate([im_A, im_B], 1)
                    # cv2.imwrite(path_AB, im_AB)
                    image_write(path_A, path_B, path_AB)


    if not args.no_multiprocessing:
        pool.close()
        pool.join()
