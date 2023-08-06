"""Helpers to access AWS information."""

import botocore
import boto3


CHANGESET_NAME = "cfhelper-changeset"


def get_cloudformation_client():
    return boto3.client("cloudformation")


def stack_exists(stack_name):
    client = get_cloudformation_client()

    try:
        client.describe_stacks(StackName=stack_name)
    except botocore.exceptions.ClientError as error:
        if (
            error.response["Error"]["Code"] == "ValidationError"
            and "does not exist" in error.response["Error"]["Message"]
        ):
            return False
        raise error

    return True


def create_stack(stack_name, stack_file, capabilities):
    client = get_cloudformation_client()
    with open(stack_file) as f:
        template = f.read()

    client.create_stack(
        StackName=stack_name,
        TemplateBody=template,
        Capabilities=sorted(capabilities),
    )
    waiter = client.get_waiter("stack_create_complete")

    waiter.wait(StackName=stack_name, WaiterConfig={"Delay": 15, "MaxAttempts": 120})


def update_stack(stack_name, stack_file, capabilities):
    client = get_cloudformation_client()
    with open(stack_file) as f:
        template = f.read()

    # TODO, handle errors
    # botocore.errorfactory.InsufficientCapabilitiesException: An error occurred (InsufficientCapabilitiesException)
    # when calling the UpdateStack operation: Requires capabilities : [CAPABILITY_IAM]
    # botocore.exceptions.ClientError: An error occurred (ValidationError) when calling the UpdateStack operation: No updates are to be performed.
    client.update_stack(
        StackName=stack_name,
        TemplateBody=template,
        Capabilities=sorted(capabilities),
    )

    waiter = client.get_waiter("stack_update_complete")
    waiter.wait(StackName=stack_name, WaiterConfig={"Delay": 15, "MaxAttempts": 120})


def has_changeset(stack_name):
    try:
        get_changeset(stack_name)
    except botocore.exceptions.ClientError as error:
        if (
            error.response["Error"]["Code"] == "ValidationError"
            and "does not exist" in error.response["Error"]["Message"]
        ):
            return False
        if error.response["Error"]["Code"] == "ChangeSetNotFound":
            return False
        raise error

    return True


def get_changeset(stack_name):
    client = get_cloudformation_client()

    return client.describe_change_set(
        StackName=stack_name,
        ChangeSetName=CHANGESET_NAME,
    )


def create_changeset(stack_name, stack_file, is_creation, capabilities):
    client = get_cloudformation_client()
    changeset_type = "CREATE" if is_creation else "UPDATE"
    with open(stack_file) as f:
        template = f.read()

    client.create_change_set(
        StackName=stack_name,
        TemplateBody=template,
        Capabilities=sorted(capabilities),
        ChangeSetName=CHANGESET_NAME,
        ChangeSetType=changeset_type,
    )

    waiter = client.get_waiter("change_set_create_complete")
    waiter.wait(
        ChangeSetName=CHANGESET_NAME,
        StackName=stack_name,
        WaiterConfig={"Delay": 15, "MaxAttempts": 120},
    )


def execute_changeset(stack_name, is_creation):
    client = get_cloudformation_client()
    client.execute_change_set(
        StackName=stack_name,
        ChangeSetName=CHANGESET_NAME,
    )

    waiter_type = "stack_create_complete" if is_creation else "stack_update_complete"
    waiter = client.get_waiter(waiter_type)
    waiter.wait(StackName=stack_name, WaiterConfig={"Delay": 15, "MaxAttempts": 120})


def delete_changeset(stack_name):
    client = get_cloudformation_client()

    client.delete_change_set(
        StackName=stack_name,
        ChangeSetName=CHANGESET_NAME,
    )
