In this assignment you will write an app inspired by twitter/ facebook/threads but with some differences:
1) You will use the built-in auth to register and create accounts.
2) You must be logged in to access any page other the buil-in auth pages
3) App will consist of a single page vie app with 2 columns
4) The left column has a textarea to input a post followed by your feed
5) Posts are text only they may contain tags as in #news #technology #whatever. When a new post is submitted, the post is parsed for tags, and it will be tagged in database with the provided tags.
6) The right columns shows known tags and they should be toggable
7) The feed shows the 100 most recents posts containing the selected tags. Filtering must be done server side.
8) the app must be called "tagged_posts" and live in apps/tagged_posts
9) Any alphanumeric word in a post content that starts with a ``#`` is a tag (regex ``(\#\w+)``). The tag must be stored in the ``tag_item.name`` without the ``#`` and always in lowercase.

You must create (1 point each):

- a database table for ``post_item`` (must have a ``content`` and an ``auth.signature``)
- a database table for ``tag_item`` (must have a ``name`` and a ``post_item_id`` which references a ``post_item``)
- a POST ``api/posts`` to create a new post from body ``{content: "..."}``.
- upon posting a post_item the server should store it, parse it, and create the corresponding tags.
- a GET ``api/tags`` to retrieve all known tags (without duplicates, sorted alphabetically)
- a GET ``api/posts?tags=x,y,z`` to retrieve the 100 most recent posts with tags x or y or z (without duplicates). If no ``?tags=`` specified it should return the 100 most recent (in reverse chronological order)
- a DELETE ``api/posts/<post_item_id>`` delete an item. Only the author can delete items.
- a single page vue app contains the two columns, including a textarea of class ``post-content`` and a button of class ``submit-content`` to submit the content. A feed (class ``feed`` containing ``<div>`` of class ``post_item`` displaying the posted item populated from the ``api/posts`` API.
- the single page app second column displays a list of known tags populated from the ``api/tags`` API. Individual tags should be buttons of class ``tag`` contained in a larged div of class ``tags``.
- posting a new item should refresh the feed and the tags (keep the existing toggle).
- tags should be toggable and toggling tags should refresh the feed and tags. When a a tag is toggled/selected should have an additional class ``selected``.
- feed items should have a button to delete them which uses the DELETE API and refreshes the feed and tags.

Example output of ``api/tags``: ``{"tags": ["x", "y", "z"]}``
Example output of ``api/posts``: ``{"posts": [{"content": "...", "created_on": "...", "created_by": "..."}, ...]}``
