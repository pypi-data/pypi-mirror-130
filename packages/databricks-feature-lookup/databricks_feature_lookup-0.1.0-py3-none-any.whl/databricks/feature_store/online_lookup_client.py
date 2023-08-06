from databricks.feature_store.entities.online_feature_table import OnlineFeatureTable
from databricks.feature_store.entities.store_type import StoreType
from databricks.feature_store.lookup_engine import (
    LookupMySqlEngine,
    LookupSqlEngine,
    LookupSqlServerEngine,
    LookupEngine,
    LookupDynamoDbEngine,
)

from typing import List, Tuple
import pandas as pd
import os

# The provisioner of this model is expected to set the following environment variable for each
# feature table if the feature store is SQL based:
#  (1) <online_store_for_serving.read_secret_prefix>_USER
#  (2) <online_store_for_serving.read_secret_prefix>_PASSWORD
# For no-sql based stores such as DynamoDB following variables should be set:
#  (1) <online_store_for_serving.read_secret_prefix>_ACCESS_KEY
#  (2) <online_store_for_serving.read_secret_prefix>_SECRET_KEY
USER_SUFFIX = "_USER"
PASSWORD_SUFFIX = "_PASSWORD"
ACCESS_KEY_SUFFIX = "_ACCESS_KEY"
SECRET_KEY_SUFFIX = "_SECRET_KEY"


def generate_lookup_sql_engine(
    online_feature_table: OnlineFeatureTable,
    creds: Tuple[str, str],
) -> LookupSqlEngine:
    ro_user, ro_password = creds
    if online_feature_table.online_store.store_type == StoreType.SQL_SERVER:
        return LookupSqlServerEngine(online_feature_table, ro_user, ro_password)
    return LookupMySqlEngine(online_feature_table, ro_user, ro_password)


def generate_lookup_dynamodb_engine(
    online_feature_table: OnlineFeatureTable,
    creds: Tuple[str, str],
) -> LookupDynamoDbEngine:
    access_key, secret_key = creds
    return LookupDynamoDbEngine(online_feature_table, access_key, secret_key)


def load_credentials_from_env(online_ft: OnlineFeatureTable):
    read_secret_prefix = online_ft.online_store.read_secret_prefix
    creds = ()
    if online_ft.online_store.store_type == StoreType.DYNAMODB:
        access_key_env_var = read_secret_prefix + ACCESS_KEY_SUFFIX
        secret_key_env_var = read_secret_prefix + SECRET_KEY_SUFFIX
        if not (access_key_env_var in os.environ and secret_key_env_var in os.environ):
            raise Exception(
                f"Internal error: Access Key and Secret Key not found for feature table "
                f"{online_ft.feature_table_name}."
            )
        creds = os.getenv(access_key_env_var), os.getenv(secret_key_env_var)
    else:
        user_env_var = read_secret_prefix + USER_SUFFIX
        password_env_var = read_secret_prefix + PASSWORD_SUFFIX
        if not (user_env_var in os.environ and password_env_var in os.environ):
            raise Exception(
                f"Internal error: User and Password not found for feature table "
                f"{online_ft.feature_table_name}."
            )
        creds = os.getenv(user_env_var), os.getenv(password_env_var)

    return creds


class OnlineLookupClient:
    def __init__(self, online_feature_table: OnlineFeatureTable):
        creds = load_credentials_from_env(online_feature_table)
        if online_feature_table.online_store.store_type == StoreType.DYNAMODB:
            self.lookup_engine = generate_lookup_dynamodb_engine(
                online_feature_table, creds
            )
        else:
            self.lookup_engine = generate_lookup_sql_engine(online_feature_table, creds)

    def lookup_features(
        self,
        lookup_df: pd.DataFrame,
        feature_names: List[str],
    ) -> pd.DataFrame:
        """Uses a Python database connection to lookup features in feature_names using
        the lookup keys and values in lookup_df. The online store database and table name are
        obtained from the OnlineFeatureTable passed to the constructor.

        The resulting DataFrame has the same number of rows as lookup_df. In the case that a lookup
        key cannot be found, a row of NaNs will be returned in the resulting DataFrame.

        Throws an exception if the table, lookup keys, or feature columns do not exist in the
        online store.

        :param lookup_df: Pandas DataFrame containing lookup keys and values. The DataFrame should
        contain one column for each primary key of the online feature table, and one row for each
        entity to look up.
        :param feature_names: A list of feature names to look up.
        :return: Pandas DataFrame containing feature keys and values fetched from the online store.
        """
        features = self.lookup_engine.lookup_features(
            lookup_df,
            feature_names,
        )
        return features

    def cleanup(self):
        """
        Performs any cleanup associated with the online store.
        :return:
        """
        self.lookup_engine.shutdown()
