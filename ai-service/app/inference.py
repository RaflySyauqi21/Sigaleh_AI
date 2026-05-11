import numpy as np


def predict_price(model, scaler, input_data):
    try:
        input_data = np.array(input_data)

        if input_data.shape != (30, 5):
            raise ValueError(
                f"Input harus shape (30,5), dapat {input_data.shape}"
            )

        scaled_input = scaler.transform(input_data)

    except Exception as e:
        raise ValueError(f"Preprocessing error: {str(e)}")

    X_input = np.array([scaled_input])

    prediction = model.predict(X_input, verbose=0)

    harga_min = scaler.data_min_[0]
    harga_max = scaler.data_max_[0]

    prediction_inverse = (
        prediction * (harga_max - harga_min)
    ) + harga_min

    predicted_price = float(prediction_inverse[0][0])

    predicted_price = max(0, predicted_price)

    return predicted_price