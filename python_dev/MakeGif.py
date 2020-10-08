import imageio
import pathlib

def make_gif(image_directory, frames_per_second, file_gif, image_type = "png"):
    images = []
    for file_name in image_directory.glob('*.' + image_type):
        images.append(imageio.imread(image_directory.joinpath(file_name)))
    imageio.mimsave(file_gif.as_posix(), images, fps=frames_per_second)

fps = 2
png_dir = pathlib.Path('E:/Download/python/album/')
gif_fin = pathlib.Path('E:/Download/python/final.gif')
make_gif(png_dir, fps, gif_fin)