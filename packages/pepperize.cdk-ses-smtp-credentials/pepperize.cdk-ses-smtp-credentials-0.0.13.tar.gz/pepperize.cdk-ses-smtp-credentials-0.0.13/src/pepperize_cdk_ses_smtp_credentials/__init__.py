'''
[![GitHub](https://img.shields.io/github/license/pepperize/cdk-ses-smtp-credentials?style=flat-square)](https://github.com/pepperize/cdk-ses-smtp-credentials/blob/main/LICENSE)
[![npm (scoped)](https://img.shields.io/npm/v/@pepperize/cdk-ses-smtp-credentials?style=flat-square)](https://www.npmjs.com/package/@pepperize/cdk-ses-smtp-credentials)
[![PyPI](https://img.shields.io/pypi/v/pepperize.cdk-ses-smtp-credentials?style=flat-square)](https://pypi.org/project/pepperize.cdk-ses-smtp-credentials/)
[![Nuget](https://img.shields.io/nuget/v/Pepperize.CDK.SesSmtpCredentials?style=flat-square)](https://www.nuget.org/packages/Pepperize.CDK.SesSmtpCredentials/)
[![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/pepperize/cdk-ses-smtp-credentials/release/main?label=release&style=flat-square)](https://github.com/pepperize/cdk-ses-smtp-credentials/actions/workflows/release.yml)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/pepperize/cdk-ses-smtp-credentials?sort=semver&style=flat-square)](https://github.com/pepperize/cdk-ses-smtp-credentials/releases)

# AWS CDK Ses Smtp Credentials

This projects provides a CDK construct to create ses smtp credentials for a given user. It takes a username, creates an AccessKey and generates the smtp password.

## Example

```shell
npm install @pepperize/cdk-ses-smtp-credentials
```

```python
# Example automatically generated from non-compiling source. May contain errors.
import { User } from "@aws-cdk/aws-iam";

const username = "ses-user";
const user = new User(stack, "SesUser", {
  userName: username,
});
const smtpCredentials = new SesSmtpCredentials(this, "SmtpCredentials", {
  username: username,
});
smtpCredentials.node.addDependency(user);

// returns {username: "<the generated access key id>", password: "<the calculated ses smtp password>"}
console.log(smtpCredentials.credentials);
```
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.core


class SesSmtpCredentials(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@pepperize/cdk-ses-smtp-credentials.SesSmtpCredentials",
):
    '''This construct converts the access key to SMTP credentials.

    Example::

        # Example automatically generated from non-compiling source. May contain errors.
        const accessKey = new CfnAccessKey(this, "ses-access-key", {
             userName: username,
        });
        new SmtpCredentials(this, 'SmtpCredentials', {
            accessKey: accessKey,
        });
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        username: builtins.str,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param username: 
        '''
        props = SesSmtpCredentialsProps(username=username)

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="credentials")
    def credentials(self) -> "SmtpCredentials":
        return typing.cast("SmtpCredentials", jsii.get(self, "credentials"))


@jsii.data_type(
    jsii_type="@pepperize/cdk-ses-smtp-credentials.SesSmtpCredentialsProps",
    jsii_struct_bases=[],
    name_mapping={"username": "username"},
)
class SesSmtpCredentialsProps:
    def __init__(self, *, username: builtins.str) -> None:
        '''
        :param username: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "username": username,
        }

    @builtins.property
    def username(self) -> builtins.str:
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SesSmtpCredentialsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@pepperize/cdk-ses-smtp-credentials.SmtpCredentials",
    jsii_struct_bases=[],
    name_mapping={"password": "password", "username": "username"},
)
class SmtpCredentials:
    def __init__(self, *, password: builtins.str, username: builtins.str) -> None:
        '''
        :param password: 
        :param username: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "password": password,
            "username": username,
        }

    @builtins.property
    def password(self) -> builtins.str:
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SmtpCredentials(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "SesSmtpCredentials",
    "SesSmtpCredentialsProps",
    "SmtpCredentials",
]

publication.publish()
