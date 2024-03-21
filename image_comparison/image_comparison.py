import imageio.v3 as iio

from .image_processing import (
    generate_diff,
    image_similarity,
    normalize_image,
    prep_for_write,
    resize_to_match,
)


def compare_images(
    img_path, ref_path, threshold=0.2, fuzz=0.03, diff_path=None, assert_ok=True
):
    """Compare two images and assert their similarity based on
    threshold parameter.

    Additionally generated a diff screenshot based on fuzz parameter
    if diff_path is not None.

    The similarity threshold should be a number 0..1 where 0 is a
    perfect match. The normalized RMSE is used to compute this
    similarity metric, so larger errors (euclidian distance
    between two RGB colors) will have a disproportionately
    larger effect on the score than smaller errors.

    In other words, lots of small errors will lead to a good score
    (closer to 0) whereas a few large errors will lead to a bad score
    (closer to 1).
    """
    img = iio.imread(img_path)
    ref_img = iio.imread(ref_path)

    img = normalize_image(img)
    ref_img = normalize_image(ref_img)

    img = resize_to_match(img, ref_img)

    similar, rmse = image_similarity(img, ref_img, threshold=threshold)

    if not similar and diff_path is not None:
        diff_img = generate_diff(img, ref_img, fuzz=fuzz)

        diff_img = prep_for_write(diff_img)

        iio.imwrite(diff_path, diff_img)

    if assert_ok:
        assert similar, (
            f"image {img_path} failed similarity test"
            f" ({rmse:.3f} >= {threshold:.3f})"
        )
