from typing import Callable, Union, List, Tuple


def apply_mapping(
    string: str, mapping: dict, convert_ending: bool
) -> List[Tuple[int, int, str]]:
    root = mapping.copy()  # no idea if it's being mutated but they decided to copy it

    def assign(target: dict, source: dict) -> dict:
        if isinstance(source, dict):
            target.update(source)
        else:
            target.update({"0": source})
        return target

    def next_subtree(tree: dict, next_char: str):
        try:
            subtree = tree[next_char]
        except:
            return
        return assign({"": tree[""] + next_char}, subtree)

    def new_chunk(remaining: str, current_cursor: int):
        first_char = remaining[0]
        return parse(
            assign({"": first_char}, root.get(first_char)),
            remaining[1:],
            current_cursor,
            current_cursor + 1,
        )

    def parse(tree: dict, remaining: str, last_cursor: int, current_cursor: int):
        if not remaining:
            if convert_ending or len(tree.keys()) == 1:
                # nothing more to consume, just commit the last chunk and return it
                # so as not to have an empty element at the end of the result
                return [(last_cursor, current_cursor, tree[""])] if tree[""] else []
            # if we don't want to convert the ending, because there are still possible
            # continuations, return None as the final node value
            return [(last_cursor, current_cursor, None)]

        if len(tree.keys()) == 1:
            return [(last_cursor, current_cursor, tree[""])] + new_chunk(
                remaining, current_cursor
            )

        subtree = next_subtree(tree, remaining[0])

        if not subtree:
            return [(last_cursor, current_cursor, tree[""])] + new_chunk(
                remaining, current_cursor
            )
        # continue current branch
        return parse(subtree, remaining[1:], last_cursor, current_cursor + 1)

    return new_chunk(string, 0)


# transform the tree, so that for example hepburn_tree['ゔ']['ぁ'][''] == 'va'
# or kana_tree['k']['y']['a'][''] == 'きゃ'
def transform(tree: dict):
    map = {}
    for char, subtree in tree.items():
        end_of_branch = isinstance(subtree, str)
        map[char] = {"": subtree} if end_of_branch else transform(subtree)
    return map


def get_subtree_of(tree: dict, string: str):
    correct_subtree = tree
    for char in string:
        next_subtree = correct_subtree.get(char)
        if not next_subtree:
            next_subtree = correct_subtree[char] = {}
        correct_subtree = next_subtree
    return correct_subtree


def create_custom_mapping(custom_map: dict = None) -> Callable[[dict], dict]:
    """Creates a custom mapping tree, returns a function that accepts a default_map
    with which the newly created custom_mapping will be merged and returned"""
    if custom_map is None:
        custom_map = {}

    custom_tree = {}

    if isinstance(custom_map, dict):
        for key, value in custom_map.items():
            subtree = custom_tree
            for char in key:
                if not subtree.get(char):
                    subtree[char] = {}
                subtree = subtree[char]
            subtree[""] = value

    def make_map(map: dict):
        map_copy = map.copy()

        def transform_map(map_subtree, custom_subtree):
            if (not map_subtree) or isinstance(map_subtree, str):
                return custom_subtree
            new_subtree = map_subtree
            for char, subtree in custom_subtree.items():
                new_subtree[char] = transform_map(map_subtree.get(char), subtree)
            return new_subtree

        return transform_map(map_copy, custom_tree)

    return make_map


def merge_custom_mapping(
    map: dict, custom_mapping: Union[dict, Callable[[dict], dict]] = None
) -> dict:
    if not custom_mapping:
        return map
    return (
        create_custom_mapping(custom_mapping)(map)
        if isinstance(custom_mapping, dict)
        else custom_mapping(map)
    )

