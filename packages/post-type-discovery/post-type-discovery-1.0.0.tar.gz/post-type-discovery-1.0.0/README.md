# IndieWeb Post Type Discovery

A library to discover the post type of a web page in accordance with the IndieWeb Post Type Discovery specification.

## Installation

To install this package, run the following command:

    pip install post-type-discovery

You can import the package using the following line of code:

    import post_type_discovery

## Usage

This library contains a `get_post_type` function that returns the post type of a linked web page.

This function uses the following syntax:

    get_post_type(url, custom_properties=[])

Here are the arguments you can use:

- `url`: The URL of the web page to discover the post type of.
- `custom_properties`: A list of custom properties to use when discovering the post type. This list must contain tuples.

The function returns a single string with the post type of the specified web page.

See the Post Type Discovery specification for a full list of post types.

### Custom Properties

The structure of the custom properties tuple is:

(attribute_to_look_for, value_to_return)

An example custom property value is:

    custom_properties = [
        ("poke-of", "poke")
    ]

This function would look for a poke-of attribute on a web page and return the "poke" value.

By default, this function contains all of the attributes in the Post Type Discovery mechanism.

Custom properties are added to the end of the post type discovery list, just before the "article" property. All specification property types will be checked before your custom attribute.

Here is an example of the `get_post_type` function in use:

    import indieauth_helpers

    url = "https://jamesg.blog/2021/12/06/advent-of-bloggers-6/"

    post_type = indieauth_helpers.discover_endpoint(url)

    print(post_type)

This code returns the following string:

    article

## License

This project is licensed under the [MIT license](LICENSE).

## Contributing

This project welcomes contributions from anyone who wants to improve the library.

Feel free to create an issue or pull request on GitHub and your contribution will be reviewed.

## Contributors

- capjamesg