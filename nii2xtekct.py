import nibabel as nib

file_path = 'LNM_0263_0001.nii'
img = nib.load(file_path)
header = img.header

DetectorPixelsX = header.get_data_shape()[0]
DetectorPixelsY = header.get_data_shape()[1]
DetectorPixelSizeX = header.get_zooms()[0]
DetectorPixelSizeY = header.get_zooms()[1]
SrcToObject = header.get_sform()[0, 3]
SrcToDetector = header.get_sform()[1, 3]
MaskRadius = None  # You would need specific information about this from the dataset
VoxelsX = header.get_data_shape()[0]
VoxelsY = header.get_data_shape()[1]
VoxelsZ = header.get_data_shape()[2]
VoxelSizeX = header.get_zooms()[0]
VoxelSizeY = header.get_zooms()[1]
VoxelSizeZ = header.get_zooms()[2]

img = nib.load(file_path)
img_reoriented = nib.as_closest_canonical(img)
data = img_reoriented.get_fdata()
Projections = data.shape[0] # 0 saggital and 1 coronal

print("DetectorPixelsX:", DetectorPixelsX)
print("DetectorPixelsY:", DetectorPixelsY)
print("DetectorPixelSizeX:", DetectorPixelSizeX)
print("DetectorPixelSizeY:", DetectorPixelSizeY)
print("SrcToObject:", SrcToObject)
print("SrcToDetector:", SrcToDetector)
print("MaskRadius:", MaskRadius)
print("Projections:", Projections)
print("VoxelsX:", VoxelsX)
print("VoxelsY:", VoxelsY)
print("VoxelsZ:", VoxelsZ)
print("VoxelSizeX:", VoxelSizeX)
print("VoxelSizeY:", VoxelSizeY)
print("VoxelSizeZ:", VoxelSizeZ)
