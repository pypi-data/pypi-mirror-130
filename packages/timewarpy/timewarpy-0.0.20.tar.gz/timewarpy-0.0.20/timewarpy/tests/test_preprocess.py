from timewarpy import datasets, preprocess


def test_create_univariate_windows():
    df = datasets.load_energy_data()
    X, y = preprocess.create_univariate_windows(df, 1680, 240, 'Appliances')
    assert X.shape == (17816, 1680, 1)


def test_create_multivariate_windows():
    df = datasets.load_energy_data()
    X, y = preprocess.create_multivariate_windows(
        df, 1680, 240, train_columns=['Appliances', 'T1', 'RH_1'], pred_columns=['Appliances', 'T1']
    )
    assert X.shape == (17816, 1680, 3)
    assert y.shape == (17816, 240, 2)
    X, y = preprocess.create_multivariate_windows(
        df, 1680, 240, train_columns=['Appliances', 'T1', 'RH_1'], pred_columns=['Appliances', ]
    )
    assert X.shape == (17816, 1680, 3)
    assert y.shape == (17816, 240, 1)
