# `odc-typer-test`

Awesome CLI user manager.

**Usage**:

```console
$ odc-typer-test [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `create`: Create a new user with USERNAME.
* `delete`: Delete an existing user with USERNAME.
* `delete-all`: Delete all users in the database.
* `init`: Initialize the user database.

## `odc-typer-test create`

Create a new user with USERNAME.

**Usage**:

```console
$ odc-typer-test create [OPTIONS] USERNAME
```

**Arguments**:

* `USERNAME`: The name of user to create.  [required]

**Options**:

* `--help`: Show this message and exit.

## `odc-typer-test delete`

Delete an existing user with USERNAME.

If --force is not used, confirmation is required.

**Usage**:

```console
$ odc-typer-test delete [OPTIONS] USERNAME
```

**Arguments**:

* `USERNAME`: The name of user to delete.  [required]

**Options**:

* `--force / --no-force`: Force deletion without confirmation.  [required]
* `--help`: Show this message and exit.

## `odc-typer-test delete-all`

Delete all users in the database.

If --force is not used, confirmation is required.

**Usage**:

```console
$ odc-typer-test delete-all [OPTIONS]
```

**Options**:

* `--force / --no-force`: Force deletion without confirmation.  [required]
* `--help`: Show this message and exit.

## `odc-typer-test init`

Initialize the user database.

**Usage**:

```console
$ odc-typer-test init [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.
