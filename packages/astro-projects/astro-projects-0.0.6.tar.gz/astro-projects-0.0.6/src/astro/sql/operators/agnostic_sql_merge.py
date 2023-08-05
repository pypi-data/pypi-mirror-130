"""
Copyright Astronomer, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from typing import Dict

from airflow.exceptions import AirflowException
from airflow.hooks.base import BaseHook

from astro.sql.operators.sql_decorator import SqlDecoratoratedOperator
from astro.utils.postgres_merge_func import postgres_merge_func
from astro.utils.snowflake_merge_func import snowflake_merge_func


class SqlMergeOperator(SqlDecoratoratedOperator):
    def __init__(
        self,
        target_table,
        merge_table,
        merge_keys,
        target_columns,
        merge_columns,
        conflict_strategy,
        conn_id,
        **kwargs,
    ):
        self.target_table = target_table
        self.merge_table = merge_table
        self.merge_keys = merge_keys
        self.target_columns = target_columns
        self.merge_columns = merge_columns
        self.conflict_strategy = conflict_strategy
        self.conn_id = conn_id
        task_id = target_table + "_" + merge_table + "_" + "merge"

        def null_function():
            pass

        super().__init__(
            raw_sql=True,
            parameters={},
            conn_id=conn_id,
            task_id=task_id,
            op_args=(),
            python_callable=null_function,
            **kwargs,
        )

    def execute(self, context: Dict):
        conn_type = BaseHook.get_connection(self.conn_id).conn_type
        if conn_type == "postgres":
            self.sql = postgres_merge_func(
                target_table=self.target_table,
                merge_table=self.merge_table,
                merge_keys=self.merge_keys,
                target_columns=self.target_columns,
                merge_columns=self.merge_columns,
                conflict_strategy=self.conflict_strategy,
                conn_id=self.conn_id,
            )
        elif conn_type == "snowflake":
            self.sql, self.parameters = snowflake_merge_func(
                target_table=self.target_table,
                merge_table=self.merge_table,
                merge_keys=self.merge_keys,
                target_columns=self.target_columns,
                merge_columns=self.merge_columns,
                conflict_strategy=self.conflict_strategy,
            )
        else:
            raise AirflowException(f"please give a postgres conn id")

        super().execute(context)
