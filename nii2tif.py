import os
import nibabel as nib
from PIL import Image, ImageEnhance

def save_nifti_slices_with_contrast(nii_file, output_dir, slice_direction, contrast_factor, format='tif'):
    # Load the NIfTI file
    img = nib.load(nii_file)
    # Reorient the image to RAS orientation
    img_reoriented = nib.as_closest_canonical(img)
    data = img_reoriented.get_fdata()

    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Determine the number of slices based on the direction
    if slice_direction == 'sagittal':
        num_slices = data.shape[0]
        slice_data = lambda i: data[i, :, :]
    elif slice_direction == 'coronal':
        num_slices = data.shape[1]
        slice_data = lambda i: data[:, i, :]
    elif slice_direction == 'axial':
        num_slices = data.shape[2]
        slice_data = lambda i: data[:, :, i]
    else:
        raise ValueError("Invalid slice direction. Choose from 'sagittal', 'coronal', or 'axial'.")

    # Loop through each slice, enhance contrast, and save
    for i in range(num_slices):
        slice = slice_data(i)
        image = Image.fromarray(slice)

        # Convert to uint8 (if necessary)
        if image.mode != 'L':
            image = image.convert('L')

        # Enhance contrast
        enhancer = ImageEnhance.Contrast(image)
        enhanced_image = enhancer.enhance(contrast_factor)

        enhanced_image = enhanced_image.rotate(90, expand=True)

        enhanced_image.save(os.path.join(output_dir, f'{slice_direction}_slice_{i:03d}.{format}'))

if __name__ == '__main__':
    # Example usage
    nii_file = 'LNM_0263_0001.nii'
    output_dir = 'saggital_slices'
    slice_direction = 'coronal'  # Change to 'coronal' or 'axial' as needed
    save_nifti_slices_with_contrast(nii_file, output_dir, slice_direction, 0.5)
