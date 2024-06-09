

base_path = "/content/drive/My Drive/DLAssignments/Assignment2"
data_path = base_path+"/data"
cifar_10_files = ['data_batch_1', 'data_batch_2', 'data_batch_3', 'data_batch_4', 'data_batch_5']

data_files = []
labels = []
for file in cifar_10_files:
    data_dict = unpickle(f"{data_path}/cifar-10-batches-py/{file}")
    data_files.append(data_dict['data'])
    labels.extend(data_dict['labels'])

data = np.vstack(data_files)
labels = np.array(labels)



data = data.reshape(-1, 3, 32, 32)
data = data/255
centralized_data = (data-0.5)/0.5

indices = np.arange(len(data))
validation_indices = np.random.choice(indices, size = 5000, replace = False)
train_indices = list(set(indices) - set(validation_indices))

train_dataset = CIFAR10(centralized_data[train_indices], labels[train_indices])
validation_dataset = CIFAR10(centralized_data[validation_indices], labels[validation_indices])

