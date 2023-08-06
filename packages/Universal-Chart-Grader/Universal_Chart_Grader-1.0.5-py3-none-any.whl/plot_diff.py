import numpy as np
from PIL import Image


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Display the two input figures and the difference images side by side')
    parser.add_argument('img1', type=str)
    parser.add_argument('img2', type=str)
    parser.add_argument('--out_file', type=str)
    args = parser.parse_args()

    img1 = np.array(Image.open(args.img1).convert('L'))
    img2 = np.array(Image.open(args.img2).convert('L'))
    img_diff = img2 - img1
    img_concatenated = Image.fromarray(np.hstack([img1, img2, img_diff]))
    img_concatenated.show()


if __name__ == '__main__':
    main()
