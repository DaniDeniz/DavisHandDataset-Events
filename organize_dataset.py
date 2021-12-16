import os
import shutil
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def unsplit_dataset(path, dest_path):
    for split in os.listdir(path):
        for object in os.listdir(os.path.join(path, split)):
            for action in os.listdir(os.path.join(path, split, object)):
                for file in os.listdir(os.path.join(path, split, object, action)):
                    os.makedirs(os.path.join(dest_path, object, action), exist_ok=True)
                    shutil.copy(os.path.join(path, split, object, action, file),
                                os.path.join(dest_path, object, action, file))
    
    
def split_dataset_train_val_test(dataset_path, train=0.7, val=0.15):
    import random
    import math
    new_folder_name = "all_{}".format(os.path.basename(dataset_path))
    dest_dir = os.path.join(os.path.dirname(dataset_path), new_folder_name)
    for item in os.listdir(dataset_path):
        for actions in os.listdir(os.path.join(dataset_path, item)):
            segments_list = []
            for individual_segment in os.listdir(os.path.join(dataset_path, item, actions)):
                segments_list.append((item, actions, individual_segment))
            random.shuffle(segments_list)
            segments_list_len = len(segments_list)
            os.makedirs(os.path.join(dest_dir, "train", item, actions))
            os.makedirs(os.path.join(dest_dir, "validation", item, actions))
            os.makedirs(os.path.join(dest_dir, "test", item, actions))
            [shutil.copy(os.path.join(dataset_path, segment[0], segment[1], segment[2]),
                         os.path.join(dest_dir, "train", segment[0], segment[1], segment[2]))
             for segment in segments_list[:math.floor(segments_list_len*train)]]

            [shutil.copy(os.path.join(dataset_path, segment[0], segment[1], segment[2]),
                         os.path.join(dest_dir, "validation", segment[0], segment[1], segment[2]))
             for segment in segments_list[math.floor(segments_list_len * train):math.floor(segments_list_len * (train + val))]]

            [shutil.copy(os.path.join(dataset_path, segment[0], segment[1], segment[2]),
                         os.path.join(dest_dir, "test", segment[0], segment[1], segment[2]))
             for segment in segments_list[math.floor(segments_list_len * (train + val)):]]
    
    
def split_dataset_train_val_test_author(dataset_path, train=0.85, author="s1"):
    import random
    import math
    folder_name = os.path.basename(dataset_path)
    new_folder_name = "{}_{}".format(author, folder_name)
    dest_dir = os.path.join(os.path.dirname(dataset_path), new_folder_name)
    for item in os.listdir(dataset_path):
        for actions in os.listdir(os.path.join(dataset_path, item)):
            segments_list = []
            for individual_segment in os.listdir(os.path.join(dataset_path, item, actions)):
                segments_list.append((item, actions, individual_segment))
            test_list = [s for s in segments_list if author in s[-1]]
            train_val_list = [s for s in segments_list if author not in s[-1]]
            random.shuffle(train_val_list)
            train_val_list_len = len(train_val_list)
            os.makedirs(os.path.join(dest_dir, "train", item, actions))
            os.makedirs(os.path.join(dest_dir, "validation", item, actions))
            os.makedirs(os.path.join(dest_dir, "test", item, actions))
            [shutil.copy(os.path.join(dataset_path, segment[0], segment[1], segment[2]),
                         os.path.join(dest_dir, "train", segment[0], segment[1], segment[2]))
             for segment in train_val_list[:math.floor(train_val_list_len*train)]]

            [shutil.copy(os.path.join(dataset_path, segment[0], segment[1], segment[2]),
                         os.path.join(dest_dir, "validation", segment[0], segment[1], segment[2]))
             for segment in train_val_list[math.floor(train_val_list_len * train):]]

            [shutil.copy(os.path.join(dataset_path, segment[0], segment[1], segment[2]),
                         os.path.join(dest_dir, "test", segment[0], segment[1], segment[2]))
             for segment in test_list]
    
    
def split_dataset_by_subjects(dataset_path, train=0.85):
    subjects = ["s1", "s2", "s3", "s4", "s5"]
    
    for s in subjects:
        logger.info("Splitting dataset for subject {}".format(s))
        split_dataset_train_val_test_author(dataset_path, author=s, train=train)
        logger.info("Splitting dataset for subject {} done".format(s))
    
if __name__ == '__main__':
    logger.info("Split Tracker Events Dataset by Subjects")
    split_dataset_by_subjects(os.getcwd() + "/TrackerEvents/davis_hand_dataset_tracker_npy", train=0.85)
    
    logger.info("Split Tracker Events Dataset into Train, Validation and Test randomly")
    split_dataset_train_val_test(os.getcwd() + "/TrackerEvents/davis_hand_dataset_tracker_npy", train=0.7, val=0.15)
    
    logger.info("Split All Events Dataset by Subjects")
    split_dataset_by_subjects(os.getcwd() + "/AllEvents/davis_hand_dataset_npy", train=0.85)
    
    logger.info("Split All Events Dataset into Train, Validation and Test randomly")
    split_dataset_train_val_test(os.getcwd() + "/AllEvents/davis_hand_dataset_npy", train=0.7, val=0.15)