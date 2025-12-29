DEFAULT_PAGE_SIZE = 20
DEFAULT_SORT_ORDER = "asc"
MAX_PAGE_SIZE = 100
DEFAULT_NAME = "World"


# def get(
#     page: int = 1,
#     page_size: int = DEFAULT_PAGE_SIZE,
#     sort: str = DEFAULT_SORT_ORDER,
#     max_items: int = MAX_PAGE_SIZE,
# ):
#     """
#     Get items with pagination and sorting.

#     This demonstrates that default values can reference module-level variables.
#     Before the fix, these parameters would be treated as required.
#     """
#     return {
#         "items": [f"item_{i}" for i in range((page - 1) * page_size, page * page_size)],
#         "page": page,
#         "page_size": page,
#     }


def get(name=DEFAULT_NAME):
    return {"message": f"Hello, {name}!"}
