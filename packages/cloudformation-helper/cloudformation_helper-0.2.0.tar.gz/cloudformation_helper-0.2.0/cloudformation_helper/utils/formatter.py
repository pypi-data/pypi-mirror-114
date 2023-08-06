"""Helpers to format/display various information."""

import click


def display_changeset(changeset):
    for change in changeset["Changes"]:
        if change["Type"] != "Resource":
            continue
        action = change["ResourceChange"]["Action"]
        resource_type = change["ResourceChange"]["ResourceType"]
        resource_id = change["ResourceChange"]["LogicalResourceId"]
        click.echo(f"{resource_type} {resource_id} -> {action}")
