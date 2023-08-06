""" Defines the LookupDynamoDbEngine class, which is used to perform lookups on DynamoDB store.
"""

from databricks.feature_store.lookup_engine.lookup_engine import LookupEngine
from databricks.feature_store.entities.data_type import DataType
from databricks.feature_store.protos.feature_store_serving_pb2 import (
    DataType as ProtoDataType,
)
from databricks.feature_store.entities.online_feature_table import (
    OnlineFeatureTable,
    PrimaryKeyDetails,
    FeatureDetails,
)
from databricks.feature_store.utils.dynamodb_type_utils import (
    DynamoDbPandasInt64TypeConverter,
    DynamoDbPandasBooleanTypeConverter,
    DynamoDbPandasStringTypeConverter,
    DynamoDbPandasFloat64TypeConverter,
    DynamoDbPandasTimestampTypeConverter,
    DynamoDbPandasDateTypeConverter,
    DynamoDbPandasTypeConverter,
)

import collections
import functools
import logging
import numpy as np
import pandas as pd
from typing import List, Tuple, Union, Dict, Any
import boto3
from botocore.exceptions import ClientError

_logger = logging.getLogger(__name__)


def get_converter(
    details: Union[FeatureDetails, PrimaryKeyDetails]
) -> DynamoDbPandasTypeConverter:
    """
    Looks up the data type converter subclass of DynamoDbPandasTypeConverter based on the input
    FeatureDetails or PrimaryKeyDetails. For the type mapping of pandas to dynamodb checkout the
    documentation at https://docs.google.com/document/d/1CvdYWUDqEsv69YVv1S9Co2vx-akEaki3v_H3Q2ZMDmo/edit#bookmark=id.qdunvvvuke0e
    :return:DynamoDbPandasTypeConverter
    """

    # Integer, long, float and double are stored as Number in DynamoDB.
    if details.data_type == DataType.INTEGER or details.data_type == DataType.LONG:
        return DynamoDbPandasInt64TypeConverter
    elif details.data_type == DataType.FLOAT or details.data_type == DataType.DOUBLE:
        return DynamoDbPandasFloat64TypeConverter
    elif details.data_type == DataType.BOOLEAN:
        return DynamoDbPandasBooleanTypeConverter
    elif details.data_type == DataType.STRING:
        return DynamoDbPandasStringTypeConverter
    elif details.data_type == DataType.TIMESTAMP:
        return DynamoDbPandasTimestampTypeConverter
    elif details.data_type == DataType.DATE:
        return DynamoDbPandasDateTypeConverter
    else:
        raise ValueError(
            f"Unsupported data type: {ProtoDataType.Name(details.data_type)}"
        )


class LookupDynamoDbEngine(LookupEngine):
    TABLE = "Table"
    KEY_SCHEMA = "KeySchema"
    ATTRIBUTE_NAME = "AttributeName"
    ITEM = "Item"

    def __init__(
        self, online_feature_table: OnlineFeatureTable, access_key: str, secret_key: str
    ):
        self.table_name = online_feature_table.online_feature_table_name
        self.region = online_feature_table.online_store.extra_configs.region

        self.primary_keys_to_type_converter = {
            pk.name: get_converter(pk) for pk in online_feature_table.primary_keys
        }
        self.features_to_type_converter = {
            feature.name: get_converter(feature)
            for feature in online_feature_table.features
        }

        self.dynamodb_client = boto3.client(
            "dynamodb",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=self.region,
        )
        self._validate_online_feature_table()

        dynamodb = boto3.resource(
            "dynamodb",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=self.region,
        )
        self.dynamodb_table = dynamodb.Table(self.table_name)

    def lookup_features(
        self, lookup_df: pd.DataFrame, feature_names: List[str]
    ) -> pd.DataFrame:
        query = functools.partial(self._run_lookup_dynamodb_query, feature_names)
        feature_df = lookup_df.apply(query, axis=1, result_type="expand")
        feature_df.columns = feature_names
        return feature_df

    def _validate_online_feature_table(
        self,
    ) -> None:
        # Fetch the online feature table from online store as specified by the OnlineFeatureTable if
        # exists else throw an error.
        try:
            table_desc = self.dynamodb_client.describe_table(TableName=self.table_name)
        except ClientError as ce:
            raise ce

        # Validate the online feature table has the same primary keys specified by the OnlineFeatureTable.
        if (
            not self.TABLE in table_desc
            or not self.KEY_SCHEMA in table_desc[self.TABLE]
            or not self._store_contains_primary_keys(
                table_desc[self.TABLE][self.KEY_SCHEMA]
            )
        ):
            raise ValueError(
                f"Table {self.table_name} does not contain primary keys {list(self.primary_keys_to_type_converter.keys())}."
            )

    def _store_contains_primary_keys(self, key_schema: dict):
        """
        Returns true if the primary keys in online store are same as primary keys set in
        initializing the class object, else False.
        """
        primary_keys = [element[self.ATTRIBUTE_NAME] for element in key_schema]
        return collections.Counter(primary_keys) == collections.Counter(
            [primary_key for primary_key in self.primary_keys_to_type_converter]
        )

    def _run_lookup_dynamodb_query(
        self, feature_names: List[str], lookup_row: pd.core.series.Series
    ):
        """
        This helper function executes a single DynamoDB query.
        """
        query_params = lookup_row.to_dict()
        query_params = self._pandas_to_dynamodb(query_params)
        feat_row = self.dynamodb_table.get_item(
            Key=query_params, AttributesToGet=feature_names
        )
        if not self.ITEM in feat_row:
            _logger.warning(
                f"No feature values found in {self.table_name} for {query_params}."
            )
            nan_features = np.empty(len(feature_names))
            nan_features[:] = np.nan
            return nan_features

        # Return the result
        results = [
            feat_row[self.ITEM][f] if f in feat_row[self.ITEM] else np.nan
            for f in feature_names
        ]
        return self._dynamodb_to_pandas(results, feature_names)

    def _pandas_to_dynamodb(self, query_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Converts the input query_params dictionary values to dynamodb compatible python types based on
        the input.
        :return:dict[string, ...]
        """
        return {
            pk_name: self.primary_keys_to_type_converter[pk_name].to_dynamodb(pk_value)
            for pk_name, pk_value in query_params.items()
        }

    def _dynamodb_to_pandas(
        self, results: List[Any], feature_names: List[str]
    ) -> List[Any]:
        """
        Converts the input results list with dynamodb-compatible python values to pandas types based on
        the input features_names and features converter.
        :return:List[Any]
        """
        feature_names_and_values = zip(feature_names, results)
        return [
            self.features_to_type_converter[feature_name].to_pandas(feature_value)
            for feature_name, feature_value in feature_names_and_values
        ]

    def shutdown(self) -> None:
        """
        Cleans up the store connection if it exists on the DynamoDB online store.
        :return:
        """
        # DynamoDB connections are stateless http connections and hence do not need an explicit
        # shutdown operation.
        pass
