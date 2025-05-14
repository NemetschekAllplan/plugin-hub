# ALLPLAN Plugin Hub

ALLPLAN Plugin Hub is the index of ALLPLAN plugins available for the ALLPLAN users to download and install.

## How it works

Each plugin has an entry in the _allplan-extensions.json_ file, e.g. like this:

```json
{
    "uuid": "9c2f32ad-f2e5-4bcd-b586-c220a00a64e5",
    "name": "Example Plugin",
    "developer": "example-developer",
    "description": "Lorem ipsum dolor sit amet",
    "github": {
        "owner": "john-nonexistent",
        "repo": "example-plugin"
    }
}
```

Additionally, a plugin must have a GitHub repository, which:

-   is public
-   has at least one release
-   an `.allep` file is attached to this release

This is enough for the plugin to appear in the plugin manager of ALLPLAN. The users
can download and install the plugin. Also, they can check if there are new releases
available and easily update the plugin.

## Submitting a Plugin

### Step 1 - host your plugin on GitHub

1.  Prepare a GitHub repo to host your plugin.
2.  Prepare your the `.allep` package with you plugin according to the
    [documentation](https://pythonparts.allplan.com/latest/manual/for_developer/allep/)
3.  Create a release and attach the `.allep` file to it. The tag you use
    to create the release must be the version of your plugin, e.g. `v1.2.3`.

    **Important**: Make sure, the version specified in your install-config.yaml file matches the tag name!

### Step 2 - add your plugin to the Index

1.  Fork this repo
2.  Switch on the appropriate branch. If you want your plugin to be available in ALLPLAN 2026, switch to branch _2026_
3.  Modify the file *allplan-extensions.json* to include following information for your plugin:

    ```json
    {
        "uuid": "9c2f32ad-f2e5-4bcd-b586-c220a00a64e5",
        "name": "Example Plugin",
        "developer": "example-developer",
        "description": "Lorem ipsum dolor sit amet",
        "github": {
            "owner": "john-nonexistent",
            "repo": "example-plugin"
        },
        "compatibility": ">=2.0.0"
    }
    ```

    +   `uuid`: Version 4 UUID of your plugin. Must be identical with the one in *install-config.yaml*!
    +   `name`: Use a user-friendly name for your plugin.
    +   `developer`: your developer id registered in the `plugin-developers.json`
    +   `description`: A one-line description of your plugin
    +   `compatibility`: _OPTIONAL_ If your plugin has multiple versions, but only some of them are compatible
        with the ALLPLAN version, which you are registering the plugin for, specify the compatibility specifier.
        It should match only the versions of your plugin, that are compatible. E.g. if your plugin works
        with the current ALLPLAN version only since major release 2.0.0, speficify `>=2.0`.
        The specifiers are the same as in the _requirements.txt_ of a python project.

4.  If you're adding a plugin for the first time, add an entry also to the *plugin-developers.json* with
    information about your organization:

    ```json
    {
        "id": "your-developer-id",
        "name": "Example Organization",
        "address": {
            "street": "123 Example Street",
            "city": "Example City",
            "zip": "12345",
            "country": "Example Country"
        },
        "homepage": "https://www.example.com",
        "support": {
            "email": "support@example.com",
            "languages": [
                "eng",
                "spa"
            ]
        },
        "github": "https://github.com/example/"
        }
    ```

-   `id`: The unique id of your organization. A *slugified*, url-friendly name. Use small-caps and `-` as separator.
-   `support`: provide the contact data, where the users should reach out in case of problems
-   `github`, `homepage`: these fields are optional.

After we review and approve your pull request, your plugin will show up automatically in the *Plugin Manager* of ALLPLAN.
Want to ship an update? Just create a new release on your GitHub repo.
