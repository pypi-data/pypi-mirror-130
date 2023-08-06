from databricks.feature_store.entities.online_store_for_serving import (
    OnlineStoreForServing,
)
from databricks.feature_store.entities.data_type import DataType
from typing import List, Optional


class PrimaryKeyDetails:
    def __init__(self, name: str, data_type: DataType):
        self._name = name
        self._data_type = data_type

    @property
    def name(self):
        return self._name

    @property
    def data_type(self):
        return self._data_type

    def __str__(self):
        return "{" + self._name + "}"

    def __repr__(self):
        return str(self)


class FeatureDetails:
    def __init__(
        self, name: str, data_type: DataType, data_type_details: Optional[str] = None
    ):
        self._name = name
        self._data_type = data_type
        self._data_type_details = data_type_details

    @property
    def name(self):
        return self._name

    @property
    def data_type(self):
        return self._data_type

    @property
    def data_type_details(self):
        return self._data_type_details


class OnlineFeatureTable:
    def __init__(
        self,
        feature_table_name: str,
        online_feature_table_name: str,
        online_store: OnlineStoreForServing,
        primary_keys: List[PrimaryKeyDetails],
        features: List[FeatureDetails],
    ):
        self._feature_table_name = feature_table_name
        self._online_feature_table_name = online_feature_table_name
        self._online_store = online_store
        self._primary_keys = primary_keys
        self._features = features

    @property
    def feature_table_name(self):
        return self._feature_table_name

    @property
    def online_feature_table_name(self):
        return self._online_feature_table_name

    @property
    def online_store(self):
        return self._online_store

    @property
    def primary_keys(self):
        return self._primary_keys

    @property
    def features(self):
        return self._features

    @classmethod
    def from_proto(cls, the_proto):
        return cls(
            feature_table_name=the_proto.feature_table_name,
            online_feature_table_name=the_proto.online_feature_table_name,
            online_store=OnlineStoreForServing.from_proto(the_proto.online_store),
            primary_keys=[
                PrimaryKeyDetails(primary_key.name, primary_key.data_type)
                for primary_key in the_proto.primary_keys
            ],
            features=[
                FeatureDetails(
                    feature.name, feature.data_type, feature.data_type_details
                )
                for feature in the_proto.features
            ],
        )
