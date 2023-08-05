import yaml

# Create a list of dictionaries for transformations
transformations = []

# Define the number of transformation entries you want to create
num_transformations = 5

# Define a list of values for the translation and quaternion components
translation_values = [1, 2, 3, 4, 5]
quaternion_values = [0.1, 0.2, 0.3, 0.4, 0.5]

for i in range(num_transformations):
    transformation_entry = {
        'id': f'{i}',
        'frame_id': 'map',
        'transform': {
            'translation_x': translation_values[i],
            'translation_y': translation_values[i],
            'translation_z': translation_values[i],
            'quaternion_x': quaternion_values[i],
            'quaternion_y': quaternion_values[i],
            'quaternion_z': quaternion_values[i],
            'quaternion_w': quaternion_values[i],
        }
    }
    transformations.append(transformation_entry)

# Create a dictionary with the transformations list
data = {'transformations': transformations}

# Save the data to a YAML file
with open('output.yaml', 'w') as file:
    yaml.dump(data, file)