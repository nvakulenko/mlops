from os import listdir
from os.path import isfile, join

from autokeras.image_supervised import ImageClassifier, load_image_dataset


def train():
    base_dir = '/Users/sangre/Documents/GitHub/mlops/data/autokeras-data/'

    train_path = base_dir + 'train_cats_dogs_rabbits/'
    train_labels = base_dir + 'train_cats_dogs_rabbits.csv'

    validation_path = base_dir + 'validation_cats_dogs_rabbits/'
    validation_labels = base_dir + 'validation_cats_dogs_rabbits.csv'

    files = [f for f in listdir(train_path) if isfile(join(train_path, f))]
    print(files)

    x_train, y_train = load_image_dataset(csv_file_path=train_labels, images_path=train_path)
    print(x_train.shape)
    print(y_train.shape)

    x_val, y_val = load_image_dataset(csv_file_path=validation_labels, images_path=validation_path)

    print(x_val.shape)
    print(y_val.shape)

    # (x_train, y_train), (x_val, y_val) = mnist.load_data()

    # Initialize the image classifier.
    clf = ImageClassifier(overwrite=True, max_trials=1)
    # Feed the image classifier with training data.
    clf.fit(x_train, y_train, epochs=10)

    # Predict with the best model.
    predicted_y = clf.predict(x_val)
    print(predicted_y)

    # Evaluate the best model with testing data.
    print(clf.evaluate(x_val, y_val))


def main():
    train()


if __name__ == "__main__":
    main()