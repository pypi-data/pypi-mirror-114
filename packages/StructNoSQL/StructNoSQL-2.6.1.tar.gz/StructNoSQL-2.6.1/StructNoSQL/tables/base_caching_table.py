import abc
from typing import Optional, List, Dict, Any, Tuple, Callable, Union, Type

from StructNoSQL import BaseField, TableDataModel
from StructNoSQL.clients_middlewares.dynamodb.backend.dynamodb_core import PrimaryIndex
from StructNoSQL.models import DatabasePathElement, FieldGetter, FieldRemover, FieldSetter, UnsafeFieldSetter, \
    FieldPathSetter, QueryMetadata
from StructNoSQL.practical_logger import message_with_vars
from StructNoSQL.tables.base_table import BaseTable
from StructNoSQL.tables.shared_table_behaviors import _model_contain_all_index_keys, \
    unpack_validate_retrieved_field_if_need_to, unpack_validate_multiple_retrieved_fields_if_need_to
from StructNoSQL.utils.data_processing import navigate_into_data_with_field_path_elements
from StructNoSQL.utils.process_render_fields_paths import process_and_make_single_rendered_database_path, \
    process_validate_data_and_make_single_rendered_database_path, join_field_path_elements


class BaseCachingTable(BaseTable):
    def __init__(self, data_model: Type[TableDataModel], primary_index: PrimaryIndex):
        super().__init__(data_model=data_model, primary_index=primary_index)
        self._cached_data_per_primary_key: Dict[str, Any] = {}
        self._pending_update_operations_per_primary_key: Dict[str, Dict[str, FieldPathSetter]] = {}
        self._pending_remove_operations_per_primary_key: Dict[str, Dict[str, List[DatabasePathElement]]] = {}
        self._debug = False
        self._wrap_item_value = BaseCachingTable._without_debug_wrap_item_value

    @staticmethod
    def _without_debug_wrap_item_value(item_value: Any, from_cache: bool) -> Any:
        return item_value

    @staticmethod
    def _with_debug_wrap_item_value(item_value: Any, from_cache: bool) -> Any:
        return {'value': item_value, 'fromCache': from_cache}

    @property
    def wrap_item_value(self):
        return self._wrap_item_value

    def wrap_item_value_from_cache(self, item_value: Any) -> Any:
        return self._wrap_item_value(item_value=item_value, from_cache=True)

    def wrap_item_value_not_from_cache(self, item_value: Any) -> Any:
        return self._wrap_item_value(item_value=item_value, from_cache=False)

    @property
    def debug(self) -> bool:
        return self._debug

    @debug.setter
    def debug(self, debug: bool):
        self._debug = debug
        self._wrap_item_value = (
            BaseCachingTable._with_debug_wrap_item_value
            if debug is True else
            BaseCachingTable._without_debug_wrap_item_value
        )

    def clear_cached_data(self):
        self._cached_data_per_primary_key = {}

    def clear_cached_data_for_record(self, record_primary_key: str):
        self._cached_data_per_primary_key.pop(record_primary_key, None)

    def clear_pending_update_operations(self):
        self._pending_update_operations_per_primary_key = {}

    def clear_pending_remove_operations(self):
        self._pending_remove_operations_per_primary_key = {}

    def clear_pending_operations(self):
        self.clear_pending_update_operations()
        self.clear_pending_remove_operations()

    def clear_cached_data_and_pending_operations(self):
        self.clear_cached_data()
        self.clear_pending_operations()

    def _index_cached_data(self, primary_key_value: str) -> dict:
        if primary_key_value not in self._cached_data_per_primary_key:
            self._cached_data_per_primary_key[primary_key_value] = {}
        return self._cached_data_per_primary_key[primary_key_value]

    def _remove_index_from_cached_data(self, primary_key_value: str) -> Optional[dict]:
        return self._cached_data_per_primary_key.pop(primary_key_value, None)

    def _index_pending_update_operations(self, primary_key_value: str) -> dict:
        if primary_key_value not in self._pending_update_operations_per_primary_key:
            self._pending_update_operations_per_primary_key[primary_key_value] = {}
        return self._pending_update_operations_per_primary_key[primary_key_value]

    def _index_pending_remove_operations(self, primary_key_value: str) -> dict:
        if primary_key_value not in self._pending_remove_operations_per_primary_key:
            self._pending_remove_operations_per_primary_key[primary_key_value] = {}
        return self._pending_remove_operations_per_primary_key[primary_key_value]

    def has_pending_update_operations(self) -> bool:
        for index_operations in self._pending_update_operations_per_primary_key.values():
            if len(index_operations) > 0:
                return True
        return False

    def has_pending_remove_operations(self) -> bool:
        for index_operations in self._pending_remove_operations_per_primary_key.values():
            if len(index_operations) > 0:
                return True
        return False

    def has_pending_operations(self) -> bool:
        return self.has_pending_update_operations() or self.has_pending_remove_operations()

    @abc.abstractmethod
    def commit_update_operations(self) -> bool:
        raise Exception("commit_update_operations not implemented")

    @abc.abstractmethod
    def commit_remove_operations(self) -> bool:
        raise Exception("commit_remove_operations not implemented")

    def commit_operations(self) -> bool:
        update_operations_commit_success: bool = self.commit_update_operations()
        remove_operations_commit_success: bool = self.commit_remove_operations()
        return all([update_operations_commit_success, remove_operations_commit_success])

    @staticmethod
    def _cache_put_data(index_cached_data: dict, field_path_elements: List[DatabasePathElement], data: Any):
        if len(field_path_elements) > 0:
            navigated_cached_data = index_cached_data
            for path_element in field_path_elements[:-1]:
                stringed_element_key = f'{path_element.element_key}'
                # We wrap the element_key inside a string, to handle a scenario where we would put an item from a list,
                # where the element_key will be an int, that could be above zero, and cannot be handled by a classical list.

                if stringed_element_key not in navigated_cached_data:
                    navigated_cached_data[stringed_element_key] = {}
                navigated_cached_data = navigated_cached_data[stringed_element_key]

            last_field_path_element = field_path_elements[-1]
            navigated_cached_data[f'{last_field_path_element.element_key}'] = data
            # todo: handle list's and set's

    def _cache_get_data(self, primary_key_value: str, field_path_elements: List[DatabasePathElement]) -> Tuple[bool, Any]:
        if len(field_path_elements) > 0:
            index_cached_data: dict = self._index_cached_data(primary_key_value=primary_key_value)
            navigated_cached_data: dict = index_cached_data

            for path_element in field_path_elements[:-1]:
                stringed_element_key = f'{path_element.element_key}'
                # We wrap the element_key inside a string, to handle a scenario where we would put an item from a list,
                # where the element_key will be an int, that could be above zero, and cannot be handled by a classical list.
                navigated_cached_data = (
                    navigated_cached_data[stringed_element_key]
                    if stringed_element_key in navigated_cached_data
                    else path_element.get_default_value()
                )

            last_field_path_element: DatabasePathElement = field_path_elements[-1]
            if last_field_path_element.element_key in navigated_cached_data:
                retrieved_item_value: Any = navigated_cached_data[last_field_path_element.element_key]
                return True, retrieved_item_value
        return False, None

    def _cache_delete_field(self, index_cached_data: dict, primary_key_value: str, field_path_elements: List[DatabasePathElement]) -> str:
        """Will remove the element value from the cache, and remove any update operations associated with the same field in the same index and key_value"""
        BaseCachingTable._cache_put_data(index_cached_data=index_cached_data, field_path_elements=field_path_elements, data=None)

        pending_update_operations: dict = self._index_pending_update_operations(primary_key_value=primary_key_value)
        item_joined_field_path: str = join_field_path_elements(field_path_elements)

        if item_joined_field_path in pending_update_operations:
            pending_update_operations.pop(item_joined_field_path)
        return item_joined_field_path

    def _cache_remove_field(self, index_cached_data: dict, primary_key_value: str, field_path_elements: List[DatabasePathElement]):
        """Unlike the _cache_delete_field, this must be used when a remove operation to the database will be performed right away"""
        item_joined_field_path = self._cache_delete_field(
            index_cached_data=index_cached_data,
            primary_key_value=primary_key_value,
            field_path_elements=field_path_elements
        )
        pending_remove_operations = self._index_pending_remove_operations(primary_key_value=primary_key_value)
        if item_joined_field_path in pending_remove_operations:
            pending_remove_operations.pop(item_joined_field_path)

    def _cache_add_delete_operation(self, index_cached_data: dict, pending_remove_operations: dict, field_path_elements: List[DatabasePathElement]):
        self._cache_put_data(index_cached_data=index_cached_data, field_path_elements=field_path_elements, data=None)
        # We put a None value in the cache, instead of removing it. Because if we de delete an item, we have the
        # in-memory knowledge that its expected value will be None, we do not need to forget its in-memory representation.
        joined_field_path = join_field_path_elements(field_path_elements)
        pending_remove_operations[joined_field_path] = field_path_elements

    def _cache_process_add_delete_operation(self, index_cached_data: dict, pending_remove_operations: dict, field_path: str, query_kwargs: Optional[dict] = None):
        target_field_container, is_multi_selector = process_and_make_single_rendered_database_path(
            field_path=field_path, fields_switch=self.fields_switch, query_kwargs=query_kwargs
        )
        if is_multi_selector is not True:
            target_field_container: Tuple[BaseField, List[DatabasePathElement]]
            field_object, field_path_elements = target_field_container

            self._cache_add_delete_operation(
                index_cached_data=index_cached_data,
                pending_remove_operations=pending_remove_operations,
                field_path_elements=field_path_elements
            )
        else:
            target_field_container: Dict[str, Tuple[BaseField, List[DatabasePathElement]]]

            for item_field_container in target_field_container.values():
                item_field_object, item_field_path_elements = item_field_container

                self._cache_add_delete_operation(
                    index_cached_data=index_cached_data,
                    pending_remove_operations=pending_remove_operations,
                    field_path_elements=item_field_path_elements
                )

    def _validate_cache_format_field_value_if_need_to(
            self, value: Any, data_validation: bool,
            field_object: BaseField, field_path_elements: List[DatabasePathElement],
            index_cached_data: dict, from_cache: bool
    ) -> Optional[Any]:
        if data_validation is True:
            field_object.populate(value=value)
            validated_data, is_valid = field_object.validate_data()
        else:
            validated_data = value

        BaseCachingTable._cache_put_data(
            index_cached_data=index_cached_data,
            field_path_elements=field_path_elements,
            data=validated_data
        )
        return self.wrap_item_value(item_value=validated_data, from_cache=from_cache)

    def _validate_cache_format_fields_values_if_need_to(
            self, data_validation: bool, record_item_data: dict, primary_key_value: str,
            target_fields_containers: Dict[str, Tuple[BaseField, List[DatabasePathElement]]]
    ) -> dict:
        output: dict = {}
        index_cached_data: dict = self._index_cached_data(primary_key_value=primary_key_value)

        for item_key, item_container in target_fields_containers.items():
            item_field_object, item_field_path_elements = item_container

            record_item_matching_item_data: Optional[Any] = record_item_data.get(item_key, None)
            output[item_key] = self._validate_cache_format_field_value_if_need_to(
                value=record_item_matching_item_data, data_validation=data_validation,
                field_object=item_field_object, field_path_elements=item_field_path_elements,
                index_cached_data=index_cached_data, from_cache=False
            )
        return output

    @staticmethod
    def _validate_field_value_if_need_to(value: Any, data_validation: bool, field_object: BaseField) -> Optional[Any]:
        if data_validation is not True:
            return value
        else:
            field_object.populate(value=value)
            validated_data, is_valid = field_object.validate_data()
            # Even if is_valid is False, we still return the validated_data, which will be None.
            return validated_data

    def _validate_format_field_value_if_need_to(self, value: Any, data_validation: bool, field_object: BaseField, from_cache: bool) -> Optional[Any]:
        validated_data: Optional[Any] = BaseCachingTable._validate_field_value_if_need_to(
            value=value, data_validation=data_validation, field_object=field_object
        )
        return self.wrap_item_value(item_value=validated_data, from_cache=from_cache)

    def _put_record(self, middleware: Callable[[dict], bool], record_dict_data: dict) -> bool:
        self.model_virtual_map_field.populate(value=record_dict_data)
        validated_data, is_valid = self.model_virtual_map_field.validate_data()
        put_record_success: bool = middleware(validated_data) if is_valid is True else False
        if put_record_success is True:
            self._cached_data_per_primary_key[record_dict_data[self.primary_index_name]] = record_dict_data
        return put_record_success

    def _delete_record(self, middleware: Callable[[dict], bool], indexes_keys_selectors: dict) -> bool:
        found_all_indexes: bool = _model_contain_all_index_keys(model=self.model, indexes_keys=indexes_keys_selectors.keys())
        if found_all_indexes is not True:
            return False

        deletion_success: bool = middleware(indexes_keys_selectors)
        if deletion_success is True:
            self._remove_index_from_cached_data(primary_key_value=indexes_keys_selectors[self.primary_index_name])
        return deletion_success

    def _remove_record(
            self, middleware: Callable[[dict], Optional[dict]],
            indexes_keys_selectors: dict, data_validation: bool
    ) -> Optional[dict]:
        found_all_indexes: bool = _model_contain_all_index_keys(model=self.model, indexes_keys=indexes_keys_selectors.keys())
        if found_all_indexes is not True:
            return None

        removed_record_data: Optional[dict] = middleware(indexes_keys_selectors)
        if removed_record_data is None:
            return None

        self._remove_index_from_cached_data(primary_key_value=indexes_keys_selectors[self.primary_index_name])
        return self._validate_format_field_value_if_need_to(
            value=removed_record_data, data_validation=data_validation,
            field_object=self.model_virtual_map_field, from_cache=False
        )

    def _get_field(
            self, middleware: Callable[[Union[List[DatabasePathElement], Dict[str, List[DatabasePathElement]]], bool], Any],
            key_value: str, field_path: str, query_kwargs: Optional[dict], data_validation: bool
    ) -> Optional[Any]:

        index_cached_data: dict = self._index_cached_data(primary_key_value=key_value)
        target_field_container, is_multi_selector = process_and_make_single_rendered_database_path(
            field_path=field_path, fields_switch=self.fields_switch, query_kwargs=query_kwargs
        )
        if is_multi_selector is not True:
            target_field_container: Tuple[BaseField, List[DatabasePathElement]]
            field_object, field_path_elements = target_field_container

            found_in_cache, field_value_from_cache = self._cache_get_data(
                primary_key_value=key_value, field_path_elements=field_path_elements
            )
            if found_in_cache is True:
                return self._validate_format_field_value_if_need_to(
                    value=field_value_from_cache, data_validation=data_validation,
                    field_object=field_object, from_cache=True
                )

            retrieved_data: Optional[Any] = middleware(field_path_elements, False)
            return self._validate_cache_format_field_value_if_need_to(
                value=retrieved_data, data_validation=data_validation,
                field_object=field_object, field_path_elements=field_path_elements,
                index_cached_data=index_cached_data, from_cache=False
            )
        else:
            target_field_container: Dict[str, Tuple[BaseField, List[DatabasePathElement]]]

            output_items: Dict[str, Optional[Any]] = {}
            keys_fields_already_cached_to_pop: List[str] = []

            for item_key, item_container in target_field_container.items():
                item_field_object, item_field_path_elements = item_container

                found_item_value_in_cache, field_item_value_from_cache = self._cache_get_data(
                    primary_key_value=key_value, field_path_elements=item_field_path_elements
                )
                if found_item_value_in_cache is True:
                    output_items[item_key] = self._validate_format_field_value_if_need_to(
                        value=field_item_value_from_cache, data_validation=data_validation,
                        field_object=item_field_object, from_cache=True
                    )
                    keys_fields_already_cached_to_pop.append(item_key)

            for key_to_pop in keys_fields_already_cached_to_pop:
                target_field_container.pop(key_to_pop)

            if len(target_field_container) > 0:
                fields_paths_elements: Dict[str, List[DatabasePathElement]] = {key: item[1] for key, item in target_field_container.items()}
                retrieved_items_data: Dict[str, Optional[Any]] = middleware(fields_paths_elements, True)
                for item_key, item_container in target_field_container.items():
                    item_field_object, item_field_path_elements = item_container
                    matching_item_data: Optional[Any] = retrieved_items_data.get(item_key, None)

                    output_items[item_key] = self._validate_cache_format_field_value_if_need_to(
                        value=matching_item_data, data_validation=data_validation,
                        field_object=item_field_object, field_path_elements=item_field_path_elements,
                        index_cached_data=index_cached_data, from_cache=False
                    )
            return output_items

    def inner_query_fields_secondary_index(
            self, middleware: Callable[[List[List[DatabasePathElement]]], Tuple[Optional[List[Any]], QueryMetadata]],
            fields_database_paths: List[List[DatabasePathElement]],
    ) -> Tuple[Optional[dict], QueryMetadata]:
        from StructNoSQL.tables.shared_table_behaviors import _inner_query_fields_secondary_index
        return _inner_query_fields_secondary_index(
            primary_index_name=self.primary_index_name,
            get_primary_key_database_path=self._get_primary_key_database_path,
            middleware=middleware,
            fields_paths_elements=fields_database_paths
        )

    def format_item_value_if_need_to(self, item_value: Any):
        pass

    def unpack_validate_cache_getters_record_attributes_if_need_to(
            self, single_getters_target_fields_containers: Dict[str, Tuple[BaseField, List[DatabasePathElement]]],
            grouped_getters_target_fields_containers: Dict[str, Dict[str, Tuple[BaseField, List[DatabasePathElement]]]],
            data_validation: bool, record_attributes: dict, index_cached_data: dict, base_output_values: Optional[Dict[str, Any]] = None
    ):
        def item_mutator(item_value: Any, item_field_path_elements: List[DatabasePathElement]) -> Any:
            BaseCachingTable._cache_put_data(
                index_cached_data=index_cached_data,
                field_path_elements=item_field_path_elements,
                data=item_value
            )
            return self.wrap_item_value(item_value=item_value, from_cache=False)

        from StructNoSQL.tables.shared_table_behaviors import _unpack_validate_getters_record_attributes_if_need_to
        return _unpack_validate_getters_record_attributes_if_need_to(
            single_getters_target_fields_containers=single_getters_target_fields_containers,
            grouped_getters_target_fields_containers=grouped_getters_target_fields_containers,
            item_mutator=item_mutator, data_validation=data_validation,
            record_attributes=record_attributes, base_output_values=base_output_values
        )

    def _shared_rar(
            self, middleware: Callable[[List[List[DatabasePathElement]]], Tuple[List[Any], QueryMetadata]],
            key_value: str, target_fields_containers: Dict[str, Tuple[BaseField, List[DatabasePathElement]]], data_validation: bool
    ) -> Tuple[Optional[dict], QueryMetadata]:
        existing_record_data: dict = {}

        keys_fields_already_cached_to_pop: List[str] = []
        for item_key, item_container in target_fields_containers.items():
            item_field_object, item_field_path_elements = item_container
            found_item_value_in_cache, field_item_value_from_cache = self._cache_get_data(
                primary_key_value=key_value, field_path_elements=item_field_path_elements
            )
            if found_item_value_in_cache is True:
                existing_record_data[item_key] = self._validate_format_field_value_if_need_to(
                    value=field_item_value_from_cache, data_validation=data_validation,
                    field_object=item_field_object, from_cache=True
                )
                keys_fields_already_cached_to_pop.append(item_key)

        for key_to_pop in keys_fields_already_cached_to_pop:
            target_fields_containers.pop(key_to_pop)

        if not len(target_fields_containers) > 0:
            return {key_value: existing_record_data}, QueryMetadata(count=1, has_reached_end=True, last_evaluated_key=None)

        fields_paths_elements: List[List[DatabasePathElement]] = [item[1] for item in target_fields_containers.values()]
        retrieved_records_items_data, query_metadata = middleware(fields_paths_elements)
        if retrieved_records_items_data is not None and len(retrieved_records_items_data) > 0:
            # Since we query the primary_index, we know for a fact that we will never be returned more than
            # one record item. Hence why we do not have a loop that iterate over the records_items_data,
            # and that we return a dict with the only one record item being the requested key_value.
            index_cached_data: dict = self._index_cached_data(primary_key_value=key_value)
            def item_mutator(item_value: Any, item_field_path_elements: List[DatabasePathElement]) -> Any:
                BaseCachingTable._cache_put_data(
                    index_cached_data=index_cached_data,
                    field_path_elements=item_field_path_elements,
                    data=item_value
                )
                return self.wrap_item_value(item_value=item_value, from_cache=False)

            rar_item_value: Optional[Any] = unpack_validate_multiple_retrieved_fields_if_need_to(
                target_fields_containers=target_fields_containers,
                data_validation=data_validation,
                record_attributes=retrieved_records_items_data[0],
                item_mutator=item_mutator,
                base_output_values=existing_record_data
            )
            # todo: rename rar_item_value
            return {key_value: rar_item_value}, query_metadata

    def _query_field(
            self, middleware: Callable[[List[List[DatabasePathElement]]], Tuple[Optional[List[Any]], QueryMetadata]],
            key_value: str, field_path: str, query_kwargs: Optional[dict], index_name: Optional[str],
            data_validation: bool
    ) -> Tuple[Optional[dict], QueryMetadata]:

        target_field_container, is_multi_selector = process_and_make_single_rendered_database_path(
            field_path=field_path, fields_switch=self.fields_switch, query_kwargs=query_kwargs
        )
        if index_name is not None and index_name != self.primary_index_name:
            output_records_values: dict = {}

            if is_multi_selector is not True:
                target_field_container: Tuple[BaseField, List[DatabasePathElement]]
                fields_database_paths: List[List[DatabasePathElement]] = [target_field_container[1]]

                records_attributes, query_metadata = self.inner_query_fields_secondary_index(
                    middleware=middleware, fields_database_paths=fields_database_paths
                )
                for record_key, record_attributes in records_attributes.items():
                    index_cached_data: dict = self._index_cached_data(primary_key_value=record_key)
                    def item_mutator(item_value: Any, item_field_path_elements: List[DatabasePathElement]) -> Any:
                        BaseCachingTable._cache_put_data(
                            index_cached_data=index_cached_data,
                            field_path_elements=item_field_path_elements,
                            data=item_value
                        )
                        return self.wrap_item_value(item_value=item_value, from_cache=False)

                    output_records_values[record_key] = unpack_validate_retrieved_field_if_need_to(
                        record_attributes=record_attributes,
                        target_field_container=target_field_container,
                        data_validation=data_validation,
                        item_mutator=item_mutator
                    )
            else:
                target_field_container: Dict[str, Tuple[BaseField, List[DatabasePathElement]]]
                fields_database_paths: List[List[DatabasePathElement]] = [item[1] for item in target_field_container.values()]

                records_attributes, query_metadata = self.inner_query_fields_secondary_index(
                    middleware=middleware, fields_database_paths=fields_database_paths
                )
                for record_key, record_item_attributes in records_attributes.items():
                    index_cached_data: dict = self._index_cached_data(primary_key_value=record_key)
                    def item_mutator(item_value: Any, item_field_path_elements: List[DatabasePathElement]) -> Any:
                        BaseCachingTable._cache_put_data(
                            index_cached_data=index_cached_data,
                            field_path_elements=item_field_path_elements,
                            data=item_value
                        )
                        return self.wrap_item_value(item_value=item_value, from_cache=False)

                    output_records_values[record_key] = unpack_validate_multiple_retrieved_fields_if_need_to(
                        target_fields_containers=target_field_container,
                        record_attributes=record_item_attributes,
                        data_validation=data_validation,
                        item_mutator=item_mutator,
                    )
            return output_records_values, query_metadata
        else:
            # If requested index is primary index
            if is_multi_selector is not True:
                target_field_container: Tuple[BaseField, List[DatabasePathElement]]
                field_object, field_path_elements = target_field_container

                found_in_cache, field_value_from_cache = self._cache_get_data(
                    primary_key_value=key_value, field_path_elements=field_path_elements
                )
                if found_in_cache is True:
                    # A single field was requested from a primary index, which means that only one record will have been 
                    # found for the specified index (primary index values are unique). Since the query_field function needs 
                    # to return a Dict[str, Any] with keys being the primary_key_value of the record, the the item being 
                    # the request data, we need to create a dict that wrap our retrieved value as a record result.
                    query_metadata = QueryMetadata(count=1, has_reached_end=True, last_evaluated_key=None)
                    # We can also create a representation of what the query metadata should look like, all from the in memory data.

                    output_item_value = self.wrap_item_value(item_value=field_value_from_cache, from_cache=True)
                    return {key_value: output_item_value}, query_metadata

                records_attributes, query_metadata = middleware([field_path_elements])
                if records_attributes is not None and len(records_attributes) > 0:
                    # Since we query the primary_index, we know for a fact that we will never be returned more than
                    # one record item. Hence why we do not have a loop that iterate over the records_items_data,
                    # and that we return a dict with the only one record item being the requested key_value.
                    single_record_attributes: dict = records_attributes[0]
                    navigated_record_item_value: Optional[Any] = navigate_into_data_with_field_path_elements(
                        data=single_record_attributes,
                        field_path_elements=field_path_elements,
                        num_keys_to_navigation_into=len(field_path_elements)
                    )
                    index_cached_data: dict = self._index_cached_data(primary_key_value=key_value)
                    validated_record_item_value: Optional[Any] = self._validate_cache_format_field_value_if_need_to(
                        value=navigated_record_item_value, data_validation=data_validation,
                        field_object=field_object, field_path_elements=field_path_elements,
                        index_cached_data=index_cached_data, from_cache=False
                    )
                    return {key_value: validated_record_item_value}, query_metadata
                return None, query_metadata
            else:
                target_field_container: Dict[str, Tuple[BaseField, List[DatabasePathElement]]]
                return self._shared_rar(
                    middleware=middleware, key_value=key_value,
                    target_fields_containers=target_field_container,
                    data_validation=data_validation
                )

    def _prepare_getters_with_cache(self, data_validation: bool, key_value: str, getters: Dict[str, FieldGetter]) -> Tuple[
        dict,
        List[List[DatabasePathElement]],
        Dict[str, Tuple[BaseField, List[DatabasePathElement]]],
        Dict[str, Dict[str, Tuple[BaseField, List[DatabasePathElement]]]]
    ]:
        existing_values: dict = {}
        getters_database_paths: List[List[DatabasePathElement]] = []
        single_getters_target_fields_containers: Dict[str, Tuple[BaseField, List[DatabasePathElement]]] = {}
        grouped_getters_target_fields_containers: Dict[str, Dict[str, Tuple[BaseField, List[DatabasePathElement]]]] = {}

        for getter_key, getter_item in getters.items():
            target_field_container, is_multi_selector = process_and_make_single_rendered_database_path(
                field_path=getter_item.field_path, fields_switch=self.fields_switch, query_kwargs=getter_item.query_kwargs
            )
            if is_multi_selector is not True:
                target_field_container: Tuple[BaseField, List[DatabasePathElement]]
                field_object, field_path_elements = target_field_container
                found_item_value_in_cache, field_item_value_from_cache = self._cache_get_data(
                    primary_key_value=key_value, field_path_elements=field_path_elements
                )
                if found_item_value_in_cache is True:
                    if data_validation is True:
                        field_object.populate(value=field_item_value_from_cache)
                        validated_data, is_valid = field_object.validate_data()
                    else:
                        validated_data = field_item_value_from_cache
                    existing_values[getter_key] = self.wrap_item_value(item_value=validated_data, from_cache=True)
                else:
                    single_getters_target_fields_containers[getter_key] = target_field_container
                    getters_database_paths.append(target_field_container[1])
            else:
                target_field_container: Dict[str, Tuple[BaseField, List[DatabasePathElement]]]

                container_existing_values: dict = {}
                container_fields: Dict[str, Tuple[BaseField, List[DatabasePathElement]]] = {}

                field_path_object: Dict[str, BaseField]
                getter_field_path_elements: Dict[str, List[DatabasePathElement]]

                grouped_getters_target_fields_containers[getter_key] = target_field_container
                for item_key, item_target_field_container in target_field_container.items():
                    item_field_object, item_field_path_elements = item_target_field_container
                    found_item_value_in_cache, field_item_value_from_cache = self._cache_get_data(
                        primary_key_value=key_value, field_path_elements=item_field_path_elements
                    )
                    if found_item_value_in_cache is True:
                        if data_validation is True:
                            item_field_object.populate(value=field_item_value_from_cache)
                            validated_data, is_valid = item_field_object.validate_data()
                        else:
                            validated_data = field_item_value_from_cache
                        container_existing_values[item_key] = self.wrap_item_value(item_value=validated_data, from_cache=True)
                    else:
                        container_fields[getter_key] = item_target_field_container
                        getters_database_paths.append(item_field_path_elements)

                grouped_getters_target_fields_containers[getter_key] = container_fields
                existing_values[getter_key] = container_existing_values

        return existing_values, getters_database_paths, single_getters_target_fields_containers, grouped_getters_target_fields_containers

    def _query_multiple_fields(
            self, middleware: Callable[[List[List[DatabasePathElement]]], Tuple[Optional[List[Any]], QueryMetadata]],
            key_value: str, getters: Dict[str, FieldGetter], index_name: Optional[str], data_validation: bool
    ):
        existing_values, getters_database_paths, single_getters_target_fields_containers, grouped_getters_target_fields_containers = (
            self._prepare_getters_with_cache(data_validation=data_validation, key_value=key_value, getters=getters)
        )
        if index_name is None or index_name == self.primary_index_name:
            records_attributes, query_metadata = middleware(getters_database_paths)
            if records_attributes is not None and len(records_attributes) > 0:
                # Since we query the primary_index, we know for a fact that we will never be returned more than
                # one record item. Hence why we do not have a loop that iterate over the records_items_data,
                # and that we return a dict with the only one record item being the requested key_value.
                index_cached_data: dict = self._index_cached_data(primary_key_value=key_value)
                record_values: Dict[str, Any] = self.unpack_validate_cache_getters_record_attributes_if_need_to(
                    single_getters_target_fields_containers=single_getters_target_fields_containers,
                    grouped_getters_target_fields_containers=grouped_getters_target_fields_containers,
                    data_validation=data_validation, record_attributes=records_attributes[0],
                    index_cached_data=index_cached_data, base_output_values=existing_values
                )
                return {key_value: record_values}, query_metadata
            return None, query_metadata
        else:
            records_attributes, query_metadata = self.inner_query_fields_secondary_index(
                middleware=middleware, fields_database_paths=getters_database_paths
            )
            index_cached_data: dict = self._index_cached_data(primary_key_value=key_value)
            output_records_values: dict = {
                record_key: self.unpack_validate_cache_getters_record_attributes_if_need_to(
                    data_validation=data_validation, record_attributes=record_item_attributes, index_cached_data=index_cached_data,
                    single_getters_target_fields_containers=single_getters_target_fields_containers,
                    grouped_getters_target_fields_containers=grouped_getters_target_fields_containers
                ) for record_key, record_item_attributes in records_attributes.items()
            }
            return output_records_values, query_metadata

    def _get_multiple_fields(
            self, middleware: Callable[[List[List[DatabasePathElement]]], Any],
            key_value: str, getters: Dict[str, FieldGetter], data_validation: bool
    ) -> Optional[dict]:
        output_data: Dict[str, Any] = {}

        single_getters_target_fields_containers: Dict[str, Tuple[BaseField, List[DatabasePathElement]]] = {}
        grouped_getters_target_fields_containers: Dict[str, Dict[str, Tuple[BaseField, List[DatabasePathElement]]]] = {}

        getters_database_paths: List[List[DatabasePathElement]] = []
        for getter_key, getter_item in getters.items():
            target_field_container, is_multi_selector = process_and_make_single_rendered_database_path(
                field_path=getter_item.field_path, fields_switch=self.fields_switch, query_kwargs=getter_item.query_kwargs
            )
            if is_multi_selector is not True:
                target_field_container: Tuple[BaseField, List[DatabasePathElement]]
                field_object, field_path_elements = target_field_container

                found_value_in_cache, field_value_from_cache = self._cache_get_data(
                    primary_key_value=key_value, field_path_elements=field_path_elements
                )
                if found_value_in_cache is True:
                    output_data[getter_key] = self._validate_format_field_value_if_need_to(
                        value=field_value_from_cache, data_validation=data_validation,
                        field_object=field_object, from_cache=True
                    )
                else:
                    single_getters_target_fields_containers[getter_key] = target_field_container
                    getters_database_paths.append(field_path_elements)
            else:
                target_field_container: Dict[str, Tuple[BaseField, List[DatabasePathElement]]]

                current_getter_grouped_database_paths_elements: Dict[str, Tuple[BaseField, List[DatabasePathElement]]] = {}
                container_data: Dict[str, Any] = {}

                for item_key, item_container in target_field_container.items():
                    item_field_object, item_field_path_elements = item_container

                    found_item_value_in_cache, field_item_value_from_cache = self._cache_get_data(
                        primary_key_value=key_value, field_path_elements=item_field_path_elements
                    )
                    if found_item_value_in_cache is True:
                        container_data[item_key] = self._validate_format_field_value_if_need_to(
                            value=key_value, data_validation=data_validation,
                            field_object=item_field_object, from_cache=True
                        )
                    else:
                        current_getter_grouped_database_paths_elements[item_key] = item_container
                        getters_database_paths.append(item_field_path_elements)

                output_data[getter_key] = container_data
                grouped_getters_target_fields_containers[getter_key] = current_getter_grouped_database_paths_elements

        record_attributes: Optional[dict] = middleware(getters_database_paths)
        if record_attributes is None:
            return output_data

        index_cached_data: dict = self._index_cached_data(primary_key_value=key_value)
        unpacked_retrieved_items: dict = self.unpack_validate_cache_getters_record_attributes_if_need_to(
            data_validation=data_validation, record_attributes=record_attributes, index_cached_data=index_cached_data,
            single_getters_target_fields_containers=single_getters_target_fields_containers,
            grouped_getters_target_fields_containers=grouped_getters_target_fields_containers
        )
        return {**output_data, **unpacked_retrieved_items}

    def _update_field(self, key_value: str, field_path: str, value_to_set: Any, query_kwargs: Optional[dict] = None) -> bool:
        field_object, field_path_elements, validated_data, is_valid = process_validate_data_and_make_single_rendered_database_path(
            field_path=field_path, fields_switch=self.fields_switch, query_kwargs=query_kwargs, data_to_validate=value_to_set
        )
        if is_valid is True:
            index_cached_data = self._index_cached_data(primary_key_value=key_value)
            BaseCachingTable._cache_put_data(index_cached_data=index_cached_data, field_path_elements=field_path_elements, data=validated_data)

            joined_field_path = join_field_path_elements(field_path_elements)
            pending_update_operations = self._index_pending_update_operations(primary_key_value=key_value)
            pending_update_operations[joined_field_path] = FieldPathSetter(
                field_path_elements=field_path_elements, value_to_set=validated_data
            )
            return True
        return False

    def _update_field_return_old(
            self, middleware: Callable[[List[DatabasePathElement], Any], Tuple[bool, Optional[Any]]],
            key_value: str, field_path: str, value_to_set: Any, query_kwargs: Optional[dict], data_validation: bool
    ) -> Tuple[bool, Optional[Any]]:

        field_object, field_path_elements, validated_update_data, update_data_is_valid = process_validate_data_and_make_single_rendered_database_path(
            field_path=field_path, fields_switch=self.fields_switch, query_kwargs=query_kwargs, data_to_validate=value_to_set
        )
        if update_data_is_valid is not True:
            return False, None

        index_cached_data = self._index_cached_data(primary_key_value=key_value)

        field_path_elements: List[DatabasePathElement]
        found_value_in_cache, field_value_from_cache = self._cache_get_data(
            primary_key_value=key_value, field_path_elements=field_path_elements
        )
        if found_value_in_cache is True:
            # When the old value of our field is found in cache, we are not forced to perform a database operation right away in order
            # to know the old value of our field, but we still need to schedule an update operation, then update the in memory cache.
            joined_field_path = join_field_path_elements(field_path_elements)
            pending_update_operations = self._index_pending_update_operations(primary_key_value=key_value)
            pending_update_operations[joined_field_path] = FieldPathSetter(
                field_path_elements=field_path_elements, value_to_set=validated_update_data
            )

            self._cache_put_data(
                index_cached_data=index_cached_data,
                field_path_elements=field_path_elements,
                data=validated_update_data
            )
            return True, self._validate_format_field_value_if_need_to(
                value=field_value_from_cache, data_validation=data_validation,
                field_object=field_object, from_cache=True
            )
        else:
            update_success, response_attributes = middleware(field_path_elements, validated_update_data)
            if update_success is not True:
                return False, None

            self._cache_put_data(
                index_cached_data=index_cached_data,
                field_path_elements=field_path_elements,
                data=validated_update_data
            )

            old_item_data: Optional[Any] = navigate_into_data_with_field_path_elements(
                data=response_attributes, field_path_elements=field_path_elements,
                num_keys_to_navigation_into=len(field_path_elements)
            ) if response_attributes is not None else None

            return update_success, self._validate_format_field_value_if_need_to(
                value=old_item_data, data_validation=data_validation,
                field_object=field_object, from_cache=False
            )

    def _update_multiple_fields(self, key_value: str, setters: List[FieldSetter or UnsafeFieldSetter]) -> bool:
        index_cached_data = self._index_cached_data(primary_key_value=key_value)
        for current_setter in setters:
            if isinstance(current_setter, FieldSetter):
                field_object, field_path_elements, validated_data, is_valid = process_validate_data_and_make_single_rendered_database_path(
                    field_path=current_setter.field_path, fields_switch=self.fields_switch,
                    query_kwargs=current_setter.query_kwargs, data_to_validate=current_setter.value_to_set
                )
                if is_valid is True:
                    BaseCachingTable._cache_put_data(index_cached_data=index_cached_data, field_path_elements=field_path_elements, data=validated_data)
                    joined_field_path = join_field_path_elements(field_path_elements)
                    pending_update_operations = self._index_pending_update_operations(primary_key_value=key_value)
                    pending_update_operations[joined_field_path] = FieldPathSetter(
                        field_path_elements=field_path_elements, value_to_set=validated_data
                    )
            elif isinstance(current_setter, UnsafeFieldSetter):
                raise Exception(f"UnsafeFieldSetter not supported in caching_table")
                """safe_field_path_object, is_multi_selector = process_and_get_field_path_object_from_field_path(
                    field_path_key=current_setter.safe_base_field_path, fields_switch=self.fields_switch
                )
                # todo: add support for multiple fields path
                if current_setter.unsafe_path_continuation is None:
                    field_path_elements = safe_field_path_object.database_path
                else:
                    field_path_elements = safe_field_path_object.database_path + current_setter.unsafe_path_continuation

                processed_value_to_set: Any = float_to_decimal_serializer(current_setter.value_to_set)
                # Since the data is not validated, we pass it to the float_to_decimal_serializer
                # function (which normally should be called by the data validation function)

                rendered_field_path_elements = make_rendered_database_path(
                    database_path_elements=field_path_elements,
                    query_kwargs=current_setter.query_kwargs
                )
                dynamodb_setters.append(FieldPathSetter(
                    field_path_elements=rendered_field_path_elements,
                    value_to_set=processed_value_to_set
                ))"""
        return True

    def _update_multiple_fields_return_old(
            self, middleware: Callable[[Dict[str, FieldPathSetter]], Tuple[bool, Optional[dict]]],
            key_value: str, setters: Dict[str, FieldSetter], data_validation: bool
    ) -> Tuple[bool, Dict[str, Optional[Any]]]:

        setters_containers: Dict[str, Tuple[BaseField, List[DatabasePathElement]]] = {}
        dynamodb_setters: Dict[str, FieldPathSetter] = {}
        output_data: Dict[str, Optional[Any]] = {}
        index_cached_data = self._index_cached_data(primary_key_value=key_value)

        for setter_key, setter_item in setters.items():
            field_object, field_path_elements, validated_data, is_valid = process_validate_data_and_make_single_rendered_database_path(
                field_path=setter_item.field_path, fields_switch=self.fields_switch,
                query_kwargs=setter_item.query_kwargs, data_to_validate=setter_item.value_to_set
            )
            if is_valid is True:
                found_value_in_cache, field_value_from_cache = self._cache_get_data(
                    primary_key_value=key_value, field_path_elements=field_path_elements
                )
                if found_value_in_cache is True:
                    # When the old value of our field is found in cache, we are not forced to perform a database operation right away in order
                    # to know the old value of our field, but we still need to schedule an update operation, then update the in memory cache.
                    joined_field_path = join_field_path_elements(field_path_elements)
                    pending_update_operations = self._index_pending_update_operations(primary_key_value=key_value)
                    pending_update_operations[joined_field_path] = FieldPathSetter(
                        field_path_elements=field_path_elements, value_to_set=validated_data
                    )

                    self._cache_put_data(
                        index_cached_data=index_cached_data,
                        field_path_elements=field_path_elements,
                        data=validated_data
                    )

                    output_data[setter_key] = self._validate_format_field_value_if_need_to(
                        value=field_value_from_cache, data_validation=data_validation,
                        field_object=field_object, from_cache=True
                    )
                else:
                    setters_containers[setter_key] = (field_object, field_path_elements)
                    dynamodb_setters[setter_key] = FieldPathSetter(
                        field_path_elements=field_path_elements, value_to_set=validated_data
                    )
                    self._cache_put_data(
                        index_cached_data=index_cached_data,
                        field_path_elements=field_path_elements,
                        data=validated_data
                    )

        if not len(dynamodb_setters) > 0:
            # If all the fields old values have been found in cache, and their update
            # have been scheduled, but we do not need to send a database request.
            return True, output_data

        update_success, setters_response_attributes = middleware(dynamodb_setters)

        for item_key, item_container in setters_containers.items():
            item_field_object, item_field_path_elements = item_container

            item_data: Optional[Any] = navigate_into_data_with_field_path_elements(
                data=setters_response_attributes, field_path_elements=item_field_path_elements,
                num_keys_to_navigation_into=len(item_field_path_elements)
            )
            output_data[item_key] = self._validate_format_field_value_if_need_to(
                value=item_data, data_validation=data_validation,
                field_object=item_field_object, from_cache=False
            )

        return update_success, output_data

    def _remove_field(
            self, middleware: Callable[[List[List[DatabasePathElement]]], Any],
            key_value: str, field_path: str, query_kwargs: Optional[dict], data_validation: bool
    ) -> Optional[Any]:

        target_field_container, is_multi_selector = process_and_make_single_rendered_database_path(
            field_path=field_path, fields_switch=self.fields_switch, query_kwargs=query_kwargs
        )
        index_cached_data = self._index_cached_data(primary_key_value=key_value)

        if is_multi_selector is not True:
            target_field_container: Tuple[BaseField, List[DatabasePathElement]]
            field_object, field_path_elements = target_field_container

            found_value_in_cache, field_value_from_cache = self._cache_get_data(
                primary_key_value=key_value, field_path_elements=field_path_elements
            )
            if found_value_in_cache is True:
                pending_remove_operations = self._index_pending_remove_operations(primary_key_value=key_value)
                self._cache_add_delete_operation(
                    index_cached_data=index_cached_data,
                    pending_remove_operations=pending_remove_operations,
                    field_path_elements=field_path_elements
                )
                # Even when we retrieve a removed value from the cache, and that we do not need to perform a remove operation right away to retrieve
                # the removed value, we still want to add a delete_operation that will be performed on operation commits, because if we remove a value
                # from the cache, it does not remove a potential older value present in the database, that the remove operation should remove.
                return self._validate_format_field_value_if_need_to(
                    value=field_value_from_cache, data_validation=data_validation,
                    field_object=field_object, from_cache=True
                )
            else:
                target_path_elements: List[List[DatabasePathElement]] = [field_path_elements]
                self._cache_remove_field(
                    index_cached_data=index_cached_data,
                    primary_key_value=key_value,
                    field_path_elements=field_path_elements
                )
                response_attributes: Optional[dict] = middleware(target_path_elements)
                removed_item_data: Optional[Any] = navigate_into_data_with_field_path_elements(
                    data=response_attributes, field_path_elements=field_path_elements,
                    num_keys_to_navigation_into=len(field_path_elements)
                )
                return self._validate_format_field_value_if_need_to(
                    value=removed_item_data, data_validation=data_validation,
                    field_object=field_object, from_cache=False
                )
        else:
            target_field_container: Dict[str, Tuple[BaseField, List[DatabasePathElement]]]

            target_path_elements: List[List[DatabasePathElement]] = []
            container_output_data: Dict[str, Any] = {}

            for item_key, item_container in target_field_container.items():
                item_field_object, item_field_path_elements = item_container

                found_item_value_in_cache, field_item_value_from_cache = self._cache_get_data(
                    primary_key_value=key_value, field_path_elements=item_field_path_elements
                )
                if found_item_value_in_cache is True:
                    pending_remove_operations = self._index_pending_remove_operations(primary_key_value=key_value)
                    self._cache_add_delete_operation(
                        index_cached_data=index_cached_data,
                        pending_remove_operations=pending_remove_operations,
                        field_path_elements=item_field_path_elements
                    )
                    container_output_data[item_key] = self._validate_format_field_value_if_need_to(
                        value=field_item_value_from_cache, data_validation=data_validation,
                        field_object=item_field_object, from_cache=True
                    )
                else:
                    target_path_elements.append(item_field_path_elements)
                    self._cache_remove_field(
                        index_cached_data=index_cached_data,
                        primary_key_value=key_value,
                        field_path_elements=item_field_path_elements
                    )

            if len(target_path_elements) > 0:
                response_attributes: Optional[dict] = middleware(target_path_elements)
                for item_key, item_container in target_field_container.items():
                    item_field_object, item_field_path_elements = item_container

                    removed_item_data: Optional[Any] = navigate_into_data_with_field_path_elements(
                        data=response_attributes, field_path_elements=item_field_path_elements,
                        num_keys_to_navigation_into=len(item_field_path_elements)
                    )
                    container_output_data[item_key] = self._validate_format_field_value_if_need_to(
                        value=removed_item_data, data_validation=data_validation,
                        field_object=item_field_object, from_cache=False
                    )

            return container_output_data

    def _delete_field(self, key_value: str, field_path: str, query_kwargs: Optional[dict] = None) -> bool:
        index_cached_data = self._index_cached_data(primary_key_value=key_value)
        pending_remove_operations = self._index_pending_remove_operations(primary_key_value=key_value)
        self._cache_process_add_delete_operation(
            index_cached_data=index_cached_data,
            pending_remove_operations=pending_remove_operations,
            field_path=field_path, query_kwargs=query_kwargs
        )
        return True

    def _grouped_remove_multiple_fields(
            self, middleware: Callable[[List[List[DatabasePathElement]]], Any],
            key_value: str, removers: Dict[str, FieldRemover], data_validation: bool
    ) -> Optional[Dict[str, Any]]:
        # todo: do not perform the operation but store it as pending if a matching value exists in the cache
        if not len(removers) > 0:
            # If no remover has been specified, we do not run the database
            # operation, and since no value has been removed, we return None.
            return None
        else:
            output_data: dict = {}
            index_cached_data = self._index_cached_data(primary_key_value=key_value)

            removers_field_paths_elements: Dict[str, Tuple[BaseField, List[DatabasePathElement]]] = {}
            grouped_removers_field_paths_elements: Dict[str, Dict[str, Tuple[BaseField, List[DatabasePathElement]]]] = {}

            # todo: add the remove items present in cache to the output_data instead of only returning the items not removed from cache

            removers_database_paths: List[List[DatabasePathElement]] = []
            for remover_key, remover_item in removers.items():
                target_field_container, is_multi_selector = process_and_make_single_rendered_database_path(
                    field_path=remover_item.field_path, fields_switch=self.fields_switch,
                    query_kwargs=remover_item.query_kwargs
                )
                if is_multi_selector is not True:
                    target_field_container: Tuple[BaseField, List[DatabasePathElement]]
                    field_object, field_path_elements = target_field_container

                    removers_field_paths_elements[remover_key] = target_field_container
                    removers_database_paths.append(field_path_elements)
                    self._cache_remove_field(
                        index_cached_data=index_cached_data,
                        primary_key_value=key_value,
                        field_path_elements=field_path_elements
                    )
                else:
                    target_field_container: Dict[str, Tuple[BaseField, List[DatabasePathElement]]]

                    grouped_removers_field_paths_elements[remover_key] = target_field_container
                    for item_container in target_field_container.values():
                        item_field_object, item_field_path_elements = item_container

                        removers_database_paths.append(item_field_path_elements)
                        self._cache_remove_field(
                            index_cached_data=index_cached_data,
                            primary_key_value=key_value,
                            field_path_elements=item_field_path_elements
                        )

            record_attributes = middleware(removers_database_paths)
            if record_attributes is None:
                return None

            index_cached_data: dict = self._index_cached_data(primary_key_value=key_value)
            return self.unpack_validate_cache_getters_record_attributes_if_need_to(
                data_validation=data_validation, record_attributes=record_attributes, index_cached_data=index_cached_data,
                single_getters_target_fields_containers=removers_field_paths_elements,
                grouped_getters_target_fields_containers=grouped_removers_field_paths_elements
            )

    def _grouped_delete_multiple_fields(self, key_value: str, removers: List[FieldRemover]) -> bool:
        index_cached_data = self._index_cached_data(primary_key_value=key_value)
        pending_remove_operations = self._index_pending_remove_operations(primary_key_value=key_value)

        for current_remover in removers:
            self._cache_process_add_delete_operation(
                index_cached_data=index_cached_data,
                pending_remove_operations=pending_remove_operations,
                field_path=current_remover.field_path,
                query_kwargs=current_remover.query_kwargs
            )
        return True
