import sys
sys.path.append('..')

from model.models import LGBMmodel, LGBMmodel_classification
import numpy as np

# Model Training
bst_classification = LGBMmodel_classification()
bst_regression_high = LGBMmodel('high')
bst_regression_mid = LGBMmodel('mid')
bst_regression_low = LGBMmodel('low')

# Predicting
def predict(input_data): 
    # Classification
    class_proba = bst_classification.predict(input_data)
    predicted_class = np.argmax(class_proba, axis=1)  # 상: 2, 중: 1, 하: 0
    detail_risk = 0

    # Regression
    if predicted_class == 2:  # 상
        dmg_scale = bst_regression_high.predict(input_data)
        detail_risk = (np.expm1(dmg_scale) - 1) * 100
    elif predicted_class == 1:  # 중
        dmg_scale = bst_regression_mid.predict(input_data)
        detail_risk = (np.expm1(dmg_scale) - 0.5) * 100 * 2
    else:  # 하
        dmg_scale = bst_regression_low.predict(input_data)
        detail_risk = (np.expm1(dmg_scale)) * 100 * 2

    return predicted_class, detail_risk 