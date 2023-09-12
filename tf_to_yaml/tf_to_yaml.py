import rclpy
from rclpy.node import Node
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener

from tf2_ros import LookupException, ConnectivityException, ExtrapolationException
import yaml
import os
import time
from rclpy.executors import MultiThreadedExecutor


class GetYAML(Node):

    def __init__(self):
        super().__init__('get_yaml')

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self, spin_thread=True)

        self.used_apriltags = [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16,18]  # add the apriltag ids that you used
        self.all_transforms_received = False
        self.transformation_ids_added = []
        self.transformations = []

    def get_transform_matrix_aptags_from_tf(self):
        # Create a list of dictionaries for transformations
        self.transformation_ids_added = []
        print(self.transformations)
        for aptag in self.used_apriltags:
            if aptag in self.transformation_ids_added:
                continue
            # print('aptag', aptag)
            str_aptag = str(aptag)
            source_frame = "unity"  # to
            frame = "aptag_" + str_aptag  # from

            try:
                # print('tryg', aptag)
                transformation = self.tf_buffer.lookup_transform(source_frame, frame, rclpy.time.Time(),
                                                                 timeout=rclpy.duration.Duration(seconds=5.0))
                # print('transformation', transformation)
                transformation_entry = {
                    'id': f'{frame}',
                    'frame_id': 'map',
                    # 'transform': {
                    #     'translation_x': transformation.transform.translation.x,
                    #     'translation_y': transformation.transform.translation.y,
                    #     'translation_z': transformation.transform.translation.z,
                    #     'quaternion_x': transformation.transform.rotation.x,
                    #     'quaternion_y': transformation.transform.rotation.y,
                    #     'quaternion_z': transformation.transform.rotation.z,
                    #     'quaternion_w': transformation.transform.rotation.w,
                    # }
                    'transform': [transformation.transform.translation.x, transformation.transform.translation.y,
                                  transformation.transform.translation.z,
                                  transformation.transform.rotation.x, transformation.transform.rotation.y,
                                  transformation.transform.rotation.z, transformation.transform.rotation.w,
                                  ]
                }

                self.transformations.append(transformation_entry)
                print()
                self.get_logger().info(f'transform ready from {frame} to {source_frame}')
                self.transformation_ids_added.append(aptag)
                print(self.transformation_ids_added)

            except (LookupException, ConnectivityException, ExtrapolationException):
                pass

    def check_all_tags_processed(self):
        # Check if all IDs from used_apriltags are in the transformations list
        if all(tag_id in self.transformation_ids_added for tag_id in self.used_apriltags):
            # Create a dictionary with the transformations list
            data = {'transformations': self.transformations}
            # Save the data to a YAML file
            file_path = os.environ['HOME'] + '/smart-home/src/smart-home/external/aptags_tf_broadcast/config/'
            file_name = 'output.yaml'
            with open(file_path + file_name, 'w') as file:
                yaml.dump(data, file)
                print('file_save')
            return True
        return False


def main(args=None):
    rclpy.init(args=args)
    get_yaml = GetYAML()

    # Run the loop to process transformations until all used apriltags are processed
    while rclpy.ok() and not get_yaml.all_transforms_received:
        get_yaml.transformations = []  # Initialize the transformations list for each iteration
        get_yaml.get_transform_matrix_aptags_from_tf()
        rclpy.spin_once(get_yaml)

        # Check if all transformations for the used apriltags have been received
        get_yaml.all_transforms_received = get_yaml.check_all_tags_processed()
        print(get_yaml.all_transforms_received)

        rclpy.shutdown()


if __name__ == '__main__':
    main()
