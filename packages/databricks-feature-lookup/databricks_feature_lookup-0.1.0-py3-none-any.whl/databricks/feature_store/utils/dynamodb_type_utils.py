""" Defines the type conversion classes from pandas to dynamodb and vice versa.
"""

import pandas as pd
from abc import ABC, ABCMeta, abstractmethod
import numpy as np


class DynamoDbPandasTypeConverter(ABC):
    @staticmethod
    @abstractmethod
    def to_dynamodb(value):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def to_pandas(value):
        raise NotImplementedError


class DynamoDbPandasBooleanTypeConverter(DynamoDbPandasTypeConverter):
    @staticmethod
    def to_dynamodb(value: np.bool) -> int:
        if value:
            return 1
        else:
            return 0

    @staticmethod
    def to_pandas(value: int) -> np.bool:
        if value == 1:
            return True
        elif value == 0:
            return False
        else:
            raise ValueError("Unsupported value for bool: " + str(value))


class DynamoDbPandasInt64TypeConverter(DynamoDbPandasTypeConverter):
    @staticmethod
    def to_dynamodb(value: np.int64) -> int:
        return int(value)

    @staticmethod
    def to_pandas(value: int) -> np.int64:
        return pd.to_numeric(value)


class DynamoDbPandasStringTypeConverter(DynamoDbPandasTypeConverter):
    @staticmethod
    def to_dynamodb(value: np.object) -> str:
        return str(value)

    @staticmethod
    def to_pandas(value: str) -> np.object:
        return value


class DynamoDbPandasFloat64TypeConverter(DynamoDbPandasTypeConverter):
    @staticmethod
    def to_dynamodb(value: np.float64) -> float:
        return float(value)

    @staticmethod
    def to_pandas(value: float) -> np.float64:
        return pd.to_numeric(value)


class DynamoDbPandasTimestampTypeConverter(DynamoDbPandasTypeConverter):
    @staticmethod
    def to_dynamodb(value: np.datetime64) -> int:
        return int(value.floor("us").timestamp() * 1000000)

    @staticmethod
    def to_pandas(value: int) -> np.datetime64:
        return pd.to_datetime(int(value), unit="us")


class DynamoDbPandasDateTypeConverter(DynamoDbPandasTypeConverter):
    @staticmethod
    def to_dynamodb(value: np.datetime64) -> int:
        return int(value.floor("s").timestamp())

    @staticmethod
    def to_pandas(value: int) -> np.datetime64:
        return pd.to_datetime(int(value), unit="s")
