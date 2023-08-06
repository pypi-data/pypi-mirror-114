import os
import argparse
import nibabel as nib
from nilearn.image import resample_to_img
import numpy as np
from SubBrainSegment.unet3d.training import load_old_model
from SubBrainSegment.unet3d.prediction import run_validation_cases, Run_validation_case
from SubBrainSegment.unet3d.utils.utils import  read_image
from distutils.util import strtobool


config = dict()
config["image_shape"] = (128, 128, 128)  # This determines what shape the images will be cropped/resampled to.
config["labels"] = (2,3,4,5,7,8,10,11,12,13,14,15,16,17,18,24,26,28,30,31,41,42,43,44,46,47,49,50,51,52,53,54,58,60,62,63,77,85,251,252,253,254,255)
config["training_modalities"] = [""]  # set for the data
print("hhhhhh")
# def parse_args():
#     parser = argparse.ArgumentParser()
#
#     parser.add_argument('-i', '--i', default='CANDI_HC_001.nii.gz', required=True, type=str, help='The name of the input data')
#     parser.add_argument('-o', '--o', default="{subject}.nii.gz", required=True, type=str, help='The name of the output data')
#     parser.add_argument('-model', '--model', default='raw_nu_NKI_freesurfer', type=str, help='The name of the model')
#     parser.add_argument("--prediction_dir", default="./predict/freesurfer/OASIS/test", required=True, )
#     parser.add_argument('-permute', '--permute', default='False', type = strtobool, help='enable permute or not')
#
#
#     return parser.parse_args()


def main():
    print("hello")
    return 3



    # kwargs = vars(parse_args())
    # args = parse_args()
    # WORKING_PATH = os.getcwd()
    # DATA = 'data'
    # MODEL = 'model'
    # prediction_dir = args.prediction_dir
    # output_label_map = True
    # config['model_file'] =  os.path.join(WORKING_PATH,MODEL,args.model + '_unet_model.h5')
    # config["permute"] = bool(args.permute)
    #
    #
    # data_file = os.path.join(os.getcwd(),args.i)
    # single_file = read_image(data_file, image_shape=(128,128,128), crop=False, interpolation='linear')
    # model = load_old_model(config["model_file"])
    # Run_validation_case(output_dir=prediction_dir,
    #                     model=model,
    #                     data_file=single_file,
    #                     training_modalities=config["training_modalities"],
    #                     output_label_map=output_label_map,
    #                     labels=config["labels"],
    #                     threshold=0.5,
    #                     overlap=16,
    #                     permute=False,
    #                     output_basename=args.o,
    #                     test=False)
    # prediction_filename = os.path.join(os.path.join(prediction_dir,args.o))
    # ref = nib.load(data_file)
    # pred = nib.load(prediction_filename)
    # pred_resampled = resample_to_img(pred, ref, interpolation="nearest")
    # label = pred_resampled.get_fdata()
    # nib.save(nib.Nifti1Image(label.astype(np.uint8),pred_resampled.affine),prediction_filename)



if __name__ == "__main__":
    print('called as script')
    main()
