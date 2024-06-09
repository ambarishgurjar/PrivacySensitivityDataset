

def denoise_audio(model, device, noisy_path):
  X_signal, X, sr = get_spectogram(noisy_path)
  abs_X = np.abs(X)
  abs_X_transpose = abs_X.T


  silent_frames = np.random.uniform(low = 1e-15, high = 1e-10, size = (19,513))
  augmented_X = np.concatenate((silent_frames, abs_X_transpose), axis = 0)


  grouped_X = [augmented_X[i:i+20, :] for i in range(abs_X_transpose.shape[0])]
  data = np.stack(grouped_X, axis = 0)
  data = np.expand_dims(data, axis = 1)
  # predict using model
  S_prime = model(T.tensor(data).float().to(device)).T
  assert(S_prime.shape == abs_X.shape)

  S_prime = S_prime.cpu().data.numpy()
  S = np.multiply(X/abs_X, S_prime)
  clean = librosa.core.istft(S, hop_length=512, length = X_signal.shape[0]) 
  return clean, sr
  
