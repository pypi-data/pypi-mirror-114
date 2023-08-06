from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.hooks_filter import HooksFilter
from ..models.login_methods import LoginMethods
from ..models.patterns_filter import PatternsFilter
from ..models.supported_protocols import SupportedProtocols
from ..models.user_filters_tls_username import UserFiltersTlsUsername
from ..models.web_client_options import WebClientOptions
from ..types import UNSET, Unset

T = TypeVar("T", bound="UserFilters")


@attr.s(auto_attribs=True)
class UserFilters:
    """Additional user options"""

    allowed_ip: Union[Unset, List[str]] = UNSET
    denied_ip: Union[Unset, List[str]] = UNSET
    denied_login_methods: Union[Unset, List[LoginMethods]] = UNSET
    denied_protocols: Union[Unset, List[SupportedProtocols]] = UNSET
    file_patterns: Union[Unset, List[PatternsFilter]] = UNSET
    max_upload_file_size: Union[Unset, int] = UNSET
    tls_username: Union[Unset, UserFiltersTlsUsername] = UNSET
    hooks: Union[Unset, HooksFilter] = UNSET
    disable_fs_checks: Union[Unset, bool] = UNSET
    web_client: Union[Unset, List[WebClientOptions]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        allowed_ip: Union[Unset, List[str]] = UNSET
        if not isinstance(self.allowed_ip, Unset):
            allowed_ip = self.allowed_ip

        denied_ip: Union[Unset, List[str]] = UNSET
        if not isinstance(self.denied_ip, Unset):
            denied_ip = self.denied_ip

        denied_login_methods: Union[Unset, List[str]] = UNSET
        if not isinstance(self.denied_login_methods, Unset):
            denied_login_methods = []
            for denied_login_methods_item_data in self.denied_login_methods:
                denied_login_methods_item = denied_login_methods_item_data.value

                denied_login_methods.append(denied_login_methods_item)

        denied_protocols: Union[Unset, List[str]] = UNSET
        if not isinstance(self.denied_protocols, Unset):
            denied_protocols = []
            for denied_protocols_item_data in self.denied_protocols:
                denied_protocols_item = denied_protocols_item_data.value

                denied_protocols.append(denied_protocols_item)

        file_patterns: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.file_patterns, Unset):
            file_patterns = []
            for file_patterns_item_data in self.file_patterns:
                file_patterns_item = file_patterns_item_data.to_dict()

                file_patterns.append(file_patterns_item)

        max_upload_file_size = self.max_upload_file_size
        tls_username: Union[Unset, str] = UNSET
        if not isinstance(self.tls_username, Unset):
            tls_username = self.tls_username.value

        hooks: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.hooks, Unset):
            hooks = self.hooks.to_dict()

        disable_fs_checks = self.disable_fs_checks
        web_client: Union[Unset, List[str]] = UNSET
        if not isinstance(self.web_client, Unset):
            web_client = []
            for web_client_item_data in self.web_client:
                web_client_item = web_client_item_data.value

                web_client.append(web_client_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if allowed_ip is not UNSET:
            field_dict["allowed_ip"] = allowed_ip
        if denied_ip is not UNSET:
            field_dict["denied_ip"] = denied_ip
        if denied_login_methods is not UNSET:
            field_dict["denied_login_methods"] = denied_login_methods
        if denied_protocols is not UNSET:
            field_dict["denied_protocols"] = denied_protocols
        if file_patterns is not UNSET:
            field_dict["file_patterns"] = file_patterns
        if max_upload_file_size is not UNSET:
            field_dict["max_upload_file_size"] = max_upload_file_size
        if tls_username is not UNSET:
            field_dict["tls_username"] = tls_username
        if hooks is not UNSET:
            field_dict["hooks"] = hooks
        if disable_fs_checks is not UNSET:
            field_dict["disable_fs_checks"] = disable_fs_checks
        if web_client is not UNSET:
            field_dict["web_client"] = web_client

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        allowed_ip = cast(List[str], d.pop("allowed_ip", UNSET))

        denied_ip = cast(List[str], d.pop("denied_ip", UNSET))

        denied_login_methods = []
        _denied_login_methods = d.pop("denied_login_methods", UNSET)
        for denied_login_methods_item_data in _denied_login_methods or []:
            denied_login_methods_item = LoginMethods(denied_login_methods_item_data)

            denied_login_methods.append(denied_login_methods_item)

        denied_protocols = []
        _denied_protocols = d.pop("denied_protocols", UNSET)
        for denied_protocols_item_data in _denied_protocols or []:
            denied_protocols_item = SupportedProtocols(denied_protocols_item_data)

            denied_protocols.append(denied_protocols_item)

        file_patterns = []
        _file_patterns = d.pop("file_patterns", UNSET)
        for file_patterns_item_data in _file_patterns or []:
            file_patterns_item = PatternsFilter.from_dict(file_patterns_item_data)

            file_patterns.append(file_patterns_item)

        max_upload_file_size = d.pop("max_upload_file_size", UNSET)

        _tls_username = d.pop("tls_username", UNSET)
        tls_username: Union[Unset, UserFiltersTlsUsername]
        if isinstance(_tls_username, Unset):
            tls_username = UNSET
        else:
            tls_username = UserFiltersTlsUsername(_tls_username)

        _hooks = d.pop("hooks", UNSET)
        hooks: Union[Unset, HooksFilter]
        if isinstance(_hooks, Unset):
            hooks = UNSET
        else:
            hooks = HooksFilter.from_dict(_hooks)

        disable_fs_checks = d.pop("disable_fs_checks", UNSET)

        web_client = []
        _web_client = d.pop("web_client", UNSET)
        for web_client_item_data in _web_client or []:
            web_client_item = WebClientOptions(web_client_item_data)

            web_client.append(web_client_item)

        user_filters = cls(
            allowed_ip=allowed_ip,
            denied_ip=denied_ip,
            denied_login_methods=denied_login_methods,
            denied_protocols=denied_protocols,
            file_patterns=file_patterns,
            max_upload_file_size=max_upload_file_size,
            tls_username=tls_username,
            hooks=hooks,
            disable_fs_checks=disable_fs_checks,
            web_client=web_client,
        )

        user_filters.additional_properties = d
        return user_filters

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
