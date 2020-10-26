import pandas as pd
import pytest
from sklearn.exceptions import NotFittedError

from feature_engine.selection import DropConstantFeatures


def test_drop_constant_features(df_constant_features):
    transformer = DropConstantFeatures(tol=1, variables=None)
    X = transformer.fit_transform(df_constant_features)

    # expected result
    df = pd.DataFrame(
        {
            "Name": ["tom", "nick", "krish", "jack"],
            "City": ["London", "Manchester", "Liverpool", "Bristol"],
            "Age": [20, 21, 19, 18],
            "Marks": [0.9, 0.8, 0.7, 0.6],
            "dob": pd.date_range("2020-02-24", periods=4, freq="T"),
            "quasi_feat_num": [1, 1, 1, 2],
            "quasi_feat_cat": ["a", "a", "a", "b"],
        }
    )

    # init params
    assert transformer.tol == 1
    assert transformer.variables == [
        "Name",
        "City",
        "Age",
        "Marks",
        "dob",
        "const_feat_num",
        "const_feat_cat",
        "quasi_feat_num",
        "quasi_feat_cat",
    ]
    # fit attributes
    assert transformer.constant_features_ == ["const_feat_num", "const_feat_cat"]
    assert transformer.input_shape_ == (4, 9)

    # transform output
    pd.testing.assert_frame_equal(X, df)


def test_drop_constant_and_quasiconstant_features(df_constant_features):
    transformer = DropConstantFeatures(tol=0.7, variables=None)
    X = transformer.fit_transform(df_constant_features)

    # expected result
    df = pd.DataFrame(
        {
            "Name": ["tom", "nick", "krish", "jack"],
            "City": ["London", "Manchester", "Liverpool", "Bristol"],
            "Age": [20, 21, 19, 18],
            "Marks": [0.9, 0.8, 0.7, 0.6],
            "dob": pd.date_range("2020-02-24", periods=4, freq="T"),
        }
    )

    # init params
    assert transformer.tol == 0.7
    assert transformer.variables == [
        "Name",
        "City",
        "Age",
        "Marks",
        "dob",
        "const_feat_num",
        "const_feat_cat",
        "quasi_feat_num",
        "quasi_feat_cat",
    ]

    # fit attr
    assert transformer.constant_features_ == [
        "const_feat_num",
        "const_feat_cat",
        "quasi_feat_num",
        "quasi_feat_cat",
    ]
    assert transformer.input_shape_ == (4, 9)

    # transform params
    pd.testing.assert_frame_equal(X, df)


def test_drop_constant_features_with_list_of_variables(df_constant_features):
    # test case 3: drop features showing threshold more than 0.7 with variable list
    transformer = DropConstantFeatures(
        tol=0.7, variables=["Name", "const_feat_num", "quasi_feat_num"]
    )
    X = transformer.fit_transform(df_constant_features)

    # expected result
    df = pd.DataFrame(
        {
            "Name": ["tom", "nick", "krish", "jack"],
            "City": ["London", "Manchester", "Liverpool", "Bristol"],
            "Age": [20, 21, 19, 18],
            "Marks": [0.9, 0.8, 0.7, 0.6],
            "dob": pd.date_range("2020-02-24", periods=4, freq="T"),
            "const_feat_cat": ["a", "a", "a", "a"],
            "quasi_feat_cat": ["a", "a", "a", "b"],
        }
    )

    # init params
    assert transformer.tol == 0.7
    assert transformer.variables == ["Name", "const_feat_num", "quasi_feat_num"]

    # fit attr
    assert transformer.constant_features_ == ["const_feat_num", "quasi_feat_num"]
    assert transformer.input_shape_ == (4, 9)

    # transform params
    pd.testing.assert_frame_equal(X, df)


def test_drop_constant_features_if_fit_input_not_df():
    # test case 4: input is not a dataframe
    with pytest.raises(TypeError):
        DropConstantFeatures().fit({"Name": ["Karthik"]})


def test_drop_constant_features_if_tol_out_of_range():
    # test case 5: threshold not between 0 and 1
    with pytest.raises(ValueError):
        DropConstantFeatures(tol=2)


def test_drop_constant_features_if_input_all_constant_features():
    # test case 6: when input contains all constant features
    with pytest.raises(ValueError):
        DropConstantFeatures().fit(pd.DataFrame({"col1": [1, 1, 1], "col2": [1, 1, 1]}))


def test_error_if_input_constant_and_quasi_constant_features():
    # test case 7: when input contains all constant and quasi constant features
    with pytest.raises(ValueError):
        transformer = DropConstantFeatures(tol=0.7)
        transformer.fit_transform(
            pd.DataFrame(
                {
                    "col1": [1, 1, 1, 1],
                    "col2": [1, 1, 1, 1],
                    "col3": [1, 1, 1, 2],
                    "col4": [1, 1, 1, 2],
                }
            )
        )


def test_non_fitted_error(df_constant_features):
    # test case 8: when fit is not called prior to transform
    with pytest.raises(NotFittedError):
        transformer = DropConstantFeatures()
        transformer.transform(df_constant_features)