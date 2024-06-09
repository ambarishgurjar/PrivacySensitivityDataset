


def train(model, optimizer, loss_fn, data_loader, val_loader = None):
    batch_train_loss = []
    batch_val_loss = []

    # Train loop
    model.train()
    for batch_idx, (x, y) in enumerate(data_loader):
        y_hat = model(x)
        optimizer.zero_grad()
        loss = loss_fn(y, y_hat)
        batch_train_loss.append(loss.item())
        loss.backward()
        optimizer.step()

    if val_loader is not None:
        # Validation loop
        model.eval()
        for batch_idx, (x, y) in enumerate(val_loader):
            y_hat = model(x)
            loss = loss_fn(y, y_hat)
            batch_val_loss.append(loss.item())
    return np.mean(batch_train_loss), np.mean(batch_val_loss)
    
