import rclpy
from rclpy.node import Node
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener

from tf2_ros import LookupException, ConnectivityException, ExtrapolationException
import yaml
import os
import time
from rclpy.executors import MultiThreadedExecutor


class GetYAMLROOM(Node):

    def __init__(self):
        super().__init__('get_yaml_room')

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self, spin_thread=True)

        ### run this when localization is accurate
        self.used_rooms = ["map", "bedroom", "door", "couch", "outside", "living_room", "kitchen", "bathroom",
                           "dining_room", "hallway", "home"]  # add the rooms youu want the tfs for plus map
        self.all_transforms_received = False
        self.transformation_rooms_added = []
        self.transformations = []

    def get_transform_matrix_room_from_tf(self):
        # Create a list of dictionaries for transformations
        self.transformation_rooms_added = []
        print(self.transformations)
        for room in self.used_rooms:
            if room in self.transformation_rooms_added:
                continue
            print('room', room)
            source_frame = "unity"  # to
            frame = room  # from

            try:
                print('tryg', room)
                transformation = self.tf_buffer.lookup_transform(source_frame, frame, rclpy.time.Time(),
                                                                 timeout=rclpy.duration.Duration(seconds=5.0))
                # print('transformation', transformation)
                transformation_entry = {
                    'id': f'{frame}',
                    'frame_id': 'unity',
                    'transform': [transformation.transform.translation.x, transformation.transform.translation.y,
                                  transformation.transform.translation.z,
                                  transformation.transform.rotation.x, transformation.transform.rotation.y,
                                  transformation.transform.rotation.z, transformation.transform.rotation.w,
                                  ]
                }

                self.transformations.append(transformation_entry)
                print('here')
                self.get_logger().info(f'transform ready from {frame} to {source_frame}')
                self.transformation_rooms_added.append(room)
                print(self.transformation_rooms_added)

            except (LookupException, ConnectivityException, ExtrapolationException):
                pass

    def check_all_rooms_processed(self):
        # Check if all IDs from used_apriltags are in the transformations list
        print('dfszsxdzdgvdf', self.transformation_rooms_added)
        print('self.used_apriltags', self.used_rooms)
        if all(tag_id in self.transformation_rooms_added for tag_id in self.used_rooms):
            # Create a dictionary with the transformations list
            data = {'transformations': self.transformations}
            # Save the data to a YAML file
            file_path = os.environ['HOME'] + '/smart-home/src/smart-home/external/aptags_tf_broadcast/config/'
            file_name = 'hewitthall_rooms.yaml'
            with open(file_path + file_name, 'w') as file:
                yaml.dump(data, file)
                print('file_save')
            return True
        return False


def main(args=None):
    rclpy.init(args=args)
    get_yaml = GetYAMLROOM()

    # Run the loop to process transformations until all used apriltags are processed
    while rclpy.ok() and not get_yaml.all_transforms_received:
        get_yaml.transformations = []  # Initialize the transformations list for each iteration
        get_yaml.get_transform_matrix_room_from_tf()
        rclpy.spin_once(get_yaml)

        # Check if all transformations for the used apriltags have been received
        get_yaml.all_transforms_received = get_yaml.check_all_rooms_processed()
        print('hreergsdfhasjfgasdf', get_yaml.all_transforms_received)

        rclpy.shutdown()


if __name__ == '__main__':
    main()
