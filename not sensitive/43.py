
train1=[]
train2=[]
label=[]
for speaker in range(50):

  for i in range(10):
      input1index=(speaker*10)+i
      input2index=pair_positive(speaker)
      
      positivesample1=librosa.stft(trs[input1index,:].numpy(), n_fft=1024, hop_length=512)
      positivesample2=librosa.stft(trs[input2index,:].numpy(), n_fft=1024, hop_length=512)

      positivesample1 = (torch.from_numpy(np.abs(positivesample1)))
      positivesample2 = (torch.from_numpy(np.abs(positivesample2)))

      positivesample1 = positivesample1.t()
      positivesample2 = positivesample2.t()
      labelt = torch.tensor(1.0)

      train1.append(positivesample1)
      train2.append(positivesample2)
      label.append(labelt)

  for i in range(10):
      input1index=(speaker*10)+i
      input2index=pair_negative_train(speaker)
      
      negativesample1=librosa.stft(trs[input1index,:].numpy(), n_fft=1024, hop_length=512)
      negativesample2=librosa.stft(trs[input2index,:].numpy(), n_fft=1024, hop_length=512)

      negativesample1 = (torch.from_numpy(np.abs(negativesample1)))
      negativesample2 = (torch.from_numpy(np.abs(negativesample2)))

      negativesample1 = negativesample1.t()
      negativesample2 = negativesample2.t()
      labelt = torch.tensor(0.0)

      train1.append(negativesample1)
      train2.append(negativesample2)
      label.append(labelt)

  for i in range(10):
      input1index=(speaker*10)+i
      input2index=pair_positive(speaker)
      
      positivesample1=librosa.stft(trs[input1index,:].numpy(), n_fft=1024, hop_length=512)
      positivesample2=librosa.stft(trs[input2index,:].numpy(), n_fft=1024, hop_length=512)

      positivesample1 = (torch.from_numpy(np.abs(positivesample1)))
      positivesample2 = (torch.from_numpy(np.abs(positivesample2)))

      positivesample1 = positivesample1.t()
      positivesample2 = positivesample2.t()
      labelt = torch.tensor(1.0)

      train1.append(positivesample1)
      train2.append(positivesample2)
      label.append(labelt)

  for i in range(10):
      input1index=(speaker*10)+i
      input2index=pair_negative_train(speaker)
      
      negativesample1=librosa.stft(trs[input1index,:].numpy(), n_fft=1024, hop_length=512)
      negativesample2=librosa.stft(trs[input2index,:].numpy(), n_fft=1024, hop_length=512)

      negativesample1 = (torch.from_numpy(np.abs(negativesample1)))
      negativesample2 = (torch.from_numpy(np.abs(negativesample2)))

      negativesample1 = negativesample1.t()
      negativesample2 = negativesample2.t()
      labelt = torch.tensor(0.0)

      train1.append(negativesample1)
      train2.append(negativesample2)
      label.append(labelt)

print(len(train1))


